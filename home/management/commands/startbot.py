from django.core.management.base import BaseCommand
from home.bot import run_bot

class Command(BaseCommand):
    help = "Start the Telegram bot"

    def handle(self, *args, **kwargs):
        run_bot()
