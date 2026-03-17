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
    await bot.load_extension("cogs.spin")
    await bot.load_extension("cogs.leaderboard")
    await bot.load_extension("cogs.loadout")
    await bot.load_extension("cogs.shop")
    await bot.load_extension("cogs.squads")
    await bot.load_extension("cogs.stats")
    await bot.load_extension("cogs.story")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        embed = discord.Embed(
            title="👋 Welcome Agent!",
            description=f"Hello {message.author.mention}! To start your Border journey, use **/joinborder**.",
            color=0x1abc9c
        )
        await message.channel.send(embed=embed)

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
