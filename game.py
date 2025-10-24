from map import rooms
import player
from items import *
from interactions import *
from commands import *
from gameparser import *

def menu(exits, room_items, inv_items):

    user_input = input("> ")
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input

def main():

    while True:

        if player.current_turn == 0:
            print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print_room(player.current_room)
            player.current_turn = player.current_turn + 1

        print("What do you want to do?")
        command = menu(player.current_room["exits"], player.current_room["items"], player.inventory)
        execute_command(command)


if __name__ == "__main__":
    main()