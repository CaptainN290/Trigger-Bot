import random

def win_elo(current):
    """
    Increase ELO by a random amount between +15 and +30 on a win.
    """
    return current + random.randint(15, 30)

def lose_elo(current):
    """
    Decrease ELO by a random amount between -15 and -30 on a loss, but not below 0.
    """
    return max(current - random.randint(15, 30), 0)
