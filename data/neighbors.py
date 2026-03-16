# Canon Neighbor Types for PvE Arena
NEIGHBORS = {
    "Bamster": {"hp":120,"damage":10},
    "Marmod": {"hp":80,"damage":18},
    "Rabbit": {"hp":200,"damage":25},
    "Ilgar": {"hp":150,"damage":20},
    "Bander": {"hp":110,"damage":16},
    "Rad": {"hp":30,"damage":5},
    "Dog": {"hp":60,"damage":12},
    "Idra": {"hp":90,"damage":15}
}

# For AI PvE, randomly pick a neighbor
def random_neighbor():
    import random
    name = random.choice(list(NEIGHBORS.keys()))
    stats = NEIGHBORS[name]
    return name, stats["hp"], stats["damage"]
