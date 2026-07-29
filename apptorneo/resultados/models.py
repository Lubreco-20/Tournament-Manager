from django.db import models
from usuarios.models import Usuario as Jugador
from torneos.models import Torneo

# Create your models here.
class Inscripcion(models.Model):
    # Registra la relación entre un jugador y un torneo, indicando que el jugador se ha inscrito en ese torneo.

    jugador = models.ForeignKey(Jugador, 
                                on_delete=models.CASCADE, 
                                related_name="inscripciones")   # El jugador que se inscribe en el torneo
    torneo = models.ForeignKey(Torneo, 
                               on_delete=models.CASCADE, 
                               related_name="inscripciones")    # El torneo al que se inscribe el jugador
    fecha_inscripcion = models.DateTimeField(auto_now_add=True) # Fecha y hora en que el jugador se inscribió en el torneo

    class Meta:
        unique_together = ('jugador', 'torneo') # No permite duplicados

    def __str__(self):
        return f"{self.jugador} inscrito en {self.torneo}"
    

class Resultado(models.Model):
    # Registra el desempeño de cada jugador en un torneo específico
    jugador = models.ForeignKey(Jugador, 
                                on_delete=models.CASCADE, 
                                related_name="resultados")  # Jugador al que corresponde el resultado
    torneo = models.ForeignKey(Torneo,
                               on_delete=models.CASCADE,
                               related_name="resultados",
                               null=True,
                               blank=True)  # Torneo en el que el jugador obtuvo esta puntuación
    posicion = models.PositiveIntegerField(default=0)                # Posición del jugador
    puntos = models.PositiveIntegerField(default=0)                  # Puntos obtenidos por el jugador

    class Meta:
        unique_together = ('jugador', 'torneo')  # Un jugador solo puede tener un resultado por torneo

    def __str__(self):
        return f"{self.jugador}: Posición {self.posicion}, Puntos {self.puntos} en {self.torneo}"