"""
This file acts as the merchant system, which is used as an item shop for the player. 
It allows the user to buy or sell items during their adventure. The merchant will be 
accessible in certain locations within the over world, helping the player earn stronger 
items as they collect more 'gold,' which is the currency used towards buying items.
"""
from map import rooms
import player
from items import *
from interactions import *
from interaction_commands import *
import time
import sys
import threading
import queue
import textwrap
import tts
import voice_input

village_shop = [weapon_spear, armour_wooden_shield, accessory_badge, item_healing_potion, item_chest_key, item_city_key_1]
igloo_shop = [weapon_club, armour_jacket, item_healing_potion, item_chest_key, item_city_key_2]
kingdom_shop = [weapon_longsword, armour_chainmail, item_healing_potion, item_chest_key]

def open_shop():
    global village_shop
    global igloo_shop
    global kingdom_shop

    match player.current_room["id"]:

        case "village_e":
            npc_merchant["inventory"] = []
            items_for_sale = village_shop
            for item in items_for_sale:
                npc_merchant["inventory"].append(item)

        case "igloos_w":
            npc_merchant["inventory"] = []
            items_for_sale = igloo_shop
            for item in items_for_sale:
                npc_merchant["inventory"].append(item)

        case "kingdom_north":
            npc_merchant["inventory"] = []
            items_for_sale = kingdom_shop
            for item in items_for_sale:
                npc_merchant["inventory"].append(item)

    print("\nMerchant: Greetings! How may I help you today?")

    main_input = None
    while main_input == None:
        print("\nWhat do you want to do?")
        print("1 - Buy Item")
        print("2 - Sell Item")
        print("3 - Exit")
        
        main_input = str(input("> "))
        match main_input:

            case "1":

                buy_input = None
                success = False
                print(f"\nMerchant: What do you want to buy? You have {player.gold} gold.\n")

                for item in npc_merchant["inventory"]:
                    print(f"ITEM: {item["name"].title()}        ID: {item["id"]}        TYPE: {item["type"]}        BUY PRICE: {item["price"]} gold")
                    print(f"DESCRIPTION: {item["description"]}")
                    print()
                print("Enter 'back' to go back to the main shop menu.\n")

                while buy_input == None:
                    buy_input = str(input("Enter an Item ID > "))

                    if buy_input == "back":
                        main_input = None
                        break

                    for item in npc_merchant["inventory"]:
                        if buy_input == item["id"]:
                            if player.inventory == 16:
                                print(f"\nERROR: You cannot buy {buy_input.upper()} because your inventory is full. Please drop, sell or store away an item from your inventory in order to buy an item.\n")
                                success = True
                                main_input = None
                                break
                            else:
                                print(f"You have successfully bought {item["name"].upper()} for {item["price"]} gold.")
                                print(f"You now have {player.gold} gold.")
                                player.gold = player.gold - item["price"]
                                player.inventory.append(item)

                                if item == item_city_key_1 or item == item_city_key_2:
                                    npc_merchant["inventory"].remove(item)
                                    village_shop.remove(item)

                                success = True
                                main_input = None
                                break
                                
                    if success == False:
                        print(f"\nERROR: Item '{buy_input}' is not being sold by this merchant or does not.\n")
                        buy_input = None

            case "2":

                sell_input = None
                success = False
                print("\nWhat do you want to sell? Remember that you can only sell items that are being sold by merchants.\n")

                for item in player.inventory:
                    print(f"ITEM: {item["name"].title()}        ID: {item["id"]}        TYPE: {item["type"]}        SELL PRICE: {int(item["price"] / 2)} gold")
                    print()
                print("Enter 'back' to go back to the main shop menu.\n")

                while sell_input == None:
                    sell_input = str(input("Enter an Item ID > "))

                    if sell_input == "back":
                        main_input = None
                        break

                    for item in player.inventory:
                        if sell_input == item["id"]:
                            if item["price"] == 0 or item == item_city_key_1 or item == item_city_key_2:
                                print(f"\nERROR: Item '{sell_input}' cannot be sold.\n")
                                success = True
                                sell_input = None
                                break
                            else:
                                sell_price = int(item["price"] / 2)
                                print(f"You have successfully sold {item["name"].upper()} for {sell_price} gold.")
                                print(f"You now have {player.gold} gold.")
                                player.gold = player.gold + sell_price
                                player.inventory.remove(item)
                                success = True
                                main_input = None
                                break
                    
                    if success == False:
                        print(f"\nERROR: Item '{sell_input}' is not in your inventory or does not exist.\n")
                        sell_input = None

            case "3":
                print("\nMerchant: Pleasure doing business with you!\n")
                npc_merchant["state"] = 0
                player.menu_state = False

            # THE BELOW CASES ARE USED BECAUSE OF DEADLINES, I KNOW THIS ISN'T OPTIMAL -Muhammad

            case "buy":

                buy_input = None
                success = False
                print(f"\nMerchant: What do you want to buy? You have {player.gold} gold.\n")

                for item in npc_merchant["inventory"]:
                    print(f"ITEM: {item["name"].title()}        ID: {item["id"]}        TYPE: {item["type"]}        BUY PRICE: {item["price"]} gold")
                    print(f"DESCRIPTION: {item["description"]}")
                    print()
                print("Enter 'back' to go back to the main shop menu.\n")

                while buy_input == None:
                    buy_input = str(input("Enter an Item ID > "))

                    if buy_input == "back":
                        main_input = None
                        break

                    for item in npc_merchant["inventory"]:
                        if buy_input == item["id"]:
                            if player.inventory == 16:
                                print(f"\nERROR: You cannot buy {buy_input.upper()} because your inventory is full. Please drop, sell or store away an item from your inventory in order to buy an item.\n")
                                success = True
                                main_input = None
                                break
                            else:
                                print(f"\nYou have successfully bought {item["name"].upper()} for {item["price"]} gold.")
                                print(f"You now have {player.gold} gold.")
                                player.gold = player.gold - item["price"]
                                player.inventory.append(item)

                                if item == item_city_key_1 or item == item_city_key_2:
                                    npc_merchant["inventory"].remove(item)
                                    village_shop.remove(item)

                                success = True
                                main_input = None
                                break
                                
                    if success == False:
                        print(f"\nERROR: Item '{buy_input}' is not being sold by this merchant or does not exist.\n")
                        buy_input = None

            case "sell":

                sell_input = None
                success = False
                print("\nWhat do you want to sell? Remember that you can only sell items that are being sold by merchants.\n")

                for item in player.inventory:
                    print(f"ITEM: {item["name"].title()}        ID: {item["id"]}        TYPE: {item["type"]}        SELL PRICE: {int(item["price"] / 2)} gold")
                    print()
                print("Enter 'back' to go back to the main shop menu.\n")

                while sell_input == None:
                    sell_input = str(input("Enter an Item ID > "))

                    if sell_input == "back":
                        main_input = None
                        break

                    for item in player.inventory:
                        if sell_input == item["id"]:
                            if item["price"] == 0 or item == item_city_key_1 or item == item_city_key_2:
                                print(f"\nERROR: Item '{sell_input}' cannot be sold.\n")
                                success = True
                                sell_input = None
                                break
                            else:
                                sell_price = int(item["price"] / 2)
                                print(f"\nYou have successfully sold {item["name"].upper()} for {sell_price} gold.")
                                print(f"You now have {player.gold} gold.")
                                player.gold = player.gold + sell_price
                                player.inventory.remove(item)
                                success = True
                                main_input = None
                                break
                    
                    if success == False:
                        print(f"\nERROR: Item '{sell_input}' is not in your inventory or does not exist.\n")
                        sell_input = None

            case "exit":
                print("\nMerchant: Pleasure doing business with you!\n")
                npc_merchant["state"] = 0
                player.menu_state = False

            case _:
                print(f"\nERROR: '{main_input}' is not a valid command for the shop menu.")
                main_input = None