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

        match room["area"]:

            case "Forest":
                spawn_chance = random.randint(1, 100)

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

    else:
        enemy_attack() # If current room already has an enemy, the enemy will attack the player instead



def player_buffs(): # unfinished
    accessory = player.equipment["accessory"]

    match accessory:
        case accessory_ivory:
            return 3



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

    match attacker:
        case "player": # When the player is attacking an enemy
            match attack_type:
                case "normal": # Damage based from player's current weapon
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = player_damage - (player_damage * damage_absorbed)
                    return final_damage
                
                case "charge": # Charge attack deals 2.5x normal attack damage
                    charge_multiplier = player_buffs() # buff accounting will move to a different function later
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = (player_damage - (player_damage * damage_absorbed)) * charge_multiplier
                    return final_damage
                
                case "counter": # Counter attack deals 2x normal damage if enemy is charging up a charge attack, if not then counter attack deals 0.5x damage
                    if enemy_charge_attack["charge"] == True:
                        damage_multiplier = 2
                    else:
                        damage_multiplier = 0.5
                        
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = (player_damage - (player_damage * damage_absorbed)) * damage_multiplier
                    return final_damage
        
        case "enemy": # When an enemy is attacking the player
            match attack_type:
                case "normal": # Damage based from enemy normal damage stat
                    damage_absorbed = (random.randint(0, player_defence) / 100)
                    final_damage = enemy_normal_attack["damage"] - (enemy_normal_attack["damage"] * damage_absorbed)
                    return final_damage
                
                case "charge": # Damage based from enemy charge damage stat
                    damage_absorbed = (random.randint(0, player_defence) / 100)
                    final_damage = (enemy_charge_attack["damage"] - (enemy_charge_attack["damage"] * damage_absorbed))
                    return final_damage
                
                case "counter": # Damage based from enemy counter damage stat
                    if player.charge_attack == True:
                        damage_multiplier = 2
                    else:
                        damage_multiplier = 0.5
                        
                    damage_absorbed = (random.randint(0, enemy_defence) / 100)
                    final_damage = (enemy_counter_attack["damage"] - (player_damage * damage_absorbed)) * damage_multiplier
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

    match target:
        case "player": # Player evasion chance
            match opposition_attack_type:
                case "normal": # For enemy normal attacks, chance of player evasion is equal to the player's evasion stat

                    evasion_rng = random.randint(0, 100)
                    player_evasion_chance = player.stats["evasion"]

                    if evasion_rng <= player_evasion_chance:
                        return True
                    else:
                        return False
                
                case "charge": # For enemy charge attacks, chance of player evasion is multiplied by enemy charge attack miss chance multiplier

                    evasion_rng = random.randint(0, 100)
                    player_evasion_chance = player.stats["evasion"] * enemy_charge_miss

                    if evasion_rng <= player_evasion_chance:
                        return True
                    else:
                        return False
                    
                case "counter": # For enemy counter attacks, chance of player evasion is affected by if player is charging up an attack
                    
                    evasion_rng = random.randint(0, 100)

                    if player.charge_attack == True:
                        player_evasion_chance = player.stats["evasion"] * 0.5
                    else:
                        player_evasion_chance = player.stats["evasion"] * 2

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
            print(f"You evaded {enemy_name.upper().upper()}'s charge attack!\n")
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
                    print(f"You evaded {enemy_name.upper().upper()}'s counter attack!\n")
                    enemy_charge_attack["charge"] = False

                else:
                    damage_dealt = round(calculate_damage("enemy", "counter"), 1)
                    player.stats["health"] = player.stats["health"] - damage_dealt

                    print(f"The {enemy_name.upper()} countered you!")
                    print(f"You took {damage_dealt} damage from the attack. You are now at {round(player.stats["health"], 1)} health.\n")
            
            else:

                attack_evaded = calculate_evade("player", "counter")
                if attack_evaded == True:
                    print(f"You evaded {enemy_name.upper().upper()}'s counter attack!\n")
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
                print(f"You evaded {enemy_name.upper().upper()}'s normal attack!\n")
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

    gold_rng = random.randint(0, int(enemy["gold"] * 0.5))
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


def evade_attack(): # Function for the 'evade' command
    player.evade_attack = True

"""def take_damage(damage):
    global health
    global enemy_posture
    global player_posture
    health -= damage
    player_posture-=1
    enemy_posture=3
    if health < 0:
        health = 0
    return health


def deal_damage(damage):
    global enemy_health
    global enemy_posture
    global player_posture
    enemy_health -= damage
    enemy_posture-=1
    player_posture=3
    if enemy_health < 0:
        enemy_health = 0
    return enemy_health


def posture_break(enemy_posture,player_posture):
    print(f"Your posture is {player_posture}")
    print(f"Enemy posture is {enemy_posture}")
    if enemy_posture <=0:
        deal_damage(50)
        print("Enemy's posture is broken! You dealt extra damage!")
    if player_posture <=0:
        take_damage(50)
        print("Your posture is broken! Enemy dealt extra damage!")

enemy_prompts={
    "Counter":"Enemy is watching you closely",
    "Quick":"Enemy is rushing towards you",
    "Charge":"Enemy is charging up for a big attack"
}

def enemy_prompt(enemy_attack):
    print(enemy_prompts.get(enemy_attack))


"""
"""
def enemy_prompt(enemy_attack):
    if enemy_attack==attack_types[0]:
        print("Enemy is watching you closely")
    elif enemy_attack==attack_types[1]:
        print("Enemy is rushing towards you")
    else:
        print("Enemy is charging up for a big attack")
"""
"""



def quick_attack(enemy_attack):

    if enemy_attack.lower() == attack_types[0].lower():
        take_damage(counterdmg)
        posture_break(enemy_posture,player_posture)
        print(f"Enemy countered! Player health is now {health}.")
    elif enemy_attack.lower() == attack_types[2].lower():
        deal_damage(quickdmg)
        posture_break(enemy_posture,player_posture)
        print(f"Enemy wasn't ready player got a hit Enemy health is now {enemy_health}.")
    else:
        deal_damage(10)
        take_damage(10)
        print(f"Both players rushed! Player health is now {health}, Enemy health is now {enemy_health}.")

def counter_attack(enemy_attack):

    if enemy_attack.lower() == attack_types[2].lower():
        take_damage(chargedmg)
        posture_break(enemy_posture,player_posture)
        print(f"Enemy rushed you! Player health is now {health}.")
    elif enemy_attack.lower() == attack_types[1].lower():
        deal_damage(counterdmg)
        posture_break(enemy_posture,player_posture)
        print(f"Enemy got countered Enemy health is now {enemy_health}.")
    else:
        print("Both players waited, no damage dealt.")
def charge_attack(enemy_attack):

    if enemy_attack.lower() == attack_types[0].lower():
        deal_damage(chargedmg)
        posture_break(enemy_posture,player_posture)
        print(f"Enemy waited too long and got hit! Enemy health is now {enemy_health}.")
    elif enemy_attack.lower() == attack_types[1].lower():
        take_damage(quickdmg)
        posture_break(enemy_posture,player_posture)
        print(f"Enemy rushed through your charge! Player health is now {health}.")
    else:
        deal_damage(20)
        take_damage(20)

        print(f"Both players charged! Player health is now {health}, Enemy health is now {enemy_health}.")
 



while health > 0 and enemy_health > 0:
    enemy_attack=random.choice(attack_types)
    enemy_prompt(enemy_attack)
    while True:
       selected_attack = input("Enter attack type (Counter, Quick, Charge): ").strip().lower()
       if selected_attack in [attack.lower() for attack in attack_types]:
          break
       print(f"Invalid attack type. Please choose from: {', '.join(attack_types)}")
     
    
    if selected_attack.lower() ==attack_types[1].lower():
      quick_attack(enemy_attack)
      
    elif selected_attack.lower() ==attack_types[0].lower():
      counter_attack(enemy_attack)
      
    elif selected_attack.lower() ==attack_types[2].lower():
      charge_attack(enemy_attack)
      
    
    
    if health <=0 and enemy_health <= 0:
        print("Draw!")
        break
    elif enemy_health <= 0:
        print("Enemy has been defeated!")
        break
    elif health <= 0:
        print("Player has been defeated!")
        break
"""