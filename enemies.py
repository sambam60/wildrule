"""
This file stores all enemies in the game, including bosses.
Health corresponds to the enemy's health.
Defence corresponds to the maximum amount of damage the player can absorb in %. Minimum 0, maximum 50.
Evasion corresponds to the %chance of the enemy dodging the player's attack. Minimum 0, maximum 80.
Status corresponds to the enemy's current state.
Attacks corresponds to a list of attacks the enemy can do.
Loot corresponds to a list of items the enemy can drop when killed. Enemies should only drop 1 item at a time.
"""

from items import *

# FOREST ENEMIES

enemy_goose = {

    "id": "goose",
    "name": "Angry Goose",
    "area": "Forest",

    "description": """A wild Canadian Goose, infamous for its reckless aggression onto any innocent bystander that stands in its way.""",

    "health": 50,
    "max_health": 50, # This attribute is used when respawning enemies
    "defence": 5,
    "evasion": 20,
    
    "normal_attack": { "damage": 15, },
    "charge_attack": { "damage": 0, "chance": 0, "charge": False, "miss_multiplier": 0, },
    "counter_attack": { "damage": 25, "chance": 30, },

    "gold": 30,
    "loot": { "item": accessory_feather, "chance": 15, }
}

enemy_bear = {

    "id": "bear",
    "name": "Brown Bear",
    "area": "Forest",

    "description": """The famous forest brown bear. It's sharp claws and signature shape sends fear down any average hunter who comes across it.""",

    "health": 80,
    "max_health": 80, # This attribute is used when respawning enemies
    "defence": 15,
    "evasion": 10,
    
    "normal_attack": { "damage": 20, },
    "charge_attack": { "damage": 0, "chance": 0, "charge": False, "miss_multiplier": 0, },
    "counter_attack": { "damage": 0, "chance": 0, },

    "gold": 30,
    "loot": { "item": None, "chance": 0, }
}

enemy_bull = {

    "id": "bull",
    "name": "Horned Bull",
    "area": "Forest",

    "description": """A crazy male bull, known for its lethal and violent charges. It's large horns protrude high in the air.""",

    "health": 100,
    "max_health": 100, # This attribute is used when respawning enemies
    "defence": 20,
    "evasion": 0,
    
    "normal_attack": { "damage": 0, },
    "charge_attack": { "damage": 40, "chance": 100, "charge": False, "miss_multiplier": 3, },
    "counter_attack": { "damage": 0, "chance": 0, },

    "gold": 30,
    "loot": { "item": accessory_horn, "chance": 15, }
}

miniboss_giant = {

    "id": "giant",
    "name": "Forest Giant",
    "area": "Forest",

    "description": """A rare and elusive monster, the infamous Forest Giant towers over the tall trees of the surrounding woodland.
    Only the strongest of heroes can vanquish this beast.""",

    "health": 300,
    "max_health": 300, # This attribute is used when respawning enemies
    "defence": 50,
    "evasion": 0,
    
    "normal_attack": { "damage": 20, },
    "charge_attack": { "damage": 40, "chance": 20, "charge": False, "miss_multiplier": 2, },
    "counter_attack": { "damage": 30, "chance": 10, },

    "gold": 500,
    "loot": { "item": item_forest_trophy, "chance": 100, }
}

# TUNDRA ENEMIES

enemy_polarbear = {

    "id": "bear",
    "name": "Polar Bear",
    "area": "Tundra",

    "description": """The famous arctic polar bear. It's razor-sharp claws paired with its camouflaging white fur makes this beast a signature of the region.""",

    "health": 120,
    "max_health": 120, # This attribute is used when respawning enemies
    "defence": 20,
    "evasion": 10,
    
    "normal_attack": { "damage": 35, },
    "charge_attack": { "damage": 0, "chance": 0, "charge": False, "miss_multiplier": 0, },
    "counter_attack": { "damage": 40, "chance": 20, },

    "gold": 65,
    "loot": { "item": None, "chance": 0, }
}

enemy_leopard = {

    "id": "leopard",
    "name": "Snow Leopard",
    "area": "Tundra",

    "description": """A spotted mountain snow leopard. Strong and nimble, this feline uses its unmatched speed to outsmart its prey.""",

    "health": 120,
    "max_health": 120, # This attribute is used when respawning enemies
    "defence": 15,
    "evasion": 30,
    
    "normal_attack": { "damage": 30, },
    "charge_attack": { "damage": 45, "chance": 10, "charge": False, "miss_multiplier": 1.5, },
    "counter_attack": { "damage": 35, "chance": 30, },

    "gold": 65,
    "loot": { "item": accessory_paw, "chance": 15, }
}

enemy_owl = {

    "id": "owl",
    "name": "Snowy Owl",
    "area": "Tundra",

    "description": """A white-feathered snowy owl. Silent and precise, this bird of prey prides itself in its stealth and evasion.""",

    "health": 100,
    "max_health": 100, # This attribute is used when respawning enemies
    "defence": 10,
    "evasion": 50,
    
    "normal_attack": { "damage": 25, },
    "charge_attack": { "damage": 30, "chance": 30, "charge": False, "miss_multiplier": 1, },
    "counter_attack": { "damage": 35, "chance": 15, },

    "gold": 65,
    "loot": { "item": None, "chance": 0, }
}

miniboss_werewolf = {

    "id": "werewolf",
    "name": "Tundra Werewolf",
    "area": "Tundra",

    "description": """A rare and elusive monster, the infamous Tundra Werewolf is the apex predator it's frigid environment.
Only the strongest of heroes can vanquish this beast.""",

    "health": 300,
    "max_health": 300, # This attribute is used when respawning enemies
    "defence": 30,
    "evasion": 25,
    
    "normal_attack": { "damage": 35, },
    "charge_attack": { "damage": 50, "chance": 40, "charge": False, "miss_multiplier": 1.5, },
    "counter_attack": { "damage": 40, "chance": 10, },

    "gold": 500,
    "loot": { "item": item_tundra_trophy, "chance": 100, }
}

# PLAINS ENEMIES

enemy_fox = {

    "id": "fox",
    "name": "Fennec Fox",
    "area": "Plains",

    "description": """A relatively small fox, with large pointy ears. It's small body and heightened senses allow for it to safely avoid almost all danger it comes across.""",

    "health": 100,
    "max_health": 100, # This attribute is used when respawning enemies
    "defence": 15,
    "evasion": 50,
    
    "normal_attack": { "damage": 30, },
    "charge_attack": { "damage": 0, "chance": 0, "charge": False, "miss_multiplier": 0, },
    "counter_attack": { "damage": 40, "chance": 30, },

    "gold": 50,
    "loot": { "item": None, "chance": 0, }
}

enemy_rhino = {

    "id": "rhino",
    "name": "Black Rhinoceros",
    "area": "Plains",

    "description": """The famous but endangered rhino. It's bulky body and tough horn make for a formidable foe.""",

    "health": 150,
    "max_health": 150, # This attribute is used when respawning enemies
    "defence": 40,
    "evasion": 5,
    
    "normal_attack": { "damage": 0, },
    "charge_attack": { "damage": 60, "chance": 50, "charge": False, "miss_multiplier": 2, },
    "counter_attack": { "damage": 40, "chance": 50, },

    "gold": 50,
    "loot": { "item": accessory_hide, "chance": 25, }
}

enemy_elephant = {

    "id": "elephant",
    "name": "Bush Elephant",
    "area": "Plains",

    "description": """The large and famous elephant. It is deceptively fast despite it's large size.""",

    "health": 150,
    "max_health": 150, # This attribute is used when respawning enemies
    "defence": 30,
    "evasion": 20,
    
    "normal_attack": { "damage": 35, },
    "charge_attack": { "damage": 50, "chance": 30, "charge": False, "miss_multiplier": 2, },
    "counter_attack": { "damage": 30, "chance": 30, },

    "gold": 50,
    "loot": { "item": None, "chance": 0, }
}

miniboss_python = {

    "id": "python",
    "name": "Plains Python",
    "area": "Plains",

    "description": """A rare and elusive monster, the infamous Plains Python is a silent but deadly killer, hidden amongst the bare foliage.
Only the strongest of heroes can vanquish this beast.""",

    "health": 300,
    "max_health": 300, # This attribute is used when respawning enemies
    "defence": 20,
    "evasion": 65,
    
    "normal_attack": { "damage": 30, },
    "charge_attack": { "damage": 40, "chance": 10, "charge": False, "miss_multiplier": 1.5, },
    "counter_attack": { "damage": 50, "chance": 40, },

    "gold": 500,
    "loot": { "item": item_plains_trophy, "chance": 100, }
}

# DUNGEON ENEMIES

skeleton_king = {

    "id": "king",
    "name": "The Skeleton King",
    "area": "Dungeon",

    "description": """A rare and elusive monster, the infamous Plains Python is a silent but deadly killer, hidden amongst the bare foliage.
Only the strongest of heroes can vanquish this beast.""",

    "health": 500,
    "max_health": 500, # This attribute is used when respawning enemies
    "defence": 50,
    "evasion": 10,
    
    "normal_attack": { "damage": 50, },
    "charge_attack": { "damage": 80, "chance": 20, "charge": False, "miss_multiplier": 2, },
    "counter_attack": { "damage": 65, "chance": 30, },

    "gold": 9999,
    "loot": { "item": temple_sword, "chance": 100, }
}