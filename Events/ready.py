def setup(bot):
    @bot.event
    async def on_ready():
        print(f"{bot.user} ist bereit!")
