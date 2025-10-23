from map import rooms
from player import *
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


def print_room(room): # Displays details of the current room when room changes occur

    print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
    print(f" — {room["name"].upper()} — \n")
    print(f"{room["description"]}\n")


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


def menu(exits, room_items, inv_items):

    user_input = input("> ")
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


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