from time import sleep

from django.apps import AppConfig


class EmailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emailing'

    verbose_name = 'рассылка'

    def ready(self):
        from emailing.services import start
        sleep(2)
        start()
