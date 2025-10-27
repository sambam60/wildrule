"""
This file stores all the commands used to play the game.
Functions named "execute_XXXX" are for specific commands.
Other functions may be helper functions for the main command functions.
"""

from map import rooms
import player
from items import *
from interactions import *
from interaction_commands import *
from shops import *
from combat import *
from minimap import draw_minimap
import time
import sys
import threading
import queue
import textwrap
import tts
import voice_input

# when True, narrative printing should avoid slow typewriter and just speak/print
TTS_ENABLED = False

def turn_change(function, *args): # CONTROLS FUNCTIONS THAT WILL RUN WHEN A TURN CHANGE COMMAND IS SUCCESSFULLY RUN

    if player.change_turn == True:
        print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
        function(*args)
        function_name = function.__name__
        #print(function_name) # for debugging
        player.current_turn = player.current_turn + 1
        player.change_turn = False

    match function_name:
        case "execute_wait":
            spawn_enemy()

        case "print_room":
            spawn_enemy()

        case "player_attack":
            if len(player.current_room["enemies"]) > 0:
                if player.current_room["enemies"][0]["health"] >= 0:
                    enemy_attack()

        case "evade_attack":
            enemy_attack()



def execute_command(command): # Command list

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
            turn_change(execute_wait)

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

        case "map":
            execute_map()

        case "menu":
            execute_menu()

        case "inventory":
            execute_inventory(player.inventory)

        case "inspect":
            if len(command) > 1:
                execute_inspect(command[1])
            else:
                print("\nERROR: Please input something to inspect.")
                print("You can inspect objects, enemies or items in your current room, or items from your inventory.\n")

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

        case "equip":
            if len(command) > 1:
                execute_equip(command[1])
            else:
                print("\nERROR: Please input an item to equip.\n")

        case "unequip":
            if len(command) > 1:
                execute_unequip(command[1])
            else:
                print("\nERROR: Please input an item to unequip.\n")

        case "attack":
            if len(command) > 2:
                player.change_turn = True
                execute_attack(command[1], command[2])
            elif len(command) == 2:
                print("\nERROR: Please specify an attack type.\n")
            else:
                print("\nERROR: Please specify the enemy to attack and the attack type.\n")

        case "evade":
            execute_evade()

        case "dodge":
            execute_evade()

        case "quit":
            exit()

        case "test":
            draw_minimap(player.current_room)

        case _:
            print(f"\nERROR: '{command[0]}' is not a valid command. Please enter 'help' for a list of valid commands.\n")



def list_of_items(items):

    item_list = []
    for item in items:
        item_list.append(item["name"])
    item_name_list = ", ".join(item_list)

    return item_name_list



def print_room_items(room):
    
    room_items = list_of_items(room["items"])
    if len(room_items) > 0:
        print(f"There is {room_items} on the ground.\n")



def print_room_enemies(room):
    room_enemies = room["enemies"]
    if len(room_enemies) > 0:
        print(f"A wild {room_enemies[0]["name"].upper()} spots you!")



def print_slowly(text, delay=0.03):
    """Print text character by character with a small delay. Press 'SPACE' to skip."""
    skip_queue = queue.Queue()
    stop_event = threading.Event()
    
    def get_input():
        try:
            import msvcrt  # Windows
            while not stop_event.is_set():
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key in [' ']:
                        skip_queue.put(True)
                        break
        except ImportError:
            try:
                # Only use raw mode if interactive TTY
                if sys.stdin.isatty():
                    import termios, tty  # Unix/Linux/Mac
                    import select
                    fd = sys.stdin.fileno()
                    old_settings = termios.tcgetattr(fd)
                    try:
                        tty.setraw(sys.stdin.fileno())
                        while not stop_event.is_set():
                            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                                char = sys.stdin.read(1).lower()
                                if char in ['s', ' ']:
                                    skip_queue.put(True)
                                    break
                    finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception:
                # Non-interactive or unsupported terminal; skip skip-key feature
                pass
    
    # Start input thread only in interactive terminals
    input_thread = None
    if sys.stdin.isatty():
        input_thread = threading.Thread(target=get_input, daemon=True)
        input_thread.start()
    
    # Print text character by character
    for idx, char in enumerate(text):
        print(char, end='', flush=True)
        time.sleep(delay)
        
        # Check if skip was requested
        try:
            skip_queue.get_nowait()
            # Skip was requested, print remaining text immediately
            remaining_text = text[idx + 1:]
            if remaining_text:
                print(remaining_text, end='', flush=True)
            break
        except queue.Empty:
            continue
    
    # Ensure input thread stops and terminal settings are restored
    stop_event.set()
    try:
        if input_thread is not None:
            input_thread.join(timeout=0.1)
    except Exception:
        pass

    print()  # Add newline at the end



def print_room(room): # Displays details of the current room when room changes occur

    say_text(f" — {room['name'].upper()} — \n")
    # Normalise any incidental indentation/newlines in multi-line descriptions
    description_text = textwrap.dedent(room["description"]).strip()
    def _wrap_block(block):
        return textwrap.fill(
            block.strip(),
            width=90,
            replace_whitespace=True,
            drop_whitespace=True,
            break_long_words=False,
            break_on_hyphens=False,
        )
    wrapped_lines = [_wrap_block(p) for p in description_text.split("\n") if p.strip() != ""]
    wrapped_text = "\n".join(wrapped_lines)
    say_text(wrapped_text)
    print_room_items(room)
    print_room_enemies(room)
    print()



def say_text(text: str):
    """print text if tts on or type slow"""
    if TTS_ENABLED:
        print(text)
        tts.speak(text)
    else:
        print_slowly(text)



def exit_leads_to(exits, direction):
    return rooms[exits[direction]]["name"]



def is_valid_exit(exits, chosen_exit):
    return chosen_exit in exits



def check_exit_availability(direction): # This function stores exits that can only be accessed after certain game progress

    match player.current_room["name"]:

        case "test room 1":
            if direction == "south" and npc_guard["state"] == 0:
                print("\nYou cannot go south because the door is locked.\n")
                return False
            
        case _:
            return True
        


def move(exits, direction):

    return rooms[exits[direction]]

# Commands

def explore_room(room):
    if room["explored"] == False:
        room["explored"] = True

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
                    explore_room(player.current_room)

                case "south":
                    exit = move(player.current_room["exits"], "south")
                    player.current_room = exit
                    player.change_turn = True
                    turn_change(print_room, player.current_room)
                    explore_room(player.current_room)

                case "east":
                    exit = move(player.current_room["exits"], "east")
                    player.current_room = exit
                    player.change_turn = True
                    turn_change(print_room, player.current_room)
                    explore_room(player.current_room)

                case "west":
                    exit = move(player.current_room["exits"], "west")
                    player.current_room = exit
                    player.change_turn = True
                    turn_change(print_room, player.current_room)
                    explore_room(player.current_room)
                        
                case _:
                    print(f"\nERROR: '{direction}' is not a valid exit or does not exist.\n")

        except KeyError:
            print(f"\nERROR: The current room does not have a valid exit in the inputted direction '{direction}'.\n")



def execute_wait():
    print("You waited for one turn.\n")



def execute_take(item_id): # Take item command

    room_items = player.current_room["items"]

    if len(player.inventory) == 16:
        print("\nERROR: Your inventory is full. Please drop or store an item away if you want to pickup another item.\n")
        return

    for item in room_items:
        if item["id"] == item_id:
            room_items.remove(item)
            player.inventory.append(item)
            print(f"\nYou have taken the {item["name"]}.\n")
            return

    print("\nERROR: That item is not in the current room or does not exist.\n")



def execute_drop(item_id): # Drop item command
    
    room_items = player.current_room["items"]

    for item in player.inventory:
        if item["id"] == item_id:
            player.inventory.remove(item)
            room_items.append(item)
            print(f"\nYou have dropped the {item["name"]}.\n")
            return

    print("\nERROR: That item is not in your inventory or does not exist.\n")



def execute_help(exits, room_items, inv_items): # Prints all valid commands that can be inputted

    print("\n — Available Commands — \n")

    # Valid exits in the current room
    for direction in exits:
        print(f"GO {direction.upper()} to {exit_leads_to(exits, direction)}.")
    print()
    # Take items from current room
    for item in room_items:
        print(f"TAKE {item["id"].upper()} to take {item["name"]}.")
    print()
    # Valid interactions in the current room
    for interact in player.current_room["interacts"]:
        print(f"INTERACT {interact["id"].upper()} to interact with {interact["name"]}.")
    print()
    # Valid interactions for enemies in the current room
    for enemy in player.current_room["enemies"]:
        print(f"ATTACK {player.current_room["enemies"][0]["id"].upper()} [attack type] to attack the {player.current_room["enemies"][0]["name"]}.")
        print(f"DODGE/EVADE to try and dodge the {player.current_room["enemies"][0]["id"].upper()}'s oncoming attack.")

    print("\nHELP for a list of available commands.")
    print("MAP to view the world map and your exploration progress.")
    print("MENU to view your player stats.")
    print("INSPECT [id] to view the attributes of an object/item/enemy.")
    print("INVENTORY to view items in your inventory.")
    print("\nDROP [item id] to drop an item from your inventory.")
    print("USE [item id] to use an item from your inventory.")
    print("EQUIP [item id] to equip an item from your inventory.")
    print("UNEQUIP [item id] to unequip an item from your equipment.")
    print("\nQUIT to close the program.\n")



def execute_map():
    print("\n — World Map — \n")
    draw_minimap(player.current_room)
    print("\n — Key — \n")
    print(f"[X] = Your current position -> {player.current_room["name"].upper()}")
    print("[?] = Unexplored area")
    print("[F] = Forest tile")
    print("[T] = Tundra tile")
    print("[P] = Plains tile")
    print("[V] = Village tile")
    print()

def execute_inspect(target_id):

    room = player.current_room

    if len(room["enemies"]) > 0:
        if target_id == room["enemies"][0]["id"]:
            enemy = room["enemies"][0]
            print("\n — Inspection — \n")
            print(f"NAME: {enemy["name"].title()}        ENEMY ID: {enemy["id"]}        TYPE: enemy")
            print(f"DESCRIPTION: {enemy["description"]}")
            print(f"HEALTH: {enemy["health"]}/{enemy["max_health"]}        DEFENCE: {enemy["defence"]}        EVASION: {enemy["evasion"]}")
            print(f"NORMAL ATTACK DAMAGE: {enemy["normal_attack"]["damage"]}")
            print(f"CHARGE ATTACK DAMAGE: {enemy["charge_attack"]["damage"]}        CHANCE: {enemy["charge_attack"]["chance"]}%        MISS CHANCE: {enemy["charge_attack"]["miss_multiplier"]}x")
            print(f"COUNTER ATTACK DAMAGE: {enemy["counter_attack"]["damage"]}        CHANCE: {enemy["counter_attack"]["chance"]}%")
            print(f"MAX GOLD DROP: {enemy["gold"]}")
            loot_item = enemy["loot"]["item"]
            if loot_item is not None:
                print(f"AVAILABLE LOOT: {loot_item['name'].title()}        DROP CHANCE: {enemy['loot']['chance']}%")
            else:
                print("AVAILABLE LOOT: None")
            print()
            return
        
    if len(room["items"]) > 0:
        for item in room["items"]:
            if target_id == item["id"]:
                print("\n — Inspection — \n")
                print(f"NAME: {item["name"].title()}        ITEM ID: {item["id"]}        TYPE: {item["type"]}")
                print(f"DESCRIPTION: {item["description"]}")
                print()
                return
            
    print(f"\nERROR: '{target_id.upper()}' is not a valid object/enemy/item that can be inspected.")
    print("You can inspect objects, enemies or items in your current room, or items from your inventory.\n")



def execute_menu():

    print("\n — Player Stats — \n")
    player.print_health()
    print(f"BASE DAMAGE: {player.equipment["weapon"]["damage"]}")
    print(f"BASE DEFENCE: {player.equipment["armour"]["defence"]}")
    print(f"BASE EVASION: {player.stats["evasion"]}")
    print(f"GOLD: {player.gold}")
    print(f"\nYou are currently in {player.current_room["name"].upper()} on turn {player.current_turn}.\n")



def execute_inventory(items): # Displays the current items in the player's inventory

    print("\n — Your Equipment — \n")
    print(f"WEAPON: {player.equipment["weapon"]["name"].title()} [{player.equipment["weapon"]["id"]}]    DAMAGE: {player.equipment["weapon"]["damage"]}")
    print(f"ARMOUR: {player.equipment["armour"]["name"].title()} [{player.equipment["armour"]["id"]}]    DEFENCE: {player.equipment["armour"]["defence"]}")
    print(f"ACCESSORY: {player.equipment["accessory"]["name"].title()} [{player.equipment["accessory"]["id"]}]   BUFF: {player.equipment["accessory"]["buff_desc"]}")
    print(f"GOLD: {player.gold}")

    print(f"\n — Your Inventory [{len(player.inventory)}/16] —")
    print("FORMAT: (item name) [ (item id) | (item type) ] -> (item description)\n")
    for item in items:
        print(f"{item["name"].title()} [{item["id"]} | {item["type"]}] -> {item["description"]}\n")



# execute_interaction function in file 'interaction_commands.py'
# execute_use function in file 'interaction_commands.py'



def execute_equip(item_id):

    for inv_item in player.inventory:
        if inv_item["id"] == item_id:

            if (inv_item["type"] != "weapon") and (inv_item["type"] != "armour") and (inv_item["type"] != "accessory"):
                print(f"\nERROR: '{item_id.upper()}' cannot be equipped.\n")
                print(inv_item["type"])
                return
            
            else:
                player.inventory.remove(inv_item)
                item_type = inv_item["type"]          

                for equip_item in player.equipment.items():

                    if equip_item[1]["type"] == item_type:
                        equip_item_type = equip_item[1]["type"]

                        match equip_item_type:
                            case "weapon":
                                if equip_item[1] == weapon_default:
                                    break
                                else:
                                    player.inventory.append(equip_item[1])
                                break
                            
                            case "armour":
                                if equip_item[1] == armour_default:
                                    break
                                else:
                                    player.inventory.append(equip_item)
                                break
                            
                            case "accessory":
                                if equip_item[1] == accessory_default:
                                    break
                                else:
                                    player.inventory.append(equip_item[1])
                                break                  

                player.equipment.update({item_type: inv_item})
                print(f"\nYou have equipped {item_id.upper()} as your {item_type}.\n")
                return



def execute_unequip(item_id):

    if item_id == "default":
        print("\nERROR: You cannot unequip that.\n")
        return
    
    if len(player.inventory) == 16:
        print("\nERROR: Your inventory is full. Please drop or store an item away if you want to unequip an item.\n")
        return
    
    for item in player.equipment.items():

        if item[1]["id"] == item_id:
            item_type = item[1]["type"]

            match item_type:
                case "weapon":
                    player.equipment.update({"weapon": weapon_default})
                    player.inventory.append(item[1])
                    print(f"\nYou unequipped your {item[1]["name"].upper()}\n")
                    return
                
                case "armour":
                    player.equipment.update({"armour": armour_default})
                    player.inventory.append(item[1])
                    print(f"\nYou unequipped your {item[1]["name"].upper()}\n")
                    return
                
                case "accessory":
                    player.equipment.update({"accessory": accessory_default})
                    player.inventory.append(item[1])
                    print(f"\nYou unequipped your {item[1]["name"].upper()}\n")
                    return
                
    print(f"\nERROR: '{item_id.upper()}' is not an item you have equipped.\n")



def execute_attack(enemy_id, attack_type):
    room = player.current_room

    if len(room["enemies"]) == 0:
        print("\nERROR: Specified enemy is not in this room or does not exist.\n")

    else:
        room_enemy = room["enemies"][0]["id"]
        if room_enemy != enemy_id:
            print("\nERROR: Specified enemy is not in this room or does not exist.\n")

        elif (attack_type != "normal") and (attack_type != "charge") and (attack_type != "counter"):
            print(f"\nERROR: '{attack_type}' is not a valid attack type (Normal, Charge or Counter).\n")
        
        else:
            turn_change(player_attack, enemy_id, attack_type)



def execute_evade():
    if len(player.current_room["enemies"]) > 0:
        player.change_turn = True
        turn_change(evade_attack)
    else:
        print("\nERROR: You cannot evade an attack when there are no enemies nearby.\n")