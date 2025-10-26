"""
This file stores all items that can be carried, used and equipped by the player.
"""

weapon_default = {
    "id": "default",
    "name": "Bare Hands",
    "type": "weapon",
    "description": "default weapon",
    "damage": 10,
}

armour_default = {

    "id": "default",
    "name": "t-shirt",
    "type": "armour",
    "description": "default armour",
    "defence": 5,
}

accessory_default = {

    "id": "default",
    "name": "rusty ring",
    "type": "armour",
    "description": "default accessory",
    "buff": None,
    "buff_desc": "N/A",
}

weapon_dev = {
    "id": "wdev",
    "name": "dev weapon",
    "type": "weapon",
    "description": "dev weapon",
    "damage": 75,
}

armour_dev = {
    "id": "adev",
    "name": "dev armour",
    "type": "armour",
    "description": "dev armour",
    "defence": 50,
}

accessory_horn = {
    "id": "horn",
    "name": "Bull Horn",
    "type": "accessory",
    "description": """A fine ivory horn from a male bull, famous for its antique value as a hunter's trophy and a collector's item.
This accessory will increase the damage multiplier of your charge attacks to 3x from the 2.5x base multiplier.""",
    "buff": 3,
    "buff_desc": "Player charge Attacks will deal 3x more normal damage instead of 2.5x more normal damage.",
}

accessory_feather = {
    "id": "feather",
    "name": "Goose Feather",
    "type": "accessory",
    "description": """A soft delicate feather taken from the wing of a Canadian Goose, an animal infamous for its aggression and persistence.
This accessory will increase the damage multiplier of your counter attacks to 2.5x from the 2x base multiplier.""",
    "buff": 2.5,
    "buff_desc": "Successful player counter attacks will deal 2.5x more normal damage instead of 2x more normal damage.",
}

accessory_paw = {
    "id": "paw",
    "name": "Leopard Paw",
    "type": "accessory",
    "description": """A furry yet lightweight paw taken from a leg of a nimble snow leopard.
This accessory will add +10 to your evasion stat.""",
    "buff": 25,
    "buff_desc": "Player evasion stat is increased by 25.",
}

accessory_hide = {
    "id": "hide",
    "name": "Rhino Hide",
    "type": "accessory",
    "description": """A tough and priceless hide from the body of a black rhinoceros.
This accessory will add +10 to your defence stat.""",
    "buff": 10,
    "buff_desc": "Player defence stat is increased by 10.",
}

item_city_key_1 = {
    "id": "key1",
    "name": "Gate Key Part 1",
    "type": "item",
    "description": """A part from a broken key. Seems like this used to be the bow of the key.""",
}

item_city_key_2 = {
    "id": "key2",
    "name": "Gate Key Part 2",
    "type": "item",
    "description": """A part from a broken key. Seems like this used to be the blade of the key.""",
}

item_forest_trophy = {
    "id": "foresttrophy",
    "name": "Forest Trophy",
    "type": "item",
    "description": """A shining trophy, decorated with a wreath of tree back and moss.
This item is only obtainable by killing the rare and elusive Forest Giant.""",
}

item_tundra_trophy = {
    "id": "tundratrophy",
    "name": "Tundra Trophy",
    "type": "item",
    "description": """A shining trophy, decorated with a wreath of snow and mistletoe.
This item is only obtainable by killing the rare and elusive Tundra Werewolf.""",
}

item_plains_trophy = {
    "id": "plainstrophy",
    "name": "Plains Trophy",
    "type": "item",
    "description": """A shining trophy, decorated with a wreath of wheat and sunflowers.
This item is only obtainable by killing the rare and elusive Plains Python.""",
}

temple_sword = {
    "id": "templesword",
    "name": "Temple Sword",
    "type": "item",
    "description": """temple sword""",
}