from django.shortcuts import render
from django.http import JsonResponse
from .models import User
import requests

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

    return render(request, "idex.html", {"username": username, "message": message})

def success(request):
    return JsonResponse({"success": True, "message": "Signup complete"})
