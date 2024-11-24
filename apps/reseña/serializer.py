from rest_framework import serializers
from .models import Reseña

class ReseñaSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    cancha = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Reseña
        fields = ['id', 'usuario', 'cancha', 'calificacion', 'comentario', 'fecha_creacion']
        read_only_fields = ['id', 'usuario', 'cancha', 'fecha_creacion']
    
    def validate_reseña(self, value):
        """Validar que la calificacion esté entre 1 y 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("La calificacion debe estar entre 1 y 5.")
        return value