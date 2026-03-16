import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from database import DB_NAME

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

    @app_commands.command(name="shop", description="View and buy triggers with credits")
    async def shop(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🛒 Trigger Shop",
            color=0x9b59b6
        )
        for trigger, price in TRIGGERS.items():
            embed.add_field(name=trigger, value=f"Price: {price} Credits", inline=False)
        embed.set_footer(text="Use /buytrigger <trigger_name> to purchase and equip triggers.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buytrigger", description="Buy and equip a trigger")
    @app_commands.describe(trigger="Name of the trigger to buy")
    async def buytrigger(self, interaction: discord.Interaction, trigger: str):
        user_id = interaction.user.id
        trigger = trigger.title()
        if trigger not in TRIGGERS:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Trigger Not Found",
                    description=f"{trigger} is not available in the shop.",
                    color=0xe74c3c
                ),
                ephemeral=True
            )
            return

        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute("SELECT credits FROM agents WHERE user_id=?", (user_id,))
            data = await cursor.fetchone()
            if not data:
                await interaction.response.send_message("You are not a registered agent! Use /joinborder.", ephemeral=True)
                return
            credits = data[0]
            price = TRIGGERS[trigger]

            if credits < price:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="❌ Not Enough Credits",
                        description=f"You need {price} Credits to buy {trigger}.",
                        color=0xe74c3c
                    ),
                    ephemeral=True
                )
                return

            # Deduct credits and add trigger
            await db.execute("UPDATE agents SET credits=credits-? WHERE user_id=?", (price, user_id))
            await db.execute("INSERT INTO triggers (user_id, trigger) VALUES (?,?)", (user_id, trigger))
            await db.commit()

        await interaction.response.send_message(
            embed=discord.Embed(
                title="✅ Trigger Purchased",
                description=f"You have purchased and equipped **{trigger}**!",
                color=0x2ecc71
            )
        )

async def setup(bot):
    await bot.add_cog(Shop(bot))
