import json
import logging
import requests
import threading
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
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

    # Web App URL with query parameters
    web_app_url = f"{WEB_APP_BASE_URL}/?chat_id={chat_id}&username={username}"

    # Inline button with WebApp URL
    keyboard = [
        [InlineKeyboardButton("Start Mining 🚀", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send message with WebApp button
    await update.message.reply_text(
        f"Hello {username}! Click the button below to start mining in the web app 🚀",
        reply_markup=reply_markup,
    )


def signup(request):
    """Signup page that processes user data."""
    chat_id = request.GET.get("chat_id")
    username = request.GET.get("username")

    if not chat_id or not username:
        return JsonResponse({"error": "Chat ID and username are required"}, status=400)

    # Simulate user signup
    message = f"Hello {username}! Your signup is complete. 🚀"

    # Send a message back to Telegram
    send_message(chat_id, message)

    # Render an HTML page (no JavaScript required)
    return render(request, "index.html", {"username": username, "message": message})


@csrf_exempt
def telegram_webhook(request):
    """Handle Telegram webhook."""
    if request.method == "POST":
        try:
            logger.info("Webhook called")
            logger.info(f"Request body: {request.body}")

            update = json.loads(request.body)

            chat_id = update.get("message", {}).get("chat", {}).get("id")
            text = update.get("message", {}).get("text")

            if chat_id and text:
                if text == "/start":
                    send_message(chat_id, "Welcome! Click the button to start mining.")
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


def send_message(chat_id, text):
    """Send a message to a Telegram chat."""
    try:
        requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})
    except Exception as e:
        logger.error(f"Failed to send message: {e}")


# Run the bot in a separate thread
def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


def start_bot_in_thread():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
