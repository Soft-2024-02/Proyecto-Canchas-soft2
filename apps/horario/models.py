from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.cancha.models import Cancha
from datetime import datetime, time

class Horario(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='horarios')
    dia = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    
    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ['cancha', 'dia']
    
    def __str__(self):
        return f'{self.cancha.nombre} - {self.dia} de {self.hora_inicio} a {self.hora_fin}'
    
    def clean(self):
        ahora = datetime.now()
        
        if isinstance(self.dia, str):
            self.dia = datetime.strptime(self.dia, "%Y-%m-%d").date()
        if isinstance(self.hora_inicio, str):
            self.hora_inicio = datetime.strptime(self.hora_inicio, "%H:%M").time()
        if isinstance(self.hora_fin, str):
            self.hora_fin = datetime.strptime(self.hora_fin, "%H:%M").time()
        
        # Validación: Solo permitir horarios en fechas futuras o la fecha actual en horas posteriores
        if self.dia < ahora.date() or (self.dia == ahora.date() and self.hora_inicio <= ahora.time()):
            raise ValidationError("El horario debe ser en una fecha y hora futuras.")
        # Validación: La hora de inicio debe ser antes de la hora de fin
        if self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        # Validación: La hora de fin puede ser 23:59 pero no más allá
        if self.hora_fin > time(23, 59):
            raise ValidationError("La hora de fin no puede superar las 23:59.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)