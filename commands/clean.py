from discord.ext import commands
import discord

class Clean(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clean", help="clean the channel")
    async def clean(self, ctx):
        await ctx.channel.purge(limit=100)
        await ctx.send("Channel cleaned!")
        await ctx.message.delete(delay=5)
    
async def setup(bot):
    cog = Clean(bot)
    await bot.add_cog(cog)