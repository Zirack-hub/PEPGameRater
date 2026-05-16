from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse


# Modelo para los géneros de los videojuegos
class Genero(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'géneros'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# Modelo principal de la aplicación
class Videojuego(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='juegos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Relación con el usuario que lo creó
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videojuegos')
    # Relación con el género, puede estar vacío
    genero = models.ForeignKey(
        Genero, on_delete=models.SET_NULL, null=True, blank=True, related_name='videojuegos'
    )

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo

    # Devuelve la URL del detalle del videojuego
    def get_absolute_url(self):
        return reverse('juegos:detalle', kwargs={'pk': self.pk})

    # Calcula la media de las calificaciones del videojuego
    def media_calificacion(self):
        resultado = self.calificaciones.aggregate(Avg('puntuacion'))
        media = resultado['puntuacion__avg']
        return round(media, 1) if media is not None else None

    # Devuelve el número de calificaciones
    def num_calificaciones(self):
        return self.calificaciones.count()


# Modelo para las calificaciones de los videojuegos
class Calificacion(models.Model):
    PUNTUACIONES = [(i, str(i)) for i in range(1, 11)]

    puntuacion = models.IntegerField(choices=PUNTUACIONES)
    resena = models.TextField(verbose_name='Reseña')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Relación con el videojuego calificado
    videojuego = models.ForeignKey(
        Videojuego, on_delete=models.CASCADE, related_name='calificaciones'
    )
    # Relación con el usuario que calificó
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones')

    class Meta:
        # Un usuario solo puede calificar una vez cada videojuego
        unique_together = ('videojuego', 'usuario')
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} → {self.videojuego.titulo}: {self.puntuacion}/10"


# Modelo para los comentarios de los videojuegos
class Comentario(models.Model):
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # Relación con el videojuego comentado
    videojuego = models.ForeignKey(
        Videojuego, on_delete=models.CASCADE, related_name='comentarios'
    )
    # Relación con el usuario que comentó
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.autor.username} en '{self.videojuego.titulo}'"
