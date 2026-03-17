import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
import asyncio
import random
import time

from database import DB_NAME
from utils.arena_utils import calculate_damage, win_elo, lose_elo
from data.neighbors import random_neighbor

COOLDOWN_SECONDS = 30

class Arena(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.cooldowns = {}  # user_id: timestamp

    @app_commands.command(name="arena", description="Enter Solo Arena matchmaking")
    async def arena(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        username = interaction.user.display_name

        # Cooldown check
        now = time.time()
        last = self.cooldowns.get(user_id, 0)
        if now - last < COOLDOWN_SECONDS:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="⏳ Arena Cooldown",
                    description=f"Please wait {int(COOLDOWN_SECONDS - (now - last))} seconds before entering arena again.",
                    color=0xe67e22
                ),
                ephemeral=True
            )
            return
        self.cooldowns[user_id] = now

        # Check if player exists
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT trion, side_effect, elo, wins, losses FROM agents WHERE user_id=?",
                (user_id,)
            )
            player = await cursor.fetchone()
        if not player:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Not Registered",
                    description="You have not joined Border yet! Use /joinborder.",
                    color=0xe74c3c
                ),
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚔️ Arena Queue",
                description=f"{username} has entered the Solo Arena queue...",
                color=0x1abc9c
            )
        )

        # Add to queue
        self.queue.append((interaction.user, player))
        await asyncio.sleep(5)  # matchmaking wait

        # PvP matchmaking
        opponent = None
        for queued in self.queue:
            if queued[0].id != user_id:
                opponent = queued
                break

        if opponent:
            self.queue.remove((interaction.user, player))
            self.queue.remove(opponent)
            opponent_user, opponent_stats = opponent
            await self.start_battle(interaction.user, player, opponent_user, opponent_stats, pvp=True)
        else:
            # PvE fallback
            self.queue.remove((interaction.user, player))
            wave_count = random.randint(2, 3)
            enemy_names = []
            total_enemy_hp = 0
            total_enemy_dmg = 0
            for _ in range(wave_count):
                name, hp, dmg = random_neighbor()
                enemy_names.append(name)
                total_enemy_hp += hp
                total_enemy_dmg += dmg
            ai_name = f"Neighbor Wave: {', '.join(enemy_names)}"
            ai_stats = (total_enemy_hp//10, None, 1000, 0, 0)  # Simplified AI stats
            await self.start_battle(interaction.user, player, ai_name, ai_stats, pvp=False)

    async def start_battle(self, user1, stats1, user2, stats2, pvp=True):
        trion1, side1, elo1, wins1, losses1 = stats1
        trion2, side2, elo2, wins2, losses2 = stats2

        # Load equipped triggers
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT trigger FROM loadouts WHERE user_id=?", (user1.id,))
            triggers1 = [row[0] for row in await cursor.fetchall()]

        import json

side1 = json.loads(side1) if side1 else None
side2 = json.loads(side2) if side2 else None

# Get stats
async with aiosqlite.connect(DB_NAME) as db:
    cursor = await db.execute(
        "SELECT attack, defense, mobility, intelligence, trion_control, perception FROM agent_stats WHERE user_id=?",
        (user1.id,)
    )
    stats1 = await cursor.fetchone()

stats1 = {
    "attack": stats1[0],
    "defense": stats1[1],
    "mobility": stats1[2],
    "intelligence": stats1[3],
    "trion_control": stats1[4],
    "perception": stats1[5],
}

# AI stats (basic)
stats2 = {"attack": 1, "defense": 1, "mobility": 1, "intelligence": 1, "trion_control": 1, "perception": 1}

dmg1 = calculate_damage(trion1, side1, triggers1, stats1)
dmg2 = calculate_damage(trion2, side2, [], stats2)

        battle_log = f"**Battle Start!**\n"
        battle_log += f"{user1.display_name if pvp else user1} deals {dmg1} damage.\n"
        battle_log += f"{user2.display_name if pvp else user2} deals {dmg2} damage.\n"

        # Determine winner
        if dmg1 > dmg2:
            winner = user1
            loser = user2
            winner_elo = win_elo(elo1)
            loser_elo = lose_elo(elo2)
            wins1 += 1
            losses2 += 1
            battle_log += f"🏆 **Winner: {user1.display_name}**"
        elif dmg2 > dmg1:
            winner = user2
            loser = user1
            winner_elo = win_elo(elo2)
            loser_elo = lose_elo(elo1)
            wins2 += 1
            losses1 += 1
            battle_log += f"🏆 **Winner: {user2 if not pvp else user2.display_name}**"
        else:
            winner = None
            loser = None
            winner_elo = elo1
            loser_elo = elo2
            battle_log += "⚔️ **It's a tie!**"

        # Update database
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "UPDATE agents SET elo=?, wins=?, losses=? WHERE user_id=?",
                (winner_elo if dmg1 > dmg2 else loser_elo, wins1, losses1, user1.id)
            )
            if pvp:
                await db.execute(
                    "UPDATE agents SET elo=?, wins=?, losses=? WHERE user_id=?",
                    (winner_elo if dmg2 > dmg1 else loser_elo, wins2, losses2, user2.id)
                )
            await db.commit()

        # Send embed to both users
        embed = discord.Embed(
            title="⚔️ Solo Arena Battle",
            description=battle_log,
            color=0x1abc9c
        )
        await (user1 if pvp else user1).send(embed=embed)
        if pvp:
            await user2.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Arena(bot))
