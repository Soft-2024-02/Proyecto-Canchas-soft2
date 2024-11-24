from rest_framework import serializers
from .models import Reserva
from django.core.exceptions import ValidationError

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'horario', 'hora_reserva_inicio', 'hora_reserva_fin', 'fecha_reserva']
        read_only_fields = ['fecha_reserva']
    
    def validate(self, data):
        reserva = Reserva(**data)
        try:
            reserva.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
        return data