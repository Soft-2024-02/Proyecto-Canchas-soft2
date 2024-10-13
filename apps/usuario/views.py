from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework import viewsets
from .serializer import UsuarioSerializer
from .models import Usuario
from .forms import RegistroUsuarioForm

# ViewSet para la API REST
class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    lookup_field = 'slug'


# Vista para la página de inicio
def inicio(request):
    from apps.cancha.models import Cancha
    canchas = Cancha.objects.prefetch_related('direcciones').all()
    contexto = {
        'canchas': canchas
    }
    return render(request, 'usuario/inicio/inicio.html', contexto)


# Registro de usuarios (formulario de signup)
def signup(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                return render(request, 'usuario/signup.html', {'form': form, 'error': 'Error al autenticar. Intente nuevamente.'})
        else:
            return render(request, 'usuario/signup.html', {'form': form, 'error': 'Datos no válidos. Intente nuevamente.'})
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuario/signup.html', {'form': form})


# Inicio de sesión
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect(reverse('admin:index'))
            return redirect('inicio')
        return render(request, 'usuario/signin.html', {'form': AuthenticationForm, 'error': 'Correo o contraseña incorrectos.'})
    return render(request, 'usuario/signin.html', {'form': AuthenticationForm})


# Cerrar sesión
@login_required
def signout(request):
    logout(request)
    return redirect('signin')


# Ver el perfil de usuarios
def perfil(request, usuario_id, usuario_slug):
    user = get_object_or_404(Usuario, id=usuario_id, slug=usuario_slug)
    contexto = {'user': user}
    if user.is_responsible:
        contexto['responsable'] = user
    return render(request, 'usuario/perfil/perfil.html', contexto)


# Lleva a la vista de edición de perfil
@login_required
def editar_perfil(request):
    return render(request, 'usuario/editar_perfil/editar_perfil.html')


def validar_datos(request, user):
    email = request.POST.get('email')
    dni = request.POST.get('dni')
    nombre = request.POST.get('nombre')
    apellidos = request.POST.get('apellidos')
    celular = request.POST.get('celular')
    
    if not (email, dni, nombre, apellidos, celular):
        return None, 'Datos no válidos. Intente nuevamente.'
    
    if len(dni) != 8 or not dni.isdigit():
        return None, 'El DNI debe tener 8 dígitos numéricos.'
    if len(celular) != 9 or not celular.isdigit():
        return None, 'El número de celular debe tener 9 dígitos numéricos.'
    
    User = get_user_model()
    
    if email != user.email and User.objects.filter(email=email).exists():
        return None, 'El correo ingresado ya está en uso.'
    if dni != user.dni and User.objects.filter(dni=dni).exists():
        return None, 'El DNI ingresado ya está en uso.'
    if celular != user.celular and User.objects.filter(celular=celular).exists():
        return None, 'El número de celular ingresado ya está en uso.'
    
    return {
        'email': email,
        'dni': dni,
        'nombre': nombre,
        'apellidos': apellidos,
        'celular': celular
    }, None

# Actualizar perfil (con validación)
@login_required
def actualizar_perfil(request):
    user = request.user
    if request.method == 'POST':
        datos_comunes, error = validar_datos(request, user)
        if error:
            contexto = {'error': error, 'user': user}
            return render(request, 'usuario/editar_perfil/editar_perfil.html', contexto)
        user.email = datos_comunes['email']
        user.dni = datos_comunes['dni']
        user.nombre = datos_comunes['nombre']
        user.apellidos = datos_comunes['apellidos']
        user.celular = datos_comunes['celular']
        user.save()
    return redirect('perfil', user.id, user.slug)


# Cambiar imagen de perfil
@login_required
def cambiar_imagen(request):
    user = request.user
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        if imagen:
            user.imagen = imagen
            user.save()
            return redirect('perfil', user.id, user.slug)
        else:
            user.imagen = 'usuarios/default-avatar.jpg'
            user.save()
            return redirect('perfil', user.id, user.slug)
    return render(request, 'usuario/editar_perfil/editar_perfil.html', {'user': user})


# Validar contraseñas
def validar_password(password):
    if len(password) < 8:
        return 'La contraseña debe tener al menos 8 caracteres.'
    if password.isdigit() or password.isalpha():
        return 'La contraseña debe incluir al menos una letra y un número.'
    if password.islower() or password.isupper():
        return 'La contraseña debe tener al menos una letra mayúscula y una minúscula.'
    return None

# Cambiar la contraseña
@login_required
def cambiar_contrasena(request):
    user = request.user
    contexto = {'user': user}
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if user.check_password(password):
            if new_password == confirm_password:
                error = validar_password(new_password)
                if error:
                    contexto['error'] = error
                    return render(request, 'usuario/editar_perfil/editar_perfil.html', contexto)
                user.set_password(new_password)
                user.save()
                logout(request)  # Desloguear al usuario tras cambiar contraseña
                return redirect('signin')
            contexto['error'] = 'Las contraseñas no coinciden.'
        else:
            contexto['error'] = 'Contraseña actual incorrecta.'
    return render(request, 'usuario/editar_perfil/editar_perfil.html', contexto)


# Eliminar cuenta de usuario
@login_required
def eliminar_cuenta(request):
    user = request.user
    user.delete()
    return redirect('inicio')


# Manejo de errores 404 personalizados
def error_404_view(request, exception):
    return render(request, 'base/404.html', status=404)