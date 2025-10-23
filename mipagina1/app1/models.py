from django.db import models

class Solicitud(models.Model):
    nombre_legal = models.CharField("Nombre legal", max_length=200)
    apellidos = models.CharField("Apellidos", max_length=200, blank=True)
    rut = models.CharField("RUT", max_length=30)
    fecha_nacimiento = models.CharField("Fecha de nacimiento", max_length=50, blank=True)
    direccion = models.CharField("Dirección/Domicilio", max_length=300, blank=True)
    telefono = models.CharField("Teléfono", max_length=50, blank=True)
    correo = models.EmailField("Correo institucional")
    campus = models.CharField("Campus/Sede", max_length=100, blank=True)
    nombre_social = models.CharField("Nombre social", max_length=200, blank=True)
    rol = models.CharField("Rol", max_length=50)  
    firma = models.BooleanField("Acepta y firma (checkbox)", default=False)


    pdf_file = models.FileField("PDF generado", upload_to='generated_pdfs/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_social or self.nombre_legal} - {self.correo}"
