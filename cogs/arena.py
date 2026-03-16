import discord
from discord import app_commands
from discord.ext import commands, tasks
import aiosqlite
import asyncio
from database import DB_NAME
from utils.arena_utils import calculate_damage, win_elo, lose_elo
import random

class Arena(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = []

    @app_commands.command(name="arena", description="Enter Solo Arena matchmaking")
    async def arena(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        username = interaction.user.display_name

        # Check if user exists
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT trion, side_effect, elo, wins, losses FROM agents WHERE user_id=?", (user_id,))
            player = await cursor.fetchone()

        if not player:
            await interaction.response.send_message("You have not joined Border yet! Use /joinborder.", ephemeral=True)
            return

        await interaction.response.send_message(f"{username} has entered the Solo Arena queue...", ephemeral=False)

        # Add player to queue
        self.queue.append((interaction.user, player))

        # Wait 5 seconds for matchmaking
        await asyncio.sleep(5)

        # Try to find an opponent
        opponent = None
        for queued in self.queue:
            if queued[0].id != user_id:
                opponent = queued
                break

        if opponent:
            # PvP match
            self.queue.remove((interaction.user, player))
            self.queue.remove(opponent)
            opponent_user, opponent_stats = opponent
            await self.start_battle(interaction.user, player, opponent_user, opponent_stats, pvp=True)
        else:
            # PvE match
            self.queue.remove((interaction.user, player))
            # Generate AI opponent
            ai_trion = random.randint(2, 15)
            ai_side = None
            ai_name = "AI Opponent"
            ai_stats = (ai_trion, ai_side, 1000, 0, 0)
            await self.start_battle(interaction.user, player, ai_name, ai_stats, pvp=False)

    async def start_battle(self, user1, stats1, user2, stats2, pvp=True):
        # Unpack stats
        trion1, side1, elo1, wins1, losses1 = stats1
        trion2, side2, elo2, wins2, losses2 = stats2

        dmg1 = calculate_damage(trion1, side1)
        dmg2 = calculate_damage(trion2, side2)

        battle_log = f"**Battle Start!**\n"
        battle_log += f"{user1.display_name if pvp else user1} deals {dmg1} damage.\n"
        battle_log += f"{user2.display_name if pvp else user2} deals {dmg2} damage.\n"

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
            battle_log += f"🏆 **Winner: {user2.display_name if pvp else user2}**"
        else:
            winner = None
            loser = None
            winner_elo = elo1
            loser_elo = elo2
            battle_log += "⚔️ **It's a tie!**"

        # Update DB
        async with aiosqlite.connect(DB_NAME) as db:
            # Update player 1
            await db.execute("UPDATE agents SET elo=?, wins=?, losses=? WHERE user_id=?",
                             (winner_elo if dmg1 > dmg2 else loser_elo, wins1, losses1, user1.id))
            if pvp:
                # Update player 2
                await db.execute("UPDATE agents SET elo=?, wins=?, losses=? WHERE user_id=?",
                                 (winner_elo if dmg2 > dmg1 else loser_elo, wins2, losses2, user2.id))
            await db.commit()

        embed = discord.Embed(title="⚔️ Solo Arena Battle", description=battle_log, color=0xe74c3c)
        await (user1 if pvp else user1).send(embed=embed)
        if pvp:
            await user2.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Arena(bot))
