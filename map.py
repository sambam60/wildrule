"""
This file stores all the rooms and areas in the game.
"""

from items import *
from interactions import *

room_template = {
    "id": "temp",

    "name": "TEMPLATE ROOM",

    "description":
    """THIS IS USED AS A BASE FOR ADDING NEW ROOMS TO THE MAP""",

    "exits": {},

    "items": [],

    "interacts": [],

    "enemies": [],
}

room_starter = {
    "id": "start",

    "name": "starting room",

    "description":
    """You are now in the starting room.""",

    "exits": {"south": "Test1"},

    "items": [item_test2],

    "interacts": [],

    "enemies": [],
}

room_test1 = {
    "id": "test1",

    "name": "test room 1",

    "description":
    """You are now in Test Room 1.
    \nThere is a path to your east and a door to your south.
    \nThe starting room is north.""",

    "exits":  {"north": "Starter", "south": "Test3", "east": "Test2"},

    "items": [],

    "interacts": [],

    "enemies": [],
}

room_test2 = {
    "id": "test2",

    "name": "test room 2",

    "description":
    """You are now in Test Room 2.
    \nThere is an NPC standing in the room.
    \nThe exit back to Test Room 1 is to your west.""",

    "exits": {"west": "Test1"},

    "items": [],

    "interacts": [npc_test],

    "enemies": [],
}

room_test3 = {
    "id": "test3",

    "name": "test room 3",

    "description":
    """You are now in Test Room 3.
    \nThere is nothing here.
    \nThe exit back to Test Room 1 is back through the door north.""",

    "exits": {"north": "Test1"},

    "items": [],

    "interacts": [],

    "enemies": [],
}

rooms = {
    "Template": room_template, # MAKE SURE TO ADD NEW ROOMS TO THIS DICTIONARY
    "Starter": room_starter,
    "Test1": room_test1,
    "Test2": room_test2,
    "Test3": room_test3,
}