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
import re

class CanchaViewSet(viewsets.ModelViewSet):
    serializer_class = CanchaSerializer
    queryset = Cancha.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

def obtener_dias_horarios(cancha):
    horarios = Horario.objects.filter(cancha=cancha).order_by('dia', 'hora_inicio')
    today = datetime.now().date()
    
    dias_horarios = []
    
    for dia, horarios_dia in groupby(horarios, key=attrgetter('dia')):
        horarios_dia = list(horarios_dia)
        horas_dia = []
        # Generar todas las horas entre 00:00 y 23:00
        for h in range(24):
            hora_inicio = time(hour=h, minute=0)
            if h == 23:  # Último bloque del día
                hora_fin = time(hour=23, minute=59)
            else:
                hora_fin = (datetime.combine(today, hora_inicio) + timedelta(hours=1)).time()
            # Buscar si la hora está dentro de algún horario creado
            horario_encontrado = next(
                (horario for horario in horarios_dia if horario.hora_inicio <= hora_inicio < horario.hora_fin),
                None
            )
            if horario_encontrado:
                # Verificar si está reservado
                reservado = Reserva.objects.filter(
                    horario=horario_encontrado,
                    hora_reserva_inicio=hora_inicio,
                    hora_reserva_fin=hora_fin
                ).exists()
                if reservado:
                    estado = "rojo"  # Reservado
                else:
                    estado = "verde"  # Disponible
            else:
                estado = "gris"  # Sin horario
            # Añadir bloque de hora
            horas_dia.append({
                "id": horario_encontrado.id if horario_encontrado else None,
                "hora_inicio": hora_inicio.strftime('%H:%M'),
                "hora_fin": hora_fin.strftime('%H:%M'),
                "estado": estado,
            })
        # Agregar información del día
        dias_horarios.append({
            "dia": dia.strftime('%Y-%m-%d'),
            "horas": horas_dia,
            "hora_inicio": horarios_dia[0].hora_inicio.strftime('%H:%M') if horarios_dia else None,
            "hora_fin": horarios_dia[-1].hora_fin.strftime('%H:%M') if horarios_dia else None,
        })
    return dias_horarios

@login_required
def detalle_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug)
    dias_horarios = obtener_dias_horarios(cancha)
    calificacion = cancha.promedio_calificaciones()
    reseña = Reseña.objects.filter(usuario=request.user, cancha=cancha).first()
    reseñas = Reseña.objects.filter(cancha=cancha).order_by('-id')
    contexto = {
        'cancha': cancha,
        'responsable': request.user == cancha.responsable,
        'reseña': reseña,
        'reseñas': reseñas,
        'calificacion': calificacion,
        'dias_horarios': dias_horarios,
        'horas': [time(hour=h).strftime('%H:%M') for h in range(24)],
        'hoy': datetime.now().date().strftime('%Y-%m-%d'),
    }
    return render(request, 'cancha/detalle_cancha/detalle_cancha.html', contexto)

def validar_datos_cancha(request):
    nombre = request.POST.get('nombre', '').strip()
    tipo_calle = request.POST.get('tipo_calle', '').strip()
    nombre_calle = request.POST.get('nombre_calle', '').strip()
    numero_calle = request.POST.get('numero_calle', '').strip()
    distrito = request.POST.get('distrito', '').strip()
    referencia = request.POST.get('referencia', '').strip()
    imagen = request.FILES.get('imagen')
    
    if not all([nombre, tipo_calle, nombre_calle, numero_calle, distrito]):
        return None, 'Todos los campos obligatorios deben estar completos.'
    if not re.match(r'^[A-Za-z0-9\s]+$', nombre):
        return None, 'El nombre solo puede contener letras, números y espacios.'
    if not numero_calle.isdigit():
        return None, 'El número de la calle debe ser un valor numérico.'
    if referencia and not re.match(r'^[A-Za-z0-9\s,.]+$', referencia):
        return None, 'La referencia solo puede contener letras, números, comas y puntos.'
    if not imagen:
        imagen = 'canchas/default-cancha.jpg'
    
    return {
        'nombre': nombre,
        'tipo_calle': tipo_calle,
        'nombre_calle': nombre_calle,
        'numero_calle': numero_calle,
        'distrito': distrito,
        'referencia': referencia,
        'imagen': imagen
    }, None

@login_required
def registro_cancha(request):
    if request.method == 'POST':
        datos, error = validar_datos_cancha(request)
        if error:
            return render(request, 'cancha/registro_cancha.html', {'error': error})
        
        # Usar la fábrica para crear la cancha con su dirección
        factory = CanchaConcreteFactory()
        cancha = factory.create_cancha(
            nombre=datos['nombre'],
            usuario=request.user
        )
        if cancha:
            direccion = factory.create_direccion(
                cancha=cancha,
                tipo_calle=datos['tipo_calle'],
                nombre_calle=datos['nombre_calle'],
                numero_calle=datos['numero_calle'],
                distrito=datos['distrito'],
                referencia=datos['referencia'],
            )
            if direccion:
                messages.success(request, 'Cancha registrada correctamente.')
                return redirect('detalle_cancha', cancha.id, cancha.slug)
            else:
                return render(request, 'cancha/registro_cancha.html', {'error': 'Error al registrar la dirección. Intente nuevamente.'})
        return render(request, 'cancha/registro_cancha.html', {'error': 'Error al crear la cancha. Intente nuevamente.'})
    return render(request, 'cancha/registro_cancha.html')

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
def agregar_horario(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug)
    dia = request.POST.get('dia')
    hora_inicio = request.POST.get('hora_inicio')
    hora_fin = request.POST.get('hora_fin')
    try:
        ahora = datetime.now()
        if isinstance(dia, str):
            dia = datetime.strptime(dia, "%Y-%m-%d").date()
        if isinstance(hora_inicio, str):
            hora_inicio = datetime.strptime(hora_inicio, "%H:%M").time()
        if isinstance(hora_fin, str):
            hora_fin = datetime.strptime(hora_fin, "%H:%M").time()
        
        # Validar que el horario sea en una fecha y hora futuras
        if dia < ahora.date() or (dia == ahora.date() and hora_inicio <= ahora.time()):
            raise ValueError("El horario debe ser en una fecha y hora futuras.")
        # Validar que hora de inicio debe ser antes de la hora de fin
        if hora_inicio >= hora_fin:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin.")
        # Validar que no exista un horario con el mismo dia y hora
        if Horario.objects.filter(cancha_id=cancha_id, dia=dia).exists():
            raise ValueError("Ya existe un horario para este día y cancha.")
        
        # Crear el horario
        Horario.objects.create(
            cancha=cancha,
            dia=dia,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        messages.success(request, "Horario agregado exitosamente.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)

@login_required
@require_POST
def editar_horarios_dia(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    dia = request.POST.get('dia')
    hora_inicio = request.POST.get('hora_inicio')
    hora_fin = request.POST.get('hora_fin')
    try:
        # Validación de existencia de horarios para el día seleccionado
        horarios_existentes = Horario.objects.filter(cancha=cancha, dia=dia)
        if not horarios_existentes.exists():
            messages.error(request, f"No hay horarios existentes para el día {dia}.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        
        # Validaciones de entrada
        if not hora_inicio or not hora_fin:
            messages.error(request, "Debe especificar una hora de inicio y una hora de fin.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        
        # Validar formato de las horas
        hora_inicio_dt = datetime.strptime(hora_inicio, "%H:%M").time()
        hora_fin_dt = datetime.strptime(hora_fin, "%H:%M").time()
        if hora_inicio_dt >= hora_fin_dt:
            messages.error(request, "La hora de inicio debe ser anterior a la hora de fin.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        if hora_fin_dt > time(23, 59):
            messages.error(request, "La hora de fin no puede superar las 23:59.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        
        # Verificar reservas en conflicto
        reservas_en_conflicto = []
        for horario in horarios_existentes:
            reservas = Reserva.objects.filter(horario=horario)
            for reserva in reservas:
                if reserva.hora_reserva_inicio < hora_inicio_dt or reserva.hora_reserva_fin > hora_fin_dt:
                    reservas_en_conflicto.append(reserva)
        
        if reservas_en_conflicto:
            reservas_detalle = ", ".join(
                f"Reserva de {reserva.usuario} de {reserva.hora_reserva_inicio} a {reserva.hora_reserva_fin}" for reserva in reservas_en_conflicto
            )
            messages.error(
                request, 
                f"No se pueden modificar los horarios porque existen reservas en conflicto: {reservas_detalle}."
            )
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        
        # Actualizar los horarios
        for horario in horarios_existentes:
            horario.hora_inicio = hora_inicio_dt
            horario.hora_fin = hora_fin_dt
            horario.save()
        
        messages.success(request, f"Horarios del día {dia} actualizados exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al editar horarios: {str(e)}")
    return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)

@login_required
@require_POST
def eliminar_horarios_dia(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    dia = request.POST.get('dia')
    try:
        # Eliminar todos los horarios asociados al día y a la cancha seleccionada
        horarios_eliminados = Horario.objects.filter(cancha=cancha, dia=dia).delete()
        if horarios_eliminados[0] > 0:  # Chequea si se eliminaron registros
            messages.success(request, f"Todos los horarios del día {dia} han sido eliminados.")
        else:
            messages.warning(request, f"No se encontraron horarios para el día {dia}.")
    except Exception as e:
        messages.error(request, f"Error al eliminar horarios: {str(e)}")
    return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)

@login_required
def detalle_horario(request, cancha_id, cancha_slug, horario_id, hora_inicio, hora_fin):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug)
    horario = get_object_or_404(Horario, id=horario_id, cancha=cancha)
    precio = 100  # Precio ficticio por hora
    
    # Convertir las horas de inicio y fin de la URL
    hora_inicio_obj = datetime.strptime(hora_inicio, "%H:%M").time()
    hora_fin_obj = datetime.strptime(hora_fin, "%H:%M").time()
    
    contexto = {
        'cancha': cancha,
        'horario': horario,
        'hora_inicio': hora_inicio_obj,
        'hora_fin': hora_fin_obj,
        'responsable': cancha.responsable,
        'precio': precio,
    }
    return render(request, 'cancha/detalle_cancha/reservar_horario/detalle_horario.html', contexto)

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
