from django.apps import AppConfig


class RaadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'raad'

    def ready(self):
        import raad.signals
