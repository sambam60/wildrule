"""
This file stores all the rooms and areas in the game.
"""

from items import *
from interactions import *
from enemies import *

# TUTORIAL ROOMS

room_starter = {

    "id": "start",
    "name": "Forest Entrance",
    "area": "Forest",
    "explored": False,

    "description":
"""You are now in the starting room. Go SOUTH to the actual map of the game.""",

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
"""You are now in the north side of the Forest, your starting point on the Map.
You can go EAST to the northeast corner of the forest, SOUTH to the forest's southern side or WEST to the northwest corner.""",

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
"""You've reached the forest's northeastern corner.
You can go SOUTH to the southeast corner of the forest, WEST back to the northern forest or EAST into the Icy Tundra.""",

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
"""You've reached the forest's northwestern corner.
You can go SOUTH for the forest's southwestern corner, EAST to the northern forest or WEST into the Plains.""",

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
"""You've reached the forest's southern side.
You can NORTH back to the northern forest, EAST to the forest's southeastern corner, WEST to the forest's southwestern corner or SOUTH into the Plains.""",

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
"""You've reached the forest's southeastern corner.
You can NORTH to the forest's northeast, WEST to the forest's south, or EAST/SOUTH into the Icy Tundra.""",

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
"""You've reached the forest's southwestern corner.
You can NORTH to the northwestern forest, EAST to the forest's south side or WEST/SOUTH into the Plains.""",

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
"""You're now in the north of the Icy Tundra.
You can go SOUTH towards the tundra's centre or WEST back to the Forest.""",

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
"""You're now in the centre of the Icy Tundra.
You can NORTH to the northern tundra, SOUTH to the southern tundra, EAST towards the Icy Igloos or WEST back to the Forest.""",

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
"""You're now in the south of the Icy Tundra.
You can go NORTH towards the centre of the tundra or WEST to the tundra's southwestern corner.""",

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
"""You're now in the southwestern corner of the Icy Tundra.
You can go EAST back into the tundra's south, NORTH back to the Forest or WEST into the Plains.""",

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
"""You have reached the western side of the Icy Igloos, situated in the eastern flung of the harsh tundra.
The small igloo village sits on top of a large icy clearing, itself broken up by the collections of the village's buildings.
Move carefully... Don't want to see you end up frozen under the ice like the last adventurer.
You can go EAST to the eastern side of the village or WEST back into the centre of the tundra.""",

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
"""You are now the eastern side of the Icy Igloos.
You can go WEST back to the western side of the village.""",

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
"""You have reached the northwestern corner of the Rolling Plains.
You can go SOUTH to the western plains or NORTH back to the Forest.""",

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
"""You are now in the western Plains.
You can go NORTH to the plain's northwest corner, SOUTH to it's southwest corner, EAST into the Forest or WEST towards the Vengeful Village.""",

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
"""You are now in the southwestern corner of the Plains.
You can go NORTH to the western plains or EAST into the southern plains.""",

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
"""You are now in the southern side Plains.
You can go EAST to the southeastern plains, WEST to the southwestern plains, NORTH back into the Forest or SOUTH towards the Little Kingdom.""",

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
"""You are now in the southeastern corner Plains.
You can go WEST to the southern plains, NORTH into the Forest or EAST into the Icy Tundra.""",

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
"""You have reached the eastern side of the Vengeful Village, situated in the dry environment of the Rolling Plains.
You can go WEST to the western side of the village, or EAST back into the plains.""",

    "exits": {
        "east": "Plains_W",
        "west": "Village_W",
    },

    "items": [],
    "interacts": [],
    "enemies": [],
}

village_west = {

    "id": "village_w",
    "name": "Vengeful Village West",
    "area": "Village",
    "explored": False,

    "description":
"""You have reached the western side of the Vengeful Village, situated in the dry environment of the Rolling Plains.
You can go EAST back to the eastern side of the village.""",

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
"""You have reached the northern side of the Little Kingdom. The city boasts a bustling hub filled with different stalls, merchants and guilds.
You can go SOUTH to the southern side of the city or NORTH back into the plains.""",

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
"""You have reached the southern side of the Little Kingdom.
Here is where you can find the entrance to the fabled dungeon that you have been working so hard to reach.
You can go NORTH back to the city's northern side.""",

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