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
