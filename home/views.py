import json
import logging
import requests
import threading
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import User
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logger = logging.getLogger(__name__)

# Telegram Bot Token
BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Replace with your frontend web app URL
WEB_APP_BASE_URL = "https://telegram-jf1m.vercel.app/"

# Telegram bot start function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "User"

    # Generate a unique URL for the web app with query parameters
    web_app_url = f"{WEB_APP_BASE_URL}/?chat_id={chat_id}&username={username}"

    # Create a button that opens the web app
    keyboard = [
        [InlineKeyboardButton("Start Mining 🚀", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the WebApp button
    await update.message.reply_text(
        f"Hello {username}! 🎉 To complete your signup, click the button below and follow the steps in the web app. 🚀",
        reply_markup=reply_markup,
    )

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 Signup/Login successful! You are now ready to mine!")

# Run the bot in a separate thread
def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("confirm", confirm))
    application.run_polling()

# Function to start the bot in a separate thread
def start_bot_in_thread():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

# Signup View
def signup(request):
    chat_id = request.GET.get("chat_id")
    username = request.GET.get("username")

    if not chat_id or not username:
        return JsonResponse({"error": "Chat ID and username are required"}, status=400)

    # Check if the user exists or create a new one
    user, created = User.objects.get_or_create(chat_id=chat_id, defaults={"username": username})

    if not created:
        message = f"Welcome back, {username}! You are already signed up. 🎉"
    else:
        message = f"Hello {username}! Your signup is complete. 🚀"

    # Send confirmation message to Telegram
    requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": message})

    # Start the bot in a background thread
    start_bot_in_thread()

    return render(request, "index.html", {"username": username, "message": message})

# Telegram Webhook View
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
                # Respond to the user based on the message
                if text == "/start":
                    send_message(chat_id, "Welcome! How can I help you today?")
                else:
                    send_message(chat_id, f"You said: {text}")
                return JsonResponse({"ok": True})
            else:
                logger.error("Invalid Telegram payload")
                return JsonResponse({"error": "Invalid Telegram payload"}, status=400)

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# Send message to Telegram
def send_message(chat_id, text):
    """Send a message to a Telegram chat."""
    try:
        requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
