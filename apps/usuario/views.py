from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
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
    
    query = request.GET.get('q', '')
    distrito = request.GET.get('distrito', '')
    if query:
        canchas = canchas.filter(nombre__icontains=query)
    if distrito:
        canchas = canchas.filter(direcciones__distrito=distrito)
        
    contexto = {
        'canchas': canchas,
        'query': query,
        'distrito': distrito,
        'DISTRITOS': [
            ('barranco', 'Barranco'),
            ('callao', 'Callao'),
            ('cercado_de_lima', 'Cercado de Lima'),
            ('chorrillos', 'Chorrillos'),
            ('jesus_maria', 'Jesús María'),
            ('la_molina', 'La Molina'),
            ('lince', 'Lince'),
            ('los_olivos', 'Los Olivos'),
            ('magdalena', 'Magdalena'),
            ('miraflores', 'Miraflores'),
            ('pueblo_libre', 'Pueblo Libre'),
            ('rimac', 'Rímac'),
            ('san_borja', 'San Borja'),
            ('san_isidro', 'San Isidro'),
            ('san_juan_de_lurigancho', 'San Juan de Lurigancho'),
            ('san_juan_de_miraflores', 'San Juan de Miraflores'),
            ('san_miguel', 'San Miguel'),
            ('santiago_de_surco', 'Santiago de Surco'),
            ('surquillo', 'Surquillo'),
            ('ventanilla', 'Ventanilla'),
            ('villa_maria_del_triunfo', 'Villa María del Triunfo'),
        ],
    }
    
    return render(request, 'usuario/inicio/inicio.html', contexto)


# Registro de usuarios (formulario de signup)
def signup(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Bienvenido, ' + user.nombre + '.')
                return redirect('inicio')
            else:
                messages.error(request, 'Error al autenticar. Intente nuevamente.')
                return render(request, 'usuario/signup.html', {'form': form})
        else:
            messages.error(request, 'Datos no válidos. Intente nuevamente.')
            return render(request, 'usuario/signup.html', {'form': form})
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuario/signup.html', {'form': form})


# Inicio de sesión
def signin(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect(reverse('admin:index'))
            messages.success(request, 'Bienvenido, ' + user.nombre + '.')
            return redirect('inicio')
        messages.error(request, 'El correo o la contraseña son incorrectos.')
        return render(request, 'usuario/signin.html', {'form': AuthenticationForm})
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
@require_POST
def actualizar_perfil(request):
    user = request.user
    if request.method == 'POST':
        datos_comunes, error = validar_datos(request, user)
        if error:
            messages.error(request, error)
            return render(request, 'usuario/editar_perfil/editar_perfil.html', {'user': user})
        user.email = datos_comunes['email']
        user.dni = datos_comunes['dni']
        user.nombre = datos_comunes['nombre']
        user.apellidos = datos_comunes['apellidos']
        user.celular = datos_comunes['celular']
        user.save()
        messages.success(request, 'Datos actualizados correctamente.')
    return redirect('perfil', user.id, user.slug)


# Cambiar imagen de perfil
@login_required
@require_POST
def cambiar_imagen(request):
    user = request.user
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        if imagen:
            user.imagen = imagen
            user.save()
            messages.success(request, 'Imagen actualizada correctamente.')
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
@require_POST
def cambiar_contrasena(request):
    user = request.user
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if user.check_password(password):
            if new_password == confirm_password:
                error = validar_password(new_password)
                if error:
                    messages.error(request, error)
                    return render(request, 'usuario/editar_perfil/editar_perfil.html', {'user': user})
                user.set_password(new_password)
                user.save()
                logout(request)
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('signin')
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            messages.error(request, 'Contraseña actual incorrecta.')
    return render(request, 'usuario/editar_perfil/editar_perfil.html', {'user': user})


@login_required
@require_POST
def eliminar_cuenta(request):
    user = request.user
    password = request.POST.get('password')
    if authenticate(username=user.email, password=password):
        user.delete()
        logout(request)
        messages.success(request, 'Tu cuenta ha sido eliminada correctamente.')
        return redirect('inicio')
    else:
        messages.error(request, 'Contraseña incorrecta. No se pudo eliminar la cuenta.')
        return redirect('editar_perfil')


# Manejo de errores 404 personalizados
def error_404_view(request, exception):
    return render(request, 'base/404.html', status=404)