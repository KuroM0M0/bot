from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()
YOUR_CHANNEL_ID = os.getenv("YOUR_CHANNEL_ID")

def setup(bot):
    @bot.event
    async def on_ready():
        channel = bot.get_channel(YOUR_CHANNEL_ID)
        start_webhook_server(bot, channel)
        print(f"{bot.user} ist bereit!")
