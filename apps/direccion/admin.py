from django.contrib import admin
from .models import Direccion

class DireccionAdmin(admin.ModelAdmin):
    list_display = ['cancha', 'tipo_calle', 'nombre_calle', 'numero_calle', 'distrito']
    search_fields = ['nombre_calle', 'numero_calle', 'distrito']
    list_filter = ['distrito', 'tipo_calle']
    
    def distrito_legible(self, obj):
        return obj.get_distrito_display()
    distrito_legible.short_description = 'Distrito'

admin.site.register(Direccion, DireccionAdmin)