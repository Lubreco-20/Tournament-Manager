from django.contrib import admin
from .models import Inscripcion, Resultado

# Registramos el modelo de inscripción para que sea visible en el admin de Django
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('jugador', 
                    'torneo', 
                    'fecha_inscripcion')    # Campos que se mostrarán en la lista de inscripciones
    search_fields = ('jugador__nombre', 
                     'torneo__nombre')      # Campos por los que se podrá buscar en el admin
    

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('jugador',
                    'posicion',
                    'puntos')   # Campos que se mostrarán en la lista de resultados
    search_fields = ('jugador',) # Campos por los que se podrá buscar en el admin