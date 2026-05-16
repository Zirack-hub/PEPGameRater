from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistroForm


# Vista para registrar un nuevo usuario
def registro(request):
    # Si ya está logueado lo mandamos al inicio
    if request.user.is_authenticated:
        return redirect('juegos:lista')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardamos el usuario y lo logueamos automáticamente
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Cuenta creada correctamente.')
            return redirect('juegos:lista')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})
