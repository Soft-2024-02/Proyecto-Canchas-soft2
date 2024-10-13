from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)

urlpatterns = [
    # Rutas relacionadas con la API REST
    path('api/', include(router.urls)),
    # Rutas generales
    path('', views.inicio, name='inicio'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    # Rutas relacionadas con el perfil del usuario
    path('perfil/<int:usuario_id>/<slug:usuario_slug>/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    path('perfil/cambiar-imagen/', views.cambiar_imagen, name='cambiar_imagen'),
    path('perfil/cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('perfil/eliminar/', views.eliminar_cuenta, name='eliminar_cuenta'),
    
]