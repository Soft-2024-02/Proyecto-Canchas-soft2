from django.test import TestCase
from django.contrib.auth.models import Group
from tests.factories import UsuarioFactory, CanchaFactory


class CanchaModelTest(TestCase):
    def setUp(self):
        # Crear los grupos necesarios
        Group.objects.create(name="Cliente")
        Group.objects.create(name="Responsable")
        
        # Crear usuario y cancha
        self.usuario = UsuarioFactory()
        self.cancha = CanchaFactory(responsable=self.usuario)
    
    def test_cancha_creacion(self):
        """Verifica que una cancha se crea correctamente"""
        self.assertEqual(self.cancha.nombre, "Cancha Test")
        self.assertEqual(self.cancha.responsable, self.usuario)
        self.assertFalse(self.cancha.disponibilidad)
    
    def test_cancha_slug(self):
        """Verifica que el slug se genera correctamente"""
        self.assertEqual(self.cancha.slug, "cancha-test")
    
    def test_responsable_es_responsable(self):
        """Verifica que el responsable pertenece al grupo 'Responsable'"""
        self.assertTrue(self.usuario.groups.filter(name="Responsable").exists())