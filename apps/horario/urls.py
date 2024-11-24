from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'horarios', views.HorarioViewSet)

urlpatterns = [
    # Rutas relacionadas con la API REST
    path('api/', include(router.urls)),
    
]