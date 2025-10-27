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
    "name": "Shop Merchant", # name will be set based on which village the player is currently in
    "description": "A shop merchant, wearing a feather hat and a fleece jacket. He is standing in front of a small market stand.", # description will be set based on which village the player is currently in
    "state": 0,
    "inventory": [], # items on sale will be set based on which village the player is currently in
}

obj_chest1 = {

    "id": "chest",
    "name": "Locked Chest",
    "description": "A locked chest, perhaps containing a valuable item.",
    "state": 0,
}

obj_chest2 = {

    "id": "chest",
    "name": "Locked Chest",
    "description": "A locked chest, perhaps containing a valuable item.",
    "state": 0,
}

obj_chest3 = {

    "id": "chest",
    "name": "Locked Chest",
    "description": "A locked chest, perhaps containing a valuable item.",
    "state": 0,
}

obj_mantle = {
    "id": "mantle",
    "name": "Sword Mantle",
    "description": "A mantle that was once used to display the Temple Sword, which has been lost in the dungeon.",
    "state": False,
}