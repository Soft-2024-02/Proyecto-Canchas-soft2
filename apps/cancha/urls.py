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
    path('detalle/<int:cancha_id>/<slug:cancha_slug>/', views.detalle_cancha, name='detalle_cancha'),
    path('editar/<int:cancha_id>/<slug:cancha_slug>/', views.editar_cancha, name='editar_cancha'),
    path('eliminar/<int:cancha_id>/<slug:cancha_slug>/', views.eliminar_cancha, name='eliminar_cancha'),
]