from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializer import CanchaSerializer
from apps.usuario.factory import CanchaConcreteFactory
from apps.horario.models import Horario
from apps.reserva.models import Reserva
from apps.reseña.models import Reseña
from .models import Cancha
from datetime import timedelta, datetime, time
from itertools import groupby
from operator import attrgetter


class CanchaViewSet(viewsets.ModelViewSet):
    serializer_class = CanchaSerializer
    queryset = Cancha.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

@login_required
def editar_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    direccion = cancha.direcciones.first()
    if request.method == 'POST':
        datos, error = validar_datos_cancha(request)
        if error:
            messages.error(request, error)
            return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})
        if not direccion:
            messages.error(request, 'Dirección no encontrada.')
            return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})
        
        cancha.nombre = datos['nombre']
        cancha.imagen = datos['imagen']
        direccion.tipo_calle = datos['tipo_calle']
        direccion.nombre_calle = datos['nombre_calle']
        direccion.numero_calle = datos['numero_calle']
        direccion.distrito = datos['distrito']
        direccion.referencia = datos['referencia']
        
        direccion.save()
        cancha.save()
        
        messages.success(request, 'Datos actualizados correctamente.')
        return redirect('detalle_cancha', cancha.id, cancha.slug)
    return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})

@login_required
@require_POST
def cambiar_imagen(request):
    user = request.user
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

@login_required
@require_POST
def eliminar_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    contraseña = request.POST.get('password')
    if not request.user.check_password(contraseña):
        messages.error(request, 'Contraseña incorrecta.')
        return redirect('editar_cancha', cancha_id, cancha_slug)
    cancha.delete()
    messages.success(request, 'La cancha fue eliminada correctamente.')
    return redirect('inicio')

@login_required
@require_POST
def reservar_horario(request, cancha_id, cancha_slug, horario_id, hora_inicio, hora_fin):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug)
    horario = get_object_or_404(Horario, id=horario_id, cancha=cancha)
    try:
        hora_inicio_obj = hora_inicio if isinstance(hora_inicio, time) else time.fromisoformat(hora_inicio)
        hora_fin_obj = hora_fin if isinstance(hora_fin, time) else time.fromisoformat(hora_fin)
        
        # Validar que las horas sean consistentes con el horario general
        if not (horario.hora_inicio <= hora_inicio_obj < hora_fin_obj <= horario.hora_fin):
            messages.error(request, "El rango de horas no es válido dentro del horario disponible.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        
        # Validar si el rango de horas ya está reservado
        reservas_conflictivas = Reserva.objects.filter(
            horario=horario,
            hora_reserva_inicio__lt=hora_fin_obj,
            hora_reserva_fin__gt=hora_inicio_obj
        )
        if reservas_conflictivas.exists():
            hora_inicio = reservas_conflictivas.first().hora_reserva_inicio.strftime('%H:%M')
            hora_fin = reservas_conflictivas.first().hora_reserva_fin.strftime('%H:%M')
            messages.error(request, "Este horario ya está reservado.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        
        # Crear la reserva
        Reserva.objects.create(
            usuario=request.user,
            horario=horario,
            hora_reserva_inicio=hora_inicio_obj,
            hora_reserva_fin=hora_fin_obj,
        )
        messages.success(request, f"Reserva exitosa: {hora_inicio_obj.strftime('%H:%M')} - {hora_fin_obj.strftime('%H:%M')}")
    except ValueError:
        messages.error(request, "Formato de hora inválido.")
    except Exception as e:
        messages.error(request, f"Error al reservar el horario: {e}")
    
    return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
