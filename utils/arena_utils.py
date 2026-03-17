import random
from utils.elo import win_elo, lose_elo

# Example stat points dict structure:
# stats = {
#   "attack": 3,
#   "defense": 2,
#   "mobility": 2,
#   "intelligence": 1,
#   "trion_control": 2,
#   "perception": 1
# }

# Triggers buff dictionary
TRIGGER_BUFFS = {
    "Grasshopper": {"mobility": 2},
    "Escudo": {"defense": 3},
    "Spider": {"attack": 2},
    "Bagworm": {"mobility": 1, "attack": 1},
    "Chameleon": {"evasion": 3}  # e.g., could reduce damage taken
}

# Side effects buff example (already integrated in side_effects.py)
# side_effect = {"name": "Combat Instinct", "buffs": {"attack": 2, "mobility": 1}}

def calculate_damage(trion: int, side_effect: dict = None, triggers: list = None, stats: dict = None):
    """
    Calculates damage in arena battles.
    - trion: agent's Trion level
    - side_effect: dict from roll_side_effect (name + buffs)
    - triggers: list of equipped triggers
    - stats: agent stats dict
    """
    if stats is None:
        stats = {"attack": 1, "defense": 1, "mobility": 1, "intelligence": 1, "trion_control": 1, "perception": 1}

    base = trion * 10  # Base damage scales with Trion
    buff = 0

    # Apply side effect buffs
    if side_effect:
        for stat, value in side_effect.get("buffs", {}).items():
            if stat == "attack":
                buff += value * 5  # Each attack point adds 5 damage
            elif stat == "mobility":
                buff += value * 2  # Mobility slightly increases damage
            elif stat == "perception":
                buff += value * 2  # Better accuracy
            elif stat == "intelligence":
                buff += value * 3  # Smarter attacks
            elif stat == "trion_control":
                buff += value * 4  # Better Trion efficiency
            elif stat == "defense":
                buff += value  # Minor bonus
            elif stat == "evasion":
                buff += value * 1  # Minor bonus

    # Apply trigger buffs
    if triggers:
        for trig in triggers:
            trig_buff = TRIGGER_BUFFS.get(trig, {})
            for stat, value in trig_buff.items():
                if stat == "attack":
                    buff += value * 5
                elif stat == "mobility":
                    buff += value * 2
                elif stat == "defense":
                    buff += value * 3
                elif stat == "evasion":
                    buff += value * 1

    # Apply raw stats
    buff += stats.get("attack", 1) * 5
    buff += stats.get("mobility", 1) * 2
    buff += stats.get("intelligence", 1) * 3
    buff += stats.get("trion_control", 1) * 4
    buff += stats.get("perception", 1) * 2
    buff += stats.get("defense", 1) * 1

    # Add small randomness
    damage = base + buff + random.randint(0, 10)
    return damage

# Example ELO adjustment (unchanged)
def win_elo(current_elo):
    return current_elo + 25

def lose_elo(current_elo):
    return max(current_elo - 25, 0)
