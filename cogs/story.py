import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
import asyncio
import json
import random
from database import DB_NAME
from utils.arena_utils import calculate_damage, win_elo, lose_elo
from data.neighbors import random_neighbor

class Story(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="story", description="View your current story mission")
    async def story(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT arc, chapter, mission FROM story_progress WHERE user_id=?", (user_id,))
            progress = await cursor.fetchone()
            if not progress:
                # Initialize
                await db.execute("INSERT INTO story_progress (user_id) VALUES (?)", (user_id,))
                await db.commit()
                arc, chapter, mission = 'Prologue', 1, 1
            else:
                arc, chapter, mission = progress

            # Fetch current mission
            cursor = await db.execute(
                "SELECT type, description, choices, reward_type, reward_amount, reward_trigger, replayable FROM story_missions WHERE arc=? AND chapter=? AND mission=?",
                (arc, chapter, mission)
            )
            mission_data = await cursor.fetchone()

        if not mission_data:
            embed = discord.Embed(
                title="📖 Story Mode",
                description="You have completed all current missions. More coming soon!",
                color=0x1abc9c
            )
            await interaction.response.send_message(embed=embed)
            return

        m_type, desc, choices_json, reward_type, reward_amount, reward_trigger, replayable = mission_data
        embed = discord.Embed(
            title=f"📖 {arc} — Chapter {chapter}, Mission {mission}",
            description=desc,
            color=0x1abc9c
        )
        if m_type == 'choice':
            embed.add_field(name="Choices", value="React or click a button to choose.", inline=False)
        embed.set_footer(text=f"Reward: {reward_amount} {reward_type}{' / Trigger: ' + reward_trigger if reward_trigger else ''} | {'Replayable' if replayable else 'One-time'}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mission", description="Start your current mission")
    async def mission(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT arc, chapter, mission FROM story_progress WHERE user_id=?", (user_id,))
            progress = await cursor.fetchone()
            if not progress:
                await db.execute("INSERT INTO story_progress (user_id) VALUES (?)", (user_id,))
                await db.commit()
                arc, chapter, mission = 'Prologue', 1, 1
            else:
                arc, chapter, mission = progress

            # Fetch mission data
            cursor = await db.execute(
                "SELECT type, description, choices, reward_type, reward_amount, reward_trigger, replayable FROM story_missions WHERE arc=? AND chapter=? AND mission=?",
                (arc, chapter, mission)
            )
            mission_data = await cursor.fetchone()
        if not mission_data:
            embed = discord.Embed(
                title="❌ No Mission Found",
                description="You have completed all current missions. More coming soon!",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed)
            return

        m_type, desc, choices_json, reward_type, reward_amount, reward_trigger, replayable = mission_data

        # Handle mission types
        if m_type == 'arena' or m_type == 'boss':
            await self.start_arena_mission(interaction, m_type, reward_type, reward_amount, reward_trigger)
        elif m_type == 'choice':
            await self.start_choice_mission(interaction, choices_json, reward_type, reward_amount, reward_trigger)
        elif m_type == 'exploration':
            await self.start_exploration(interaction, desc, reward_type, reward_amount, reward_trigger)

        # Update progress for non-replayable
        if not replayable:
            async with aiosqlite.connect(DB_NAME) as db:
                await db.execute(
                    "UPDATE story_progress SET mission=mission+1 WHERE user_id=?", (user_id,)
                )
                await db.commit()

    async def start_arena_mission(self, interaction, m_type, reward_type, reward_amount, reward_trigger):
        user_id = interaction.user.id
        username = interaction.user.display_name

        # Fetch player stats
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT trion, side_effect, elo, wins, losses FROM agents WHERE user_id=?", (user_id,))
            stats = await cursor.fetchone()
            # Load triggers
            cursor2 = await db.execute("SELECT trigger FROM loadouts WHERE user_id=?", (user_id,))
            triggers = [row[0] for row in await cursor2.fetchall()]

        trion, side, elo, wins, losses = stats
        dmg1 = calculate_damage(trion, side, triggers)

        # Generate AI wave
        wave_count = random.randint(2, 3)
        enemy_names = []
        total_enemy_hp = 0
        total_enemy_dmg = 0
        for _ in range(wave_count):
            name, hp, dmg = random_neighbor()
            enemy_names.append(name)
            total_enemy_hp += hp
            total_enemy_dmg += dmg
        dmg2 = total_enemy_hp + total_enemy_dmg//2

        battle_log = f"**Battle Start!**\n{username} deals {dmg1} damage.\nNeighbors ({', '.join(enemy_names)}) deal {dmg2} damage.\n"

        # Determine winner
        if dmg1 >= dmg2:
            won = True
            battle_log += "🏆 **You won!**"
        else:
            won = False
            battle_log += "⚔️ **You lost!**"

        # Reward
        if won:
            async with aiosqlite.connect(DB_NAME) as db:
                if reward_type == 'credits':
                    await db.execute("UPDATE agents SET credits=credits+? WHERE user_id=?", (reward_amount, user_id))
                elif reward_type == 'spins':
                    await db.execute("UPDATE agents SET spins=spins+? WHERE user_id=?", (reward_amount, user_id))
                elif reward_type == 'trigger' and reward_trigger:
                    await db.execute("INSERT INTO triggers (user_id, trigger) VALUES (?,?)", (user_id, reward_trigger))
                await db.commit()

        embed = discord.Embed(
            title=f"{'🛡️ Boss Fight' if m_type=='boss' else '⚔️ Mission Arena'}",
            description=battle_log,
            color=0x1abc9c
        )
        embed.set_footer(text=f"Reward: {reward_amount} {reward_type}{' / Trigger: ' + reward_trigger if reward_trigger else ''}")
        await interaction.response.send_message(embed=embed)

    async def start_choice_mission(self, interaction, choices_json, reward_type, reward_amount, reward_trigger):
        # Parse choices
        choices = json.loads(choices_json)
        buttons = []
        for choice in choices:
            buttons.append(discord.ui.Button(label=choice['label'], custom_id=choice['id']))

        # View for buttons
        view = discord.ui.View()
        for btn in buttons:
            view.add_item(btn)

        embed = discord.Embed(
            title="📜 Choice Mission",
            description="Make your choice wisely! ⚔️",
            color=0x1abc9c
        )
        embed.set_footer(text=f"Reward: {reward_amount} {reward_type}{' / Trigger: ' + reward_trigger if reward_trigger else ''}")
        await interaction.response.send_message(embed=embed, view=view)

    async def start_exploration(self, interaction, desc, reward_type, reward_amount, reward_trigger):
        embed = discord.Embed(
            title="🔍 Exploration Mission",
            description=desc,
            color=0x1abc9c
        )
        embed.set_footer(text=f"Reward: {reward_amount} {reward_type}{' / Trigger: ' + reward_trigger if reward_trigger else ''}")
        await interaction.response.send_message(embed=embed)
        # Give reward immediately
        user_id = interaction.user.id
        async with aiosqlite.connect(DB_NAME) as db:
            if reward_type == 'credits':
                await db.execute("UPDATE agents SET credits=credits+? WHERE user_id=?", (reward_amount, user_id))
            elif reward_type == 'spins':
                await db.execute("UPDATE agents SET spins=spins+? WHERE user_id=?", (reward_amount, user_id))
            elif reward_type == 'trigger' and reward_trigger:
                await db.execute("INSERT INTO triggers (user_id, trigger) VALUES (?,?)", (user_id, reward_trigger))
            await db.commit()

async def setup(bot):
    await bot.add_cog(Story(bot))
