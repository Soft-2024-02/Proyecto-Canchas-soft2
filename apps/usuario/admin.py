from django.contrib import admin
from .models import Usuario
from django.contrib.auth.models import Group

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['email', 'dni', 'nombre', 'apellidos', 'celular', 'is_responsible', 'is_staff', 'is_superuser', 'is_active', 'slug']
    search_fields = ['email', 'dni', 'nombre', 'apellidos', 'celular']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    list_editable = ['is_active', 'is_staff', 'is_superuser']
    prepopulated_fields = {'slug': ('nombre', 'apellidos')}
    actions = ['make_responsable', 'remove_responsable']
    
    def is_responsible(self, obj):
        return obj.groups.filter(name='Responsable').exists()
    is_responsible.boolean = True
    is_responsible.short_description = 'Es Responsable'
    
    def make_responsable(self, request, queryset):
        responsable_group, _ = Group.objects.get_or_create(name='Responsable')
        cliente_group = Group.objects.get(name='Cliente')
        for user in queryset:
            user.groups.add(responsable_group)
            user.groups.remove(cliente_group)
        self.message_user(request, "Los usuarios seleccionados ahora son Responsables.")
    make_responsable.short_description = "Convertir a Responsables"
    
    def remove_responsable(self, request, queryset):
        responsable_group = Group.objects.get(name='Responsable')
        cliente_group, _ = Group.objects.get_or_create(name='Cliente')
        for user in queryset:
            user.groups.add(cliente_group)
            user.groups.remove(responsable_group)
        self.message_user(request, "Los usuarios seleccionados han vuelto a ser Clientes.")
    remove_responsable.short_description = "Revertir a Clientes"

admin.site.register(Usuario, UsuarioAdmin)
