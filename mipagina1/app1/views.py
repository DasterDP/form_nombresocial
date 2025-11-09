from django.shortcuts import render, redirect, get_object_or_404
from .forms import SolicitudForm
from .models import Solicitud
from .utils_pdf import generar_pdf_para_solicitud
    
# New imports for emailing and responses
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.mail import EmailMessage
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os


def home(request):
    return render(request, 'app1/home.html')


def formulario(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            # guardar instancia en BD primero (sin pdf)
            solicitud = form.save(commit=False)
            solicitud.firma = form.cleaned_data.get('firma', False)
            solicitud.save()

            # generar pdf y actualizar modelo (utils hace update del campo pdf_file)
            generar_pdf_para_solicitud(solicitud)

            # enviar el PDF generado al correo del solicitante
            try:
                if solicitud.pdf_file:
                    pdf_abs_path = os.path.join(settings.MEDIA_ROOT, solicitud.pdf_file.name)
                    if os.path.exists(pdf_abs_path):
                        subject = 'Tu formulario en PDF'
                        body = 'Adjuntamos el PDF generado de tu solicitud.'
                        to_email = [solicitud.correo] if solicitud.correo else []
                        if to_email:
                            email = EmailMessage(subject=subject, body=body, to=to_email)
                            email.attach_file(pdf_abs_path)
                            email.send(fail_silently=False)
            except Exception:
                # No interrumpir el flujo del usuario si el correo falla
                pass

            # redirigir a página de éxito (descarga automática)
            return redirect('app1:exito', pk=solicitud.pk)
    else:
        form = SolicitudForm()
    return render(request, 'app1/formulario.html', {'form': form})


def exito(request, pk):
    solicitud = get_object_or_404(Solicitud, pk=pk)
    # URL pública al archivo
    pdf_url = solicitud.pdf_file.url if solicitud.pdf_file else None
    return render(request, 'app1/exito.html', {'solicitud': solicitud, 'pdf_url': pdf_url})


# Step 3: Endpoint to generate a minimal PDF in-memory and email it
# This does not depend on any external PDF libraries.
@csrf_exempt
def send_pdf_view(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')

    to_email = (request.POST.get('to_email') or '').strip()
    subject = (request.POST.get('subject') or 'Your PDF').strip()
    message = (request.POST.get('message') or '').strip()

    if not to_email:
        return HttpResponseBadRequest('to_email is required')

    # For this endpoint, prefer sending the most recently generated file on disk
    try:
        generated_path = None
        # If a specific file path is provided, honor it, else fallback to latest
        provided_rel = (request.POST.get('pdf_rel_path') or '').strip()
        if provided_rel:
            candidate = os.path.join(settings.MEDIA_ROOT, provided_rel)
            if os.path.exists(candidate):
                generated_path = candidate
        if not generated_path:
            # fallback: newest in media/generated_pdfs
            folder = os.path.join(settings.MEDIA_ROOT, 'generated_pdfs')
            if os.path.isdir(folder):
                pdfs = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith('.pdf')]
                if pdfs:
                    generated_path = max(pdfs, key=os.path.getmtime)
        if not generated_path:
            return HttpResponseBadRequest('No PDF available to send')

        email = EmailMessage(subject=subject, body=(message or 'Adjuntamos el PDF generado.'), to=[to_email])
        email.attach_file(generated_path)
        email.send(fail_silently=False)
        return JsonResponse({'success': True, 'sent_file': os.path.basename(generated_path)})
    except Exception as e:
        return HttpResponseBadRequest(f'Error sending PDF: {e}')