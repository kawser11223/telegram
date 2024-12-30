import json
import logging
import requests
import threading
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Configuration
BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"  # Replace with your bot token
WEB_APP_BASE_URL = "https://telegram-jf1m.vercel.app/"  # Replace with your actual web app URL

# Telegram bot /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "User"

    # Inline button pointing to the web app
    web_app_url = f"{WEB_APP_BASE_URL}/?chat_id={chat_id}&username={username}"
    keyboard = [[InlineKeyboardButton("Start Mining 🚀", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Log the web app URL for debugging
    logger.info(f"Web App URL for {username}: {web_app_url}")

    # Send message with WebApp button
    await update.message.reply_text(
        f"Hello {username}! Click the button below to start mining 🚀",
        reply_markup=reply_markup,
    )

# Django signup view
def signup(request):
    chat_id = request.GET.get("chat_id")
    username = request.GET.get("username")

    if not chat_id or not username:
        return JsonResponse({"error": "Chat ID and username are required"}, status=400)

    # Simulate signup
    message = f"Hello {username}! Your signup is complete. 🚀"
    send_message(chat_id, message)

    # Render the HTML page
    return render(request, "index.html", {"username": username, "message": message})


def telegram_webhook(request):
    if request.method == "POST":
        try:
            update = json.loads(request.body)
            logger.info(f"Received update: {update}")
            
            # Extract data from the update
            chat_id = update.get("message", {}).get("chat", {}).get("id")
            text = update.get("message", {}).get("text")

            if chat_id and text:
                send_message(chat_id, f"You said: {text}")

            return JsonResponse({"ok": True})
        except Exception as e:
            logger.error(f"Error processing update: {str(e)}")
            return JsonResponse({"error": "Failed to process update"}, status=500)
    return JsonResponse({"error": "Invalid method"}, status=405)

def send_message(chat_id, text):
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})

