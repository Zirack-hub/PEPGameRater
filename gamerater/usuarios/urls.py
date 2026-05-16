from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Página de registro de nuevos usuarios
    path('registro/', views.registro, name='registro'),
    # Login usando la vista integrada de Django con nuestro template
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    # Logout usando la vista integrada de Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
