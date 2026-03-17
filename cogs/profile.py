import discord
import os
from discord import app_commands
from discord.ext import commands
import aiosqlite
from config import DB_NAME
import requests
from io import BytesIO
from utils.profile_card import generate_profile_card

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="View your agent profile")
    async def profile(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:
            # Agent info
            cursor = await db.execute(
                "SELECT trion, side_effect, spins, credits, elo, wins, losses FROM agents WHERE user_id=?",
                (user_id,)
            )
            agent = await cursor.fetchone()

            if not agent:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="❌ Not Registered",
                        description="You have not joined Border yet! Use /joinborder.",
                        color=0xe74c3c
                    ),
                    ephemeral=True
                )
                return

            trion, side, spins, credits, elo, wins, losses = agent

            # Stats
            cursor = await db.execute(
                "SELECT attack, defense, mobility, intelligence, trion_control, perception FROM agent_stats WHERE user_id=?",
                (user_id,)
            )
            stats_row = await cursor.fetchone()
            stats = {
                "Attack": stats_row[0],
                "Defense": stats_row[1],
                "Mobility": stats_row[2],
                "Intelligence": stats_row[3],
                "Trion Control": stats_row[4],
                "Perception": stats_row[5]
            }

            # Triggers (Main, Sub, Optional)
            cursor = await db.execute(
                "SELECT trigger FROM loadouts WHERE user_id=?",
                (user_id,)
            )
            triggers = [row[0] for row in await cursor.fetchall()]

            # Story progress
            cursor = await db.execute(
                "SELECT arc, mission FROM story_progress WHERE user_id=?",
                (user_id,)
            )
            story_row = await cursor.fetchone()
            story_arc, story_mission = story_row if story_row else ("Prologue", 1)

        # Download avatar temporarily
        avatar_url = interaction.user.display_avatar.url
        response = requests.get(avatar_url)
        avatar_path = f"temp_avatar_{user_id}.png"
        with open(avatar_path, "wb") as f:
            f.write(response.content)

        # Generate profile card
        card_path = generate_profile_card(
            username=interaction.user.display_name,
            avatar_path=avatar_path,
            trion=trion,
            side_effect=side,
            spins=spins,
            credits=credits,
            elo=elo,
            wins=wins,
            losses=losses,
            stats=stats,
            triggers=triggers,
            story_arc=story_arc,
            story_mission=story_mission,
            user_id=user_id
        )

        # Send card
        file = discord.File(card_path)
        await interaction.response.send_message(file=file)

        # Cleanup temporary avatar
        if os.path.exists(avatar_path):
            os.remove(avatar_path)


async def setup(bot):
    await bot.add_cog(Profile(bot))
