from discord.ext import commands
from discord import app_commands, Interaction

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Klassischer Text-Command: !ping
    @commands.command(name="ping", help="Antwortet mit Pong (klassisch)!")
    async def ping_text(self, ctx):
        await ctx.send("🏓 Pong (klassisch)!")

    # Slash-Command: /ping_slash (wird automatisch registriert)
    @app_commands.command(name="ping_slash", description="Antwortet mit Pong (slash)!")
    async def ping_slash(self, interaction: Interaction):
        await interaction.response.send_message("🏓 Pong (slash)!")

    # ⚠️ KEIN cog_load() mehr nötig – discord.py kümmert sich drum

async def setup(bot):
    cog = Ping(bot)
    await bot.add_cog(cog)