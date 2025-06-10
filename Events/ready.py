def setup(bot):
    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f"{bot.user} ist bereit!")
