from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# Replace with your Telegram Bot Token
TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "User"

    # Generate a unique URL for the web app with query parameters
    web_app_url = f"http://127.0.0.1:8000/signup/?chat_id={chat_id}&username={username}"

    # Create a button that opens the web app
    keyboard = [
        [InlineKeyboardButton("Start Mining 🚀", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the WebApp button
    await update.message.reply_text(
        f"Hello {username}! 🎉 To complete your signup, click the button below and follow the steps in the web app. 🚀",
        reply_markup=reply_markup
    )

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("🎉 Signup/Login successful! You are now ready to mine!")

def run_bot():
    application = ApplicationBuilder().token(TOKEN).build()

    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Add an optional /confirm command handler
    application.add_handler(CommandHandler("confirm", confirm))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    run_bot()
