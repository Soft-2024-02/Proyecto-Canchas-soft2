from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'horario', 'hora_reserva_inicio', 'hora_reserva_fin', 'fecha_reserva']
    list_filter = ['horario__cancha', 'horario__dia', 'usuario']
    search_fields = ['usuario__email', 'horario__cancha__nombre']

admin.site.register(Reserva, ReservaAdmin)