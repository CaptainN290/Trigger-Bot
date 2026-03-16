WORLD TRIGGER DISCORD BOT DEV MEMORY

Language: Python
Library: discord.py
Commands: Slash Commands ONLY
Hosting: Render or Wispbyte
Database: SQLite using aiosqlite

Project Structure

bot.py
config.py
database.py
requirements.txt

cogs/
agent.py
profile.py
arena.py
codes.py

data/
trion.py
side_effects.py
neighbors.py
triggers.py

utils/
elo.py

Game Systems

Agents
------

Agents have:

Trion
Side Effect
Spins
Credits
ELO
Wins
Losses

Trion Range
-----------

2-6 low
7-12 average
13-20 high
21-38 extremely rare

Examples

Osamu = 2
Yuma = 7
Chika = 38

Side Effects
------------

60 percent chance to obtain.

Common
Rare

Spins
-----

Spins reroll:

Trion
Side Effect

Game Modes
----------

Story Mode
Missions
Solo Arena
Rank Wars

Solo Arena
----------

Player vs AI.

Win = +25 ELO
Loss = -25 ELO

Economy
-------

Currency = Credits

Credits buy triggers like:

Grasshopper
Escudo
Spider
Bagworm
Chameleon

Development Rule
----------------

Every time new commands are added:

1. Place them inside a Cog
2. Use slash commands
3. Update database if new data is required
4. Update DEV_INSTRUCTIONS.md

🌐 WORLD TRIGGER DISCORD BOT DEV MEMORY (UPDATED)

Language: Python
Library: discord.py
Commands: Slash Commands ONLY
Hosting: Render or Wispbyte
Database: SQLite using aiosqlite

Project Structure
bot.py
config.py
database.py
requirements.txt

cogs/
    agent.py
    profile.py
    spin.py
    arena.py
    leaderboard.py
    codes.py

data/
    trion.py
    side_effects.py
    neighbors.py
    triggers.py

utils/
    elo.py
    arena_utils.py
Commands Implemented
1️⃣ /joinborder — agent.py

Registers a new Border agent

Generates Trion and optional Side Effect

Gives starting Spins = 5

Saves user to SQLite

2️⃣ /profile — profile.py

Shows agent stats: Trion, Side Effect, Spins, Credits, ELO, Wins/Losses

Professional embed

Works for any registered agent

3️⃣ /spin — spin.py

Consumes 1 spin

Randomly rerolls Trion or Side Effect

Updates database

Shows embed/log of old → new values

4️⃣ /leaderboard — leaderboard.py

Shows top 10 agents by ELO

Embedded display

Fetches real usernames

5️⃣ /arena — arena.py

Solo Arena PvP system

Queue-based matchmaking

Fallback PvE AI if no player found

Uses Trion + Side Effect to calculate damage

ELO updated per battle (+25 win / -25 loss)

Sends battle log embeds to participants

PvE AI now uses canonical Neighbor types

Supports Trigger buffs (Grasshopper, Escudo, Spider, Bagworm, Chameleon)

PvE fights use random Neighbor from data/neighbors.py

Data Systems Implemented
Trion System — trion.py

Canon range: 2–38

Randomized rolls with rarity distribution

Side Effects — side_effects.py

60% chance to obtain

Common (85%) / Rare (15%)

Each side effect gives stat buffs

Neighbor Types — neighbors.py

Real Neighbor types with HP/Damage stats

Random selection for PvE AI

Triggers — triggers.py

Buff system added in arena_utils.py

Each trigger provides a combat bonus

Utility Functions
elo.py

win_elo() / lose_elo() for simple ELO calculation

arena_utils.py

calculate_damage(trion, side_effect, triggers)

Applies Trion base, Side Effect buffs, and Trigger buffs

Randomized minor variation

Solo Arena Details

PvP first: searches queue for real players

Fallback PvE: fights canonical Neighbor if no player available

Cooldown (to be added): prevents spamming

Battle logs: embedded and sent to all participants

ELO update: automatic

Win/loss update: automatic

Next Commands / Features to Add

Cooldown system for /arena

Trigger shop — purchase triggers with credits

Loadout system — equip triggers before fights

PvE AI enhancements — multiple neighbors or waves

Story Mode — missions and arcs from the anime

Rank Wars — squad battles, rare events

/redeem — code system for spins/credits (already started, can expand)

Mission system — daily/weekly quests for spins/credits

Profile cards / visual embeds — prettier, image-based profiles

Things to Fix / Improve

/arena currently does not implement cooldown (prevents spam)

PvE AI is single neighbor, can be multi-wave or include abilities

Damage calculation is simplified, can be improved with triggers & buffs stacking

/spin could later allow multiple spins at once

/leaderboard could support pages if >10 players

Add error handling for disconnected users / DMs in arena

Development Rules

All new commands go inside a Cog

Must be slash commands

Update database if new data is required

Update DEV_MEMORY after each major feature

Keep PvP as primary, PvE fallback if no players

Embed all messages for professional look

Store persistent data in SQLite (aiosqlite)

✅ At this point, the bot has:

Playable PvP / PvE Solo Arena

ELO system with leaderboard

Agent creation, profile, spins

Trigger buffs affecting combat

Canonical Neighbor types for PvE

WORLD TRIGGER DISCORD BOT DEV MEMORY (UPDATED)

Language: Python
Library: discord.py
Commands: Slash Commands ONLY
Hosting: Render or Wispbyte
Database: SQLite using aiosqlite

Project Structure
bot.py config.py database.py requirements.txt

cogs/
    agent.py
    profile.py  # updated with visual profile cards + triggers
    spin.py
    arena.py    # updated with cooldown, PvP queue, PvE multi-neighbor, triggers
    leaderboard.py
    codes.py
    shop.py
    loadout.py
    story.py

data/
    trion.py
    side_effects.py
    neighbors.py
    triggers.py

utils/
    elo.py
    arena_utils.py

Game Systems
Agents
Trion, Side Effect, Spins, Credits, ELO, Wins, Losses
Trion Range: 2-6 low, 7-12 avg, 13-20 high, 21-38 extremely rare
Side Effects: 60% chance, common/rare, provide stat buffs
Spins: reroll Trion or Side Effect
Triggers: buy in shop, equip in loadout, buffs applied in battle

Game Modes
Story Mode, Missions, Solo Arena, Rank Wars

Solo Arena
PvP first, PvE fallback
Cooldown: 30s
Damage uses Trion, Side Effect, Equipped Triggers
PvE: multi-neighbor waves
ELO: +25 win, -25 loss
Battle logs embedded

Loadout System
Equip up to 3 triggers
Use /loadout to view, /equip to add
Trigger buffs applied in combat

Visual Profile Cards
Embed with avatar, stats, triggers
Turquoise embed color

Story Mode
/ story to start arc
/ mission to complete tasks
Rewards: Spins, Credits, Triggers

Economy
Credits buy triggers: Grasshopper, Escudo, Spider, Bagworm, Chameleon

Commands Implemented
/joinborder, /profile, /spin, /leaderboard, /arena, /shop, /buytrigger
/loadout, /equip, /story, /mission

Next Features
- Redeem code system fully integrated with spins/credits
- Profile cards with image generation for stats & triggers
- Story mode missions fully playable with rewards
- PvE AI advanced abilities & multi-wave bosses
- Rank Wars squad PvP
