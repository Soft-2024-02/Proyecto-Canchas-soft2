from django.contrib import admin
from .models import Horario

class HorarioAdmin(admin.ModelAdmin):
    list_display = ['cancha', 'dia', 'hora_inicio', 'hora_fin']
    list_filter = ['cancha', 'dia']
    search_fields = ['cancha__nombre', 'dia']

admin.site.register(Horario, HorarioAdmin)