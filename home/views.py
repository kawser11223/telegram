from django.shortcuts import render
from django.http import JsonResponse
from .models import User
import requests
from django.http import JsonResponse
import json
import logging


BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def signup(request):
    chat_id = request.GET.get('chat_id')
    username = request.GET.get('username')

    if not chat_id or not username:
        return JsonResponse({"error": "Chat ID and username are required"}, status=400)

    # Check if the user exists
    user, created = User.objects.get_or_create(chat_id=chat_id, defaults={'username': username})

    if not created:
        message = f"Welcome back, {username}! You are already signed up. 🎉"
    else:
        message = f"Hello {username}! Your signup is complete. 🚀"

    # Send confirmation message to Telegram
    requests.post(
        TELEGRAM_API_URL,
        json={"chat_id": chat_id, "text": message}
    )

    return render(request, "index.html", {"username": username, "message": message})

def success(request):
    return JsonResponse({"success": True, "message": "Signup complete"})




def telegram_webhook(request):
    if request.method == "POST":
        try:
            # Parse the incoming Telegram update
            update = json.loads(request.body)
            logger.info(f"Received update: {update}")

            # Extract chat ID and text from the message
            chat_id = update.get("message", {}).get("chat", {}).get("id")
            text = update.get("message", {}).get("text")

            if chat_id and text:
                send_message(chat_id, f"You said: {text}")

            return JsonResponse({"ok": True})
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": "Failed to process webhook"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def send_message(chat_id, text):
    import requests
    BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})





def telegram_webhook(request):
    logger.info("Webhook accessed")
    logger.info(request.body)
    ...
