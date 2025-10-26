from map import rooms
from items import *

current_room = rooms["Starter"]
current_turn = 0
change_turn = False

inventory = [item_test1]

equipment = {
    "weapon": weapon_default,
    "armour": armour_default,
    "accessory": accessory_default,
}

stats = {
    "health": 100,
    "evasion": 0,
}

room_change = True


def print_health():
    """Print the player's health as hearts: 10 hearts, each worth 10 HP, with gaps of one space between hearts."""
    health = stats.get("health", 0)
    if health < 0:
        health = 0
    if health > 100:
        health = 100

    full_hearts = health // 10
    empty_hearts = 10 - full_hearts

    heart_full = "\u2665"  # ♥
    heart_empty = "\u2661"  # ♡

    # Join with a single space between each heart
    hearts = ([heart_full] * full_hearts) + ([heart_empty] * empty_hearts)
    hearts_str = " ".join(hearts)
    print(f"HP: {hearts_str}")
