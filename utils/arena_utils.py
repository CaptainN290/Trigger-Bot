import random
from utils.elo import win_elo, lose_elo
from data.triggers import TRIGGERS

async def calculate_damage(user_id, trion, side_effect=None, triggers=None, stats=None):
    """
    Calculates damage in arena battles.
    - trion: Agent's Trion level
    - side_effect: dict from roll_side_effect (name + buffs)
    - triggers: list of equipped triggers (main, sub, optional)
    - stats: agent's stat points dictionary
    """
    if stats is None:
        stats = {
            "attack": 1,
            "defense": 1,
            "mobility": 1,
            "intelligence": 1,
            "trion_control": 1,
            "perception": 1
        }

    base = trion * 10  # Base damage scales with Trion
    buff = 0
    remaining_trion = trion  # Track Trion consumption for triggers

    # --- Apply Side Effect Buffs ---
    if side_effect:
        for stat, value in side_effect.get("buffs", {}).items():
            if stat == "attack":
                buff += value * 5
            elif stat == "mobility":
                buff += value * 2
            elif stat == "perception":
                buff += value * 2
            elif stat == "intelligence":
                buff += value * 3
            elif stat == "trion_control":
                buff += value * 4
            elif stat == "defense":
                buff += value
            elif stat == "evasion":
                buff += value * 1

    # --- Apply Trigger Buffs & Consume Trion ---
    if triggers:
        for trig_name in triggers:
            trig = TRIGGERS.get(trig_name)
            if not trig:
                continue
            cost = trig.get("trion_cost", 0)
            if remaining_trion >= cost:
                remaining_trion -= cost
                for stat, value in trig.get("buffs", {}).items():
                    if stat == "attack":
                        buff += value * 5  # Attack potency applies to all attacks
                    elif stat == "mobility":
                        buff += value * 2
                    elif stat == "defense":
                        buff += value * 3
                    elif stat == "evasion":
                        buff += value * 1
                    elif stat == "intelligence":
                        buff += value * 3
                    elif stat == "trion_control":
                        buff += value * 4
                    elif stat == "perception":
                        buff += value * 2

# Get mastery level
cursor = await db.execute(
    "SELECT level FROM trigger_mastery WHERE user_id=? AND trigger=?",
    (user_id, trig_name)
)
result = await cursor.fetchone()
level = result[0] if result else 1

buff += level * 2
    
    # --- Apply Raw Stats ---
    buff += stats.get("attack", 1) * 5
    buff += stats.get("mobility", 1) * 2
    buff += stats.get("intelligence", 1) * 3
    buff += stats.get("trion_control", 1) * 4
    buff += stats.get("perception", 1) * 2
    buff += stats.get("defense", 1) * 1

    # --- Random variance ---
    damage = base + buff + random.randint(0, 10)
    return damage

# --- ELO adjustments ---
def win_elo(current_elo):
    return current_elo + 25

def lose_elo(current_elo):
    return max(current_elo - 25, 0)
