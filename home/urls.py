from django.urls import path
from .views import *

urlpatterns = [
    path("", signup, name="signup"),
    path("api/webhook", telegram_webhook, name="telegram_webhook"),
    path('success/', success, name='success'),
]
