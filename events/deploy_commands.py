import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")

# Setup-Funktion für den Event-Handler
def setup(bot: commands.Bot):
    @bot.event
    async def on_ready():
        # Wird ausgeführt, wenn der Bot bereit ist
        print("🔄 Slash-Command-Deployment startet ...")

        commands_dir = os.path.join(os.path.dirname(__file__), "../commands")
        command_files = [f for f in os.listdir(commands_dir) if f.endswith(".py")]

        loaded = 0  # Zähler für geladene Befehle

        for filename in command_files:
            try:
                # Importiere das Modul commands/ping.py usw.
                module = __import__(f"commands.{filename[:-3]}", fromlist=["setup"])
                if hasattr(module, "setup"):
                    # Führe setup(bot) aus, um den Command zu registrieren
                    await module.setup(bot)
                    loaded += 1
            except Exception as e:
                print(f"❌ Fehler beim Laden von {filename}: {e}")

        try:
            # Registriere alle Slash-Commands global bei Discord
            synced = await bot.tree.sync()
            print(f"✅ {loaded} Slash-Commands erfolgreich registriert ({len(synced)} synchronisiert).")
        except Exception as e:
            print(f"❌ Fehler beim Registrieren der Slash-Commands: {e}")
