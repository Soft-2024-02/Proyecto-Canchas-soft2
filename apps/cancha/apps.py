from django.apps import AppConfig


class CanchaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cancha'
    
    def ready(self):
        import apps.cancha.signals