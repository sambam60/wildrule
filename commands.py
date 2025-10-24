"""
This file stores all the commands used to play the game.
Functions named "execute_XXXX" are for specific commands.
Other functions may be helper functions for the main command functions.
"""

from map import rooms
from player import *
from items import *
from interactions import *
from combat import *



def exit_leads_to(exits, direction):

    return rooms[exits[direction]]["name"]

def is_valid_exit(exits, chosen_exit):

    return chosen_exit in exits


def check_exit_availability(direction): # This function stores exits that can only be accessed after certain game progress

    match current_room["name"]:

        case "test room 1":
            if direction == "south" and obj_door["status"] == "Locked":
                print("\nYou cannot go south because the door is locked.\n")
                return False
            
        case _:
            return True
        

        
def move(exits, direction):

    return rooms[exits[direction]]


def execute_take(item_id): # Take item command

    room_items = current_room["items"]
    take_item = False

    for item in room_items:
        if item["id"] == item_id:
            room_items.remove(item)
            inventory.append(item)
            print(f"\nYou have taken the {item["name"]}.\n")
            take_item = True
            break

    if take_item == False:
        print("\nError: That item is not in the current room or does not exist.\n")


def execute_drop(item_id): # Drop item command
    
    room_items = current_room["items"]
    drop_item = False

    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            room_items.append(item)
            print(f"\nYou have dropped the {item["name"]}.\n")
            drop_item = True
            break

    if drop_item == False:
        print("\nError: That item is not in your inventory or does not exist.\n")


def execute_help(exits, room_items, inv_items): # Prints all valid commands that can be inputted
    print("\n — Available Commands — \n")

    # Valid exits in the current room
    for direction in exits:
        print(f"GO {direction.upper()} to {exit_leads_to(exits, direction)}.")

    # Take/drop items in your inventory
    for item in room_items:
        print(f"TAKE {item["id"].upper()} to take {item["name"]}.")
    for item in inv_items:
        print(f"DROP {item["id"].upper()} to drop your {item["name"]}.")

    # Valid interactions in the current room
    for interact in current_room["interacts"]:
        print(f"INTERACT {interact["id"].upper()} to interact with {interact["name"]}.")

    print("\nHELP for a list of available commands.")
    print("INVENTORY to view items in your inventory.")
    print("USE [item] to use an item from your inventory.")
    print("QUIT to close the program.\n")



def execute_inventory(items): # Displays the current items in the player's inventory

    print("\n — Your Inventory — \n")
    for item in items:
        print(f"{item["name"].upper()} [{item["id"]}] - {item["description"]}\n")



def execute_interact(interaction): # Command for interacting with special objects/NPCs in a room
    global current_room

    for object in current_room["interacts"]:
        if interaction == object["id"]:

            match object["id"]:

                case "npc":
                    if npc_test["status"] == True:
                        print("\nThe NPC stares at you.\n")
                    else:
                        print("\nThe NPC gave you a key (test item 3).\n")
                        npc_test["status"] = True
                        inventory.append(item_test3)
                    break

                case _:
                    print("error message!!!")

        else:
            print("\nError: You cannot interact with that.\n")



def execute_use(item_id): # Command for using items in the player's inventory
    global current_room
    available_items = []

    for item in inventory:
        available_items.append(item["id"])

    if not (item_id in available_items):
        print("\nError: That item is not in your inventory or does not exist.\n")
    else:

        match item_id:

            case "test3":
                if current_room["name"] == "test room 1":
                    print("\nYou unlocked the door.\n")
                    inventory.remove(item)
                    obj_door["status"] = "Unlocked"
                else:
                    print("\nYou cannot use this item here.\n")

            case _:
                print("\nError: That item cannot be used.\n")

def execute_attack(enemy_id, attack_type):
    attack_enemy(enemy_id, attack_type)

def execute_dodge():
    pass