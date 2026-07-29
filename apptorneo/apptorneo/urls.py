"""
URL configuration for apptorneo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # Importamos include para poder incluir las URLs de las apps
from django.shortcuts import redirect # Importamos redirect para redirigir a la página de login desde la raíz

def home_redirect(request):
    return redirect('login')

urlpatterns = [
    path('', home_redirect),  # Redirige la página de inicio al login
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),  # Incluimos las URLs de la app de usuarios
    path('torneos/', include('torneos.urls')),  # Incluimos las URLs de la app de torneos
    path('resultados/', include('resultados.urls')),  # Incluimos las URLs de la app de resultados
]
