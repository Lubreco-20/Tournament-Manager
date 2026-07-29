from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm

# Creamos un formulario de creación de usuario personalizado que hereda de UserCreationForm
class usuario_creation_form(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')  # Incluimos los campos necesarios para el registro de usuario