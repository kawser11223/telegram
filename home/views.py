from django.http import JsonResponse
from django.shortcuts import render
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import json
import logging
import requests

logger = logging.getLogger(__name__)

BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def signup(request):
    chat_id = request.GET.get("chat_id")
    username = request.GET.get("username")

    if not chat_id or not username:
        return JsonResponse({"error": "Chat ID and username are required"}, status=400)

    message = f"Hello {username}! Your signup is complete. 🚀"
    send_message(chat_id, message)
    return render(request, "index.html", {"username": username, "message": message})

def telegram_webhook(request):
    if request.method == "POST":
        try:
            update = json.loads(request.body)
            chat_id = update.get("message", {}).get("chat", {}).get("id")
            text = update.get("message", {}).get("text")

            if chat_id and text:
                send_message(chat_id, f"You said: {text}")

            return JsonResponse({"ok": True})
        except Exception as e:
            logger.error(f"Error: {e}")
            return JsonResponse({"error": "Failed to process update"}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})
