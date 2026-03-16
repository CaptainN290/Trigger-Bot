import aiosqlite

DB_NAME = "worldtrigger.db"

async def setup_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS agents(
            user_id INTEGER PRIMARY KEY,
            trion INTEGER,
            side_effect TEXT,
            spins INTEGER,
            credits INTEGER,
            elo INTEGER,
            wins INTEGER,
            losses INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS triggers(
            user_id INTEGER,
            trigger TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS codes(
            code TEXT PRIMARY KEY,
            reward INTEGER
        )
        """)

        await db.commit()
