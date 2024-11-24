from django.db import models
from django.conf import settings
from apps.cancha.models import Cancha

class Reseña(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reseñas')
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='reseñas')
    calificacion = models.PositiveSmallIntegerField('Calificación', choices=[(i, i) for i in range(1, 6)], blank=False, null=False)
    comentario = models.TextField('Comentario', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'reseñas'
        unique_together = ('usuario', 'cancha')
    
    def __str__(self):
        return f'{self.usuario} - {self.cancha} - {self.calificacion} estrellas'