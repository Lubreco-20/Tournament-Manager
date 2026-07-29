from django import forms
from .models import Torneo

from datetime import date

# Creamos una clase para crear los formularios de los torneos que hereda de ModelForm
class Torneo_Form(forms.ModelForm):
    '''Esta clase nos permitirá crear un formulario para crear y editar torneos.'''

    class Meta:
        model = Torneo
        fields = ['nombre', 'descripcion', 'juego', 'fecha_inicio', 'fecha_fin', 'max_jugadores', 'activo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Si estamos editando un torneo, deshabilitamos algunos campos
        if self.instance and self.instance.pk:
            self.fields["fecha_inicio"].disabled = True

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre == "":
            raise forms.ValidationError("El campo de nombre del torneo no puede estar vacío")
        return nombre

    def clean_juego(self):
        juego = self.cleaned_data.get('juego')
        if juego == "":
            raise forms.ValidationError("El campo de juego del torneo no puede estar vacío")
        return juego

    def clean_fecha_inicio(self):
        if self.instance and self.instance.pk:
            return self.instance.fecha_inicio

        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if fecha_inicio is None:
            return fecha_inicio

        if fecha_inicio < date.today():
            raise forms.ValidationError("La fecha de inicio no puede ser pasada")
        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')
        if fecha_fin is None:
            return fecha_fin

        if fecha_fin < date.today():
            raise forms.ValidationError("La fecha de finalización no puede ser pasada")
        return fecha_fin

    def clean_max_jugadores(self):
        max_jugadores = self.cleaned_data.get('max_jugadores')
        if max_jugadores is None:
            return None

        if max_jugadores < 2:
            raise forms.ValidationError("El número máximo de jugadores debe ser al menos 2")
        return max_jugadores

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de finalización")
        return cleaned_data
    

class BuscarTorneo_Form(forms.Form):
    '''Esta clase nos permitirá crear un formulario para buscar y filtrar los torneos.'''

    nombre = forms.CharField(
        required=False,
        label="Nombre",
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nombre'})
    )

    juego = forms.CharField(
        required=False,
        label="Juego",
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por juego'})
    )

    estado_opciones = [
        ('', 'Todos'),
        ('1', 'Activos'),
        ('0', 'Inactivos'),
    ]

    activo = forms.ChoiceField(
        choices=estado_opciones,
        required=False,
        label="Estado"
    )

    orden_fecha_opciones = [
        ('asc', 'Más antiguos primero'),
        ('desc', 'Más recientes primero'),
    ]

    orden_fecha = forms.ChoiceField(
        choices=orden_fecha_opciones,
        required=False,
        label="Orden por fecha"
    )

    con_plazas = forms.BooleanField(
        required=False,
        label="Solo con plazas"
    )