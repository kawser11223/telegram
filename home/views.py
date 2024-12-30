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
BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
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

# Telegram webhook handler
@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            # Pass the incoming request to the Telegram bot application
            update_data = json.loads(request.body)
            asyncio.run(application.process_update(Update.de_json(update_data, application.bot)))
            return JsonResponse({"ok": True})
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

# Utility function to send Telegram messages
def send_message(chat_id, text):
    try:
        TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

# Run bot in a separate thread
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

def run_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())  # Create and set event loop for this thread
    application.run_polling()

def start_bot_in_thread():
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

# Main function to start the bot and server
if __name__ == "__main__":
    # Start the bot in a background thread
    start_bot_in_thread()

    # Django app setup (you'd integrate this with your Django project)
    logger.info("Bot is running in the background")
