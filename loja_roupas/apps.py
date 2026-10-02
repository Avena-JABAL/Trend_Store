from django.apps import AppConfig


class LojaRoupasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loja_roupas'

    def ready(self):
        from . import signals
