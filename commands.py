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
            if player.current_room != rooms.get("Dungeon"):
                spawn_enemy()

        case "player_attack":
            if len(player.current_room["enemies"]) > 0:
                if player.current_room["enemies"][0]["health"] >= 0:
                    if getattr(player, "time_based_combat", False) and getattr(player, "locked_in_combat", False):
                        try:
                            timed_enemy_attack()
                        except Exception:
                            enemy_attack()
                    else:
                        enemy_attack()
                    # Always show current HP after the attack turn resolves
                    try:
                        player.print_health()
                    except Exception:
                        pass

        case "evade_attack":
            if getattr(player, "time_based_combat", False) and getattr(player, "locked_in_combat", False):
                try:
                    timed_enemy_attack()
                except Exception:
                    enemy_attack()
            else:
                enemy_attack()
            # Always show current HP after the attack turn resolves
            try:
                player.print_health()
            except Exception:
                pass



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
                # Attack with just enemy name - default to normal attack
                player.change_turn = True
                execute_attack(command[1], "normal")
            else:
                print("\nERROR: Please specify the enemy to attack.\n")
                print("Usage: attack [enemy] [attack type]\n")
                print("Attack types: normal, charge, counter\n")
                print("You can also use 'attack [enemy]' to perform a normal attack.\n")

        case "evade":
            execute_evade()

        case "dodge":
            execute_evade()

        case "quit":
            exit()

        case "test":
           print(obj_chest1["state"])
           print(obj_chest2["state"])
           print(obj_chest3["state"])

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



def print_room_interactions(room):
    
    if len(room["interacts"]) > 0:
        room_interactions = list_of_items(room["interacts"])
        print(f"There is {room_interactions} nearby.\n")



def _start_skip_listener(skip_event):
    """Spawn a background thread that watches for skip key presses. Returns the thread or None."""
    stdin = getattr(sys, "stdin", None)
    if stdin is None:
        return None
    try:
        if not stdin.isatty():
            return None
    except Exception:
        return None

    def _listener():
        try:
            import msvcrt  # type: ignore

            while not skip_event.is_set():
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    try:
                        decoded = key.decode("utf-8")
                    except Exception:
                        continue
                    if decoded.lower() in {" ", "s"}:
                        skip_event.set()
                        return
        except ImportError:
            try:
                import termios
                import tty
                import select

                fd = stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)
                    while not skip_event.is_set():
                        ready, _, _ = select.select([stdin], [], [], 0.05)
                        if ready:
                            char = stdin.read(1)
                            if char and char.lower() in {" ", "s"}:
                                skip_event.set()
                                return
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception:
                return

    listener = threading.Thread(target=_listener, daemon=True)
    listener.start()
    return listener


def print_slowly(text, delay=0.03):
    """Print text character by character with a small delay. Press 'SPACE' to skip."""
    text = str(text)
    skip_event = threading.Event()
    listener = _start_skip_listener(skip_event)

    for idx, char in enumerate(text):
        if skip_event.is_set():
            remaining = text[idx:]
            if remaining:
                print(remaining, end="", flush=True)
            break
        print(char, end="", flush=True)
        time.sleep(delay)
    else:
        # Loop finished without skip; ensure trailing newline.
        print()
        skip_event.set()
        if listener is not None:
            try:
                listener.join(timeout=0.1)
            except Exception:
                pass
        return

    # Skip was triggered, ensure we finish the line and then newline.
    print()
    skip_event.set()
    if listener is not None:
        try:
            listener.join(timeout=0.1)
        except Exception:
            pass



def print_room(room): # Displays details of the current room when room changes occur

    # Reset precombat/timed state on entering a room
    if getattr(player, "time_based_combat", False):
        player.pending_precombat = None
        player.locked_in_combat = False
        player.precombat_bonus = None

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
    print()
    print_room_items(room)
    print_room_interactions(room)
    print()
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

    match player.current_room["id"]:

        case "plains_s":
            if direction == "south":
                if npc_guard["state"] < 2:
                    print("\nYou cannot go south because the city gate is locked.\n")
                    return False
                elif npc_guard["state"] == 2:
                    return True
            
        case "kingdom_south":
            if direction == "dungeon":
                if npc_dungeonkeeper["state"] < 2:
                    print("\nYou cannot enter the dungeon because the dungeon gate is locked.\n")
                    return False
                elif npc_guard["state"] == 2:
                    return True
                
        case "dungeon":
            has_sword = False
            for item in player.inventory:
                if item["id"] == "templesword":
                    has_sword = True
                    break

            if has_sword == False:
                print("\nThe dungeon gate is locked from the outside. Seems like you're all on your own now.\n")
                return False
            else:
                return True
        
        case _:
            return True
        


def move(exits, direction):

    return rooms[exits[direction]]

# Commands

def explore_room(room):
    if room["explored"] == False:
        room["explored"] = True

def execute_go(direction): # Movement command
    if getattr(player, "time_based_combat", False) and getattr(player, "locked_in_combat", False):
        print("\nERROR: You cannot leave while in combat.\n")
        return

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

                case "dungeon":
                    if player.current_room["id"] != "kingdom_south":
                        print(f"\nERROR: '{direction}' is not a valid exit or does not exist.\n")
                    else:
                        confirmation = None
                        while confirmation == None:
                            confirmation = str(input("You cannot leave once you enter the dungeon. Are you sure you want to enter? (y/n) "))
                            if confirmation == "y" or confirmation == "yes":
                                player.current_room = rooms.get("Dungeon")
                                player.change_turn = True
                                turn_change(print_room, player.current_room)
                                explore_room(player.current_room)
                            else:
                                print(confirmation)
                                print("\nYou decided you are not ready yet.\n")

                case "exit":
                    if player.current_room["id"] != "dungeon":
                        print(f"\nERROR: '{direction}' is not a valid exit or does not exist.\n")
                    else:
                        player.current_room = rooms.get("Kingdom_S")
                        player.change_turn = True
                        turn_change(print_room, player.current_room)
                        explore_room(player.current_room)
                        
                case _:
                    print(f"\nERROR: '{direction}' is not a valid exit or does not exist.\n")

        except KeyError:
            print(f"\nERROR: The current room does not have a valid exit in the inputted direction '{direction}'.\n")



def execute_wait():
    print("You waited for one turn.\n")
    # In time-based mode, waiting should still advance enemy actions if in combat
    if getattr(player, "time_based_combat", False) and getattr(player, "locked_in_combat", False):
        try:
            timed_enemy_attack()
        except Exception:
            enemy_attack()



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



def execute_drop(item_id): # drop item command
    
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
    # Take items from current room
    for item in room_items:
        print(f"TAKE {item["id"].upper()} to take {item["name"]}.")
    # Valid interactions in the current room
    for interact in player.current_room["interacts"]:
        print(f"INTERACT {interact["id"].upper()} to interact with {interact["name"]}.")
    # Valid interactions for enemies in the current room
    for enemy in player.current_room["enemies"]:
        print(f"ATTACK {player.current_room["enemies"][0]["id"].upper()} [attack type] to attack the {player.current_room["enemies"][0]["name"]}.")
        print(f"  (You can use 'attack {player.current_room["enemies"][0]["id"].upper()}' for normal attack)")
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
    print("WAIT to skip the current turn.")
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
            
    if len(room["interacts"]) > 0:
        for interact in room["interacts"]:
            if target_id == interact["id"]:
                print("\n — Inspection — \n")
                print(f"NAME: {interact["name"].title()}        INTERACTION ID: {interact["id"]}        TYPE: interaction")
                print(f"DESCRIPTION: {interact["description"]}")
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
    
    # Combat guide now shown when combat starts (spawn or charge), not on first attack

    if len(room["enemies"]) == 0:
        print("\nERROR: Specified enemy is not in this room or does not exist.\n")

    else:
        room_enemy = room["enemies"][0]["id"]
        if room_enemy != enemy_id:
            print("\nERROR: Specified enemy is not in this room or does not exist.\n")

        elif (attack_type != "normal") and (attack_type != "charge") and (attack_type != "counter"):
            print(f"\nERROR: '{attack_type}' is not a valid attack type (normal, charge or counter).\n")
        
        else:
            # If time-based combat and not locked yet but enemy present, lock now
            if getattr(player, "time_based_combat", False) and not getattr(player, "locked_in_combat", False):
                player.locked_in_combat = True
                # precombat quick-enter bonus if this attack was during pending precombat
                if getattr(player, "pending_precombat", None) == enemy_id:
                    player.precombat_bonus = 1.25
                player.pending_precombat = None
            turn_change(player_attack, enemy_id, attack_type)



def execute_evade():
    if len(player.current_room["enemies"]) > 0:
        player.change_turn = True
        turn_change(evade_attack)
    else:
        print("\nERROR: You cannot evade an attack when there are no enemies nearby.\n")