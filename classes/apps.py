from django.apps import AppConfig
from  django.db.models.signals import post_save


class ClassesConfig(AppConfig):
    name = 'classes'
    verbose_name = 'iCraft Classes'

    def ready(self):
        from . import signals
