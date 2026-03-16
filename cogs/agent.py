import discord
from discord import app_commands
from discord.ext import commands

import aiosqlite

from database import DB_NAME
from data.trion import roll_trion
from data.side_effects import roll_side_effect

class Agent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="joinborder", description="Become a Border agent")
    async def joinborder(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                "SELECT user_id FROM agents WHERE user_id=?",
                (user_id,)
            )

            existing = await cursor.fetchone()

            if existing:
                await interaction.response.send_message(
                    "You are already a Border agent.",
                    ephemeral=True
                )
                return

            trion = roll_trion()
            side = roll_side_effect()

            await db.execute(
                """
                INSERT INTO agents VALUES(?,?,?,?,?,?,?,?)
                """,
                (user_id,trion,side,5,100,1000,0,0)
            )

            await db.commit()

        embed = discord.Embed(
            title="Border Agent Registered",
            color=0x2ecc71
        )

        embed.add_field(name="Trion Level", value=trion)

        if side:
            embed.add_field(name="Side Effect", value=side)
        else:
            embed.add_field(name="Side Effect", value="None")

        embed.add_field(name="Starting Spins", value=5)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Agent(bot))
