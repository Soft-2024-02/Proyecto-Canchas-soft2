from rest_framework import serializers
from .models import Horario
from django.core.exceptions import ValidationError

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['id', 'cancha', 'dia', 'hora_inicio', 'hora_fin']
    
    def validate(self, data):
        horario = Horario(**data)
        try:
            horario.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        return data