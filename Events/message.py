import discord
from discord.ext import commands
from DataBase.dataBase import *

class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        #Ignoriere andere Bots
        if message.author.bot:
            return

        await self.addXp(message.author.id, 1) #nur als Test

        print(f'Nachricht von {message.author}: {message.content}')

    async def addXp(self, userID, xp):
        userExists = checkUserExists(userID)
        if userExists == True:
            SQLUpdate("users", "xp = xp + ?", userID)
        print(f'Added {xp} XP to user {userID}')

def setup(bot):
    bot.add_cog(MessageEvents(bot))
    print("MessageEvents geladen")