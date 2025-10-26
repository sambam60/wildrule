from map import rooms
from items import *

# WHEN USING THESE VARIABLES IN OTHER FILES, PLEASE USE player.<variable>

current_room = rooms["Starter"]
current_turn = 0
change_turn = False

inventory = []
gold = 300

equipment = {
    "weapon": weapon_default,
    "armour": armour_default,
    "accessory": accessory_default,
}

stats = {
    "health": 100,
    "evasion": 10,
}

charge_attack = False
evade_attack = False