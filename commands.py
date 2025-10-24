"""
This file stores all the commands used to play the game.
Functions named "execute_XXXX" are for specific commands.
Other functions may be helper functions for the main command functions.
"""

from map import rooms
import player
from items import *
from interactions import *
from combat import *

def turn_change(function, *args):

    if player.change_turn == True:
        print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
        function(*args)
        player.current_turn = player.current_turn + 1
        player.change_turn = False

def execute_command(command):

    if 0 == len(command):
        return

    match command[0]:

        case "go":
            if len(command) > 1:
                execute_go(command[1])
            else:
                print("\nERROR: Please input a direction to go to.\n")

        case "wait":
            player.change_turn = True
            execute_wait()

        case "take":
            if len(command) > 1:
                execute_take(command[1])
            else:
                print("\nERROR: Please input an item to take.\n")

        case "drop":
            if len(command) > 1:
                execute_drop(command[1])
            else:
                print("\nERROR: Please input an item to drop.\n")

        case "help":
            execute_help(player.current_room["exits"], player.current_room["items"], player.inventory)

        case "menu":
            execute_menu()

        case "inventory":
            execute_inventory(player.inventory)

        case "interact":
            if len(command) > 1:
                execute_interact(command[1])
            else:
                print("\nERROR: Please input something to interact with.\n")

        case "use":
            if len(command) > 1:
                execute_use(command[1])
            else:
                print("\nERROR: Please input an item to use.\n")

        case "attack":
            if len(command) > 2:
                execute_attack(command[1], command[2])
            elif len(command) == 2:
                print("\nERROR: Please specify an attack type.\n")
            else:
                print("\nERROR: Please specify the enemy to attack and the attack type.\n")

        case "quit":
            exit()

        case "test":
            test()

        case _:
            print("\nERROR: Invalid input. Please enter 'help' for a list of valid commands.\n")



# Helper Functions for different commands

def list_of_items(items):

    item_list = []
    for item in items:
        item_list.append(item["name"])
    item_name_list = ", ".join(item_list)

    return item_name_list

def print_room_items(room):
    
    room_items = list_of_items(room["items"])
    if len(room_items) > 0:
        print(f"There is {room_items} here.\n")

def print_room(room): # Displays details of the current room when room changes occur

    print(f" — {room["name"].upper()} — \n")
    print(f"{room["description"]}\n")
    print_room_items(room)

def exit_leads_to(exits, direction):
    return rooms[exits[direction]]["name"]

def is_valid_exit(exits, chosen_exit):
    return chosen_exit in exits

def check_exit_availability(direction): # This function stores exits that can only be accessed after certain game progress

    match player.current_room["name"]:

        case "test room 1":
            if direction == "south" and obj_door["status"] == "Locked":
                print("\nYou cannot go south because the door is locked.\n")
                return False
            
        case _:
            return True
        

        
def move(exits, direction):

    return rooms[exits[direction]]

# Commands

def execute_go(direction): # Movement command

    if check_exit_availability(direction) == False:
        return
    
    else:

        try:
            match direction:

                case "north":
                    exit = move(player.current_room["exits"], "north")
                    player.current_room = exit
                    player.change_turn = True
                    turn_change(print_room, player.current_room)

                case "south":
                    exit = move(player.current_room["exits"], "south")
                    player.current_room = exit
                    player.change_turn = True
                    turn_change(print_room, player.current_room)

                case "east":
                    exit = move(player.current_room["exits"], "east")
                    player.current_room = exit
                    player.change_turn = True
                    turn_change(print_room, player.current_room)

                case "west":
                    exit = move(player.current_room["exits"], "west")
                    player.current_room = exit
                    player.change_turn = True
                    turn_change(print_room, player.current_room)
                    
        except KeyError:
            print("\nERROR: The inputted direction does not have a valid exit or does not exist.\n")

def execute_wait():

    if player.change_turn == True:
        print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
        print("\nYou waited for one turn.\n")
        player.current_turn = player.current_turn + 1
        player.change_turn = False


def execute_take(item_id): # Take item command

    room_items = current_room["items"]
    take_item = False

    for item in room_items:
        if item["id"] == item_id:
            room_items.remove(item)
            player.inventory.append(item)
            print(f"\nYou have taken the {item["name"]}.\n")
            take_item = True
            break

    if take_item == False:
        print("\nError: That item is not in the current room or does not exist.\n")


def execute_drop(item_id): # Drop item command
    
    room_items = current_room["items"]
    drop_item = False

    for item in player.inventory:
        if item["id"] == item_id:
            player.inventory.remove(item)
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

def test():
    print(player.current_turn)

def execute_menu():

    print("\n — Info Menu — \n")
    print(f"You are currently in {player.current_room["name"].upper()} on turn {player.current_turn}.")

    print("\n — Player Stats — \n")
    print(f"HEALTH: {player.player_stats[0]["health"]}")
    print(f"WEAPON: {player.equipment["weapon"]["name"].upper()}")
    print(f"ARMOUR: {player.equipment["armour"]["name"].upper()}")
    print(f"EVASION: {player.player_stats[0]["evasion"]}")


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
                        player.inventory.append(item_test3)
                    break

                case _:
                    print("error message!!!")

        else:
            print("\nError: You cannot interact with that.\n")



def execute_use(item_id): # Command for using items in the player's inventory
    global current_room
    available_items = []

    for item in player.inventory:
        available_items.append(item["id"])

    if not (item_id in available_items):
        print("\nError: That item is not in your inventory or does not exist.\n")
    else:

        match item_id:

            case "test3":
                if current_room["name"] == "test room 1":
                    print("\nYou unlocked the door.\n")
                    player.inventory.remove(item)
                    obj_door["status"] = "Unlocked"
                else:
                    print("\nYou cannot use this item here.\n")

            case _:
                print("\nError: That item cannot be used.\n")

def execute_attack(enemy_id, attack_type):
    attack_enemy(enemy_id, attack_type)

def execute_dodge():
    pass