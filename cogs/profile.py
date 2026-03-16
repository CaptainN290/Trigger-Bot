import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DB_NAME

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="View your agent profile")
    async def profile(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT trion, side_effect, spins, credits, elo, wins, losses FROM agents WHERE user_id=?",
                (user_id,)
            )
            data = await cursor.fetchone()
            # Fetch equipped triggers
            cursor2 = await db.execute(
                "SELECT trigger FROM loadouts WHERE user_id=?", (user_id,)
            )
            triggers = [row[0] for row in await cursor2.fetchall()]

        if not data:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Not Registered",
                    description="You have not joined Border yet! Use /joinborder.",
                    color=0xe74c3c
                ),
                ephemeral=True
            )
            return

        trion, side, spins, credits, elo, wins, losses = data

        embed = discord.Embed(
            title=f"{interaction.user.display_name}'s Agent Profile",
            color=0x1abc9c
        )
        embed.set_thumbnail(url=interaction.user.avatar.url)
        embed.add_field(name="Trion Level", value=trion, inline=True)
        embed.add_field(name="Side Effect", value=side if side else "None", inline=True)
        embed.add_field(name="Spins", value=spins, inline=True)
        embed.add_field(name="Credits", value=credits, inline=True)
        embed.add_field(name="ELO", value=elo, inline=True)
        embed.add_field(name="Wins / Losses", value=f"{wins} / {losses}", inline=True)
        embed.add_field(name="Equipped Triggers", value=", ".join(triggers) if triggers else "None", inline=False)
        embed.set_footer(text="Use /spin to reroll Trion or Side Effect. /loadout to manage triggers.")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))
    await bot.add_cog(Profile(bot))
