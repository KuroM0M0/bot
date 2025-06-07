from aiohttp import web
import discord
import json

routes = web.RouteTableDef()

discord_channel = None  # Wird beim Start gesetzt

@routes.post("/github.com/KuroM0M0/bot")
async def github_webhook(request):
    event = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    if event == "pull_request":
        action = payload["action"]
        pr = payload["pull_request"]
        user = pr["user"]["login"]
        url = pr["html_url"]
        title = pr["title"]

        embed = discord.Embed(
            title=f"📦 Pull Request {action}",
            description=f"[{title}]({url}) von `{user}`",
            color=discord.Color.blue()
        )
        await discord_channel.send(embed=embed)

    return web.Response(text="OK")

def start_webhook_server(bot, channel):
    global discord_channel
    discord_channel = channel

    app = web.Application()
    app.add_routes(routes)

    runner = web.AppRunner(app)

    async def run():
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 5000)  # Port 5000
        await site.start()
        print("Webhook-Server läuft auf Port 5000")

    bot.loop.create_task(run())
