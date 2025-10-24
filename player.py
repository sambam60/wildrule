from map import rooms
from items import *

# WHEN USING THESE VARIABLES IN OTHER FILES, PLEASE USE player.<variable>

current_room = rooms["Starter"]
current_turn = 0
change_turn = False

inventory = [item_test1]

equipment = {
    "weapon": weapon_test,
    "armour": armour_test,
    "accessories": []
}

player_stats = {
    "health": 100,
    "evasion": 10,
}