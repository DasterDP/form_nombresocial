import fitz
import os
import uuid
from django.conf import settings


mapa_campos_texto = {
    "nombre_legal": "Text1",     
    "apellidos": "Text2",         
    "rut": "Text3",               
    "fecha_nacimiento": "Text4",  
    "direccion": "Text5",         
    "telefono": "Text6",          
    "correo": "Text7",           
    "campus": "Text8",            
    "nombre_social": "Text9",     
}

mapa_campos_radio = {
    "rol": {
        "estudiante": "Button10",
        "profesor": "Button11",
        "funcionario": "Button12"
    }
}

def generar_pdf_para_solicitud(solicitud_instance):
   
    pdf_input_path = os.path.join(settings.BASE_DIR, "app1", "pdfs", "nombre_social.pdf")
    if not os.path.exists(pdf_input_path):
        raise FileNotFoundError(f"Plantilla PDF no encontrada: {pdf_input_path}")


    out_dir = os.path.join(settings.MEDIA_ROOT, "generated_pdfs")
    os.makedirs(out_dir, exist_ok=True)
    unique_name = f"formulario_{solicitud_instance.id}_{uuid.uuid4().hex[:8]}.pdf"
    pdf_output_path = os.path.join(out_dir, unique_name)

 
    doc = fitz.open(pdf_input_path)

   
    for page in doc:
        widgets = page.widgets()
        if not widgets:
            continue
        widgets = list(widgets)

       
        for campo_form, campo_pdf in mapa_campos_texto.items():
            valor = getattr(solicitud_instance, campo_form, "") or ""
            for widget in widgets:
                if widget.field_name == campo_pdf:
                    widget.field_value = str(valor)
                    try:
                        widget.update()
                    except Exception:
                        pass

        
        for campo_form, opciones in mapa_campos_radio.items():
            valor_usuario = getattr(solicitud_instance, campo_form, None)
            for opcion_val, pdf_button_name in opciones.items():
                for widget in widgets:
                    if widget.field_name == pdf_button_name:
                        widget.field_value = "Yes" if opcion_val == valor_usuario else "Off"
                        try:
                            widget.update()
                        except Exception:
                            pass

   
    doc.save(pdf_output_path)
    doc.close()

    
    media_rel_url = settings.MEDIA_URL + f"generated_pdfs/{unique_name}"


    solicitud_instance.pdf_file.name = f"generated_pdfs/{unique_name}"
    solicitud_instance.save(update_fields=['pdf_file'])

    return media_rel_url
