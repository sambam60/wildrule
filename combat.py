"""
This file handles the entire combat system of the game.
Attacks can be of 3 attack types: Normal, Charge or Counter attacks.
Normal attacks have no special attributes, and are based off base damage values from its attacker.
Charge attacks have increased damage compared to normal attacks, but takes a turn to charge up before dealing its full damage.
Counter attacks have increased damage if the target is charging up a charge attack, but has decreased damage if target is not charging up a charge attack.
Attacks also have a small chance of being evaded/missed, based off the attacker's attack type and the target's evasion stat ('evade' command guarantees attack evasion).
"""

import random
import player
from map import rooms
from enemies import *



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

                if spawn_chance <= 20:
                    does_enemy_exist = check_enemy_exists(enemy_bull)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_bull)
                        print(f"A wild {enemy_bull["name"].upper()} spots you!\n")

                elif spawn_chance > 20 and spawn_chance <= 40:
                    does_enemy_exist = check_enemy_exists(enemy_bear)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_bear)
                        print(f"A wild {enemy_bear["name"].upper()} spots you!\n")

                elif spawn_chance > 40 and spawn_chance <= 60:
                    does_enemy_exist = check_enemy_exists(enemy_goose)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_goose)
                        print(f"A wild {enemy_goose["name"].upper()} spots you!\n")

                elif spawn_chance > 60 and spawn_chance <= 65:
                    does_enemy_exist = check_enemy_exists(miniboss_giant)
                    if does_enemy_exist == False:
                        room["enemies"].append(miniboss_giant)
                        print(f"A rare {miniboss_giant["name"].upper()} towers overhead, and locks its sights upon you.\n")

            case "Tundra":

                if spawn_chance <= 25:
                    does_enemy_exist = check_enemy_exists(enemy_polarbear)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_polarbear)
                        print(f"A wild {enemy_polarbear["name"].upper()} spots you!\n")

                elif spawn_chance > 25 and spawn_chance <= 50:
                    does_enemy_exist = check_enemy_exists(enemy_leopard)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_leopard)
                        print(f"A wild {enemy_leopard["name"].upper()} spots you!\n")

                elif spawn_chance > 50 and spawn_chance <= 75:
                    does_enemy_exist = check_enemy_exists(enemy_owl)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_owl)
                        print(f"A wild {enemy_owl["name"].upper()} spots you!\n")

                elif spawn_chance > 75 and spawn_chance <= 80:
                    does_enemy_exist = check_enemy_exists(miniboss_werewolf)
                    if does_enemy_exist == False:
                        room["enemies"].append(miniboss_werewolf)
                        print(f"A rare {miniboss_werewolf["name"].upper()} rushes towards you!\n")

            case "Plains":

                if spawn_chance <= 25:
                    does_enemy_exist = check_enemy_exists(enemy_fox)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_fox)
                        print(f"A wild {enemy_fox["name"].upper()} spots you!\n")

                elif spawn_chance > 25 and spawn_chance <= 50:
                    does_enemy_exist = check_enemy_exists(enemy_rhino)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_rhino)
                        print(f"A wild {enemy_rhino["name"].upper()} spots you!\n")

                elif spawn_chance > 50 and spawn_chance <= 75:
                    does_enemy_exist = check_enemy_exists(enemy_elephant)
                    if does_enemy_exist == False:
                        room["enemies"].append(enemy_elephant)
                        print(f"A wild {enemy_elephant["name"].upper()} spots you!\n")

                elif spawn_chance > 75 and spawn_chance <= 80:
                    does_enemy_exist = check_enemy_exists(miniboss_python)
                    if does_enemy_exist == False:
                        room["enemies"].append(miniboss_python)
                        print(f"A rare {miniboss_python["name"].upper()} slithers behind you!\n")

    else:
        enemy_attack() # If current room already has an enemy, the enemy will attack the player instead



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
                
                case "charge": # Charge attack deals 2.5x normal attack damage
                    damage_multiplier = player_charge_multiplier
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = (player_damage - (player_damage * damage_absorbed)) * damage_multiplier
                    return final_damage
                
                case "counter": # Counter attack deals 2x normal damage if enemy is charging up a charge attack, if not then counter attack deals 0.5x damage
                    if enemy_charge_attack["charge"] == True:
                        damage_multiplier = player_counter_multiplier
                    else:
                        damage_multiplier = 0.5
                        
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = (player_damage - (player_damage * damage_absorbed)) * damage_multiplier
                    return final_damage
        
        case "enemy": # When an enemy is attacking the player
            match attack_type:
                case "normal": # Damage based from enemy normal damage stat
                    damage_absorbed = (random.randint(0, (player_defence + player_defence_increase)) / 100)
                    final_damage = enemy_normal_attack["damage"] - (enemy_normal_attack["damage"] * damage_absorbed)
                    return final_damage
                
                case "charge": # Damage based from enemy charge damage stat
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
                
                case "charge": # For enemy charge attacks, chance of player evasion is multiplied by enemy charge attack miss chance multiplier

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
                
                case "charge": # For player charge attacks, chance of enemy evasion is doubled compared to normal attack evasion chance

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

        
        elif (attack_rng > enemy_counter_attack["chance"]) and (attack_rng <= enemy_charge_attack["chance"]): # Chance for enemy to use charge attack: counter chance < rng value < charge chance
            
            enemy_charge_attack["charge"] = True
            print(f"The {enemy_name.upper()} steps back and charges their attack.\n")

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

    match attack_type:
        
        case "normal":

            if selected_enemy["health"] > 0:

                damage_dealt = round(calculate_damage("player", "normal"), 1)
                selected_enemy["health"] = selected_enemy["health"] - damage_dealt

                print(f"You attacked {enemy.upper()} and dealt {damage_dealt} damage.")

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

                    damage_dealt = round(calculate_damage("player", "charge"), 1)
                    selected_enemy["health"] = selected_enemy["health"] - damage_dealt
                    print(f"You charged at {enemy.upper()} and dealt {damage_dealt} damage.")
                    player.charge_attack = False

                    if selected_enemy["health"] <= 0:
                        enemy_killed(selected_enemy)
                    else:
                        print(f"{enemy.upper()} now has {round(selected_enemy["health"], 1)} health.\n")

        case "counter":

            if selected_enemy["health"] > 0:

                    damage_dealt = round(calculate_damage("player", "counter"), 1)
                    selected_enemy["health"] = selected_enemy["health"] - damage_dealt

                    print(f"You countered {enemy.upper()} and dealt {damage_dealt} damage.")

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

    if enemy["id"] == "king":
                print(" * You can go back to the kingdom by entering 'go exit' *\n")
    
    enemy["charge_attack"]["charge"] = False
    player.enemies_killed = player.enemies_killed + 1



def evade_attack(): # Function for the 'evade' command
    player.evade_attack = True