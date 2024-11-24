from django.contrib import admin
from .models import Reseña

class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cancha', 'calificacion', 'fecha_creacion')
    list_filter = ('calificacion', 'fecha_creacion')
    search_fields = ('usuario__username', 'cancha__nombre')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion',)
    
admin.site.register(Reseña, ReseñaAdmin)