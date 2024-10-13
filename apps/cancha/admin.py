from django.contrib import admin
from .models import Cancha

class CanchaAdmin(admin.ModelAdmin):
    list_display = ['responsable', 'nombre', 'disponibilidad', 'fecha_creacion', 'ultima_modificacion', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ['fecha_creacion', 'ultima_modificacion']

admin.site.register(Cancha, CanchaAdmin)