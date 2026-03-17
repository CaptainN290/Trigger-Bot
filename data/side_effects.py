import random

# Common side effects (60% chance)
COMMON = [
    {"name": "Enhanced Vision", "buffs": {"perception": 1}},
    {"name": "Enhanced Hearing", "buffs": {"perception": 1}},
    {"name": "Emotion Detection", "buffs": {"intelligence": 1}},
    {"name": "Quick Reflexes", "buffs": {"mobility": 1}},
    {"name": "Adaptive Thinking", "buffs": {"intelligence": 1}},
]

# Rare side effects (40% chance of triggering a rare roll)
RARE = [
    {"name": "Future Sight", "buffs": {"attack": 2, "intelligence": 2}},
    {"name": "Lie Detection", "buffs": {"intelligence": 2, "perception": 2}},
    {"name": "Combat Instinct", "buffs": {"attack": 2, "mobility": 1}},
    {"name": "Trion Efficiency", "buffs": {"trion_control": 2}},
    {"name": "Sniper Precision", "buffs": {"attack": 2, "perception": 1}},
    {"name": "Battle Foresight", "buffs": {"intelligence": 2, "mobility": 1}},
    {"name": "Enhanced Agility", "buffs": {"mobility": 2}},
]

def roll_side_effect():
    """
    Rolls a side effect for a new agent.
    60% chance to get a side effect.
    Returns a dict with name and buffs.
    """
    if random.random() <= 0.6:
        roll = random.random()
        if roll <= 0.85:
            return random.choice(COMMON)
        else:
            return random.choice(RARE)
    return None
