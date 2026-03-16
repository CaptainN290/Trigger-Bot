import random

def roll_trion():

    roll = random.randint(1,100)

    if roll <= 50:
        return random.randint(2,6)

    elif roll <= 85:
        return random.randint(7,12)

    elif roll <= 97:
        return random.randint(13,20)

    else:
        return random.randint(21,38)
