from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import usuario_creation_form

#======================================
# REGISTRO Y AUTENTICACIÓN
#======================================

def registro_view(request):
    '''Vista para el registro de nuevos usuarios.'''

    tipo = request.GET.get('tipo_usuario', 'jugador') # Obtenemos el tipo de usuario desde los parámetros de la URL que puede ser 'jugador' u 'organizador'

    if tipo == "organizador" and not request.session.get("ok_organizador", False):
        messages.info(request, "Debes ingresar la clave de organizador para registrarte como organizador.")
        return redirect('registro_organizador')  # Redirigimos a la página de registro de organizadores si el tipo es organizador pero no se ha verificado la clave

    # Comprobamos que el tipo de petición sea POST
    if request.method == 'POST':

        # Creamos un formulario con los datos enviados por el usuario
        form = usuario_creation_form(request.POST)
        # Comprobamos si el formulario es válido, si lo es, lo guardamos y redirigimos al login
        if form.is_valid():
            if tipo == "organizador":
                request.session.pop("ok_organizador", None)  # Eliminamos la clave de organizador de la sesión después de usarla para evitar que se use nuevamente sin verificación
            user = form.save(commit=False)  # Guardamos el formulario sin hacer commit para asignar el rol
            user.role = tipo # Asignamos el rol al usuario antes de guardarlo
            user.save()  # Guardamos el usuario en la base de datos
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')

    else:
        # Si la petición no es POST, simplemente creamos un formulario vacío para mostrarlo al usuario
        form = usuario_creation_form()

    return render(request, 'registro/signup.html', {'form': form})


def registro_organizador(request):

    if request.method == "POST":
        clave = request.POST.get("clave")

        if clave == "TORNEO2026":  # contraseña que solo debería conocer el organizador para poder registrarse como tal
            # Si el usuario ingresa la clave correcta, guardamos un valor en la sesión para indicar que ha verificado la clave de organizador
            request.session["ok_organizador"] = True 
            return redirect(f"{reverse('registro')}?tipo_usuario=organizador")

        messages.error(request, "Clave incorrecta")

    return render(request, "registro/registro_organizador.html")


def login_view(request):
    '''Vista para el login de usuarios.'''

    if request.method == 'POST':
        #Primero obtenemos el nombre de usuario y la contraseña enviados por el formulario
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Verificamos que las credenciales sean válidas utilizando la función authenticate de Django
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Si el usuario es válido, lo asociamos a la sesión utilizando la función login de Django
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('lista_torneos')  # Redirige a la página de inicio después del login
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")

    messages.info(request, "Por favor, inicia sesión para acceder a tu cuenta.")
    return render(request, 'registro/login.html')


@login_required
def logout_view(request):
    '''Vista para el logout de usuarios.'''
    
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')  # Redirige a la página de inicio después del logout