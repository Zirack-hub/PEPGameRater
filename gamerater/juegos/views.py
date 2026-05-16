from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Videojuego, Calificacion, Comentario
from .forms import VideojuegoForm, CalificacionForm, ComentarioForm


# Vista que muestra la lista de todos los videojuegos con búsqueda
class VideojuegoListView(ListView):
    model = Videojuego
    template_name = 'juegos/lista.html'
    context_object_name = 'juegos'
    paginate_by = 9

    # Filtra los videojuegos si hay un término de búsqueda
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            # Busca en el título y en la descripción a la vez
            queryset = queryset.filter(
                Q(titulo__icontains=q) | Q(descripcion__icontains=q)
            )
        return queryset

    # Añade el término de búsqueda al contexto para mostrarlo en el template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busqueda'] = self.request.GET.get('q', '')
        return context


# Vista que muestra el detalle de un videojuego con sus calificaciones y comentarios
class VideojuegoDetailView(DetailView):
    model = Videojuego
    template_name = 'juegos/detalle.html'
    context_object_name = 'juego'

    # Añade los formularios y datos extra al contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        juego = self.get_object()

        context['form_calificacion'] = CalificacionForm()
        context['form_comentario'] = ComentarioForm()
        context['calificaciones'] = juego.calificaciones.select_related('usuario')
        context['comentarios'] = juego.comentarios.select_related('autor')

        # Comprueba si el usuario ya ha calificado este juego
        if self.request.user.is_authenticated:
            context['ya_califico'] = juego.calificaciones.filter(
                usuario=self.request.user
            ).exists()
        else:
            context['ya_califico'] = False

        return context

    # Procesa el envío de calificaciones y comentarios desde la página de detalle
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para participar.')
            return redirect('usuarios:login')

        juego = self.get_object()
        accion = request.POST.get('accion')

        if accion == 'calificar':
            # Comprueba que el usuario no haya calificado ya este juego
            if juego.calificaciones.filter(usuario=request.user).exists():
                messages.warning(request, 'Ya has calificado este juego.')
                return redirect('juegos:detalle', pk=juego.pk)

            form = CalificacionForm(request.POST)
            if form.is_valid():
                calificacion = form.save(commit=False)
                calificacion.videojuego = juego
                calificacion.usuario = request.user
                calificacion.save()
                messages.success(request, '¡Calificación enviada correctamente!')
            else:
                messages.error(request, 'Error en el formulario de calificación.')

        elif accion == 'comentar':
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.videojuego = juego
                comentario.autor = request.user
                comentario.save()
                messages.success(request, 'Comentario añadido.')
            else:
                messages.error(request, 'Error en el formulario de comentario.')

        return redirect('juegos:detalle', pk=juego.pk)


# Vista para crear un nuevo videojuego, solo usuarios autenticados
class VideojuegoCreateView(LoginRequiredMixin, CreateView):
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'juegos/formulario.html'

    # Asigna el autor automáticamente al usuario que está logueado
    def form_valid(self, form):
        form.instance.autor = self.request.user
        messages.success(self.request, '¡Videojuego añadido correctamente!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Añadir videojuego'
        context['boton_texto'] = 'Añadir'
        return context


# Vista para editar un videojuego, solo el autor o un staff puede hacerlo
class VideojuegoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'juegos/formulario.html'

    # Comprueba que el usuario sea el autor o tenga permisos de staff
    def test_func(self):
        juego = self.get_object()
        return self.request.user == juego.autor or self.request.user.is_staff

    # Si no tiene permiso muestra un mensaje y redirige
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para editar este videojuego.')
        return redirect('juegos:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Videojuego actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f'Editar: {self.get_object().titulo}'
        context['boton_texto'] = 'Guardar cambios'
        return context


# Vista para eliminar un videojuego, solo el autor o staff puede hacerlo
class VideojuegoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Videojuego
    template_name = 'juegos/confirmar_borrado.html'
    success_url = reverse_lazy('juegos:lista')
    context_object_name = 'juego'

    # Comprueba que el usuario sea el autor o tenga permisos de staff
    def test_func(self):
        juego = self.get_object()
        return self.request.user == juego.autor or self.request.user.is_staff

    # Si no tiene permiso muestra un mensaje y redirige
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para eliminar este videojuego.')
        return redirect('juegos:lista')

    def form_valid(self, form):
        messages.success(self.request, 'Videojuego eliminado.')
        return super().form_valid(form)


# Función para eliminar una calificación propia
def borrar_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    juego_pk = calificacion.videojuego.pk

    if request.user == calificacion.usuario or request.user.is_staff:
        calificacion.delete()
        messages.success(request, 'Calificación eliminada.')
    else:
        messages.error(request, 'No puedes eliminar esta calificación.')

    return redirect('juegos:detalle', pk=juego_pk)


# Función para eliminar un comentario propio
def borrar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    juego_pk = comentario.videojuego.pk

    if request.user == comentario.autor or request.user.is_staff:
        comentario.delete()
        messages.success(request, 'Comentario eliminado.')
    else:
        messages.error(request, 'No puedes eliminar este comentario.')

    return redirect('juegos:detalle', pk=juego_pk)
