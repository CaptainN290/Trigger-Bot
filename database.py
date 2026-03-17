import aiosqlite
from populate_story import populate_story
DB_NAME = "world_trigger.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        # Agents table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            user_id INTEGER PRIMARY KEY,
            trion INTEGER DEFAULT 2,
            side_effect TEXT,
            spins INTEGER DEFAULT 0,
            credits INTEGER DEFAULT 0,
            elo INTEGER DEFAULT 1000,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
        """)

        # Triggers table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS triggers (
            user_id INTEGER,
            trigger TEXT,
            PRIMARY KEY (user_id, trigger)
        )
        """)

        # Loadouts table (equipped triggers)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS loadouts (
            user_id INTEGER,
            trigger TEXT,
            PRIMARY KEY (user_id, trigger)
        )
        """)

        # Redeem codes
        await db.execute("""
        CREATE TABLE IF NOT EXISTS redeem_codes (
            code TEXT PRIMARY KEY,
            reward_type TEXT,
            reward_amount INTEGER,
            reward_trigger TEXT,
            max_uses INTEGER,
            expires TIMESTAMP
        )
        """)

        # Redeemed table (track which user claimed which code)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS redeemed (
            user_id INTEGER,
            code TEXT,
            PRIMARY KEY (user_id, code)
        )
        """)

        # Story Progress
        await db.execute("""
        CREATE TABLE IF NOT EXISTS story_progress (
            user_id INTEGER PRIMARY KEY,
            arc TEXT DEFAULT 'Prologue',
            chapter INTEGER DEFAULT 1,
            mission INTEGER DEFAULT 1
        )
        """)

        # Story Missions
        await db.execute("""
        CREATE TABLE IF NOT EXISTS story_missions (
            arc TEXT,
            chapter INTEGER,
            mission INTEGER,
            type TEXT,  -- 'arena', 'choice', 'exploration', 'boss'
            description TEXT,
            choices TEXT, -- JSON encoded choices
            reward_type TEXT,  -- 'credits', 'spins', 'trigger'
            reward_amount INTEGER,
            reward_trigger TEXT,
            replayable INTEGER DEFAULT 0,
            PRIMARY KEY (arc, chapter, mission)
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS agent_stats (
            user_id INTEGER PRIMARY KEY,
            attack INTEGER DEFAULT 1,
            defense INTEGER DEFAULT 1,    
            mobility INTEGER DEFAULT 1,
            intelligence INTEGER DEFAULT 1,
            trion_control INTEGER DEFAULT 1,
            perception INTEGER DEFAULT 1,
            stat_points INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS squads (
            squad_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            leader_id INTEGER,
            division TEXT DEFAULT 'C-Rank',
            elo INTEGER DEFAULT 1000
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS squad_members (
            squad_id INTEGER,
            user_id INTEGER,
            role TEXT
        )
        """)
        
        await db.commit()

cursor = await db.execute("SELECT COUNT(*) FROM story_missions")
count = await cursor.fetchone()

if count[0] == 0:
    await populate_story()

import aiosqlite
from populate_story import populate_story  # import the script as a function

DB_NAME = "world_trigger.db"

async def setup_database(bot):
    async with aiosqlite.connect(DB_NAME) as db:
        # Create all tables (agents, story, triggers, etc.)
        await init_db()

        # Populate story missions if empty
        cursor = await db.execute("SELECT COUNT(*) FROM story_missions")
        count = await cursor.fetchone()
        if count[0] == 0:
            await populate_story(db)  # now everything is on server

# Call this when the bot starts
async def setup_database(bot):
    await init_db()
