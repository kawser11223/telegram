from django.urls import path
from .views import signup, telegram_webhook

urlpatterns = [
    path("", signup, name="signup"),
    path("api/webhook", telegram_webhook, name="telegram_webhook"),
]
