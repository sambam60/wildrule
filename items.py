"""
This file stores all items that can be carried, used and equipped by the player.
"""

weapon_default = {
    "id": "default",
    "name": "Bare Hands",
    "type": "weapon",
    "description": "default weapon",
    "price": 0,
    "damage": 10,
}

armour_default = {

    "id": "default",
    "name": "t-shirt",
    "type": "armour",
    "description": "default armour",
    "price": 0,
    "defence": 5,
}

accessory_default = {

    "id": "default",
    "name": "rusty ring",
    "type": "armour",
    "description": "default accessory",
    "price": 0,
    "buff": None,
    "buff_desc": "N/A",
}

weapon_sword = {
    "id": "sword",
    "name": "Wooden Sword",
    "type": "weapon",
    "description": "A weathered , wooden sword with nicks along the blade. Despite its appearance, it's still effective for weaker enemies.",
    "price": 0,
    "damage": 18,
}

accessory_horn = {
    "id": "horn",
    "name": "Bull Horn",
    "type": "accessory",
    "description": """A fine ivory horn from a male bull, famous for its antique value as a hunter's trophy and a collector's item.
This accessory will increase the damage multiplier of your charge attacks to 3x from the 2.5x base multiplier.""",
    "price": 0,
    "buff": 3,
    "buff_desc": "Player charge Attacks will deal 3x more normal damage instead of 2.5x more normal damage.",
}

accessory_feather = {
    "id": "feather",
    "name": "Goose Feather",
    "type": "accessory",
    "description": """A soft delicate feather taken from the wing of a Canadian Goose, an animal infamous for its aggression and persistence.
This accessory will increase the damage multiplier of your counter attacks to 3x from the 2x base multiplier.""",
    "price": 0,
    "buff": 3,
    "buff_desc": "Successful player counter attacks will deal 3x more normal damage instead of 2x more normal damage.",
}

accessory_paw = {
    "id": "paw",
    "name": "Leopard Paw",
    "type": "accessory",
    "description": """A furry yet lightweight paw taken from a leg of a nimble snow leopard.
This accessory will add +10 to your evasion stat.""",
    "price": 0,
    "buff": 25,
    "buff_desc": "Player evasion stat is increased by 25.",
}

accessory_hide = {
    "id": "hide",
    "name": "Rhino Hide",
    "type": "accessory",
    "description": """A tough and priceless hide from the body of a black rhinoceros.
This accessory will add +10 to your defence stat.""",
    "price": 0,
    "buff": 10,
    "buff_desc": "Player defence stat is increased by 10.",
}

item_chest_key = {
    "id": "key",
    "name": "Chest Key",
    "type": "item",
    "description": """A key used to unlock a locked chest.""",
    "price": 200,
}

item_city_key_1 = {
    "id": "key1",
    "name": "Gate Key Part 1",
    "type": "item",
    "description": """A part from a broken key. Seems like this used to be the bow of the key.""",
    "price": 400,
}

item_city_key_2 = {
    "id": "key2",
    "name": "Gate Key Part 2",
    "type": "item",
    "description": """A part from a broken key. Seems like this used to be the blade of the key.""",
    "price": 400,
}

item_healing_potion = {
    "id": "hp",
    "name": "Health Potion",
    "type": "item",
    "description": """A delicate potion brewed from a skilled alchemist. Bright red liquid swirls inside the flask.
This consumable item will heal 75 health to the player.""",
    "price": 75,
}

weapon_spear = {
    "id": "spear",
    "name": "Iron-Tipped Spear",
    "type": "weapon",
    "description": """A wooden spear with a sharp tip made of iron.
This weapon has a base attack of 25.""",
    "price": 200,
    "damage": 25,
}

armour_wooden_shield = {
    "id": "woodshield",
    "name": "Wooden Shield",
    "type": "armour",
    "description": """A wooden shield, with an iron-reinforced border.
This armour piece has a base defence of 15.""",
    "price": 200,
    "defence": 15,
}

accessory_badge = {
    "id": "badge",
    "name": "Hunter Badge",
    "type": "accessory",
    "description": """A leather badge, boasting the classic hunter's insignia of two crossed swords.
This accessory will add +5 to your attack stat.""",
    "price": 150,
    "buff": 5,
    "buff_desc": "Player attack stat is increased by 5.",
}

weapon_club = {
    "id": "club",
    "name": "Spiked Club",
    "type": "weapon",
    "description": """A wooden club spiked with iron nails.
This weapon has a base attack of 35.""",
    "price": 350,
    "damage": 35,
}

armour_jacket = {
    "id": "jacket",
    "name": "Snow Jacket",
    "type": "armour",
    "description": """A think snow jacket, made of fur and cotton.
This armour piece has a base defence of 25.""",
    "price": 350,
    "defence": 25,
}

weapon_longsword = {
    "id": "longsword",
    "name": "Silver Longsword",
    "type": "weapon",
    "description": """A medieval longsword made of an alloy of iron and silver.
This weapon has a base attack of 50.""",
    "price": 500,
    "damage": 50,
}

armour_chainmail = {
    "id": "chainmail",
    "name": "Chainmail Chestpiece",
    "type": "armour",
    "description": """A strong chestpiece made of iron chainmail. Famous for its use in battle by knights.
This armour piece has a base defence of 25.""",
    "price": 500,
    "defence": 50,
}

armour_iron_shield = {
    "id": "ironshield",
    "name": "Iron Shield",
    "type": "armour",
    "description": """An iron-reinforced shield.
This armour piece has a base defence of 20.""",
    "price": 250,
    "defence": 20,
}

weapon_metalclub = {
    "id": "metalclub",
    "name": "Metallic Club",
    "type": "weapon",
    "description": """A large iron-reinforced club, with sharp blades on its end.
This weapon has a base attack of 40.""",
    "price": 400,
    "damage": 40,
}

item_forest_trophy = {
    "id": "foresttrophy",
    "name": "Forest Trophy",
    "type": "item",
    "description": """A shining trophy, decorated with a wreath of tree back and moss.
This item is only obtainable by killing the rare and elusive Forest Giant.""",
    "price": 0,
}

item_tundra_trophy = {
    "id": "tundratrophy",
    "name": "Tundra Trophy",
    "type": "item",
    "description": """A shining trophy, decorated with a wreath of snow and mistletoe.
This item is only obtainable by killing the rare and elusive Tundra Werewolf.""",
    "price": 0,
}

item_plains_trophy = {
    "id": "plainstrophy",
    "name": "Plains Trophy",
    "type": "item",
    "description": """A shining trophy, decorated with a wreath of wheat and sunflowers.
This item is only obtainable by killing the rare and elusive Plains Python.""",
    "price": 0,
}

temple_sword = {
    "id": "templesword",
    "name": "Temple Sword",
    "type": "item",
    "description": """The mythical sword of Wildrule. It radiates an aura full of power and hope.
This item can only be obtainable after defeating the almighty, rare and elusive Skeleton King.""",
    "price": 0,
}