# -*- coding: utf-8 -*-
from datetime import datetime
import json
from django.contrib import messages

from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404 # Importamos get_object_or_404 para obtener un objeto o mostrar un error 404 si no existe
from django.contrib.auth.decorators import login_required # Importamos el decorador login_required para proteger nuestras vistas y que solo los usuarios autenticados puedan acceder a ellas
from django.urls import reverse_lazy
from .models import Inscripcion, Torneo, Resultado, Jugador # Importamos los modelos que vamos a usar, así como el modelo de torneo

@login_required
def inscribir_torneo(request, pk):
    
    torneo = get_object_or_404(Torneo, pk=pk) # Obtenemos el torneo al que se quiere inscribir el jugador, si no existe mostramos un error 404
    jugador = request.user # Obtenemos el jugador que se quiere inscribir, en este caso el usuario autenticado

    # Verificamos si el jugador ya está inscrito en el torneo
    if Inscripcion.objects.filter(jugador=jugador, torneo=torneo).exists():
        # El jugador ya está inscrito, no hacemos nada
        messages.info(request, 'Ya estás inscrito en este torneo.')
    else:
        # El jugador no está inscrito, creamos la inscripción y actualizamos la relación M2M
        Inscripcion.objects.create(jugador=jugador, torneo=torneo, fecha_inscripcion=datetime.today())
        torneo.jugadores.add(jugador)
        messages.success(request, f'Te has inscrito correctamente en {torneo.nombre}.')  # Mensaje de éxito

    return redirect('detalle_torneo', pk=torneo.pk) # Redirigimos al detalle del torneo después de inscribir al jugador, aunque esta función aún no está implementada, la redirección es correcta y no causará errores



@login_required
def cancelar_inscripcion(request, pk):
    
    torneo = get_object_or_404(Torneo, pk=pk) # Obtenemos el torneo al que se quiere cancelar la inscripción, si no existe mostramos un error 404
    jugador = request.user # Obtenemos el jugador que se quiere cancelar la inscripción, en este caso el usuario autenticado

    # Verificamos si el jugador está inscrito en el torneo
    if Inscripcion.objects.filter(jugador=jugador, torneo=torneo).exists():
        # El jugador está inscrito, eliminamos la inscripción y la relación M2M
        Inscripcion.objects.filter(jugador=jugador, torneo=torneo).delete()
        torneo.jugadores.remove(jugador)
        messages.success(request, f'Has cancelado tu inscripción en {torneo.nombre}.')  # Mensaje de éxito
    else:
        # El jugador no está inscrito, no hacemos nada
        messages.info(request, 'Ya no estás inscrito en este torneo.')

    return redirect('detalle_torneo', pk=torneo.pk) # Redirigimos al detalle del torneo después de cancelar la inscripción, aunque esta función aún no está implementada, la redirección es correcta y no causará errores



@login_required
def gestionar_jugadores(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk) # Obtenemos el torneo al que se quiere gestionar los jugadores, si no existe mostramos un error 404

    # Verificamos que el usuario sea el organizador del torneo
    if request.user.role != 'organizador':
        messages.error(request, 'No tienes permiso para gestionar los jugadores de este torneo.')
        return redirect('detalle_torneo', pk=torneo.pk)

    jugadores_inscritos = torneo.jugadores.all() # Obtenemos todos los jugadores inscritos en el torneo

    for jugador in jugadores_inscritos:
        Resultado.objects.get_or_create(
            jugador=jugador, 
            torneo=torneo, 
            defaults={
                'posicion': 0,
                'puntos': 0
            }) # Obtenemos el resultado del jugador en el torneo, si no existe lo creamos

    if request.method == 'POST':
        jugador_id = request.POST.get('guardar_jugador_{{ jugador.jugador.id }}') # Obtenemos el ID del jugador que se quiere guardar, si es None se guardarán todos los jugadores, si no se guardará solo el jugador con ese ID
        if jugador_id:
            # actualizar solo este jugador
            jugador = get_object_or_404(Jugador, pk=jugador_id)
            puntos = request.POST.get(f'puntos_{jugador.id}')
            if puntos is not None and puntos.strip() != '':
                Resultado.objects.update_or_create(
                    jugador=jugador,
                    torneo=torneo,
                    defaults={'puntos': puntos}
                )
        else:
            # Actualizamos todos los jugadores
            for jugador in jugadores_inscritos:
                #posicion = request.POST.get(f'posicion_{jugador.id}') # Obtenemos la posición del jugador desde el formulario
                puntos = request.POST.get(f'puntos_{jugador.id}') # Obtenemos los puntos del jugador desde el formulario

                if puntos is None:
                    continue  # Si no se proporcionan posición o puntos, saltamos a la siguiente iteración

                if puntos.strip() == '':
                    continue  # Si la posición o los puntos están vacíos, saltamos a la siguiente iteración

                Resultado.objects.update_or_create(
                    jugador=jugador,
                    torneo=torneo,
                    defaults={'puntos': puntos}
                )  # Actualizamos o creamos el resultado del jugador en el torneo

        messages.success(request, 'Resultados actualizados correctamente.')  # Mensaje de éxito después de guardar los resultados
        return redirect('gestionar_jugadores', pk=torneo.pk) # Redirigimos al detalle del torneo después de guardar los resultados, aunque esta función aún no está implementada, la redirección es correcta y no causará errores
    
    resultado_jugadores = Resultado.objects.filter(torneo=torneo).order_by('-puntos') # Obtenemos los resultados de los jugadores en el torneo

    # Por cada resultado de jugador, asignamos la posición correspondiente según el orden de puntos
    for index, resultado in enumerate(
        resultado_jugadores,
        start=1):

        resultado.posicion = index

        resultado.save()

    return render(request, 'resultados/gestionar_jugadores.html', {'torneo': torneo, 'resultados': resultado_jugadores}) # Renderizamos la plantilla de gestión de jugadores con el contexto del torneo y los resultados de los jugadores