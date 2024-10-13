from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'direcciones', views.DireccionViewSet)

urlpatterns = [
    # Rutas relacionadas con la API REST
    path('api/', include(router.urls)),
    # Rutas generales
    
]
