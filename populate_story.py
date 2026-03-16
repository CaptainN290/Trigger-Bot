import aiosqlite
import asyncio
import json
from database import DB_NAME

async def populate_story():
    async with aiosqlite.connect(DB_NAME) as db:

        # --- PROLOGUE ARC ---
        arc = "Prologue"

        missions = [
            {
                "chapter": 1,
                "mission": 1,
                "type": "exploration",
                "description": "You arrive at Mikado City for your first Border assignment. Explore the area to understand your surroundings.",
                "choices": None,
                "reward_type": "credits",
                "reward_amount": 50,
                "reward_trigger": None,
                "replayable": 1
            },
            {
                "chapter": 1,
                "mission": 2,
                "type": "choice",
                "description": "You hear a suspicious signal. Do you investigate carefully or rush in?",
                "choices": json.dumps([
                    {"id": "investigate", "label": "Investigate Carefully"},
                    {"id": "rush", "label": "Rush In"}
                ]),
                "reward_type": "spins",
                "reward_amount": 2,
                "reward_trigger": None,
                "replayable": 0
            },
            {
                "chapter": 1,
                "mission": 3,
                "type": "arena",
                "description": "Neighbors are attacking civilians nearby. Engage them in the arena!",
                "choices": None,
                "reward_type": "credits",
                "reward_amount": 100,
                "reward_trigger": None,
                "replayable": 1
            },
            {
                "chapter": 2,
                "mission": 1,
                "type": "exploration",
                "description": "You investigate a suspicious warehouse. Look for clues and gather intel.",
                "choices": None,
                "reward_type": "credits",
                "reward_amount": 75,
                "reward_trigger": None,
                "replayable": 1
            },
            {
                "chapter": 2,
                "mission": 2,
                "type": "choice",
                "description": "A civilian asks for help. Will you escort them to safety or continue your investigation?",
                "choices": json.dumps([
                    {"id": "escort", "label": "Escort Civilian"},
                    {"id": "investigate", "label": "Continue Investigation"}
                ]),
                "reward_type": "spins",
                "reward_amount": 3,
                "reward_trigger": None,
                "replayable": 0
            },
            {
                "chapter": 2,
                "mission": 3,
                "type": "arena",
                "description": "A small group of Neighbors attacks! Defend the civilians!",
                "choices": None,
                "reward_type": "credits",
                "reward_amount": 150,
                "reward_trigger": None,
                "replayable": 1
            },
            # --- Boss Mission ---
            {
                "chapter": 3,
                "mission": 1,
                "type": "boss",
                "description": "The main Neighbor threat appears in Mikado City. Prepare for a boss battle!",
                "choices": None,
                "reward_type": "trigger",
                "reward_amount": 1,
                "reward_trigger": "Grasshopper",
                "replayable": 0
            }
        ]

        # Insert missions into DB
        for m in missions:
            await db.execute("""
                INSERT OR REPLACE INTO story_missions
                (arc, chapter, mission, type, description, choices, reward_type, reward_amount, reward_trigger, replayable)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                arc,
                m["chapter"],
                m["mission"],
                m["type"],
                m["description"],
                m["choices"],
                m["reward_type"],
                m["reward_amount"],
                m["reward_trigger"],
                m["replayable"]
            ))

        await db.commit()
        print("✅ Story missions populated successfully!")

asyncio.run(populate_story())
