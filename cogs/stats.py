import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from config import DB_NAME

COLOR = 0x1abc9c


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="View your agent stats")
    async def stats(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                "SELECT attack, defense, mobility, intelligence, trion_control, perception, stat_points FROM agent_stats WHERE user_id=?",
                (user_id,)
            )

            data = await cursor.fetchone()

        if not data:
            await interaction.response.send_message(
                "You are not registered. Use `/joinborder` first.",
                ephemeral=True
            )
            return

        attack, defense, mobility, intelligence, trion_control, perception, points = data

        embed = discord.Embed(
            title="📊 Agent Stats",
            color=COLOR
        )

        embed.add_field(name="⚔️ Attack Potency", value=attack)
        embed.add_field(name="🛡 Defense", value=defense)
        embed.add_field(name="🏃 Mobility", value=mobility)
        embed.add_field(name="🧠 Intelligence", value=intelligence)
        embed.add_field(name="🔋 Trion Control", value=trion_control)
        embed.add_field(name="👁 Perception", value=perception)

        embed.add_field(
            name="⭐ Unspent Points",
            value=points,
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="upgradestat", description="Upgrade one of your stats")
    @app_commands.describe(stat="Stat name (attack, defense, mobility, intelligence, trion_control, perception)")
    async def upgradestat(self, interaction: discord.Interaction, stat: str):

        user_id = interaction.user.id
        stat = stat.lower()

        valid_stats = [
            "attack",
            "defense",
            "mobility",
            "intelligence",
            "trion_control",
            "perception"
        ]

        if stat not in valid_stats:
            await interaction.response.send_message(
                "Invalid stat name.",
                ephemeral=True
            )
            return

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                "SELECT stat_points FROM agent_stats WHERE user_id=?",
                (user_id,)
            )

            result = await cursor.fetchone()

            if not result:
                await interaction.response.send_message(
                    "You are not registered.",
                    ephemeral=True
                )
                return

            points = result[0]

            if points <= 0:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="❌ No Stat Points",
                        description="You have no stat points available.",
                        color=0xe74c3c
                    ),
                    ephemeral=True
                )
                return

            await db.execute(
                f"UPDATE agent_stats SET {stat} = {stat} + 1, stat_points = stat_points - 1 WHERE user_id=?",
                (user_id,)
            )

            await db.commit()

        embed = discord.Embed(
            title="✅ Stat Upgraded",
            description=f"Your **{stat.replace('_',' ').title()}** increased by 1.",
            color=COLOR
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Stats(bot))
