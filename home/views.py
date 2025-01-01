from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
import logging,requests,json
from django.shortcuts import render, redirect

from .models import User

# Logger setup
logger = logging.getLogger(__name__)

# Telegram Bot Token and API URL
BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Web App URL (replace with your own frontend URL)
WEB_APP_BASE_URL = "https://telegram-jf1m.vercel.app/"

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            # Log the incoming update (for debugging)
            logger.info(f"Webhook called. Request body: {request.body}")
            
            # Parse the incoming Telegram update
            update = json.loads(request.body)
            message = update.get("message")
            
            if not message:
                return JsonResponse({"error": "No message found"}, status=400)

            chat_id = message.get("chat", {}).get("id")
            text = message.get("text")
            username = message.get("chat", {}).get("username", "User")

            if chat_id and text == "/start":
                # Generate the Web App URL with query parameters
                web_app_url = f"{WEB_APP_BASE_URL}/?chat_id={chat_id}&username={username}"

                # Create inline keyboard with the Web App button (convert it to a dictionary)
                keyboard = [
                    [InlineKeyboardButton("Start Mining 🚀", web_app=WebAppInfo(url=web_app_url))]
                ]
                
                # Convert the keyboard to dictionary format for JSON serialization
                reply_markup = {
                    "inline_keyboard": [[{
                        "text": button.text,
                        "web_app": button.web_app.to_dict() if button.web_app else None
                    } for button in row] for row in keyboard]
                }

                # Send the message with the Web App button
                send_message(chat_id, 
                             f"Hello {username}! 🎉 Click the button below to complete your signup. 🚀", 
                             reply_markup=reply_markup)
                return JsonResponse({"ok": True}, status=200)

            elif chat_id and text:
                # Echo any other text
                send_message(chat_id, f"You said: {text}")
                return JsonResponse({"ok": True}, status=200)

            return JsonResponse({"error": "Invalid payload"}, status=400)

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def send_message(chat_id, text, reply_markup=None):
    """Send a message to a Telegram chat."""
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        response = requests.post(TELEGRAM_API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message: {e}")


def signup(request):
    """Handles user signup and redirects to home.html after login/signup."""
    chat_id = request.GET.get('chat_id')
    username = request.GET.get('username')

    if not chat_id or not username:
        return JsonResponse({"error": "Chat ID and username are required"}, status=400)

   
    user, created = User.objects.get_or_create(chat_id=chat_id, defaults={'username': username})

    if created:
       
        message = f"Hello {username}! Your signup is complete. 🚀"
        user.welcome_sent = True
        user.save()
        send_message(chat_id, message)
    elif not user.welcome_sent:
       
        message = f"Welcome back, {username}! 🎉"
        user.welcome_sent = True
        user.save()
        send_message(chat_id, message)
    else:
        
        message = f"Hello {username}, you're already signed up and logged in! 🚀"
    context = {"username": username}
    return render(request, "index.html", context)



def success(request):
    """Handle successful signup."""
    return JsonResponse({"success": True, "message": "Signup complete"})
