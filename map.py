"""
This file stores all the rooms and areas in the game.
"""

from items import *
from interactions import *

room_starter = {
    "name": "starting room",

    "description":
    """You are now in the starting room.""",

    "exits": {"south": "Test1"},

    "items": [item_test2],

    "interacts": []
}

room_test1 = {
    "name": "test room 1",

    "description":
    """You are now in Test Room 1.
    \nThere is a path to your east and a door to your south.
    \nThe starting room is north.""",

    "exits":  {"north": "Starter", "south": "Test3", "east": "Test2"},

    "items": [],

    "interacts": []
}

room_test2 = {
    "name": "test room 2",

    "description":
    """You are now in Test Room 2.
    \nThere is an NPC standing in the room.
    \nThe exit back to Test Room 1 is to your west.""",

    "exits": {"west": "Test1"},

    "items": [],

    "interacts": [npc_test]
}

room_test3 = {
    "name": "test room 3",

    "description":
    """You are now in Test Room 3.
    \nThere is nothing here.
    \nThe exit back to Test Room 1 is back through the door north.""",

    "exits": {"north": "Test1"},

    "items": [],

    "interacts": []
}

rooms = {
    "Starter": room_starter,
    "Test1": room_test1,
    "Test2": room_test2,
    "Test3": room_test3,
}
