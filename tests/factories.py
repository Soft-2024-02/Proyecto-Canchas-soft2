import factory
from django.contrib.auth.models import Group
from apps.usuario.models import Usuario
from apps.cancha.models import Cancha
from apps.direccion.models import Direccion


# Usuario Factory
class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
        skip_postgeneration_save = True
    
    email = "user@test.com"
    dni = factory.Faker("random_number", digits=8, fix_len=True)
    nombre = "test"
    apellidos = "user"
    celular = factory.Faker("random_number", digits=9, fix_len=True) 
    password = factory.PostGenerationMethodCall("set_password", "TestPassword123")
    
    @factory.post_generation
    def add_group(self, create, extracted, **kwargs):
        if not create:
            return
        cliente_group, _ = Group.objects.get_or_create(name="Cliente")
        self.groups.add(cliente_group)


# Cancha Factory
class CanchaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cancha
        skip_postgeneration_save = True
    
    responsable = factory.SubFactory(UsuarioFactory)
    nombre = "Cancha Test"
    disponibilidad = False
    imagen = "canchas/default-cancha.jpg"


# Dirección Factory
class DireccionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Direccion
    
    cancha = factory.SubFactory(CanchaFactory)
    tipo_calle = "Avenida"
    nombre_calle = "Test Address"
    numero_calle = factory.Faker("random_number", digits=3, fix_len=True)
    distrito = "Miraflores"
    referencia = factory.Faker("sentence", nb_words=5)
