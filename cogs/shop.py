import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DB_NAME

SHOP_COLOR = 0x1abc9c

TRIGGERS = {
    "Grasshopper": 50,
    "Escudo": 40,
    "Spider": 60,
    "Bagworm": 70,
    "Chameleon": 80
}

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # VIEW SHOP
    @app_commands.command(name="shop", description="View the Border Trigger Shop")
    async def shop(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🛒 Border Trigger Shop",
            description="Purchase triggers using Credits.",
            color=SHOP_COLOR
        )

        for trigger, price in TRIGGERS.items():
            embed.add_field(
                name=f"⚙️ {trigger}",
                value=f"💰 Price: **{price} Credits**",
                inline=False
            )

        embed.set_footer(text="Use /buytrigger to purchase a trigger.")

        await interaction.response.send_message(embed=embed)

    # BUY TRIGGER
    @app_commands.command(name="buytrigger", description="Buy a trigger from the shop")
    @app_commands.describe(trigger="Name of the trigger")
    async def buytrigger(self, interaction: discord.Interaction, trigger: str):

        user_id = interaction.user.id
        trigger = trigger.title()

        if trigger not in TRIGGERS:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Trigger Not Found",
                    description="That trigger does not exist in the shop.",
                    color=0xe74c3c
                ),
                ephemeral=True
            )
            return

        async with aiosqlite.connect(DB_NAME) as db:

            # Check player exists
            cursor = await db.execute(
                "SELECT credits FROM agents WHERE user_id=?",
                (user_id,)
            )
            agent = await cursor.fetchone()

            if not agent:
                await interaction.response.send_message(
                    "You are not a Border agent yet. Use `/joinborder`.",
                    ephemeral=True
                )
                return

            credits = agent[0]
            price = TRIGGERS[trigger]

            # Check if already owned
            cursor = await db.execute(
                "SELECT * FROM triggers WHERE user_id=? AND trigger=?",
                (user_id, trigger)
            )
            owned = await cursor.fetchone()

            if owned:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="⚠️ Already Owned",
                        description=f"You already own **{trigger}**.",
                        color=0xf1c40f
                    ),
                    ephemeral=True
                )
                return

            if credits < price:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="❌ Not Enough Credits",
                        description=f"You need **{price} Credits**.",
                        color=0xe74c3c
                    ),
                    ephemeral=True
                )
                return

            # Deduct credits
            await db.execute(
                "UPDATE agents SET credits = credits - ? WHERE user_id=?",
                (price, user_id)
            )

            # Add trigger to inventory
            await db.execute(
                "INSERT INTO triggers (user_id, trigger) VALUES (?,?)",
                (user_id, trigger)
            )

            await db.commit()

        embed = discord.Embed(
            title="✅ Trigger Purchased",
            description=f"You bought **{trigger}**!",
            color=0x2ecc71
        )

        embed.add_field(
            name="Next Step",
            value=f"Equip it using `/equiptrigger {trigger}`"
        )

        await interaction.response.send_message(embed=embed)

    # VIEW INVENTORY
    @app_commands.command(name="inventory", description="View your owned triggers")
    async def inventory(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute(
                "SELECT trigger FROM triggers WHERE user_id=?",
                (user_id,)
            )

            triggers = await cursor.fetchall()

        if not triggers:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="📦 Inventory Empty",
                    description="You don't own any triggers yet.",
                    color=SHOP_COLOR
                )
            )
            return

        trigger_list = "\n".join(t[0] for t in triggers)

        embed = discord.Embed(
            title="📦 Your Trigger Inventory",
            description=trigger_list,
            color=SHOP_COLOR
        )

        await interaction.response.send_message(embed=embed)

    # EQUIP TRIGGER
    @app_commands.command(name="equiptrigger", description="Equip a trigger from your inventory")
    @app_commands.describe(trigger="Trigger name")
    async def equiptrigger(self, interaction: discord.Interaction, trigger: str):

        user_id = interaction.user.id
        trigger = trigger.title()

        async with aiosqlite.connect(DB_NAME) as db:

            # Check ownership
            cursor = await db.execute(
                "SELECT * FROM triggers WHERE user_id=? AND trigger=?",
                (user_id, trigger)
            )

            owned = await cursor.fetchone()

            if not owned:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="❌ Trigger Not Owned",
                        description="You must buy this trigger first.",
                        color=0xe74c3c
                    ),
                    ephemeral=True
                )
                return

            # Equip
            await db.execute(
                "INSERT OR REPLACE INTO loadouts (user_id, trigger) VALUES (?,?)",
                (user_id, trigger)
            )

            await db.commit()

        embed = discord.Embed(
            title="⚙️ Trigger Equipped",
            description=f"**{trigger}** has been equipped.",
            color=SHOP_COLOR
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
