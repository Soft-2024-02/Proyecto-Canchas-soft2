from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Cancha

@receiver(post_delete, sender=Cancha)
def cambiar_a_cliente(sender, instance, **kwargs):
    # Verificar si el usuario responsable ya no tiene canchas
    if instance.responsable.canchas.count() == 0:
        responsable_group = Group.objects.get(name='Responsable')
        cliente_group = Group.objects.get(name='Cliente')
        
        # Cambiar al grupo Cliente si ya no tiene canchas
        if responsable_group in instance.responsable.groups.all():
            instance.responsable.groups.remove(responsable_group)
            instance.responsable.groups.add(cliente_group)