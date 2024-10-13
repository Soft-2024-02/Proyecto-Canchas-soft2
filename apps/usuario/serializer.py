from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'dni', 'nombre', 'apellidos', 'celular', 'imagen', 'is_active', 'slug']
        read_only_fields = ['is_active', 'slug']