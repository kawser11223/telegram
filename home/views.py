from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import requests
import logging
import json

# Setup logger
logger = logging.getLogger(__name__)

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
    send_message(chat_id, message)

    return render(request, "index.html", {"username": username, "message": message})


def success(request):
    return JsonResponse({"success": True, "message": "Signup complete"})


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            # Log the request body
            logger.info("Webhook called")
            logger.info(f"Request body: {request.body}")

            # Parse the incoming Telegram update
            update = json.loads(request.body)

            chat_id = update.get("message", {}).get("chat", {}).get("id")
            text = update.get("message", {}).get("text")

            if chat_id and text:
                send_message(chat_id, f"You said: {text}")
                return JsonResponse({"ok": True}, status=200)
            else:
                logger.error("Invalid Telegram payload")
                return JsonResponse({"error": "Invalid Telegram payload"}, status=400)

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def send_message(chat_id, text):
    """Send a message to a Telegram chat."""
    try:
        response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message: {e}")
