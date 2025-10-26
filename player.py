from map import rooms
from items import *

current_room = rooms["Starter"]
current_turn = 0
change_turn = False
room_change = True

inventory = [weapon_dev, armour_dev]

equipment = {
    "weapon": weapon_default,
    "armour": armour_default,
    "accessory": accessory_default,
}

stats = {
    "health": 100,
    "max_health": 100,
    "evasion": 10,
}

gold = 0
charge_attack = False
evade_attack = False

def print_health():
    """Print the player's health as hearts: 10 hearts, each worth 10 HP, with gaps of one space between hearts."""
    health = stats.get("health", 0)
    if health < 0:
        health = 0
    if health > 100:
        health = 100

    full_hearts = int(health) // 10
    empty_hearts = 10 - full_hearts

    # Colours
    LIGHT_RED = "\033[38;2;255;102;102m"
    RESET = "\033[0m"

    heart_full = f"{LIGHT_RED}\u2665{RESET}"  # coloured ♥
    heart_empty = "\u2661"  # ♡

    # Join with a single space between each heart
    hearts = ([heart_full] * full_hearts) + ([heart_empty] * empty_hearts)
    hearts_str = " ".join(hearts)
    print(f"HP: {round(stats["health"], 1)}/{stats["max_health"]} | {hearts_str}")
