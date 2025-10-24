"""
This file stores all enemies in the game, including bosses.
Health corresponds to the enemy's health.
Defence corresponds to the how much damage it can absorb per attack in %. Minimum 0, maximum 50.
Evasion corresponds to the %chance of the enemy dodging the player's attack. Minimum 0, maximum 80.
Status corresponds to the enemy's current state.
Attacks corresponds to a list of attacks the enemy can do.
Loot corresponds to a list of items the enemy can drop when killed. Enemies should only drop 1 item at a time.
"""

enemy_test = {
    "id": "test",

    "name": "test enemy",

    "description": "placeholder",

    "health": 100,
    "defence": 10,
    "evasion": 0,
    "status": "idle",

    "attacks": [],

    "loot": []

    # we can add more attributes if needed
}