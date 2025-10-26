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

# ANSI colour constants
PASTEL_GREEN = "\033[38;2;144;238;144m"
RED = "\033[38;2;255;0;0m"
RESET = "\033[0m"



# when True, narrative printing should avoid slow typewriter and just speak/print
TTS_ENABLED = False

 

def list_of_items(items):

    item_list = []
    for item in items:
        item_list.append(item["name"])
    item_name_list = ", ".join(item_list)

    return item_name_list

def print_slowly(text, delay=0.03):
    """Print text character by character with a small delay. Press 'S' or spacebar to skip."""
    skip_queue = queue.Queue()
    stop_event = threading.Event()
    
    def get_input():
        try:
            import msvcrt  # Windows
            while not stop_event.is_set():
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key in ['s', ' ']:
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
    



def print_room_items(room): # This function isn't being used at the moment. It may be used later though.
    
    room_items = list_of_items(room["items"])
    if len(room_items) > 0:
        print(f"There is {room_items} here.\n")


def print_exit(direction, leads_to):
    print("- GO " + direction.upper() + " to " + leads_to + ".")


def print_room(room): # Displays details of the current room when room changes occur

    print("\n————————————————————————————————————————————————————————————————————————————————————————————————————\n")
    say_text(f" — {room['name'].upper()} — ")
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
    print()


def say_text(text: str):
    """print text if tts on or type slow"""
    if TTS_ENABLED:
        print(text)
        tts.speak(text)
    else:
        print_slowly(text)

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
            player.room_change = False
        # GAME OVER check before prompting
        if player.stats.get("health", 0) <= 0:
            print("\n————————————————————————————————————————————————————————————————————————————————————————————————————")
            if player.current_room.get("enemies") and len(player.current_room["enemies"]) > 0:
                print(f"{RED}GAME OVER: YOU HAVE BEEN KILLED BY THE {player.current_room['enemies'][0]['name'].upper()}{RESET}")
            else:
                print(f"{RED}GAME OVER: YOU HAVE DIED.{RESET}")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            exit()

        # show map and hp before asking for input
        draw_minimap(player.current_room)
        player.print_health()
        print("What do you want to do?")
        # Use voice input if enabled; fallback handled inside
        def _menu(_exits, _room_items, _inv_items):
            user_input = get_player_input(f"{PASTEL_GREEN}> {RESET}")
            normalised_user_input = normalise_input(user_input)
            return normalised_user_input
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