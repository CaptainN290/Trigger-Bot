import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from db_config import DB_NAME

class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description="View the top agents by ELO")
    async def leaderboard(self, interaction: discord.Interaction):
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT user_id, elo FROM agents ORDER BY elo DESC LIMIT 10"
            )
            data = await cursor.fetchall()

        if not data:
            await interaction.response.send_message("No agents found yet!", ephemeral=True)
            return

        embed = discord.Embed(
            title="🏆 Top Border Agents by ELO",
            color=0xf1c40f
        )

        for i, (user_id, elo) in enumerate(data, start=1):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"{i}. {user.display_name}", value=f"ELO: {elo}", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
