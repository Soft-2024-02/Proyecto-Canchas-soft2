from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'canchas', views.CanchaViewSet)

urlpatterns = [
    # Rutas relacionadas con la API REST
    path('api/', include(router.urls)),
    # Rutas generales
    path('registro-cancha/', views.registro_cancha, name='registro_cancha'),
    
]