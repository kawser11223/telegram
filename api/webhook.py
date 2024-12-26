import requests

BOT_TOKEN = "7947742121:AAEyNzPDyfS-TE9Uq1lesFScsC-nahaKIZI"
WEBHOOK_URL = "https://telegram-jf1m.vercel.app/api/webhook"

response = requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    json={"url": WEBHOOK_URL},
)
print(response.json())
