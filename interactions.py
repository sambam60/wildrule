"""
This file stores all objects/NPCs that can be interacted with using the INTERACT command.
"""

npc_dungeonkeeper = {

    "id": "keeper",
    "name": "Dungeon Keeper",
    "description": "The keeper of the kingdom dungeon, in charge with making sure nothing enters, and escapes from the dungeon.",
    "state": 0,
}

npc_guard = {

    "id": "guard",
    "name": "City Guard",
    "description": "A common kingdom city guard, wearing dainty knight armour. He looks flustered.",
    "state": 0,
}

npc_merchant = {

    "id": "shop",
    "name": "", # name will be set based on which village the player is currently in
    "description": "", # description will be set based on which village the player is currently in
    "state": 0,
    "inventory": [], # items on sale will be set based on which village the player is currently in
}

# "A rather posh looking villager, standing in front of a quaint market stand. He smiles at whoever happens to walk past his stand.",
# "A bulky looking villager, wearing a thick fur snow jacket. He looks at you and signals towards his igloo."