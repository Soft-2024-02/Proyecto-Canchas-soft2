from apps.cancha.models import Cancha
from apps.horario.models import Horario
from django.db.models import Q

class CanchaAvailabilityMiddleware:
    """
    Middleware que valida la disponibilidad de cada cancha en cada solicitud.
    Si una cancha tiene horarios no reservados, se marca como disponible.
    Si todos los horarios están reservados o no existen, se marca como no disponible.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Validar disponibilidad de las canchas
        self.actualizar_disponibilidad_canchas()
        response = self.get_response(request)
        return response
    
    def actualizar_disponibilidad_canchas(self):
        # Obtenemos todas las canchas
        canchas = Cancha.objects.all()
        
        # Actualizamos la disponibilidad para cada cancha
        for cancha in canchas:
            # Obtener horarios de la cancha
            horarios_disponibles = Horario.objects.filter(
                cancha=cancha
            ).exclude(
                Q(reservas__isnull=False)
            )
            # Actualizar el campo de disponibilidad
            cancha.disponibilidad = horarios_disponibles.exists()
            cancha.save()