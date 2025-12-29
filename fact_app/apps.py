from django.apps import AppConfig


class FactAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fact_app'
    verbose_name = 'Invoice Management'
    
    def ready(self):
        """
        Import signals when the app is ready
        """
        import fact_app.signals  # noqa
