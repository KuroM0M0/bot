from discord import Interaction
from discord.ext import commands

def setup(bot: commands.Bot):
    @bot.event
    async def on_interaction(interaction: Interaction):
        if interaction.type.name == "application_command":
            command = bot.tree.get_command(interaction.command.name)
            if command is None:
                return

            try:
                await bot.process_application_commands(interaction)
            except Exception as e:
                print(e)
                await interaction.response.send_message(
                    "Es gab einen Fehler beim Ausführen dieses Befehls.",
                    ephemeral=True
                )

        elif interaction.type.name == "component":
            custom_id = interaction.data.get("custom_id")
            if custom_id in bot.buttons:
                await bot.buttons[custom_id].execute(interaction)
            elif custom_id in bot.selects:
                await bot.selects[custom_id].execute(interaction)

        elif interaction.type.name == "modal_submit":
            custom_id = interaction.data.get("custom_id")
            if custom_id in bot.modals:
                await bot.modals[custom_id].execute(interaction)
