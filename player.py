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
    "accessories": [],
    "gold": 100
}

stats = {
    "health": 100,
    "defence": equipment["armour"]["defence"],
    "evasion": 10,
}

charge_attack = False
evade_attack = False