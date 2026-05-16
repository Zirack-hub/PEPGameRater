from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    # URLs de la app de videojuegos en la raíz del sitio
    path('', include('juegos.urls', namespace='juegos')),
    # URLs de la app de usuarios bajo /usuarios/
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
