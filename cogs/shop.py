import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from config import DB_NAME
from data.triggers import TRIGGERS

SHOP_COLOR = 0x1abc9c

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
        for name, data in TRIGGERS.items():
            embed.add_field(
                name=f"⚙️ {name} ({data['type'].capitalize()})",
                value=f"💰 Price: **{data['price']} Credits** | ⚡ Trion Cost: {data['trion_cost']}",
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

        data = TRIGGERS[trigger]
        price = data["price"]

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT credits FROM agents WHERE user_id=?", (user_id,))
            agent = await cursor.fetchone()
            if not agent:
                await interaction.response.send_message(
                    "You are not a Border agent yet. Use `/joinborder`.",
                    ephemeral=True
                )
                return
            credits = agent[0]
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
            # Check already owned
            cursor2 = await db.execute("SELECT 1 FROM triggers WHERE user_id=? AND trigger=?", (user_id, trigger))
            if await cursor2.fetchone():
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="⚠️ Already Owned",
                        description=f"You already own **{trigger}**.",
                        color=0xf1c40f
                    ),
                    ephemeral=True
                )
                return
            # Deduct credits and add trigger
            await db.execute("UPDATE agents SET credits = credits - ? WHERE user_id=?", (price, user_id))
            await db.execute("INSERT INTO triggers (user_id, trigger) VALUES (?,?)", (user_id, trigger))
            await db.commit()

        embed = discord.Embed(
            title="✅ Trigger Purchased",
            description=f"You bought **{trigger}**!",
            color=0x2ecc71
        )
        embed.add_field(name="Next Step", value=f"Equip it using `/equiptrigger {trigger}`")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
