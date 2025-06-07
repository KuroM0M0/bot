from discord.ext import commands
import discord

class MarriageView(discord.ui.View):
    def __init__(self, author, target):
        super().__init__(timeout=60)  # optional: timeout in Sekunden
        self.author = author
        self.target = target
        self.result = None

    @discord.ui.button(label="Accept 💍", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.target:
            await interaction.response.send_message("You're not the one being proposed to!", ephemeral=True)
            return
        self.result = True
        await interaction.response.edit_message(content=f"{self.author.mention} and {self.target.mention} are now married! 💖", view=None)
        self.stop()

    @discord.ui.button(label="Decline ❌", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.target:
            await interaction.response.send_message("You're not the one being proposed to!", ephemeral=True)
            return
        self.result = False
        await interaction.response.edit_message(content=f"{self.target.mention} declined {self.author.mention}'s proposal. 💔", view=None)
        self.stop()

class MarriageInfo(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

def build_family_embed(data, bot, title):
        embed = discord.Embed(
            title=title,
            color=discord.Color.gold()
        )

        # User anzeigen
        user = bot.get_user(int(data["user_id"]))
        if user:
            embed.add_field(name="👤 Benutzer", value=f"{user.mention}", inline=False)
        else:
            embed.add_field(name="👤 Benutzer", value=f"<@{data['user_id']}>", inline=False)

        # Ehepartner
        if data.get("married_to"):
            partner = bot.get_user(int(data["married_to"]))
            if partner:
                embed.add_field(name="💍 Verheiratet mit", value=f"{partner.mention} ", inline=False)
            else:
                embed.add_field(name="💍 Verheiratet mit", value=f"<@{data['married_to']}>", inline=False)

        # Kinder
        if data.get("children"):
            children_mentions = [f"<@{cid}>" for cid in data["children"]]
            embed.add_field(name="🧒 Kinder", value=", ".join(children_mentions), inline=False)

        # Eltern (falls vorhanden)
        if data.get("parents"):
            parent_mentions = [f"<@{pid}>" for pid in data["parents"]]
            embed.add_field(name="👨‍👩‍👧 Eltern", value=", ".join(parent_mentions), inline=False)
        
        # Past Marriages
        if data.get("past_marriages"):
            past_marriages = [f"<@{mid}>" for mid in data["past_marriages"]]
            embed.add_field(name="👪 Vergangene Ehepartner", value=", ".join(past_marriages), inline=False)     

        # Adoption ausstehend
        if "adoption_pending" in data:
            ap = data["adoption_pending"]
            try:
                ts = int(datetime.fromisoformat(ap["timestamp"]).timestamp())
                timestamp_str = f"<t:{ts}:F>"
            except:
                timestamp_str = ap["timestamp"]
            embed.add_field(
                name="⏳ Adoption ausstehend",
                value=f"Angefragt von <@{ap['requested_by']}> → Ziel: <@{ap['target']}>\n📅 Zeitpunkt: {timestamp_str}",
                inline=False
            )

        embed.set_footer(text="Familienstatus-System")
        return embed


class Marriage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="marry", help="send a proposal to <user>")
    async def marry(self, ctx, user: discord.User):
        if user == ctx.author:
            await ctx.send("You can't marry yourself!")
            return
        view = MarriageView(ctx.author, user)
        await ctx.send(f"{ctx.author.mention} wants to marry {user.mention}! 💍", view=view)
    
    @commands.command(name="partner", help="get information about your partner")
    async def partner(self, ctx):
        sample_data = {
            "user_id": str(ctx.author.id),
            "married_to": "789",
            "past_marriages": ["1011", "1213"]
        }
        embed = build_family_embed(sample_data, self.bot, "💍 Ehepartner")
        view = MarriageInfo()
        await ctx.send(embed=embed, view=view)

    @commands.command(name="divorce", help="divorce your partner")
    async def divorce(self, ctx):
        await ctx.send(f"You have divorced: {ctx.author.mention}")

    @commands.command(name="sendlove", help="send love to <user> with message")
    async def sendlove(self, ctx, user: discord.User, *, message):
        await ctx.send(f"{ctx.author.mention} sends love to {user.mention}: {message}")        
    
    @commands.command(name="children", help="get information about your children")
    async def children(self, ctx):
        sample_data = {
            "user_id": str(ctx.author.id),
            "children": ["789", "1011"]
        }
        embed = build_family_embed(sample_data, self.bot, "🧒 Kinder")
        view = MarriageInfo()
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name="family", help="get information about your family")
    async def family(self, ctx):
        sample_data = {
            "user_id": str(ctx.author.id),
            "married_to": "456",
            "children": ["789", "1011"],
            "parents": ["999", "998"],
            "adoption_pending": {
                "requested_by": str(ctx.author.id),
                "target": "789",
                "timestamp": "2024-06-06T12:00:00"
            }
        }

        embed = build_family_embed(sample_data, self.bot, "👪 Familiendaten")
        view = MarriageInfo()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Marriage(bot))