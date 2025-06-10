from discord.ext import commands
from discord import app_commands
import discord

class AdoptView(discord.ui.View):
    def __init__(self, author, target):
        super().__init__(timeout=60)  # optional: timeout in Sekunden
        self.author = author
        self.target = target

    @discord.ui.button(label="Accept 📝", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.target:
            await interaction.response.send_message("You're not the one being adopted!", ephemeral=True)
            return
        self.result = True
        await interaction.response.edit_message(content=f"{self.author.mention} is now adopted by {self.target.mention}", view=None) # erweiterung durch partner
        self.stop()

    @discord.ui.button(label="Decline ❌", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.target:
            await interaction.response.send_message("You're not the one being adopted!", ephemeral=True)
            return
        self.result = False
        await interaction.response.edit_message(content=f"{self.target.mention} declined {self.author.mention}'s adoption.", view=None)
        self.stop()

class Adopt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="adopt", description="ask for adoption")
    @app_commands.describe(member="The user you want to adopt")
    async def adopt(self, interaction: discord.Interaction, member: discord.Member):
        if member == interaction.author:
            await interaction.send("You can't adopt yourself!")
            return
        view = AdoptView(interaction.author, member)
        await interaction.send(f"{interaction.user.mention} wants to adopt {member.mention}!", view=view) # erweiterung durch partner
        
    @app_commands.command(name="disown", description="disown your children")
    @app_commands.describe(member="The user you want to disown")
    async def disown(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.send(f"You have disowned: {interaction.user.mention}")
    
    @app_commands.command(name="leavefamily", description="leave your family")
    async def leavefamily(self, interaction: discord.Interaction):
        await interaction.send(f"You have left your family: {interaction.user.mention}")
    
async def setup(bot):
    cog = Adopt(bot)
    await bot.add_cog(cog)