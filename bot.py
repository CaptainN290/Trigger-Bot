import discord
from discord.ext import commands
import asyncio
import traceback

from config import TOKEN, DB_NAME

print(f"TOKEN LOADED: {bool(TOKEN)}")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# List of all cogs
COGS = [
    "cogs.agent",
    "cogs.profile",
    "cogs.arena",
    "cogs.codes",
    "cogs.spin",
    "cogs.leaderboard",
    "cogs.loadout",
    "cogs.shop",
    "cogs.squads",
    "cogs.stats",
    "cogs.story"
]

# ------------------ Cog Loader ------------------
async def load_cogs():
    for cog in COGS:
        print(f"📦 Loading {cog}...")
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded {cog}")
        except Exception:
            print(f"❌ Failed to load {cog}:")
            traceback.print_exc()

# ------------------ Events ------------------
@bot.event
async def on_ready():
    print(f"🔑 Logged in as {bot.user}")
    
    # Setup database if you have this function
    try:
        await setup_db()
        print("🗄️ Database ready")
    except NameError:
        print("⚠️ setup_db() not defined, skipping DB setup")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"⚡ Synced {len(synced)} commands")
    except Exception:
        print("❌ Failed to sync commands:")
        traceback.print_exc()

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

# ------------------ Main ------------------
async def main():
    print("🚀 Starting bot...")

    try:
        # Load all cogs first
        await load_cogs()
        
        # Start the bot
        print("🔥 Connecting to Discord...")
        await bot.start(TOKEN)
    except Exception:
        print("❌ Bot crashed:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
