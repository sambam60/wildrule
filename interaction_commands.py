"""
This file stores the functions for the game commands 'interact' and 'use'.
Since each item/object that can be used/interacted with need unique functions and code.
"""

from map import rooms
import player
import shops
from items import *
from interactions import *
from interaction_commands import *
import time
import sys
import threading
import queue
import textwrap
import tts
import voice_input

def execute_interact(interaction_id): # Command for interacting with special objects/NPCs in a room

    for object in player.current_room["interacts"]:
        if interaction_id == object["id"]:

            match object["id"]:

                case "shop":
                    match npc_merchant["state"]:

                        case 0:
                            player.menu_state = True
                            shops.open_shop()
                            break

                        case 1:
                            break

                        case 2:
                            break

                case "keeper":
                    match npc_dungeonkeeper["state"]:
                        case 0:

                            print("\nDungeon Keeper: Hello adventurer. What brings you to me today?")
                            print("\nDungeon Keeper: Hm? You want to enter the dungeon? You think you are worthy enough to enter this cursed dungeon?")
                            print("\nDungeon Keeper: You must be mistaken. No normal adventurer can enter here.")
                            print("\nDungeon Keeper: Only those who prove themselves to be strong and worthy can enter here, if they want a non-zero chance to come out alive.")
                            print("\nDungeon Keeper: Bring me the trophies of the Wildrule and show me that you are the one-of-a-kind hero that you think you are.\n")
                            npc_dungeonkeeper["state"] = 1

                            break

                        case 1:

                            trophies_missing = ["FOREST TROPHY", "PLAINS TROPHY", "TUNDRA TROPHY"]

                            for item in player.inventory:
                                match item["id"]:
                                    case "foresttrophy":
                                        trophies_missing.remove("FOREST TROPHY")
                                    case "tundratrophy":
                                        trophies_missing.remove("TUNDRA TROPHY")
                                    case "plainstrophy":
                                        trophies_missing.remove("PLAINS TROPHY")

                            if len(trophies_missing) > 0:
                                print(f"\nDungeon Keeper: You have {3 - (len(trophies_missing))}/3 trophies. Please come back later when you have all the missing trophies.")
                                print(">>> Wildrule trophies are dropped by the rare minibosses that can spawn in each biome. <<<\n")
                                for trophy in trophies_missing:
                                    print(f"You are missing the {trophy}.")
                                print()
                            else:
                                print("\nDungeon Keeper: You're back already? Aren't you eager to dive into your demise.")
                                print("\nDungeon Keeper: Many a hero has come and gone only to be martyred inside the dungeon, with no one to help them or comfort them.")
                                print("\nDungeon Keeper: I see you have all the Wildrule trophies. Very well then. You have told me your potential. Now you must show it.")
                                print("\n * The Dungeon Keeper took your trophies and unlocked the door into the dungeon *\n")
                                player.inventory.remove(item_forest_trophy)
                                player.inventory.remove(item_plains_trophy)
                                player.inventory.remove(item_tundra_trophy)
                                npc_dungeonkeeper["state"] = 2

                            break

                        case 2:
                            print("\nDungeon Keeper: What are you waiting for? You forgot something?\n")
                            break
                
                case "guard":
                    match npc_guard["state"]:
                        case 0:

                            print("\nCity Guard: Oh hello there! Are you trying to get into the city too?")
                            print("\nCity Guard: Yeah? Sweet. Ah- well, that's a problem right now.")
                            print("\nCity Guard: See, I'm in change of opening the city gates and questioning any outsiders who wants to come into the kingdom.")
                            print("\nCity Guard: However... I may have lost my key. I probably dropped it while on my walk to the forest.")
                            print("\nCity Guard: Now someone's probably stolen the key...")
                            print("\nCity Guard: Well, if you could try and find who has my key, and then return the key back to me, then I'll allow you into the city without any questions.")
                            npc_guard["state"] = 1

                            break

                        case 1:

                            key_parts_missing = ["GATE KEY PART 1", "GATE KEY PART 2"]

                            for item in player.inventory:
                                match item["id"]:
                                    case "key1":
                                        key_parts_missing.remove("GATE KEY PART 1")
                                    case "key2":
                                        key_parts_missing.remove("GATE KEY PART 2")

                            if len(key_parts_missing) > 0:
                                print(f"\nCity Guard: Hey, you haven't gotten all the key parts yet!\n")
                                for part in key_parts_missing:
                                    print(f"You are missing the {part}.")
                                print()
                            else:
                                print("\nCity Guard: Ah! You've got the key! Well, at least parts of the key.")
                                print("\nCity Guard: No worries! I used to work as a locksmith. I'll fix this right up and I'll let you in.")
                                print("\n* The guard walks away for a minute, then returns back to the gate *")
                                print("\nThere! The key's all fixed up now. Here, sir, thank you very much for your help!")
                                print("\n* The guard unlocks and opens the city gate *\n")
                                player.inventory.remove(item_city_key_1)
                                player.inventory.remove(item_city_key_2)
                                npc_guard["state"] = 2

                            break

                        case 2:
                            print("\nCity Guard: Thank you so much kind sir!\n")
                            break



        else:
            print(f"\nERROR: '{interaction_id}' cannot be interacted with. Enter 'help' to see what can be interacted with in the current room.\n")



def execute_use(item_id): # Command for using items in the player's inventory
    available_items = []

    for item in player.inventory:
        available_items.append(item["id"])

    if not (item_id in available_items):
        print("\nERROR: That item is not in your inventory or does not exist.\n")
    else:

        match item_id:

            case "test3":
                if player.current_room["name"] == "test room 1":
                    print("\nYou unlocked the door.\n")
                    player.inventory.remove(item)
                else:
                    print("\nYou cannot use this item here.\n")

            case _:
                print("\nERROR: That item cannot be used.\n")