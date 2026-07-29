from django.urls import path
from .views import TorneoListView, TorneoDetailView, TorneoDeleteView, TorneoCreateView, TorneoUpdateView # Importamos las vistas que hemos creado

urlpatterns = [
    path('lista_torneos/', TorneoListView.as_view(), name='lista_torneos'),  # URL para listar los torneos
    path('torneo/<int:pk>/', TorneoDetailView.as_view(), name='detalle_torneo'),  # URL para mostrar los detalles de un torneo específico
    path('torneo_form/', TorneoCreateView.as_view(), name='crear_torneo'),  # URL para crear un nuevo torneo
    path('torneo_form/<int:pk>/', TorneoUpdateView.as_view(), name='editar_torneo'),  # URL para editar un torneo existente
    path('eliminar_torneo/<int:pk>/', TorneoDeleteView.as_view(), name='eliminar_torneo'),  # URL para eliminar un torneo existente
]