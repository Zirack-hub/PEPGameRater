from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Videojuego, Calificacion, Comentario
from .forms import VideojuegoForm, CalificacionForm, ComentarioForm

class VideojuegoListView(ListView):
    model = Videojuego
    template_name = 'juegos/lista.html'
    context_object_name = 'juegos'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) | Q(descripcion__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busqueda'] = self.request.GET.get('q', '')
        return context

class VideojuegoDetailView(DetailView):
    model = Videojuego
    template_name = 'juegos/detalle.html'
    context_object_name = 'juego'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        juego = self.get_object()
        context['form_calificacion'] = CalificacionForm()
        context['form_comentario'] = ComentarioForm()
        context['calificaciones'] = juego.calificaciones.select_related('usuario')
        context['comentarios'] = juego.comentarios.select_related('autor')
        context['ya_califico'] = False
        return context

class VideojuegoCreateView(CreateView):
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'juegos/formulario.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Añadir videojuego'
        context['boton_texto'] = 'Añadir'
        return context

class VideojuegoUpdateView(UpdateView):
    model = Videojuego
    form_class = VideojuegoForm
    template_name = 'juegos/formulario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f'Editar: {self.get_object().titulo}'
        context['boton_texto'] = 'Guardar cambios'
        return context

class VideojuegoDeleteView(DeleteView):
    model = Videojuego
    template_name = 'juegos/confirmar_borrado.html'
    success_url = reverse_lazy('juegos:lista')
    context_object_name = 'juego'