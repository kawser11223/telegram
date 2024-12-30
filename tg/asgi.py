"""
ASGI config for tg project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg.settings')

application = get_asgi_application()
# from telegram import Update
# from telegram.ext import Application

# BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
# application = Application.builder().token(BOT_TOKEN).build()

# async def webhook_handler(request):
#     update = Update.de_json(await request.json(), application.bot)
#     await application.process_update(update)
#     return {"statusCode": 200, "body": "Webhook processed"}

# def handler(request):
#     return webhook_handler(request)