from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reseñas', views.ReseñaViewSet)

urlpatterns = [
    # Rutas de la API REST
    path('api/', include(router.urls)),
    path('calificar-cancha/<int:cancha_id>/', views.calificar_cancha, name='calificar_cancha'),
    path('editar-reseña/<int:cancha_id>/', views.editar_reseña, name='editar_reseña'),
    path('eliminar-reseña/<int:reseña_id>/', views.eliminar_reseña, name='eliminar_reseña'),
]
