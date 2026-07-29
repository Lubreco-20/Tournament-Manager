# Creamos este archivo py para delegar la gestión de las URL de la aplicación de manera modular
from django.urls import path # Importamos de las urls para poder acceder a ellas
from . import views # Importamos también de las vistas para poder acceder a sus clases y funciones

# URLs específicas de la app
urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL para el login
    path('logout/', views.logout_view, name='logout'),  # URL para el logout
    path('registro/', views.registro_view, name='registro'),  # URL para el registro
    path('registro_organizador/', views.registro_organizador, name='registro_organizador'),  # URL para el registro de organizadores
]