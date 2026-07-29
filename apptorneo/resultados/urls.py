from django.urls import path
from . import views

urlpatterns = [
    path('inscribir_torneo/<int:pk>/', views.inscribir_torneo, name='inscribir_torneo'),  # URL para inscribirse en un torneo
    path('cancelar_inscripcion/<int:pk>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),  # URL para cancelar la inscripción en un torneo
    path('gestionar_jugadores/<int:pk>/', views.gestionar_jugadores, name='gestionar_jugadores'),  # URL para gestionar los jugadores inscritos en un torneo (solo para organizadores)
]
