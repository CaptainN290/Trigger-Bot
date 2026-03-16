import random

COMMON = [
"Enhanced Vision",
"Enhanced Hearing",
"Emotion Detection"
]

RARE = [
"Future Sight",
"Lie Detection",
"Combat Instinct"
]

def roll_side_effect():

    if random.random() <= 0.6:

        roll = random.random()

        if roll <= 0.85:
            return random.choice(COMMON)

        else:
            return random.choice(RARE)

    return None
