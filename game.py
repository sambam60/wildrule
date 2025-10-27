from map import rooms
import player
from items import *
from interactions import *
from commands import *
from gameparser import *
import time
import sys
import threading
import queue
import textwrap
import tts
import voice_input
from minimap import draw_minimap
from combat import timed_enemy_attack, _print_combat_guide_once
import threading

# ANSI colour constants
PASTEL_GREEN = "\033[38;2;144;238;144m"
RED = "\033[38;2;255;0;0m"
RESET = "\033[0m"



def list_of_items(items):

    item_list = []
    for item in items:
        item_list.append(item["name"])
    item_name_list = ", ".join(item_list)

    return item_name_list



def banner():
    ascii_art = """         _________ _        ______   _______           _        _______ 
|\\     /|\\__   __/( \\      (  __  \\ (  ____ )|\\     /|( \\      (  ____ \\
| )   ( |   ) (   | (      | (  \\  )| (    )|| )   ( || (      | (    \\/
| | _ | |   | |   | |      | |   ) || (____)|| |   | || |      | (__    
| |( )| |   | |   | |      | |   | ||     __)| |   | || |      |  __)   
| || || |   | |   | |      | |   ) || (\\ (   | |   | || |      | (      
| () () |___) (___| (____/\\| (__/  )| ) \\ \\__| (___) || (____/\\| (____/\\
(_______)\\_______/(_______/(______/ |/   \\__/(_______)(_______/(_______/
                                                                        """
    for line in ascii_art.splitlines():
        print(f"{PASTEL_GREEN}{line}{RESET}")
        time.sleep(0.2)
    


def menu(exits, room_items, inv_items):

    user_input = input("> ")
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input

def main():

    # ask user for tts and voice input
    try:
        use_tts = input("Enable Text-To-Speech (y/n)? ").strip().lower().startswith("y")
    except Exception:
        use_tts = False
    try:
        use_voice = input("Enable Voice Input (y/n)? ").strip().lower().startswith("y")
    except Exception:
        use_voice = False

    # setup subsystems based on user choice
    tts_enabled = False
    if use_tts:
        tts_enabled = tts.init_tts()
    voice_enabled = False
    if use_voice:
        voice_enabled = voice_input.init_model()

    global TTS_ENABLED
    TTS_ENABLED = bool(tts_enabled)

    # ask user for time-based combat only if voice input and TTS are disabled
    enable_tbc = False
    if not voice_enabled and not tts_enabled:
        try:
            enable_tbc = input("Enable Time-Based Combat (y/n)? ").strip().lower().startswith("y")
        except Exception:
            enable_tbc = False
    else:
        print("Time-Based Combat is disabled when Voice Input or TTS is enabled.")
    
    try:
        import player as _player_cfg
        _player_cfg.time_based_combat = bool(enable_tbc)
    except Exception:
        pass

    def get_player_input(prompt: str) -> str:
        if voice_enabled:
            print(prompt, end="", flush=True)
            heard = voice_input.listen_for_command(prompt)
            if heard:
                print(f"\n{PASTEL_GREEN}> {RESET}{heard}")
                return heard
            else:
                # voice failed, use text instead
                print("\nVoice input failed. switching to text...")
                return input(prompt)
        return input(prompt)

    banner()
    
    # intro text
    print("\n" + "="*100)
    opening_lines = [
        "Welcome to the World of Wildrule!",
        "You are a brave adventurer who has taken up the treacherous task of retrieving the Temple's Sword,",
        "a powerful weapon meant to be protected by Temple Guards. However, they were no match for the",
        "Skeleton King, who defeated them easily and stole the sword to his hidden dungeon. Now Wildrule",
        "stands defenseless against the Skeleton King and his army.",
        "",
        "The thieves left only one trace: a map leading to a secret location within the Little Kingdom.",
        "Here you will find the Hidden Dungeon that has claimed the lives of all who have attempted to",
        "retrieve the Temple Sword. You are risking your life to recover the sword and return it to its",
        "rightful place in the Temple.",
        "",
        "It is your choice how you proceed with your adventure. However, it is suggested that you take",
        "advantage of every bit of advice and tools you can find around the map. After all, this will",
        "NOT be an easy adventure.",
        "",
        "You start with only a stick. Along your way, you will need to collect more items to defeat",
        "stronger enemies. Make sure to take advantage of the merchants scattered throughout the map.",
        "",
        "To help you on your journey, you will find a map showing the different areas of the world and",
        "how you can travel through them. There are three biomes (Forest, Plains, and Tundra) and three",
        "cities (Vengeful Village, Icy Igloos, and Little Kingdom), along with the Hidden Dungeon you",
        "must find. Where you go from the start is up to you.",
    ]
    # print intro if tts on, speak all at once
    for line in opening_lines:
        if line == "":
            print()
        else:
            say_text(line)
    if TTS_ENABLED:
        try:
            tts.speak_many([l for l in opening_lines if l])
        except Exception:
            pass
    print("="*100 + "\n")

    while True:

        if player.current_turn == 0:

            print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print_room(player.current_room)
            player.current_turn = 1
            player.room_change = False

        if player.menu_state == False:

            print(f"TURN: {player.current_turn}")
            print("\n — Mini Map — \n")
            draw_minimap(player.current_room)
            player.print_health()
            print("\nWhat do you want to do?")
            # Use voice input if enabled; fallback handled inside
            def _menu(_exits, _room_items, _inv_items):
                user_input = get_player_input(f"{PASTEL_GREEN}> {RESET}")
                normalised_user_input = normalise_input(user_input)
                return normalised_user_input
            # Precombat prompt with concurrent bar (non-intrusive to typing)
            if getattr(player, "time_based_combat", False) and getattr(player, "pending_precombat", None) and not getattr(player, "locked_in_combat", False):
                print("\nA foe eyes you. Enter combat or escape!")
                print("Type an action now to ESCAPE (e.g., 'go south'), or type 'attack ' + enemy to ENTER with a bonus!")
                # allocate a line for the bar above the prompt
                print()  # empty line reserved for the bar
                stop_event = threading.Event()
                def _animate_precombat(total: int = 18, interval: float = 0.25):
                    import sys as _sys
                    import time as _time
                    RED = "\033[38;2;255;0;0m"
                    RESET = "\033[0m"
                    t = total
                    while t > 0 and not stop_event.is_set():
                        # Save cursor, move up 1 line, draw, restore
                        _sys.stdout.write("\033[s\033[1A\r")
                        _sys.stdout.write(f"Pre-Combat: {RED}{'|'*t}{RESET}    \033[0K")
                        _sys.stdout.write("\033[u")
                        _sys.stdout.flush()
                        _time.sleep(interval)
                        t -= 1
                    if not stop_event.is_set():
                        # Time expired: lock combat and notify
                        player.locked_in_combat = True
                        player.precombat_bonus = None
                        player.pending_precombat = None
                        _sys.stdout.write("\033[s\033[1A\r")
                        _sys.stdout.write("\033[38;2;255;102;102mCombat Entered\033[0m\033[0K")
                        _sys.stdout.write("\033[u")
                        _sys.stdout.flush()
                        try:
                            _print_combat_guide_once()
                        except Exception:
                            pass
                anim_thread = threading.Thread(target=_animate_precombat, daemon=True)
                anim_thread.start()

                # Prompt for input while bar animates
                command = _menu(player.current_room["exits"], player.current_room["items"], player.inventory)
                # stop animation cleanly once we have input
                stop_event.set()
                try:
                    anim_thread.join(timeout=0.2)
                except Exception:
                    pass
                # If the player chose to attack the pending enemy quickly, bonus is set in execute_attack
            else:
                command = _menu(player.current_room["exits"], player.current_room["items"], player.inventory)

            execute_command(command)
            # check if player died after action
            if player.stats.get("health", 0) <= 0:
                print("\n————————————————————————————————————————————————————————————————————————————————————————————————————")
                if player.current_room.get("enemies") and len(player.current_room["enemies"]) > 0:
                    print(f"{RED}GAME OVER: YOU HAVE BEEN KILLED BY THE {player.current_room['enemies'][0]['name'].upper()}{RESET}")
                else:
                    print(f"{RED}GAME OVER: YOU HAVE DIED.{RESET}")
                print("————————————————————————————————————————————————————————————————————————————————————————————————————\n")
                exit()


if __name__ == "__main__":
    main()