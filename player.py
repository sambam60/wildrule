from map import rooms
from items import *

current_room = rooms["Starter"]
turn = 0

inventory = [item_test1]

equipment = {
    "weapon": weapon_test,
    "armour": armour_test,
    "accessories": []
}

player_stats = {
    "health": 100,
    "evasion": 0,
},

room_change = True