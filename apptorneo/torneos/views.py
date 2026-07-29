from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView # Importamos ListView para crear una vista que nos permita listar los torneos
from django.contrib.auth.mixins import LoginRequiredMixin # Importamos LoginRequiredMixin para proteger las vistas de creación, edición y eliminación de torneos, solo los usuarios autenticados podrán acceder a estas vistas
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Count, F

from .forms import Torneo_Form, BuscarTorneo_Form

from .models import Torneo
from resultados.models import Resultado

class TorneoListView(LoginRequiredMixin, ListView):
    '''Esta clase al heredar de ListView nos permitirá listar los torneos de manera sencilla, 
    solo tenemos que indicarle el modelo que queremos listar y el template que queremos usar 
    para mostrar la lista'''
    
    model = Torneo
    template_name = 'torneos/torneo_list.html'
    context_object_name = 'torneos'
    paginate_by = 10  # Número de torneos por página

    def get_queryset(self):
        # Sobrescribimos el método get_queryset para agregar la funcionalidad de búsqueda y filtrado de torneos
        qs = Torneo.objects.all().order_by('-activo', '-fecha_inicio')  # Ordenamos los torneos por fecha de inicio, los más recientes primero y si están activos

        # Aquí obtendremos los datos del formulario de búsqueda y filtrado, si el formulario es válido, aplicaremos los filtros correspondientes a la consulta de torneos
        form = BuscarTorneo_Form(self.request.GET)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            juego = form.cleaned_data.get('juego')
            activo = form.cleaned_data.get('activo')

            orden_fecha = form.cleaned_data.get('orden_fecha')
            con_plazas = form.cleaned_data.get('con_plazas')

            if nombre:
                qs = qs.filter(nombre__icontains=nombre)
                
            if juego:
                qs = qs.filter(juego__icontains=juego)

            if activo != '':
                qs = qs.filter(activo=activo == '1')

            if orden_fecha == 'asc':
                qs = qs.order_by('fecha_inicio')
            elif orden_fecha == 'desc':
                qs = qs.order_by('-fecha_inicio')

            if con_plazas:
                qs = qs.annotate(
                    total_jugadores=Count('jugadores')
                ).filter(
                    total_jugadores__lt=F('max_jugadores')
                )

        return qs
    
    # Aquí sobrescribimos el método get_context_data para agregar información adicional al contexto que se pasará al template, 
    # en este caso, si el usuario es un jugador, agregaremos información sobre sus resultados en los torneos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.role == "jugador":
            resultados = Resultado.objects.filter(jugador=user)

            context["torneos_activos"] = resultados.filter(torneo__activo=True).count()
            context["puntos_totales"] = sum(r.puntos for r in resultados)
            context["media_puntos"] = (
                context["puntos_totales"] / resultados.count()
                if resultados.exists() else 0
            )

            context["resultados_usuario"] = resultados.select_related("torneo")

        return context



class TorneoDetailView(LoginRequiredMixin, DetailView):
    '''Esta clase al heredar de DetailView nos permitirá mostrar los detalles de un torneo, 
    solo tenemos que indicarle el modelo que queremos mostrar y el template que queremos usar 
    para mostrar los detalles'''
    
    model = Torneo
    template_name = 'torneos/torneo_detail.html'
    context_object_name = 'torneo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        torneo = self.get_object()

        # Obtenemos los resultados del torneo y los ordenamos por puntos de mayor a menor, también usamos select_related 
        # para evitar consultas adicionales a la base de datos al acceder a los jugadores relacionados con los resultados
        resultado = Resultado.objects.filter(torneo=torneo).select_related('jugador').order_by('-puntos')

        # Crear diccionario con puntos de cada jugador
        resultado_por_jugador = {r.jugador_id: r.puntos for r in resultado}

        # Crear lista de inscritos con puntos
        inscritos_con_puntos = []
        for jugador in torneo.jugadores.all():
            inscritos_con_puntos.append({
                'username': jugador.username,
                'puntos': resultado_por_jugador.get(jugador.id, 0),
            })

        context['resultados'] = resultado # Obtenemos los resultados del torneo para mostrar en el detalle del torneo
        context['top3'] = resultado[:3]  # Obtenemos los 3 mejores resultados para mostrar en el detalle del torneo
        context['mini_ranking'] = resultado[3:6]  # Obtenemos los siguientes 3 mejores resultados para mostrar en el detalle del torneo
        context['inscritos'] = sorted(inscritos_con_puntos, key=lambda x: x['puntos'], reverse=True)  # Obtenemos los jugadores inscritos en el torneo para mostrar en el detalle del torneo, también ordenamos la lista de inscritos por puntos

        return context



class TorneoDeleteView(LoginRequiredMixin, DeleteView):
    '''Esta clase al heredar de DeleteView nos permitirá eliminar un torneo, 
    solo tenemos que indicarle el modelo que queremos eliminar y el template que queremos usar 
    para mostrar el formulario de eliminación'''
    
    model = Torneo
    context_object_name = 'torneo'
    success_url = reverse_lazy('lista_torneos')  # URL a la que se redirigirá después de eliminar un torneo

    # Dispatch comprueba que el usario que quiere acceder a esta vista tiene el rol de organizador, si no es así, se muestra un mensaje de error y se redirige a la lista de torneos
    def dispatch(self, request, *args, **kwargs):

        if request.user.role != 'organizador':

            messages.error(request, 'No tienes permiso para crear un torneo.')

            return redirect('lista_torneos')

        return super().dispatch(request, *args, **kwargs)
    


class TorneoCreateView(LoginRequiredMixin, CreateView):
    '''Esta clase al heredar de CreateView nos permitirá crear un nuevo torneo, 
    solo tenemos que indicarle el modelo que queremos crear y el template que queremos usar 
    para mostrar el formulario de creación'''
    
    model = Torneo
    template_name = 'torneos/torneo_form.html'
    form_class = Torneo_Form
    success_url = reverse_lazy('lista_torneos')  # URL a la que se redirigirá después de crear un torneo

    # Dispatch comprueba que el usario que quiere acceder a esta vista tiene el rol de organizador, si no es así, se muestra un mensaje de error y se redirige a la lista de torneos
    def dispatch(self, request, *args, **kwargs):

        if request.user.role != 'organizador':

            messages.error(request, 'No tienes permiso para crear un torneo.')

            return redirect('lista_torneos')

        return super().dispatch(request, *args, **kwargs)
    
    # También obtendremos el contexto para pasarlo al template para mostrar el texto que queremos, ya que es un template compartido
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Formulario de creación de Torneo'
        context['encabezado'] = 'Crear Torneo'
        context['texto_boton'] = 'Crear'

        return context
    


class TorneoUpdateView(LoginRequiredMixin, UpdateView):
    '''Esta clase al heredar de UpdateView nos permitirá editar un torneo existente, 
    solo tenemos que indicarle el modelo que queremos editar y el template que queremos usar 
    para mostrar el formulario de edición'''
    
    model = Torneo
    template_name = 'torneos/torneo_form.html'
    form_class = Torneo_Form
    success_url = reverse_lazy('lista_torneos')  # URL a la que se redirigirá después de editar un torneo

    # Dispatch comprueba que el usario que quiere acceder a esta vista tiene el rol de organizador, si no es así, se muestra un mensaje de error y se redirige a la lista de torneos
    def dispatch(self, request, *args, **kwargs):

        if request.user.role != 'organizador':

            messages.error(request, 'No tienes permiso para crear un torneo.')

            return redirect('lista_torneos')

        return super().dispatch(request, *args, **kwargs)
    
    # También obtendremos el contexto para pasarlo al template para mostrar el texto que queremos, ya que es un template compartido
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Formulario de edición de Torneo'
        context['encabezado'] = 'Editar Torneo'
        context['texto_boton'] = 'Guardar Cambios'

        return context