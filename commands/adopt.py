from discord.ext import commands
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

    @commands.command(name="adopt", help="ask for adoption")
    async def adopt(self, ctx, user: discord.User):
        if user == ctx.author:
            await ctx.send("You can't adopt yourself!")
            return
        view = AdoptView(ctx.author, user)
        await ctx.send(f"{ctx.author.mention} wants to adopt {user.mention}!", view=view) # erweiterung durch partner
        
    @commands.command(name="disown", help="disown your children")
    async def disown(self, ctx):
        await ctx.send(f"You have disowned: {ctx.author.mention}")
    
    @commands.command(name="leavefamily", help="leave your family")
    async def leavefamily(self, ctx):
        await ctx.send(f"You have left your family: {ctx.author.mention}")
    
async def setup(bot):
    cog = Adopt(bot)
    await bot.add_cog(cog)