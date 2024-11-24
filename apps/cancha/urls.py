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
    path('agregar-horario/<int:cancha_id>/<slug:cancha_slug>/', views.agregar_horario, name='agregar_horario'),
    path('editar-horarios_dia/<int:cancha_id>/<slug:cancha_slug>/', views.editar_horarios_dia, name='editar_horarios_dia'),
    path('eliminar-horarios/<int:cancha_id>/<slug:cancha_slug>/', views.eliminar_horarios_dia, name='eliminar_horarios_dia'),
    path('<int:cancha_id>/<slug:cancha_slug>/horario/<int:horario_id>/<str:hora_inicio>/<str:hora_fin>/', views.detalle_horario, name='detalle_horario'),
    path('<int:cancha_id>/<slug:cancha_slug>/horario/<int:horario_id>/<str:hora_inicio>/<str:hora_fin>/reservar/', views.reservar_horario, name='reservar_horario'),
]