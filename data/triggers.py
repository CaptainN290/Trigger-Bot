# data/triggers.py
# Centralized trigger definitions for shop, loadout, arena, and stats.

TRIGGERS = {
    # Main Triggers
    "Grasshopper": {"price": 50, "trion_cost": 1, "type": "main", "buffs": {"mobility": 2}},
    "Escudo": {"price": 40, "trion_cost": 2, "type": "main", "buffs": {"defense": 3}},
    "Trion Cannon": {"price": 150, "trion_cost": 5, "type": "main", "buffs": {"attack": 5, "trion_control": 2}},
    "Escalator": {"price": 90, "trion_cost": 2, "type": "main", "buffs": {"attack": 3, "mobility": 2}},

    # Sub Triggers
    "Spider": {"price": 60, "trion_cost": 1, "type": "sub", "buffs": {"attack": 2}},
    "Bagworm": {"price": 70, "trion_cost": 2, "type": "sub", "buffs": {"mobility": 1, "attack": 1}},
    "Homing Missile": {"price": 80, "trion_cost": 2, "type": "sub", "buffs": {"attack": 3}},
    "Spider Bite": {"price": 100, "trion_cost": 3, "type": "sub", "buffs": {"attack": 4}},

    # Optional Triggers
    "Chameleon": {"price": 80, "trion_cost": 1, "type": "optional", "buffs": {"evasion": 3}},
    "Shadow Cloak": {"price": 120, "trion_cost": 2, "type": "optional", "buffs": {"evasion": 5}},
    "Silent Step": {"price": 90, "trion_cost": 1, "type": "optional", "buffs": {"mobility": 3, "evasion": 2}},
    "Wallbreaker": {"price": 70, "trion_cost": 1, "type": "optional", "buffs": {"attack": 2}},

    # Canon triggers from World Trigger anime
    "Bagworm Trap": {"price": 100, "trion_cost": 2, "type": "sub", "buffs": {"mobility": 2, "attack": 1}},
    "Spinner": {"price": 90, "trion_cost": 1, "type": "sub", "buffs": {"attack": 2}},
    "Lava Trigger": {"price": 120, "trion_cost": 3, "type": "main", "buffs": {"attack": 5, "defense": 2}},
    "Sniper Shot": {"price": 80, "trion_cost": 2, "type": "sub", "buffs": {"attack": 3}},
    "Shield": {"price": 60, "trion_cost": 1, "type": "optional", "buffs": {"defense": 3}},
    "Gunner": {"price": 70, "trion_cost": 1, "type": "main", "buffs": {"attack": 4}},
    "Bagworm Stealth": {"price": 75, "trion_cost": 1, "type": "optional", "buffs": {"mobility": 2, "evasion": 1}},
}
