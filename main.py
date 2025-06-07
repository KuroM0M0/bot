import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sys
import asyncio

sys.path.append(os.path.dirname(__file__))

current_dir = os.path.dirname(__file__)
print("Current dir:", current_dir)

# Aktuelles Verzeichnis zu sys.path hinzufügen
sys.path.append(current_dir)

# Debug: Zeige alle bekannten Importpfade
print("sys.path:", sys.path)

# Token laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents festlegen
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True
intents.reactions = True

# Bot initialisieren
bot = commands.Bot(command_prefix="!", intents=intents)

# Collections für Buttons, Selects, Modals vorbereiten (optional)
bot.buttons = {}
bot.selects = {}
bot.modals = {}

# Events
from events import ready
ready.setup(bot)

async def main():
    # Alle Commands laden
    commands_dir = os.path.join(current_dir, "commands")
    for file in os.listdir(commands_dir):
        if file.endswith(".py"):
            await bot.load_extension(f"commands.{file[:-3]}")

    # Bot starten
    await bot.start(TOKEN)

# asyncio-Einstiegspunkt
asyncio.run(main())