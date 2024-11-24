from rest_framework import serializers
from .models import Direccion

class DireccionSerializer(serializers.ModelSerializer):
    distrito_display = serializers.CharField(source='get_distrito_display', read_only=True)
    
    class Meta:
        model = Direccion
        fields = ['id', 'tipo_calle', 'nombre_calle', 'numero_calle', 'distrito', 'distrito_display', 'referencia', 'cancha']