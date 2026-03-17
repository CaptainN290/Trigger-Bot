import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
import random
from config import DB_NAME
from data.trion import roll_trion
from data.side_effects import roll_side_effect

class Spin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="spin", description="Consume a spin to reroll Trion or Side Effect")
    async def spin(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT spins, trion, side_effect FROM agents WHERE user_id=?",
                (user_id,)
            )
            data = await cursor.fetchone()

        if not data:
            await interaction.response.send_message("You have not joined Border yet. Use /joinborder first!", ephemeral=True)
            return

        spins, current_trion, current_side = data

        if spins <= 0:
            await interaction.response.send_message("You have no spins left!", ephemeral=True)
            return

        spins -= 1
        choice = random.choice(["trion", "side_effect"])

        if choice == "trion":
            new_trion = roll_trion()
            await interaction.response.send_message(
                f"🎲 You rerolled your **Trion Level**!\nOld: {current_trion} → New: {new_trion}\nSpins left: {spins}"
            )
            async with aiosqlite.connect(DB_NAME) as db:
                await db.execute(
                    "UPDATE agents SET trion=?, spins=? WHERE user_id=?",
                    (new_trion, spins, user_id)
                )
                await db.commit()

        else:
            new_side = roll_side_effect()
            await interaction.response.send_message(
                f"🎲 You rerolled your **Side Effect**!\nOld: {current_side if current_side else 'None'} → New: {new_side if new_side else 'None'}\nSpins left: {spins}"
            )
            async with aiosqlite.connect(DB_NAME) as db:
                await db.execute(
                    "UPDATE agents SET side_effect=?, spins=? WHERE user_id=?",
                    (new_side, spins, user_id)
                )
                await db.commit()

async def setup(bot):
    await bot.add_cog(Spin(bot))
