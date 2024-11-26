from django.test import TestCase
from tests.factories import UsuarioFactory


class UsuarioModelTest(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory()
    
    def test_usuario_creacion(self):
        """Verifica que un usuario se crea correctamente"""
        self.assertEqual(self.usuario.email, "user@test.com")
        self.assertTrue(self.usuario.check_password("TestPassword123"))
    
    def test_usuario_slug(self):
        """Verifica que el slug se genera correctamente"""
        self.assertEqual(self.usuario.slug, "test-user")
    
    def test_usuario_grupo_cliente(self):
        """Verifica que el usuario pertenece al grupo 'Cliente' por defecto"""
        self.assertTrue(self.usuario.groups.filter(name="Cliente").exists())
    
    def test_usuario_grupo_administrador(self):
        """Verifica que el usuario pertenece al grupo 'Administrador' por defecto"""
        self.assertFalse(self.usuario.groups.filter(name="Administrador").exists())