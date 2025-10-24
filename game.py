from map import rooms
import player
from items import *
from interactions import *
from commands import *
from gameparser import *


def list_of_items(items):

    item_list = []
    for item in items:
        item_list.append(item["name"])
    item_name_list = ", ".join(item_list)

    return item_name_list


def print_room_items(room): # This function isn't being used at the moment. It may be used later though.
    
    room_items = list_of_items(room["items"])
    if len(room_items) > 0:
        print(f"There is {room_items} here.\n")


def print_exit(direction, leads_to):
    print("- GO " + direction.upper() + " to " + leads_to + ".")


def print_room(room): # Displays details of the current room when room changes occur

    print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
    print(f" — {room["name"].upper()} — \n")
    print(f"{room["description"]}\n")
    print_room_items(room)
    print(f"You can go in the following directions:")    
    for direction, room_id in room["exits"].items():
        leads_to = rooms[room_id]["name"]
        print_exit(direction, leads_to)
    print("\n")

def menu(exits, room_items, inv_items):

    user_input = input("> ")
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input

"""
DO NOT DELETE/MOVE THE TWO FUNCTIONS execute_command AND execute_go BELLOW TO commands.py
DELETING/ADDING THEM WILL BREAK THE MOVEMENT SYSTEM
"""

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
            print(room_change)
            print(current_room)

        case _:
            print("\nERROR: Invalid input. Please enter 'help' for a list of valid commands.\n")

def execute_go(direction): # Movement command

    global current_room
    global room_change

    if check_exit_availability(direction) == False:
        return
    
    else:

        try:
            match direction:

                case "north":
                    exit = move(current_room["exits"], "north")
                    current_room = exit
                    room_change = True

                case "south":
                    exit = move(current_room["exits"], "south")
                    current_room = exit
                    room_change = True

                case "east":
                    exit = move(current_room["exits"], "east")
                    current_room = exit
                    room_change = True

                case "west":
                    exit = move(current_room["exits"], "west")
                    current_room = exit
                    room_change = True
                    
        except KeyError:
            print("\nERROR: The inputted direction does not have a valid exit or does not exist.\n")

"""
DO NOT DELETE/MOVE THE TWO FUNCTIONS execute_command AND execute_go ABOVE TO commands.py
DELETING/ADDING THEM WILL BREAK THE MOVEMENT SYSTEM
"""

def main():

    while True:
        if player.room_change == True:
            print_room(player.current_room)
            player.room_change = False
        print("What do you want to do?")
        command = menu(player.current_room["exits"], player.current_room["items"], player.inventory)
        execute_command(command)


if __name__ == "__main__":
    main()