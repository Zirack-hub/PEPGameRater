
Aplicación web de calificaciones y reseñas de videojuegos desarrollada con Django.

## Características

- Catálogo de videojuegos con imágenes
- Sistema de calificaciones (1-10) con reseñas
- Comentarios por juego
- Búsqueda y filtrado por título/descripción
- Autenticación completa (registro, login, logout)
- Solo el autor o staff puede editar/borrar su contenido
- Diseño responsivo con Bootstrap 5

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd gamerater

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser

# 6. Arrancar el servidor
python manage.py runserver
```

Accede en: http://127.0.0.1:8000

## URL en producción

https://samuelmerino.pythonanywhere.com

## Autores

- Emilio Rabadan
- Samuel Merino

## Tecnologías

- Python 3.11
- Django 4.2
- Bootstrap 5
- SQLite (desarrollo) / MySQL (producción)
- PythonAnywhere (despliegue)