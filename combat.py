"""
This file handles the entire combat system of the game.
Attacks can be of 3 attack types: Normal, Charge or Counter attacks.
Normal attacks have no special attributes, and are based off base damage values from its attacker.
Charge attacks have increased damage compared to normal attacks, but takes a turn to charge up before dealing its full damage.
Counter attacks have increased damage if the target is charging up a charge attack, but has decreased damage if target is not charging up a charge attack.
Attacks also have a small chance of being evaded/missed, based off the attacker's attack type and the target's evasion stat ('evade' command guarantees attack evasion).
"""

import random
import sys
import time
import select
import player
from map import rooms
from enemies import *



def _print_combat_guide_once() -> None:
    """Print the combat guide only the first time you enter combat."""
    try:
        if not getattr(player, "first_attack", True):
            return
    except Exception:
        return
    print("\n — Combat Guide — \n")
    print("There are three attack types you can use:")
    print("  • NORMAL: Standard damage, no special effects")
    print("  • CHARGE: High damage but requires two turns (first turn: charge up, second turn: attack)")
    print("  • COUNTER: Double damage against charging enemies, half damage otherwise")
    print("\nYou can also EVADE enemy attacks by using 'evade' or 'dodge' commands.")
    print("\nTip: Use 'attack [enemy]' for normal attack, or 'attack [enemy] [type]' for other types.\n")
    player.first_attack = False

def _end_game_if_dead() -> None:
    """Immediately end the game if the player's health is 0 or below."""
    try:
        if player.stats.get("health", 0) > 0:
            return
    except Exception:
        return
    RED = "\033[38;2;255;0;0m"
    RESET = "\033[0m"
    print(f"\n{RED}————————————————————————————————————————————————————————————————————————————————————————————————————{RESET}")
    try:
        if player.current_room.get("enemies") and len(player.current_room["enemies"]) > 0:
            print(f"{RED}GAME OVER: YOU HAVE BEEN KILLED BY THE {player.current_room['enemies'][0]['name'].upper()}{RESET}")
        else:
            print(f"{RED}GAME OVER: YOU HAVE DIED.{RESET}")
    except Exception:
        print(f"{RED}GAME OVER: YOU HAVE DIED.{RESET}")
    print(f"{RED}————————————————————————————————————————————————————————————————————————————————————————————————————{RESET}\n")
    exit()

def check_enemy_exists(enemy): 

    """
    This function checks if a specific enemy already exists in one of the rooms on the map.
    If an enemy already exists in a room, it cannot spawn in another room at the same time.
    """

    enemy_exists = False
    all_rooms = rooms.items()

    for room in all_rooms:
        room_enemies = room[1]["enemies"]
        if enemy in room_enemies:
            enemy_exists = True
            break

    return enemy_exists



def spawn_enemy():

    """
    This function handles how enemies are spawned in the current room, based on the room's area type.
    Most areas should have 3 unique enemies, each with different chances of spawning.
    """

    room = player.current_room
    if len(room["enemies"]) == 0:

        spawn_chance = random.randint(1, 100)
        match room["area"]:

            case "Forest":

                if spawn_chance <= 10:
                    does_enemy_exist = check_enemy_exists(enemy_bull)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_bull)
                        print(f"A wild {enemy_bull["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_bull["id"]

                elif spawn_chance > 10 and spawn_chance <= 18:
                    does_enemy_exist = check_enemy_exists(enemy_bear)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_bear)
                        print(f"A wild {enemy_bear["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_bear["id"]

                elif spawn_chance > 18 and spawn_chance <= 25:
                    does_enemy_exist = check_enemy_exists(enemy_goose)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_goose)
                        print(f"A wild {enemy_goose["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_goose["id"]

                elif spawn_chance > 25 and spawn_chance <= 27:
                    does_enemy_exist = check_enemy_exists(miniboss_giant)
                    if does_enemy_exist == False:
                        room["enemies"].append(miniboss_giant)
                        print(f"A rare {miniboss_giant["name"].upper()} towers overhead, and locks its sights upon you.\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = miniboss_giant["id"]

            case "Tundra":

                if spawn_chance <= 12:
                    does_enemy_exist = check_enemy_exists(enemy_polarbear)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_polarbear)
                        print(f"A wild {enemy_polarbear["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_polarbear["id"]

                elif spawn_chance > 12 and spawn_chance <= 22:
                    does_enemy_exist = check_enemy_exists(enemy_leopard)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_leopard)
                        print(f"A wild {enemy_leopard["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_leopard["id"]

                elif spawn_chance > 22 and spawn_chance <= 30:
                    does_enemy_exist = check_enemy_exists(enemy_owl)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_owl)
                        print(f"A wild {enemy_owl["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_owl["id"]

                elif spawn_chance > 30 and spawn_chance <= 32:
                    does_enemy_exist = check_enemy_exists(miniboss_werewolf)
                    if does_enemy_exist == False:
                        room["enemies"].append(miniboss_werewolf)
                        print(f"A rare {miniboss_werewolf["name"].upper()} rushes towards you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = miniboss_werewolf["id"]

            case "Plains":

                if spawn_chance <= 12:
                    does_enemy_exist = check_enemy_exists(enemy_fox)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_fox)
                        print(f"A wild {enemy_fox["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_fox["id"]

                elif spawn_chance > 12 and spawn_chance <= 22:
                    does_enemy_exist = check_enemy_exists(enemy_rhino)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_rhino)
                        print(f"A wild {enemy_rhino["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_rhino["id"]

                elif spawn_chance > 22 and spawn_chance <= 30:
                    does_enemy_exist = check_enemy_exists(enemy_elephant)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_elephant)
                        print(f"A wild {enemy_elephant["name"].upper()} spots you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = enemy_elephant["id"]

                elif spawn_chance > 30 and spawn_chance <= 32:
                    does_enemy_exist = check_enemy_exists(miniboss_python)
                    if does_enemy_exist == False:
                        room["enemies"].append(miniboss_python)
                        print(f"A rare {miniboss_python["name"].upper()} slithers behind you!\n")
                        _print_combat_guide_once()
                        if getattr(player, "time_based_combat", False):
                            player.pending_precombat = miniboss_python["id"]

    else:
        # If current room already has an enemy
        if getattr(player, "time_based_combat", False) and not getattr(player, "locked_in_combat", False):
            # Trigger pre-combat instead of immediate attack
            try:
                player.pending_precombat = room["enemies"][0]["id"]
            except Exception:
                pass
        else:
            enemy_attack() # Default behaviour: enemy attacks



def calculate_damage(attacker, attack_type):

    """
    This helper function is used to calculate the magnitude of damage an attacker does to its target based on the chosen attack type.
    Damage is first chosen based on the attack type, then altered based on specific conditions such as target defence values.
    """

    player_damage = player.equipment["weapon"]["damage"]
    player_defence = player.equipment["armour"]["defence"]
    enemy = player.current_room["enemies"][0]
    enemy_health = enemy["health"]
    enemy_defence = enemy["defence"]
    enemy_normal_attack = enemy["normal_attack"]
    enemy_charge_attack = enemy["charge_attack"]
    enemy_counter_attack = enemy["counter_attack"]

    final_damage = 0

    player_charge_multiplier = 2.5
    player_counter_multiplier = 2
    player_defence_increase = 0

    match player.equipment["accessory"]["id"]:
        case "horn":
            player_charge_multiplier = 3
        case "feather":
            player_counter_multiplier = 2.5
        case "hide":
            player_defence_increase = 10
        case _:
            pass

    match attacker:
        case "player": # When the player is attacking an enemy
            match attack_type:
                case "normal": # Damage based from player's current weapon
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = player_damage - (player_damage * damage_absorbed)
                    return final_damage
                
                case "charge" | "charged": # Charge attack deals 2.5x normal attack damage
                    damage_multiplier = player_charge_multiplier
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = (player_damage - (player_damage * damage_absorbed)) * damage_multiplier
                    return final_damage
                
                case "counter": # Counter always exceeds normal; higher if enemy is charging
                    if enemy_charge_attack["charge"] == True:
                        # Enemy preparing a charge -> use boosted counter multiplier
                        damage_multiplier = player_counter_multiplier  # default 2.0, 2.5 with feather
                    else:
                        # Not charging -> still stronger than normal
                        damage_multiplier = 1.5
                        
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = (player_damage - (player_damage * damage_absorbed)) * damage_multiplier
                    return final_damage
        
        case "enemy": # When an enemy is attacking the player
            match attack_type:
                case "normal": # Damage based from enemy normal damage stat
                    damage_absorbed = (random.randint(0, (player_defence + player_defence_increase)) / 100)
                    final_damage = enemy_normal_attack["damage"] - (enemy_normal_attack["damage"] * damage_absorbed)
                    return final_damage
                
                case "charge" | "charged": # Damage based from enemy charge damage stat
                    damage_absorbed = (random.randint(0, (player_defence + player_defence_increase)) / 100)
                    final_damage = (enemy_charge_attack["damage"] - (enemy_charge_attack["damage"] * damage_absorbed))
                    return final_damage
                
                case "counter": # Damage based from enemy counter damage stat
                    if player.charge_attack == True:
                        damage_multiplier = 2
                    else:
                        damage_multiplier = 0.5
                        
                    damage_absorbed = (random.randint(0, (player_defence + player_defence_increase)) / 100)
                    base_damage = enemy_counter_attack["damage"]
                    final_damage = (base_damage - (base_damage * damage_absorbed)) * damage_multiplier
                    return final_damage
                
                case "dodge":
                    pass
    


def calculate_evade(target, opposition_attack_type):

    """
    This helper function is used to calculate whether an attack is evaded by its target.
    Chance of evasion is affected by target evasion value, attack type etc.
    """

    enemy = player.current_room["enemies"][0]
    enemy_evasion = enemy["evasion"]
    enemy_charge_miss = enemy["charge_attack"]["miss_multiplier"]
    enemy_charge = enemy["charge_attack"]["charge"]
    player_evasion_increase = 0

    match player.equipment["accessory"]["id"]:
        case "paw":
            player_evasion_increase = 25
        case _:
            pass

    match target:
        case "player": # Player evasion chance
            match opposition_attack_type:
                case "normal": # For enemy normal attacks, chance of player evasion is equal to the player's evasion stat

                    evasion_rng = random.randint(0, 100)
                    player_evasion_chance = player.stats["evasion"] + player_evasion_increase

                    if evasion_rng <= player_evasion_chance:
                        return True
                    else:
                        return False
                
                case "charge" | "charged": # For enemy charge attacks, or if labelled 'charged', chance of player evasion is multiplied by enemy charge attack miss chance multiplier

                    evasion_rng = random.randint(0, 100)
                    player_evasion_chance = (player.stats["evasion"] + player_evasion_increase) * enemy_charge_miss

                    if evasion_rng <= player_evasion_chance:
                        return True
                    else:
                        return False
                    
                case "counter": # For enemy counter attacks, chance of player evasion is affected by if player is charging up an attack
                    
                    evasion_rng = random.randint(0, 100)

                    if player.charge_attack == True:
                        player_evasion_chance = (player.stats["evasion"] + player_evasion_increase) * 0.5
                    else:
                        player_evasion_chance = (player.stats["evasion"] + player_evasion_increase) * 2

                    if evasion_rng <= player_evasion_chance:
                        return True
                    else:
                        return False

                    
                
        case "enemy": # Enemy evasion chance
            match opposition_attack_type:
                case "normal": # For player normal attacks, chance of enemy evasion is equal to the enemy's evasion stat

                    evasion_rng = random.randint(0, 100)
                    if evasion_rng <= enemy_evasion:
                        return True
                    else:
                        return False
                
                case "charge" | "charged": # For player charge attacks, chance of enemy evasion is doubled compared to normal attack evasion chance

                    evasion_rng = random.randint(0, 100)
                    if evasion_rng <= (enemy_evasion * 2):
                        return True
                    else:
                        return False
                    
                case "counter": # For player counter attacks, chance of enemy evasion is affected by if enemy is charging up an attack
                    
                    evasion_rng = random.randint(0, 100)

                    if enemy_charge == True:
                        counter_evasion = enemy_evasion * 0.5
                    else:
                        counter_evasion = enemy_evasion * 2
                        
                    if evasion_rng <= counter_evasion:
                        return True
                    else:
                        return False



def enemy_attack():

    """
    This function handles enemy attacks towards the player.
    """

    player_damage = player.equipment["weapon"]["damage"]
    player_defence = player.equipment["armour"]["defence"]
    enemy = player.current_room["enemies"][0]
    enemy_name = enemy["name"]
    enemy_health = enemy["health"]
    enemy_normal_attack = enemy["normal_attack"]
    enemy_charge_attack = enemy["charge_attack"]
    enemy_counter_attack = enemy["counter_attack"]

    attack_rng = random.randint(1, 100) # RNG 1-100
    
    if player.evade_attack == True:
        print(f"You successfully evaded the {enemy_name.upper()}'s attack!\n")
        enemy_charge_attack["charge"] = False
        player.evade_attack = False
        return

    if enemy_charge_attack["charge"] == True: # Enemy charge attack logic

        attack_evaded = calculate_evade("player", "charge")
        if attack_evaded == True:
            print(f"You evaded {enemy_name.upper()}'s charge attack!\n")
            enemy_charge_attack["charge"] = False

        else:

            damage_dealt = round(calculate_damage("enemy", "charge"), 1)
            player.stats["health"] = player.stats["health"] - damage_dealt
            enemy_charge_attack["charge"] = False

            print(f"The {enemy_name.upper()} charged at you!")
            print(f"You took {damage_dealt} damage from the charge attack. You are now at {round(player.stats["health"], 1)} health.\n")
            _end_game_if_dead()
    
    else:

        if attack_rng <= enemy_counter_attack["chance"]: # Chance for enemy to use counter attack: rng value  < counter chance

            if player.charge_attack == True:

                attack_evaded = calculate_evade("player", "counter")
                if attack_evaded == True:
                    print(f"You evaded {enemy_name.upper()}'s counter attack!\n")
                    enemy_charge_attack["charge"] = False

                else:
                    damage_dealt = round(calculate_damage("enemy", "counter"), 1)
                    player.stats["health"] = player.stats["health"] - damage_dealt

                    print(f"The {enemy_name.upper()} countered you!")
                    print(f"You took {damage_dealt} damage from the attack. You are now at {round(player.stats["health"], 1)} health.\n")
                    _end_game_if_dead()
            
            else:

                attack_evaded = calculate_evade("player", "counter")
                if attack_evaded == True:
                    print(f"You evaded {enemy_name.upper()}'s counter attack!\n")
                    enemy_charge_attack["charge"] = False

                else:

                    damage_dealt = round(calculate_damage("enemy", "counter"), 1)
                    player.stats["health"] = player.stats["health"] - damage_dealt

                    print(f"The {enemy_name.upper()} tried to counter you, but you weren't charging up an attack.")
                    print(f"You took {damage_dealt} damage from the attack. You are now at {round(player.stats["health"], 1)} health.\n")
                    _end_game_if_dead()

        
        elif (attack_rng > enemy_counter_attack["chance"]) and (attack_rng <= enemy_charge_attack["chance"]): # Chance for enemy to use charge attack: counter chance < rng value < charge chance
            
            enemy_charge_attack["charge"] = True
            _print_combat_guide_once()
            RED = "\033[38;2;255;0;0m"
            RESET = "\033[0m"
            print(f"{RED}The {enemy_name.upper()} is PREPARING A CHARGED ATTACK!{RESET}")
            print("The foe steps back and charges their attack.\n")

        else: # If rng for counter and charge attack fails, enemy will attack normally

            attack_evaded = calculate_evade("player", "normal")
            if attack_evaded == True:
                print(f"You evaded {enemy_name.upper()}'s normal attack!\n")
                enemy_charge_attack["charge"] = False

            else:
                damage_dealt = round(calculate_damage("enemy", "normal"), 1)
                player.stats["health"] = player.stats["health"] - damage_dealt

                print(f"The {enemy_name.upper()} attacks you!")
                print(f"You took {damage_dealt} damage from the attack. You are now at {round(player.stats["health"], 1)} health.\n")
                _end_game_if_dead()


def _instant_enemy_hit(extra_multiplier: float = 1.0) -> None:
    """Resolve an immediate enemy attack, optionally with extra damage multiplier."""
    try:
        enemy = player.current_room["enemies"][0]
    except Exception:
        return
    enemy_name = enemy.get("name", "enemy")
    enemy_charge_attack = enemy.get("charge_attack", {})
    # Determine attack type
    attack_type = "charged" if enemy_charge_attack.get("charge", False) else "normal"
    base = calculate_damage("enemy", attack_type if attack_type != "charged" else "charged")
    dmg = round(base * extra_multiplier, 1)
    player.stats["health"] -= dmg
    if attack_type == "charged":
        print(f"The {enemy_name.upper()} unleashed a CHARGED strike! You took {dmg} damage.")
        enemy_charge_attack["charge"] = False
    else:
        print(f"The {enemy_name.upper()} struck you! You took {dmg} damage.")
    _end_game_if_dead()


def timed_enemy_attack():
    """Concurrent enemy countdown that can be interrupted by player input.

    - Duration is random: short/medium/long
    - Bar flashes if the enemy is charged
    - If player types 'evade'/'dodge' -> run timed evade; success cancels attack, fail takes damage
    - If player types 'attack [enemy] [type?]' -> perform player's timed attack; enemy attack is cancelled
    - Any other input cancels the enemy attack for this cycle
    """
    try:
        enemy = player.current_room["enemies"][0]
    except Exception:
        return enemy_attack()

    # Visuals
    RED = "\033[38;2;255;0;0m"
    BRIGHT = "\033[1m"
    RESET = "\033[0m"

    # Reserve a line for the bar above the prompt
    print()

    while True:
        # Randomize duration (short/medium/long)
        duration_seconds = random.choice([2.5, 5.0, 7.0])
        total_ticks = 20
        tick_time = max(0.04, duration_seconds / total_ticks)

        # Determine if enemy currently charged
        try:
            enemy = player.current_room["enemies"][0]
        except Exception:
            return
        is_charged = bool(enemy.get("charge_attack", {}).get("charge", False))
        if is_charged:
            # One-time notice per cycle
            RED = "\033[38;2;255;0;0m"
            RESET = "\033[0m"
            sys.stdout.write(f"\n{RED}The {enemy.get('name','ENEMY').upper()} is PREPARING A CHARGED ATTACK!{RESET}\n")
            sys.stdout.flush()

        for t in range(total_ticks, 0, -1):
            # Non-blocking input check
            ready, _, _ = select.select([sys.stdin], [], [], 0)
            if ready:
                try:
                    raw = sys.stdin.readline()
                except Exception:
                    raw = ""
                cmd = (raw or "").strip().lower().split()
                # stop bar rendering line
                sys.stdout.write("\033[s\033[1A\r\033[0K\033[u")
                sys.stdout.flush()

                # Handle interrupts
                if len(cmd) == 0:
                    # blank input -> instant hit with 25% extra damage, continue bar
                    _instant_enemy_hit(extra_multiplier=1.25)
                    break

                if cmd[0] in {"evade", "dodge"}:
                    zone, success = prompt_evade_indicator(duration_seconds=1.0)
                    if success:
                        print("You slipped away from the attack!")
                        # Successful evade cancels this attack; continue new cycle
                        break
                    else:
                        print("Your evade failed!\n")
                        # Failed evade -> enemy lands its attack now; continue next cycle
                        enemy_attack()
                        break

                if cmd[0] == "attack":
                    # Parse: attack enemy [type]
                    enemy_id = None
                    atk_type = "normal"
                    if len(cmd) >= 2:
                        enemy_id = cmd[1]
                    if len(cmd) >= 3:
                        atk_type = cmd[2]
                    if enemy_id == enemy.get("id"):
                        # Perform player's attack directly (cancel this enemy attack)
                        player_attack(enemy_id, atk_type)
                        # 30% chance of immediate counter
                        if random.random() < 0.3:
                            dmg = round(calculate_damage("enemy", "counter"), 1)
                            player.stats["health"] -= dmg
                            print(f"The {enemy['name'].upper()} countered your strike for {dmg} damage!")
                        # If enemy died, stop
                        try:
                            _ = player.current_room["enemies"][0]
                        except Exception:
                            return
                        break
                    else:
                        # Wrong target -> instant hit with 25% extra damage
                        _instant_enemy_hit(extra_multiplier=1.25)
                        break

                # Any other input -> instant hit with 25% extra damage
                _instant_enemy_hit(extra_multiplier=1.25)
                break

            # Draw bar
            sys.stdout.write("\033[s\033[1A\r")
            if is_charged and (t % 2 == 0):
                # flash by toggling brightness
                sys.stdout.write(f"Enemy preparing attack: {BRIGHT}{RED}{'|'*t}{RESET}    \033[0K")
            else:
                sys.stdout.write(f"Enemy preparing attack: {RED}{'|'*t}{RESET}    \033[0K")
            sys.stdout.write("\033[u")
            sys.stdout.flush()
            time.sleep(tick_time)

        else:
            # Countdown completed -> enemy attacks now
            sys.stdout.write("\033[s\033[1A\r\033[0K\033[u")
            sys.stdout.flush()
            enemy_attack()
            # continue looping for next cycle
            continue

        # After handling an input event or instant hit, continue next cycle if still in combat
        try:
            if len(player.current_room.get("enemies", [])) == 0:
                return
        except Exception:
            return
        # loop continues to render bar again



def player_attack(enemy_id, attack_type):

    """
    This functions handles how the player attacks an enemy.
    """

    room_enemies = player.current_room["enemies"]
    selected_enemy = None
    
    for enemy in room_enemies:
        if enemy["id"] == enemy_id:
            selected_enemy = enemy
            break

    enemy = selected_enemy["id"]

    # helper: apply time-based bonuses
    def _apply_time_bonuses(base_damage: float) -> tuple[float, str]:
        note = ""
        final_damage = base_damage
        if getattr(player, "time_based_combat", False) and getattr(player, "locked_in_combat", False):
            # Timed strike indicator
            zone, mult = prompt_timed_indicator()
            final_damage *= mult
            note = f" [Timed: {zone}]"
            # One-time precombat bonus (if any)
            bonus = getattr(player, "precombat_bonus", None)
            if bonus:
                final_damage *= bonus
                note += " [Precombat Bonus]"
                player.precombat_bonus = None
        return final_damage, note

    match attack_type:
        
        case "normal":

            if selected_enemy["health"] > 0:

                base = round(calculate_damage("player", "normal"), 1)
                damage_dealt, tnote = _apply_time_bonuses(base)
                selected_enemy["health"] = selected_enemy["health"] - damage_dealt

                print(f"You attacked {enemy.upper()} and dealt {round(damage_dealt,1)} damage.{tnote}")

                if selected_enemy["health"] <= 0:
                    enemy_killed(selected_enemy)
                else:
                    print(f"{enemy.upper()} now has {round(selected_enemy["health"], 1)} health.\n")

        case "charge":

            if player.charge_attack == False:
                print(f"You readied your weapon for a charge attack.\nEnter this command again to finalise your attack.\n")
                player.charge_attack = True

            else:
                if selected_enemy["health"] > 0:

                    base = round(calculate_damage("player", "charge"), 1)
                    damage_dealt, tnote = _apply_time_bonuses(base)
                    selected_enemy["health"] = selected_enemy["health"] - damage_dealt
                    print(f"You charged at {enemy.upper()} and dealt {round(damage_dealt,1)} damage.{tnote}")
                    player.charge_attack = False

                    if selected_enemy["health"] <= 0:
                        enemy_killed(selected_enemy)
                    else:
                        print(f"{enemy.upper()} now has {round(selected_enemy["health"], 1)} health.\n")

        case "counter":

            if selected_enemy["health"] > 0:

                    base = round(calculate_damage("player", "counter"), 1)
                    damage_dealt, tnote = _apply_time_bonuses(base)
                    selected_enemy["health"] = selected_enemy["health"] - damage_dealt

                    print(f"You countered {enemy.upper()} and dealt {round(damage_dealt,1)} damage.{tnote}")

                    if selected_enemy["charge_attack"]["charge"] == False:
                        print(f"Since {enemy.upper()} was not charging up an attack, your counter attack dealt less damage.")

                    if selected_enemy["health"] <= 0:
                        enemy_killed(selected_enemy)
                    else:
                        print(f"{enemy.upper()} now has {round(selected_enemy["health"], 1)} health.\n")



def enemy_killed(enemy):
    room_enemies = player.current_room["enemies"]
    room_enemies.remove(enemy)
    enemy["health"] = enemy["max_health"]

    gold_rng = random.randint(0, int(enemy["gold"] * 0.25))
    gold_gained = enemy["gold"] - gold_rng
    player.gold = (player.gold + gold_gained)

    if enemy["loot"]["item"] != None:
        loot_rng = random.randint(0, 100)
        if loot_rng <= enemy["loot"]["chance"]:
            player.inventory.append(enemy["loot"]["item"])
            print(f"\n{enemy["name"].upper()} was killed! You gained {gold_gained} gold.")
            print(f"The {enemy["name"].upper()} dropped a {enemy["loot"]["item"]["name"].upper()}! You took it.\n")
            enemy["loot"]["item"] = None
        else:
            print(f"\n{enemy["name"].upper()} was killed! You gained {gold_gained} gold.\n")
    else:
        print(f"\n{enemy["name"].upper()} was killed! You gained {gold_gained} gold.\n")
    
    enemy["charge_attack"]["charge"] = False
    # Reset combat state for time-based mode
    player.locked_in_combat = False
    player.pending_precombat = None
    player.precombat_bonus = None
    player.active_indicator_bonus = None


def evade_attack(): # Function for the 'evade' command
    player.evade_attack = True


def prompt_timed_indicator(duration_seconds: float = 3.0) -> tuple[str, float]:
    """Moving indicator with small RED, then thin YELLOW and WHITE tail (red not at end)."""
    total_ticks = 40
    tick_time = max(0.02, duration_seconds / total_ticks)

    # Segments: [0..27]=white lead, [28..31]=red small, [32..33]=yellow thin, [34..39]=white tail
    RED_START, RED_END = 28, 31
    YEL_START, YEL_END = 32, 33

    WHITE = "\033[37m"
    YELLOW = "\033[33m"
    RED = "\033[38;2;255;0;0m"
    RESET = "\033[0m"

    chars = []
    for i in range(total_ticks):
        if RED_START <= i <= RED_END:
            chars.append(f"{RED}▉{RESET}")
        elif YEL_START <= i <= YEL_END:
            chars.append(f"{YELLOW}▉{RESET}")
        else:
            chars.append(f"{WHITE}▉{RESET}")
    bar_str = "".join(chars)

    sys.stdout.write("Time your strike! Press ENTER near the RED.\n")
    sys.stdout.flush()

    pos = 0
    while pos < total_ticks:
        caret = " " * pos + "^"
        sys.stdout.write(f"\r{bar_str}\n{caret}\r")
        sys.stdout.flush()
        ready, _, _ = select.select([sys.stdin], [], [], tick_time)
        if ready:
            try:
                _ = sys.stdin.readline()
            except Exception:
                pass
            break
        pos += 1

    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

    if RED_START <= pos <= RED_END:
        return ("red", 1.5)
    if YEL_START <= pos <= YEL_END:
        return ("yellow", 1.25)
    return ("white", 1.0)


def prompt_evade_indicator(duration_seconds: float = 1.0) -> tuple[str, bool]:
    """Evade indicator: small GREEN success band, rest WHITE. Returns (zone, success)."""
    total_ticks = 35
    tick_time = max(0.02, duration_seconds / total_ticks)

    GREEN = "\033[38;2;0;200;0m"
    WHITE = "\033[37m"
    RESET = "\033[0m"

    # Thinner green band not at the end
    GREEN_START, GREEN_END = 26, 28

    chars = []
    for i in range(total_ticks):
        if GREEN_START <= i <= GREEN_END:
            chars.append(f"{GREEN}▉{RESET}")
        else:
            chars.append(f"{WHITE}▉{RESET}")
    bar_str = "".join(chars)

    sys.stdout.write("Time your dodge! Press ENTER in GREEN.\n")
    sys.stdout.flush()

    pos = 0
    while pos < total_ticks:
        caret = " " * pos + "^"
        sys.stdout.write(f"\r{bar_str}\n{caret}\r")
        sys.stdout.flush()
        ready, _, _ = select.select([sys.stdin], [], [], tick_time)
        if ready:
            try:
                _ = sys.stdin.readline()
            except Exception:
                pass
            break
        pos += 1

    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()

    success = (GREEN_START <= pos <= GREEN_END)
    return ("green" if success else "white", success)