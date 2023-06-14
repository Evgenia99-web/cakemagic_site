from django.apps import AppConfig


class SiteCakeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'site_cake'

    def ready(self):
        import site_cake.signals
