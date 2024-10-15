from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.usuario.factory import CanchaConcreteFactory
from .serializer import CanchaSerializer
from .models import Cancha

class CanchaViewSet(viewsets.ModelViewSet):
    serializer_class = CanchaSerializer
    queryset = Cancha.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

@login_required
def registro_cancha(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_calle = request.POST.get('tipo_calle')
        nombre_calle = request.POST.get('nombre_calle')
        numero_calle = request.POST.get('numero_calle')
        distrito = request.POST.get('distrito')
        referencia = request.POST.get('referencia')
        
        # Usar la fábrica para crear la cancha con su dirección
        factory = CanchaConcreteFactory()
        cancha = factory.create_cancha(
            nombre=nombre,
            usuario=request.user
        )
        if cancha:
            direccion = factory.create_direccion(
                cancha=cancha,
                tipo_calle=tipo_calle,
                nombre_calle=nombre_calle,
                numero_calle=numero_calle,
                distrito=distrito,
                referencia=referencia,
            )
            if direccion:
                messages.success(request, 'Cancha registrada correctamente.')
                return redirect('detalle_cancha', cancha.id, cancha.slug)
            else:
                return render(request, 'cancha/registro_cancha.html', {'error': 'Error al registrar la dirección. Intente nuevamente.'})
        return render(request, 'cancha/registro_cancha.html', {'error': 'Error al crear la cancha. Intente nuevamente.'})
    return render(request, 'cancha/registro_cancha.html')

@login_required
def detalle_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug)
    contexto = {
        'cancha': cancha,
        'responsable': request.user == cancha.responsable
    }
    return render(request, 'cancha/detalle_cancha/detalle_cancha.html', contexto)

@login_required
def editar_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    direccion = cancha.direcciones.first()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_calle = request.POST.get('tipo_calle')
        nombre_calle = request.POST.get('nombre_calle')
        numero_calle = request.POST.get('numero_calle')
        distrito = request.POST.get('distrito')
        referencia = request.POST.get('referencia')
        
        if not all([nombre, tipo_calle, nombre_calle, numero_calle, distrito]):
            messages.error(request, 'Todos los campos obligatorios deben estar completos.')
            return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})
        if not direccion:
            messages.error(request, 'Dirección no encontrada.')
            return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})
        
        cancha.nombre = nombre
        direccion.tipo_calle = tipo_calle
        direccion.nombre_calle = nombre_calle
        direccion.numero_calle = numero_calle
        direccion.distrito = distrito
        direccion.referencia = referencia
        direccion.save()
        cancha.save()
        messages.success(request, 'Datos actualizados correctamente.')
        return redirect('detalle_cancha', cancha.id, cancha.slug)
    return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})

@login_required
@require_POST
def eliminar_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    if request.method == 'POST':
        contraseña = request.POST.get('password')
        if not request.user.check_password(contraseña):
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('detalle_cancha', cancha_id, cancha_slug)
        cancha.delete()
        messages.success(request, 'La cancha fue eliminada correctamente.')
        return redirect('inicio')
    return redirect('detalle_cancha', cancha_id, cancha_slug)