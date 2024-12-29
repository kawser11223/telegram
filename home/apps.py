
from django.apps import AppConfig
from .views import start_bot_in_thread

class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"

    def ready(self):
        start_bot_in_thread()
