from django.urls import path
from . import views

app_name = 'juegos'

urlpatterns = [
    # Página principal con el catálogo de videojuegos
    path('', views.VideojuegoListView.as_view(), name='lista'),
    # Detalle de un videojuego concreto
    path('<int:pk>/', views.VideojuegoDetailView.as_view(), name='detalle'),
    # Formulario para añadir un nuevo videojuego
    path('nuevo/', views.VideojuegoCreateView.as_view(), name='crear'),
    # Formulario para editar un videojuego existente
    path('<int:pk>/editar/', views.VideojuegoUpdateView.as_view(), name='editar'),
    # Página de confirmación para borrar un videojuego
    path('<int:pk>/borrar/', views.VideojuegoDeleteView.as_view(), name='borrar'),
    # Borrar una calificación concreta
    path('calificacion/<int:pk>/borrar/', views.borrar_calificacion, name='borrar_calificacion'),
    # Borrar un comentario concreto
    path('comentario/<int:pk>/borrar/', views.borrar_comentario, name='borrar_comentario'),
]
