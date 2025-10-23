from django.shortcuts import render, redirect, get_object_or_404
from .forms import SolicitudForm
from .models import Solicitud
from .utils_pdf import generar_pdf_para_solicitud

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
