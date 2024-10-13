from django.core.management.base import BaseCommand
from django.utils.text import slugify
from apps.usuario.models import Usuario

class Command(BaseCommand):
    help = 'Genera slugs para usuarios existentes'
    
    def handle(self, *args, **kwargs):
        usuarios = Usuario.objects.all()
        for usuario in usuarios:
            if not usuario.slug:
                usuario.slug = slugify(f'{usuario.nombre} {usuario.apellidos}')
                usuario.save()
        self.stdout.write(self.style.SUCCESS('Slugs generados para usuarios.'))