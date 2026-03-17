import discord
from discord import app_commands
from discord.ext import commands
import json
import aiosqlite
from database import DB_NAME
from data.trion import roll_trion
from data.side_effects import roll_side_effect

COLOR = 0x1abc9c  # turquoise


class Agent(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="joinborder", description="Become a Border agent")
    async def joinborder(self, interaction: discord.Interaction):

        user_id = interaction.user.id
        username = interaction.user.display_name
        avatar = interaction.user.display_avatar.url

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                "SELECT user_id FROM agents WHERE user_id=?",
                (user_id,)
            )

            existing = await cursor.fetchone()

            if existing:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="⚠️ Already Registered",
                        description="You are already a Border agent.",
                        color=0xe67e22
                    ),
                    ephemeral=True
                )
                return

            # Roll stats
            trion = roll_trion()
            side = roll_side_effect()
            side_json = json.dumps(side) if side else None

            spins = 5
            credits = 100

            # Create Agent
            await db.execute(
                """
                INSERT INTO agents VALUES(?,?,?,?,?,?,?,?)
                """,
                (user_id, trion, side_json, spins, credits, 1000, 0, 0)
            )

            # Create Stat Profile
            await db.execute(
                """
                INSERT INTO agent_stats (user_id)
                VALUES (?)
                """,
                (user_id,)
            )

            # Create Story Progress
            await db.execute(
                """
                INSERT INTO story_progress (user_id)
                VALUES (?)
                """,
                (user_id,)
            )

            await db.commit()

        # Determine trion rarity
        if trion <= 6:
            rarity = "Low"
        elif trion <= 12:
            rarity = "Average"
        elif trion <= 20:
            rarity = "High"
        else:
            rarity = "EXTREMELY RARE"

        # Professional embed
        embed = discord.Embed(
            title="🛡 Border Agent Registered",
            description=f"Welcome to **Border**, {username}.",
            color=COLOR
        )

        embed.set_thumbnail(url=avatar)

        embed.add_field(
            name="🔋 Trion Level",
            value=f"{trion} ({rarity})",
            inline=True
        )

        embed.add_field(
            name="🧬 Side Effect",
            value=side if side else "None",
            inline=True
        )

        embed.add_field(
            name="🎰 Starting Spins",
            value=spins,
            inline=True
        )

        embed.add_field(
            name="💳 Starting Credits",
            value=credits,
            inline=True
        )

        embed.add_field(
            name="📖 Story Progress",
            value="Prologue — Chapter 1",
            inline=False
        )

        embed.set_footer(
            text="Your journey as a Border Agent begins now."
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Agent(bot))
