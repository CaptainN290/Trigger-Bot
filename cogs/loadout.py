import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DB_NAME

MAX_LOADOUT = 3

class Loadout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loadout", description="View or equip your triggers")
    async def loadout(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:
            # Fetch owned triggers
            cursor = await db.execute("SELECT trigger FROM triggers WHERE user_id=?", (user_id,))
            triggers = [row[0] for row in await cursor.fetchall()]

            # Fetch currently equipped triggers (can be stored in a separate table or same table)
            cursor2 = await db.execute("SELECT trigger FROM loadouts WHERE user_id=?", (user_id,))
            equipped = [row[0] for row in await cursor2.fetchall()]

        embed = discord.Embed(
            title=f"⚡ {interaction.user.display_name}'s Loadout",
            description="Equip triggers to use in battle!",
            color=0x1abc9c  # Turquoise
        )
        embed.add_field(name="Owned Triggers", value=", ".join(triggers) if triggers else "None", inline=False)
        embed.add_field(name="Equipped Triggers", value=", ".join(equipped) if equipped else "None", inline=False)
        embed.set_footer(text=f"You can equip up to {MAX_LOADOUT} triggers. Use /equip <trigger_name>.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="equip", description="Equip a trigger for your loadout")
    @app_commands.describe(trigger="Name of the trigger to equip")
    async def equip(self, interaction: discord.Interaction, trigger: str):
        user_id = interaction.user.id
        trigger = trigger.title()

        async with aiosqlite.connect(DB_NAME) as db:
            # Check ownership
            cursor = await db.execute("SELECT 1 FROM triggers WHERE user_id=? AND trigger=?", (user_id, trigger))
            if not await cursor.fetchone():
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="❌ Trigger Not Owned",
                        description=f"You do not own {trigger}. Buy it first in /shop.",
                        color=0xe74c3c
                    ),
                    ephemeral=True
                )
                return
            # Fetch equipped
            cursor2 = await db.execute("SELECT trigger FROM loadouts WHERE user_id=?", (user_id,))
            equipped = [row[0] for row in await cursor2.fetchall()]
            if trigger in equipped:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="⚠️ Already Equipped",
                        description=f"{trigger} is already in your loadout.",
                        color=0xe67e22
                    ),
                    ephemeral=True
                )
                return
            if len(equipped) >= MAX_LOADOUT:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="❌ Loadout Full",
                        description=f"You can only equip {MAX_LOADOUT} triggers. Unequip one first.",
                        color=0xe74c3c
                    ),
                    ephemeral=True
                )
                return
            # Equip
            await db.execute("INSERT INTO loadouts (user_id, trigger) VALUES (?,?)", (user_id, trigger))
            await db.commit()
        await interaction.response.send_message(
            embed=discord.Embed(
                title="✅ Trigger Equipped",
                description=f"{trigger} added to your loadout!",
                color=0x1abc9c
            )
        )

async def setup(bot):
    await bot.add_cog(Loadout(bot))
