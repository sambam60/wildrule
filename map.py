"""
This file stores all the rooms and areas in the game.
"""

from items import *
from interactions import *
from enemies import *

# TUTORIAL ROOMS

room_starter = {

    "id": "start",
    "name": "Abandoned Shack",
    "area": "Forest",
    "explored": False,

    "description":
"""You wake up in a small abandoned shack, its wooden walls weathered by countless seasons. Dim morning light streams through the cracks in the ceiling, illuminating motes of dust dancing in the air. The single window offers a glimpse of a lush forest beyond. An old rucksack and a worn map lie on a dusty table, beckoning you forward. The door to the SOUTH leads to the adventure that awaits.""",

    "exits": {"south": "Forest_N"},

    "items": [],

    "interacts": [],

    "enemies": [],
}

# FOREST BIOME

forest_north = {

    "id": "forest_n",
    "name": "Northern Forest",
    "area": "Forest",
    "explored": False,

    "description":
"""You step into the Northern Forest, where ancient oaks tower overhead like silent guardians. The forest floor is soft with moss and fallen leaves, crunching gently beneath your feet. Sunlight filters through the canopy in golden shafts, illuminating patches of wildflowers. The air is fresh and alive with the sounds of birdsong. You can venture EAST toward the northeast corner, SOUTH deeper into the forest, or WEST to the northwest paths.""",

    "exits": {
        "north": "Stater",
        "south": "Forest_S",
        "east": "Forest_NE",
        "west": "Forest_NW",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

forest_northeast = {

    "id": "forest_ne",
    "name": "Northeastern Forest",
    "area": "Forest",
    "explored": False,

    "description":
"""You've reached the forest's northeastern corner where the trees begin to thin. A babbling brook cuts through the landscape, its clear water glistening in the filtered light. Strange ice crystals can be seen forming on nearby leaves—a sign of the frigid tundra to the EAST. You can travel SOUTH through the forest, WEST back to the heart of the woods, or venture EAST toward the harsh Icy Tundra.""",

    "exits": {
        "south": "Forest_SE",
        "east": "Tundra_N",
        "west": "Forest_N",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}


forest_northwest = {

    "id": "forest_nw",
    "name": "Northwestern Forest",
    "area": "Forest",
    "explored": False,

    "description":
"""You stand at the forest's northwestern corner where the trees grow sparse and tall. The undergrowth is thicker here, filled with thorny brambles and wild berry bushes. A gentle breeze carries the scent of pine and the distant sounds of open grassland to the WEST. You can head SOUTH toward the southwest corner, EAST back into the forest, or WEST onto the open Plains.""",

    "exits": {
        "south": "Forest_SW",
        "east": "Forest_N",
        "west": "Plains_NW",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}


forest_south = {

    "id": "forest_s",
    "name": "Southern Forest",
    "area": "Forest",
    "explored": False,

    "description":
"""You find yourself in the southern reaches of the forest, where the canopy opens to reveal a clear blue sky. The terrain slopes gently, and you can make out rolling grasslands beyond the treeline to the SOUTH. Ancient ferns and towering bracken line the path, creating a natural corridor. You can navigate NORTH deeper into the forest, EAST or WEST to explore the corners, or SOUTH to emerge into the Plains.""",

    "exits": {
        "north": "Forest_N",
        "south": "Plains_SE",
        "east": "Forest_SE",
        "west": "Forest_SW",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}


forest_southeast = {

    "id": "forest_se",
    "name": "Southeastern Forest",
    "area": "Forest",
    "explored": False,

    "description":
"""You've reached the forest's southeastern corner, where the temperature noticeably drops. Frost patterns decorate fallen logs and the ground becomes crunchier with each step. The boundary between forest and tundra blurs here, creating an eerie transition zone. Breathing clouds form before your face as you catch glimpses of ice-capped peaks through the thinning trees. You can retreat NORTH or WEST into warmer woods, or brave EAST or SOUTH into the frigid Icy Tundra.""",

    "exits": {
        "north": "Forest_NE",
        "south": "Tundra_SW",
        "east": "Tundra_C",
        "west": "Forest_S",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}


forest_southwest = {

    "id": "forest_sw",
    "name": "Southwestern Forest",
    "area": "Forest",
    "explored": False,

    "description":
"""The southwestern corner marks where the forest gives way to the endless grasslands beyond. Here, the trees grow in irregular clusters, creating natural clearings filled with tall grass. The contrast between the shaded forest floor and the bright openness ahead is stark. A cool breeze carries the promise of adventure from the Plains. You can travel NORTH through the woods, EAST along the forest's edge, or WEST and SOUTH into the rolling Plains.""",

    "exits": {
        "north": "Forest_NW",
        "south": "Plains_S",
        "east": "Forest_S",
        "west": "Plains_W",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

# TUNDRA BIOME

tundra_north = {

    "id": "tundra_n",
    "name": "Northern Tundra",
    "area": "Tundra",
    "explored": False,

    "description":
"""A biting cold embraces you as you step into the Northern Tundra. The ground is a frozen expanse of snow and ice, sparkling like a field of diamonds under an overcast sky. Jagged ice formations rise from the frozen wasteland, and every breath you take forms visible clouds. The air itself seems to crackle with cold. You can push SOUTH into the tundra's heart or retreat WEST to the relative warmth of the Forest.""",

    "exits": {
        "south": "Tundra_C",
        "west": "Forest_NE",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

tundra_centre = {

    "id": "tundra_c",
    "name": "Central Tundra",
    "area": "Tundra",
    "explored": False,

    "description":
"""At the center of the Icy Tundra, you find yourself in a vast frozen plain. The wind howls ceaselessly, carrying the mournful cry of distant wolves. Aurora-like colors dance in the sky—blues, greens, and purples—creating an otherworldly beauty that barely masks the deadly cold. To the EAST, you spy the shapes of what might be icy igloos. You can travel NORTH, SOUTH through the tundra, EAST toward the mysterious Icy Igloos, or WEST back to the Forest.""",

    "exits": {
        "north": "Tundra_N",
        "south": "Tundra_S",
        "east": "Igloos_W",
        "west": "Forest_SE",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

tundra_south = {

    "id": "tundra_s",
    "name": "Southern Tundra",
    "area": "Tundra",
    "explored": False,

    "description":
"""The Southern Tundra stretches before you, a landscape of rolling ice hills and treacherous crevasses. Here the snow is deeper, and the cold more penetrating. Strange ice sculptures—possibly carved by wind or something more sinister—dot the landscape. Your footsteps crunch loudly in the silence, echoing in the dead air. Travel NORTH back to the center, or WEST toward the southwestern expanse.""",

    "exits": {
        "north": "Tundra_C",
        "west": "Tundra_SW",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

tundra_southwest = {

    "id": "tundra_sw",
    "name": "Southwestern Tundra",
    "area": "Tundra",
    "explored": False,

    "description":
"""At the southwestern corner of the Icy Tundra, the eternal winter begins to thaw. Patches of frozen ground alternate with bare earth as the tundra transitions to warmer lands. To the WEST, you can already see the golden hues of the Plains stretching toward the horizon. The temperature rises ever so slightly, offering a welcome respite. You can push EAST back into the tundra's depths, NORTH toward the Forest, or WEST into the rolling Plains.""",

    "exits": {
        "north": "Forest_SE",
        "east": "Tundra_S",
        "west": "Plains_SE",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

igloos_west = {

    "id": "igloos_w",
    "name": "Icy Igloos West",
    "area": "Village",
    "explored": False,

    "description":
"""You've reached the western side of the Icy Igloos, a mysterious settlement carved into the heart of the harsh tundra. The village appears abandoned, its icy domes casting long shadows in the perpetual twilight. A layer of fresh frost covers everything—walls, paths, even the air itself seems to shimmer with cold. Cracks spider-web across the ice beneath your feet, and you hear the ominous creaking of frozen structures. A weathered sign warns of the danger of falling through the treacherous ice. You can venture EAST deeper into the village or retreat WEST to the tundra.""",

    "exits": {
        "east": "Igloos_E",
        "west": "Tundra_C",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

igloos_east = {

    "id": "igloos_e",
    "name": "Icy Igloos East",
    "area": "Village",
    "explored": False,

    "description":
"""The eastern side of the Icy Igloos holds the village's secrets. Here, larger structures loom—possibly meeting halls or storage buildings—all carved from the same ethereal ice. Strange symbols are etched into the walls, glowing faintly with an inner light. The temperature drops even further, and you catch glimpses of what might be movements in the ice—reflections, or something more? The path WEST leads back to safety.""",

    "exits": {
        "west": "Igloos_W",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

# PLAINS BIOME

plains_northwest = {

    "id": "plains_nw",
    "name": "Northwestern Plains",
    "area": "Plains",
    "explored": False,

    "description":
"""You've reached the northwestern corner of the Rolling Plains, where endless grasslands stretch to the horizon. Tall golden wheat sways in the wind, and you can see for miles in every direction. The sky is wide and blue, dotted with fluffy white clouds. To the EAST, the forest provides a green contrast to the amber fields. You can journey SOUTH into the vast plains or EAST back into the shelter of the Forest.""",

    "exits": {
        "south": "Plains_W",
        "east": "Forest_NW",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

plains_west = {

    "id": "plains_w",
    "name": "Western Plains",
    "area": "Plains",
    "explored": False,

    "description":
"""The Western Plains spread before you like a golden sea, unbroken save for the occasional ancient stone circle or weathered windmill. Herds of wild creatures can be glimpsed in the distance, moving gracefully across the horizon. The air is sweet with the scent of wild flowers and wheat. In the far WEST, you can see dark plumes of smoke rising—perhaps from the Vengeful Village. Travel NORTH or SOUTH along the plains, EAST to the Forest's edge, or WEST toward the ominous Village.""",

    "exits": {
        "north": "Plains_NW",
        "south": "Plains_SW",
        "east": "Forest_SW",
        "west": "Village_E",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

plains_southwest = {

    "id": "plains_sw",
    "name": "Southwestern Plains",
    "area": "Plains",
    "explored": False,

    "description":
"""At the southwestern corner of the Plains, the landscape becomes more desolate. The wheat fields thin out, giving way to rocky outcroppings and hardy desert vegetation. Dry, hot air moves through in waves, and dust devils dance across the barren earth. Despite the harshness, there's a raw beauty here. Travel NORTH to greener pastures, or EAST across the southern plains.""",

    "exits": {
        "north": "Plains_W",
        "east": "Plains_S",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

plains_south = {

    "id": "plains_s",
    "name": "Southern Plains",
    "area": "Plains",
    "explored": False,

    "description":
"""The Southern Plains are vibrant with life, where the grasslands reach their full splendor. Bees hum from flower to flower, and birds circle overhead in intricate patterns. To the SOUTH, a majestic city rises—the Little Kingdom, with its tall spires and bustling markets visible even from here. A guard patrols nearby, his armor glinting in the sun. You can explore EAST or WEST across the plains, head NORTH back to the Forest, or continue SOUTH toward the beckoning Kingdom.""",

    "exits": {
        "north": "Forest_SW",
        "south": "Kingdom_N",
        "east": "Plains_SE",
        "west": "Plains_SW",
    },

    "items": [item_city_key_1, item_city_key_2],
    "interacts": [npc_guard],
    "enemies": [],
}

plains_southeast = {

    "id": "plains_se",
    "name": "Southeastern Plains",
    "area": "Plains",
    "explored": False,

    "description":
"""The southeastern corner of the Plains is a place of stark contrasts. To the NORTH and WEST, golden grasslands flourish. But to the EAST, an icy wall of frigid tundra looms, creating a dramatic border between warmth and cold. The temperature fluctuates weirdly here, making your skin tingle. Strange flowers bloom at the edge where the two biomes meet—flowers that seem half-frozen and half-alive. Journey WEST to warmer plains, NORTH into the Forest, or EAST into the deadly chill of the Icy Tundra.""",

    "exits": {
        "north": "Forest_S",
        "east": "Tundra_SW",
        "west": "Plains_S",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

village_east = {

    "id": "village_e",
    "name": "Vengeful Village East",
    "area": "Village",
    "explored": False,

    "description":
"""The eastern side of the Vengeful Village greets you with unsettling silence. The buildings are weathered and ominous, built from dark stone and weathered wood. Shattered windows stare at you like empty eyes. Graffiti marks the walls—some in languages you don't recognize, others clearly warning signs. The air feels heavy with history, and not a pleasant one. No lights shine from windows, no voices call out. You can retreat EAST to the safety of the plains or venture WEST deeper into the village.""",

    "exits": {
        "east": "Plains_W",
        "west": "Village_W",
    },

    "items": [],
    "interacts": [npc_merchant],
    "enemies": [],
}

village_west = {

    "id": "village_w",
    "name": "Vengeful Village West",
    "area": "Village",
    "explored": False,

    "description":
"""The western side of the Vengeful Village is the heart of its darkness. Here, the buildings are more ruined, more... violated. Burn marks scar the walls. Strange symbols are carved into every surface—symbols that make your eyes water just to look upon them. In the distance, you hear things moving, or perhaps it's just the wind playing tricks. Whatever happened here, the echoes remain strong. Only the path EAST offers escape.""",

    "exits": {
        "east": "Village_E",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

kingdom_north = {

    "id": "kingdom_north",
    "name": "Little Kingdom North",
    "area": "Village",
    "explored": False,

    "description":
"""Welcome to the Little Kingdom's northern district! Cobblestone streets bustle with life—merchants call out their wares, blacksmiths hammer at their forges, and adventurers swap stories in tavern doorways. Colorful awnings stretch between buildings, and the air is filled with the scent of fresh bread, spices, and adventure. Guild halls line the streets, their banners waving proudly. Travel SOUTH to discover more of the kingdom's secrets, or head NORTH back to the open plains.""",

    "exits": {
        "north": "Plains_S",
        "south": "Kingdom_S",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

kingdom_south = {

    "id": "kingdom_south",
    "name": "Little Kingdom South",
    "area": "Village",
    "explored": False,

    "description":
"""The southern side of the Little Kingdom holds its greatest secret—the entrance to the fabled dungeon. A massive stone archway leads deep into the earth, flanked by ancient statues of forgotten heroes. Strange runes glow faintly along the edges, and the air that drifts up from below carries the scent of old magic and hidden treasures. A dungeonkeeper stands guard, their eyes appraising you. Three trophies gleam on a nearby pedestal—the Forest, Plains, and Tundra trophies—testaments to those who have conquered the land's greatest challenges. Return NORTH to the city's heart.""",

    "exits": {
        "north": "Kingdom_N",
    },

    "items": [item_forest_trophy, item_plains_trophy, item_tundra_trophy],
    "interacts": [npc_dungeonkeeper],
    "enemies": [],
}

# ROOMS DICTIONARY

rooms = { # MAKE SURE TO ADD NEW ROOMS TO THIS DICTIONARY
    "Starter": room_starter,

    "Forest_N": forest_north,
    "Forest_NE": forest_northeast,
    "Forest_NW": forest_northwest,
    "Forest_S": forest_south,
    "Forest_SE": forest_southeast,
    "Forest_SW": forest_southwest,

    "Tundra_N": tundra_north,
    "Tundra_C": tundra_centre,
    "Tundra_S": tundra_south,
    "Tundra_SW": tundra_southwest,

    "Igloos_W": igloos_west,
    "Igloos_E": igloos_east,

    "Plains_NW": plains_northwest,
    "Plains_W": plains_west,
    "Plains_SW": plains_southwest,
    "Plains_S": plains_south,
    "Plains_SE": plains_southeast,

    "Village_E": village_east,
    "Village_W": village_west,

    "Kingdom_N": kingdom_north,
    "Kingdom_S": kingdom_south,
}