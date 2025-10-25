"""
This file stores all items that can be carried, used and equipped by the player.
"""

item_test1 = {
    "id": "1",
    "name": "test1",
    "type": "item",
    "description": "test",
}

weapon_default = {
    "id": "default",
    "name": "bare hands",
    "type": "weapon",
    "description": "default weapon",
    "damage": 10,
}

armour_default = {

    "id": "default",
    "name": "t-shirt",
    "type": "armour",
    "description": "default armour",
    "defence": 10,
}

accessory_default = {

    "id": "default",
    "name": "rusty ring",
    "type": "armour",
    "description": "default accessory",
    "buff": None,
    "buff_desc": "N/A",
}

weapon_test2 = {
    "id": "weapon2",
    "name": "test weapon 2",
    "type": "weapon",
    "description": "test 2",
    "damage": 30,
}

armour_test2 = {
    "id": "armour2",
    "name": "test armour 2",
    "type": "armour",
    "description": "test 3",
    "defence": 30,
}

accessory_ivory = {
    "id": "ivory",
    "name": "Ivory Horn",
    "type": "accessory",
    "description": """A fine ivory horn from a male bull, famous for its antique value as a hunter's trophy and a collector's item.
This accessory will increase the damage multiplier of your charge attacks to 3x from the 2.5x base multiplier.""",
    "buff": 3,
    "buff_desc": "Player Charge Attacks will deal 3x more normal damage instead of 2.5x more normal damage.",
}