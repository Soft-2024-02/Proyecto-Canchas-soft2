import logging
from abc import ABC, abstractmethod
from apps.usuario.models import Usuario
from apps.cancha.models import Cancha
from apps.direccion.models import Direccion
from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)

class CanchaFactory(ABC):
    @abstractmethod
    def create_cancha(self, nombre, usuario):
        pass
    
    @abstractmethod
    def create_direccion(self, tipo_calle, nombre_calle, numero_calle, distrito, referencia, cancha):
        pass

class CanchaConcreteFactory(CanchaFactory):
    def create_cancha(self, nombre, usuario):
        try:
            cancha = Cancha.objects.create(nombre=nombre, responsable=usuario)
            self._asignar_grupo_responsable(usuario)
            return cancha
        except Exception as e:
            logger.error(f"Error al crear la cancha: {str(e)}")
            return None
    
    # Separar la lógica de asignación de grupos en un método privado (princio SOLID: Single Responsibility)
    def _asignar_grupo_responsable(self, usuario: Usuario):
        cliente_group = Group.objects.get(name='Cliente')
        responsable_group, _ = Group.objects.get_or_create(name='Responsable')
        
        if cliente_group in usuario.groups.all():
            usuario.groups.remove(cliente_group)
            usuario.groups.add(responsable_group)
    
    def create_direccion(self, cancha, tipo_calle, nombre_calle, numero_calle, distrito, referencia):
        try:
            direccion = Direccion.objects.create(
                cancha=cancha,
                tipo_calle=tipo_calle,
                nombre_calle=nombre_calle,
                numero_calle=numero_calle,
                distrito=distrito,
                referencia=referencia,
            )
            return direccion
        except Exception as e:
            logger.error(f"Error al crear la dirección: {str(e)}")
            return None