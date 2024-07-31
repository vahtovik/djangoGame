from django.apps import AppConfig


class FirstAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'first_app'

    def ready(self):
        import first_app.signals
