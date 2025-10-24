import random
import player
from enemies import *

status_types = ["idle", "aggressive"]

# Combat system still very early in development right now

#chargedmg=30
#quickdmg=10
#counterdmg=20



def attack_enemy(enemy_id, attack_type):
    selected_enemy = None
    
    for enemy in player.current_room["enemies"]:
        if enemy["id"] == enemy_id:
            selected_enemy = enemy
            break

    if selected_enemy == None:
        print("\nError: Specified enemy is not in this room or does not exist.\n")
        return
    
    player_damage = player.equipment["weapon"]["damage"]
    enemy = selected_enemy["id"]

    match attack_type:
        
        case "quick":

            if selected_enemy["health"] > 0:
                selected_enemy["health"] = selected_enemy["health"] - player_damage
                print(f"\nYou attacked {enemy.upper()} and dealt {player_damage} damage.")
                if selected_enemy["health"] <= 0:
                    print(f"{enemy.upper()} was killed.\n")
                else:
                    print(f"{enemy.upper()} now has {selected_enemy["health"]} health.")

        case "charge":
            pass

        case "counter":
            pass

        case _:
            print(f"\nError: {attack_type} is not a valid attack type (Quick, Charge or Counter).")


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