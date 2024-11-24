from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import ReservaSerializer
from apps.horario.models import Horario
from .models import Reserva
from datetime import timedelta, datetime, time
from itertools import groupby
from operator import attrgetter

class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    queryset = Reserva.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        horario_id = request.data.get('horario')
        hora_reserva_inicio = request.data.get('hora_reserva_inicio')
        hora_reserva_fin = request.data.get('hora_reserva_fin')
        # Crear instancia de Reserva para validación
        reserva = Reserva(
            usuario=request.user,
            horario_id=horario_id,
            hora_reserva_inicio=hora_reserva_inicio,
            hora_reserva_fin=hora_reserva_fin
        )
        try:
            reserva.clean()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return super(ReservaViewSet, self).create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super(ReservaViewSet, self).destroy(request, *args, **kwargs)


@never_cache
@login_required
@require_POST
def cancelar_reserva(request, reserva_id):
    try:
        reserva = Reserva.objects.get(id=reserva_id, usuario=request.user)
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva que intentas ver ya no existe.")
        return redirect('mis_reservas')
    
    reserva.delete()
    messages.success(request, "Reserva cancelada exitosamente.")
    return HttpResponseRedirect(reverse('mis_reservas'))