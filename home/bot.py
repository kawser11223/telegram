from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token
TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"

# Replace with your frontend web app URL
WEB_APP_BASE_URL = "https://telegram-jf1m.vercel.app"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_chat.username or "User"

    # Generate a unique URL for the web app with query parameters
    web_app_url = f"{WEB_APP_BASE_URL}/?chat_id={chat_id}&username={username}"

    # Create a button that opens the web app
    keyboard = [[InlineKeyboardButton("Start Mining 🚀", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the WebApp button
    await update.message.reply_text(
        f"Hello {username}! 🎉 To complete your signup, click the button below and follow the steps in the web app. 🚀",
        reply_markup=reply_markup,
    )

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎉 Signup/Login successful! You are now ready to mine!")

# Create the application instance
application = Application.builder().token(TOKEN).build()

# Add handlers to the application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("confirm", confirm))

# Run the bot
if __name__ == "__main__":
    application.run_polling()
