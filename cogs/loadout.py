import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite

from db_config import DB_NAME
from data.triggers import TRIGGERS

SLOTS = ["Main", "Sub", "Optional"]

class Loadout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # VIEW LOADOUT
    @app_commands.command(name="loadout", description="View your trigger loadout")
    async def loadout(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                "SELECT trigger, slot FROM loadouts WHERE user_id=?",
                (user_id,)
            )

            data = await cursor.fetchall()

        loadout = {slot: "None" for slot in SLOTS}

        for trigger, slot in data:
            loadout[slot] = trigger

        embed = discord.Embed(
            title=f"⚡ {interaction.user.display_name}'s Loadout",
            color=0x1abc9c
        )

        for slot in SLOTS:
            embed.add_field(name=f"{slot} Trigger", value=loadout[slot], inline=False)

        embed.set_footer(text="Use /equip <trigger> <slot>")

        await interaction.response.send_message(embed=embed)

    # EQUIP
    @app_commands.command(name="equip", description="Equip a trigger")
    @app_commands.describe(trigger="Trigger name", slot="Main / Sub / Optional")
    async def equip(self, interaction: discord.Interaction, trigger: str, slot: str):

        user_id = interaction.user.id
        trigger = trigger.title()
        slot = slot.title()

        if slot not in SLOTS:
            await interaction.response.send_message(
                "Slot must be: Main, Sub, or Optional.",
                ephemeral=True
            )
            return

        trigger_data = TRIGGERS.get(trigger)

        if not trigger_data:
            await interaction.response.send_message(
                "That trigger does not exist.",
                ephemeral=True
            )
            return

        # Stat requirement check
        required_int = trigger_data.get("requirement", {}).get("intelligence", 0)

        async with aiosqlite.connect(DB_NAME) as db:

            # Check ownership
            cursor = await db.execute(
                "SELECT 1 FROM triggers WHERE user_id=? AND trigger=?",
                (user_id, trigger)
            )

            if not await cursor.fetchone():
                await interaction.response.send_message(
                    f"You don't own {trigger}.",
                    ephemeral=True
                )
                return

            # Get stats
            cursor = await db.execute(
                "SELECT intelligence FROM agent_stats WHERE user_id=?",
                (user_id,)
            )

            stats = await cursor.fetchone()

            if stats and stats[0] < required_int:
                await interaction.response.send_message(
                    f"You need Intelligence {required_int} to use {trigger}.",
                    ephemeral=True
                )
                return

            # Equip (replace slot)
            await db.execute(
                "INSERT OR REPLACE INTO loadouts (user_id, trigger, slot) VALUES (?,?,?)",
                (user_id, trigger, slot)
            )

            await db.commit()

        await interaction.response.send_message(
            embed=discord.Embed(
                title="✅ Equipped",
                description=f"{trigger} equipped as **{slot} Trigger**.",
                color=0x1abc9c
            )
        )

async def setup(bot):
    await bot.add_cog(Loadout(bot))
