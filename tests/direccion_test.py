from django.test import TestCase
from django.contrib.auth.models import Group
from tests.factories import UsuarioFactory, CanchaFactory, DireccionFactory


class DireccionModelTest(TestCase):
    def setUp(self):
        # Crear los grupos necesarios
        Group.objects.create(name="Cliente")
        Group.objects.create(name="Responsable")
        # Crear usuario, cancha y dirección
        self.usuario = UsuarioFactory()
        self.cancha = CanchaFactory(responsable=self.usuario)
        self.direccion = DireccionFactory(cancha=self.cancha)
    
    def test_direccion_creacion(self):
        """Verifica que una dirección se crea correctamente"""
        self.assertEqual(self.direccion.tipo_calle, "Avenida")
        self.assertTrue(self.direccion.nombre_calle, "Test Address")
        self.assertEqual(self.direccion.distrito, "Miraflores")
        self.assertEqual(self.direccion.cancha, self.cancha)
    
    def test_direccion_to_string(self):
        """Verifica que el método __str__ devuelve el formato esperado"""
        expected_string = f"{self.direccion.tipo_calle} {self.direccion.nombre_calle} {self.direccion.numero_calle}, {self.direccion.distrito}"
        self.assertEqual(str(self.direccion), expected_string)
