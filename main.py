import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import sys
import asyncio

# Aktuellen Ordner dem Pfad hinzufügen
sys.path.append(os.path.dirname(__file__))
current_dir = os.path.dirname(__file__)
print("Current dir:", current_dir)
print("sys.path:", sys.path)

# .env laden und Token holen
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents setzen (für Member, Nachrichten etc.)
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True
intents.reactions = True

# 🧠 Bot-Klasse mit Slash-Command-Unterstützung UND Cog-Management
class MyBot(commands.Bot):
    def __init__(self, *, intents):
        super().__init__(command_prefix="!", intents=intents)

# Bot-Instanz erstellen
bot = MyBot(intents=intents)

# Events auslagern (z. B. on_ready)
from events import ready
ready.setup(bot)

# Hauptfunktion zum Laden aller Cogs und Starten des Bots
async def main():
    # Cogs aus dem Unterordner "commands/" laden
    commands_dir = os.path.join(current_dir, "commands")
    if os.path.exists(commands_dir):
        for file in os.listdir(commands_dir):
            if file.endswith(".py") and not file.startswith("_"):
                try:
                    await bot.load_extension(f"commands.{file[:-3]}")
                    print(f"✔️ Geladen: commands/{file}")
                except Exception as e:
                    print(f"❌ Fehler beim Laden von commands/{file}: {e}")

    # Cogs aus dem Hauptverzeichnis laden (außer main/events)
    exclude = {"main.py", "events.py", "__init__.py"}
    for file in os.listdir(current_dir):
        if file.endswith(".py") and file not in exclude:
            try:
                await bot.load_extension(file[:-3])
                print(f"✔️ Geladen: {file}")
            except Exception as e:
                print(f"❌ Fehler beim Laden von {file}: {e}")

    # Bot starten
    await bot.start(TOKEN)

# asyncio-Start
asyncio.run(main())
