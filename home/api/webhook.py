from bot import application
from telegram import Update
import json
from django.http import JsonResponse

async def handler(request):
    if request.method == "POST":
        # Parse the incoming webhook data from Telegram
        data = json.loads(request.body.decode("utf-8"))
        update = Update.de_json(data, application.bot)
        
        # Process the update with the bot application
        await application.process_update(update)
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
