from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import time
from apps.horario.models import Horario

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='reservas')
    hora_reserva_inicio = models.TimeField()
    hora_reserva_fin = models.TimeField()
    fecha_reserva = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
    
    def __str__(self):
        return f'{self.usuario} reserva {self.horario.cancha.nombre} el {self.horario.dia} de {self.hora_reserva_inicio} a {self.hora_reserva_fin}'
    
    def clean(self):
        hora_reserva_inicio = self.hora_reserva_inicio if isinstance(self.hora_reserva_inicio, time) else time.fromisoformat(self.hora_reserva_inicio)
        hora_reserva_fin = self.hora_reserva_fin if isinstance(self.hora_reserva_fin, time) else time.fromisoformat(self.hora_reserva_fin)
        
        # Validación: La reserva debe estar dentro del horario disponible
        if not (hora_reserva_inicio >= self.horario.hora_inicio and hora_reserva_fin <= self.horario.hora_fin):
            raise ValidationError("La reserva debe estar dentro del horario disponible.")
        
        # Validación: La hora reserva de inicio debe ser antes de la hora reserva de fin
        if hora_reserva_inicio >= hora_reserva_fin:
            raise ValidationError("La hora reserva de inicio debe ser anterior a la hora reserva de fin.")
        
        # Validación: Evitar reservas cruzadas en el mismo horario
        reservas_conflictivas = Reserva.objects.filter(
            horario__cancha=self.horario.cancha,
            horario__dia=self.horario.dia,
            hora_reserva_inicio__lt=hora_reserva_fin,
            hora_reserva_fin__gt=hora_reserva_inicio
        ).exclude(id=self.id)
        
        if reservas_conflictivas.exists():
            raise ValidationError("El horario seleccionado ya está reservado. Elige otro horario.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)