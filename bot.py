import discord
from discord.ext import commands
import asyncio

from config import TOKEN
from database import setup_db

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

async def load_cogs():

    await bot.load_extension("cogs.agent")
    await bot.load_extension("cogs.profile")
    await bot.load_extension("cogs.arena")
    await bot.load_extension("cogs.codes")
    await bot.load_extension("cogs.profile")
    await bot.load_extension("cogs.spin")
    await bot.load_extension("cogs.leaderboard")

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author.bot:
        return

    # Check if bot is mentioned
    if bot.user in message.mentions:
        await message.channel.send(
            f"Hello {message.author.mention}! To start your Border journey, use **/joinborder**."
        )

    # Allow commands to still work
    await bot.process_commands(message)

@bot.event
async def on_ready():

    await setup_db()

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")

    except Exception as e:
        print(e)

    print(f"Logged in as {bot.user}")

async def main():

    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
