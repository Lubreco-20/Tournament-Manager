from django.contrib import admin
from .models import Usuario

# Registramos el modelo del jugador para que sea visible en el admin de Django
@admin.register(Usuario)
# Personalizamos la visualización del modelo en el admin
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')  # Campos que se mostrarán en la lista de jugadores
    search_fields = ('username', 'email')         # Campos por los que se podrá buscar en el admin