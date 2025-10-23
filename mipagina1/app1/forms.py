from django import forms
from .models import Solicitud

CAMPUS_CHOICES = [
    ("Casa Central (Valparaíso)", "Casa Central (Valparaíso)"),
    ("Campus San Joaquín", "Campus San Joaquín"),
    ("Campus Vitacura", "Campus Vitacura"),
    ("Campus Concepción", "Campus Concepción"),
    ("Campus José Miguel Carrera", "Campus José Miguel Carrera"),
]

ROL_CHOICES = [
    ("estudiante", "Estudiante"),
    ("profesor", "Profesor"),
    ("funcionario", "Funcionario"),
]

class SolicitudForm(forms.ModelForm):
    firma = forms.BooleanField(label="Confirmo con mi firma (checkbox)", required=True)

    campus = forms.ChoiceField(choices=CAMPUS_CHOICES, required=False)

    rol = forms.ChoiceField(choices=ROL_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = Solicitud
        fields = [
            "nombre_legal", "apellidos", "rut", "fecha_nacimiento", "direccion",
            "telefono", "correo", "campus", "nombre_social", "rol", "firma"
        ]
        widgets = {
            "fecha_nacimiento": forms.TextInput(attrs={"type": "date"}),
        }
