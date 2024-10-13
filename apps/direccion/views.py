from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import DireccionSerializer
from .models import Direccion

class DireccionViewSet(viewsets.ModelViewSet):
    serializer_class = DireccionSerializer
    queryset = Direccion.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        cancha_id = request.data.get('cancha')
        if Direccion.objects.filter(cancha_id=cancha_id).exists():
            return Response(
                {"detail": "Esta cancha ya tiene una dirección asignada."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super(DireccionViewSet, self).create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super(DireccionViewSet, self).destroy(request, *args, **kwargs)
