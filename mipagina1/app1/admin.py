from django.contrib import admin
from .models import Solicitud

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_legal', 'nombre_social', 'correo', 'rol', 'created_at')
    list_filter = ('rol', 'campus')
    search_fields = ('nombre_legal', 'nombre_social', 'rut', 'correo')
