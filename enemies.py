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

enemy_goose = {

    "id": "goose",
    "name": "Angry Goose",
    "area": "Forest",

    "description": "placeholder",

    "health": 50,
    "max_health": 50, # This attribute is used when respawning enemies
    "defence": 10,
    "evasion": 20,
    
    "normal_attack": { "damage": 15, },
    "charge_attack": { "damage": 0, "chance": 0, "charge": False, "miss_multiplier": 0, },
    "counter_attack": { "damage": 25, "chance": 30, },

    "gold": 30,
    "loot": { "item": None, "chance": 0, }

    # we can add more attributes if needed
}

enemy_bear = {

    "id": "bear",
    "name": "Brown Bear",
    "area": "Forest",

    "description": "placeholder",

    "health": 80,
    "max_health": 80, # This attribute is used when respawning enemies
    "defence": 30,
    "evasion": 20,
    
    "normal_attack": { "damage": 25, },
    "charge_attack": { "damage": 0, "chance": 0, "charge": False, "miss_multiplier": 0, },
    "counter_attack": { "damage": 0, "chance": 0, },

    "gold": 50,
    "loot": { "item": None, "chance": 0, }

    # we can add more attributes if needed
}

enemy_bull = {

    "id": "bull",
    "name": "Horned Bull",
    "area": "Forest",

    "description": "placeholder",

    "health": 100,
    "max_health": 100, # This attribute is used when respawning enemies
    "defence": 20,
    "evasion": 0,
    
    "normal_attack": { "damage": 0, },
    "charge_attack": { "damage": 50, "chance": 100, "charge": False, "miss_multiplier": 3, },
    "counter_attack": { "damage": 0, "chance": 0, },

    "gold": 70,
    "loot": { "item": accessory_ivory, "chance": 15, }

    # we can add more attributes if needed
}