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
    print("\n")

def menu(exits, room_items, inv_items):

    user_input = input("> ")
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


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