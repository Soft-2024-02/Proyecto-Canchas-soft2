import datetime
from apps.horario.models import Horario

class AutoDeleteOldHorariosMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        self.eliminar_horarios_pasados()
        
        response = self.get_response(request)
        
        return response
    
    def eliminar_horarios_pasados(self):
        ahora = datetime.datetime.now()
        horarios_pasados = Horario.objects.filter(dia__lt=ahora.date()) | Horario.objects.filter(dia=ahora.date(), hora_fin__lte=ahora.time())
        
        if horarios_pasados.exists():
            horarios_pasados.delete()
