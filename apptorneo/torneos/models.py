from datetime import date

from django.db import models
from usuarios.models import Usuario as Jugador

# Create your models here.
class Torneo(models.Model):
    nombre = models.CharField(max_length=100)               # Nombre del torneo
    juego = models.CharField(max_length=50)                 # Juego o disciplina del torneo
    descripcion = models.TextField(blank=True)              # Descripción del torneo
    fecha_inicio = models.DateField()                       # Fecha de inicio del torneo
    fecha_fin = models.DateField()                          # Fecha de finalización del torneo
    max_jugadores = models.PositiveIntegerField()           # Número máximo de jugadores permitidos
    jugadores = models.ManyToManyField(Jugador, blank=True) # Jugadores inscritos en el torneo
    activo = models.BooleanField(default=False)             # Indica si el torneo está activo

    def __str__(self):
        return f"{self.nombre} - {self.juego}"
    
    def fin_torneo(self):
        ha_terminado = self.fecha_fin < date.today()

        if ha_terminado and self.activo:
            self.activo = False
            self.save()

        return ha_terminado