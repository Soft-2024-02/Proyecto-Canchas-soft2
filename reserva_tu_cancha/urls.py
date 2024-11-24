from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.usuario.views import error_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuario.urls')),
    path('usuario/', include('apps.usuario.urls')),
    path('cancha/', include('apps.cancha.urls')),
    path('direccion/', include('apps.direccion.urls')),
    path('horario/', include('apps.horario.urls')),
    path('reserva/', include('apps.reserva.urls')),
    path('reseña/', include('apps.reseña.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuración para errores 404
handler404 = error_404_view