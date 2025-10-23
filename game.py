from map import rooms
from player import *
from items import *
from interactions import *
from gameparser import *


def list_of_items(items):

    item_list = []
    for item in items:
        item_list.append(item["name"])
    item_name_list = ", ".join(item_list)

    return item_name_list


def print_room_items(room): # This function isn't being used at the moment. It may be used later though. - Syafiq
    
    room_items = list_of_items(room["items"])
    if len(room_items) > 0:
        print(f"There is {room_items} here.\n")


def print_room(room): # Displays details of the current room when room changes occur

    print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
    print(f" — {room["name"].upper()} — \n")
    print(f"{room["description"]}\n")


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

def execute_go(direction): # Movement command

    global current_room

    if check_exit_availability(direction) == False:
        return
    
    else:

        try:
            match direction:

                case "north":
                    exit = move(current_room["exits"], "north")
                    current_room = exit

                case "south":
                    exit = move(current_room["exits"], "south")
                    current_room = exit

                case "east":
                    exit = move(current_room["exits"], "east")
                    current_room = exit

                case "west":
                    exit = move(current_room["exits"], "west")
                    current_room = exit
                    
        except KeyError:
            print("\nERROR: The inputted direction does not have a valid exit or does not exist.\n")


def execute_take(item_id): # Take item command

    room_items = current_room["items"]
    for item in room_items:
        if item["id"] == item_id:
            room_items.remove(item)
            inventory.append(item)
            print(f"\nYou have taken the {item["name"]}.\n")
            break


def execute_drop(item_id): # Drop item command
    
    room_items = current_room["items"]
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            room_items.append(item)
            print(f"\nYou have dropped the {item["name"]}.\n")
            break

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

    print(available_items, item_id)
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


def execute_command(command):

    if 0 == len(command):
        return

    match command[0]:

        case "go":
            if len(command) > 1:
                execute_go(command[1])
            else:
                print("\nERROR: Please input a direction to go to.\n")

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
            execute_help(current_room["exits"], current_room["items"], inventory)

        case "inventory":
            execute_inventory(inventory)

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

        case "quit":
            exit()

        case _:
            print("\nERROR: Invalid input. Please enter 'help' for a list of valid commands.\n")


def menu(exits, room_items, inv_items):

    user_input = input("> ")
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits, direction):

    global room_change
    room_change = True
    return rooms[exits[direction]]


def main():

    while True:
        global room_change

        if room_change == True:
            print_room(current_room)
            room_change = False
        print("What do you want to do?")
        command = menu(current_room["exits"], current_room["items"], inventory)
        execute_command(command)


if __name__ == "__main__":
    main()