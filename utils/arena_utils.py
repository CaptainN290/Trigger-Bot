import random
from utils.elo import win_elo, lose_elo

# Simple combat calculation
def calculate_damage(trion, side_effect):
    base = trion * 10
    buff = 0

    if side_effect:
        if side_effect == "Enhanced Vision":
            buff += 5
        elif side_effect == "Enhanced Hearing":
            buff += 3
        elif side_effect == "Emotion Detection":
            buff += 4
        elif side_effect == "Future Sight":
            buff += 10
        elif side_effect == "Lie Detection":
            buff += 8
        elif side_effect == "Combat Instinct":
            buff += 9

    damage = base + random.randint(0, 10) + buff
    return damage

 # Trigger buffs
    if triggers:
        for trig in triggers:
            if trig == "Grasshopper":
                buff += 5  # Mobility bonus
            elif trig == "Escudo":
                buff += 3  # Defensive bonus
            elif trig == "Spider":
                buff += 4
            elif trig == "Bagworm":
                buff += 6  # Stealth bonus
            elif trig == "Chameleon":
                buff += 7  # Evasion bonus

    damage = base + random.randint(0,10) + buff
    return damage
