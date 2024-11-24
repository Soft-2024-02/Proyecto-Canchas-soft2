from django.db import models
from apps.cancha.models import Cancha

class Direccion(models.Model):
    TIPOS_CALLE = [
        ('avenida', 'Avenida'),
        ('calle', 'Calle'),
        ('jiron', 'Jirón'),
        ('pasaje', 'Pasaje')
    ]
    
    DISTRITOS = [
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
        ('villa_maria_del_triunfo', 'Villa María del Triunfo')
    ]
    
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='direcciones')
    tipo_calle = models.CharField('Tipo de Calle', max_length=20, choices=TIPOS_CALLE, blank=False, null=False)
    nombre_calle = models.CharField('Nombre de la Calle', max_length=50, blank=False, null=False)
    numero_calle = models.CharField('Número de la Calle', max_length=5, blank=False, null=False)
    distrito = models.CharField('Distrito', max_length=50, choices=DISTRITOS, blank=False, null=False)
    referencia = models.CharField('Referencia', max_length=50, blank=True, null=True, help_text="Punto de referencia opcional")
    
    def __str__(self):
        return f'{self.tipo_calle} {self.nombre_calle} {self.numero_calle}, {self.distrito}'
    
    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'
