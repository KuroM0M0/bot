from discord.ext import commands
from discord import app_commands
import discord
from DataBase.dataBase import *
from datetime import datetime

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
        buildSQLInsert('')
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

    @app_commands.command(name="marry", description="Send a proposal to another user")
    @app_commands.describe(member="The user you want to marry")
    async def marry(self, interaction: discord.Interaction, member: discord.User):
        if member == interaction.user:
            await interaction.response.send_message("You can't marry yourself!", ephemeral=True)
            return
        view = MarriageView(interaction.user, member)
        await interaction.response.send_message(f"{interaction.user.mention} wants to marry {member.mention}! 💍", view=view)

    @app_commands.command(name="partner", description="Show info about your partner")
    async def partner(self, interaction: discord.Interaction):
        sample_data = {
            "user_id": str(interaction.user.id),
            "married_to": "789",
            "past_marriages": ["1011", "1213"]
        }
        embed = build_family_embed(sample_data, self.bot, "💍 Ehepartner")
        view = MarriageInfo()
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="divorce", description="Divorce your partner")
    async def divorce(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You have divorced: {interaction.user.mention}")

    @app_commands.command(name="sendlove", description="Send love to a user with a message")
    @app_commands.describe(member="The user you want to send love to", message="The message you want to send")
    async def sendlove(self, interaction: discord.Interaction, member: discord.Member, message: str):
        await interaction.response.send_message(f"{interaction.user.mention} sends love to {member.mention}: {message}")

    @app_commands.command(name="children", description="Show info about your children")
    async def children(self, interaction: discord.Interaction):
        sample_data = {
            "user_id": str(interaction.user.id),
            "children": ["789", "1011"]
        }
        embed = build_family_embed(sample_data, self.bot, "🧒 Kinder")
        view = MarriageInfo()
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="family", description="Show info about your family")
    async def family(self, interaction: discord.Interaction):
        sample_data = {
            "user_id": str(interaction.user.id),
            "married_to": "456",
            "children": ["789", "1011"],
            "parents": ["999", "998"],
            "adoption_pending": {
                "requested_by": str(interaction.user.id),
                "target": "789",
                "timestamp": "2024-06-06T12:00:00"
            }
        }

        embed = build_family_embed(sample_data, self.bot, "👪 Familiendaten")
        view = MarriageInfo()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    cog = Marriage(bot)
    await bot.add_cog(cog)