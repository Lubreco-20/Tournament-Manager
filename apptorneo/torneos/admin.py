from django.contrib import admin
from .models import Torneo

# Registramos el modelo del torneo para que sea visible en el admin de Django
@admin.register(Torneo)
# Personalizamos la visualización del modelo en el admin
class TorneoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 
                    'juego', 
                    'fecha_inicio', 
                    'fecha_fin',
                    'max_jugadores',
                    'activo')       # Campos que se mostrarán en la lista de torneos
    search_fields = ('nombre', 
                     'juego')       # Campos por los que se podrá buscar en el admin