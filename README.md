# Team10project

A text-based adventure game with voice input/output capabilities set in the fantasy world of Wildrule.

## Description

**Team10project** (working title) is an immersive text-based adventure game featuring:
- **Interactive storytelling**: Explore the world of Wildrule through rich narrative text and character descriptions
- **Turn-based combat system**: Engage in strategic battles using normal, charge, and counter attack mechanics
- **Voice interaction**: Optional offline text-to-speech (TTS) and voice command input using Vosk ASR
- **Open-world exploration**: Navigate through three distinct biomes (Forest, Plains, Tundra) and three cities
- **RPG elements**: Collect items, manage inventory, trade with merchants, and defeat enemies to progress

### Game Story

You are a brave adventurer tasked with retrieving the Temple's Sword, a powerful weapon stolen by the Skeleton King. The weapon is hidden in a dungeon that has claimed the lives of all who have attempted to retrieve it. Starting with only a stick, you must explore the world, gather resources, defeat enemies, and ultimately face the challenges of the Hidden Dungeon.

## Features

### Gameplay
- **Turn-based combat**: Strategic battle system with normal, charge, and counter attacks
- **Dynamic enemy spawning**: Random encounters based on location with varying difficulty
- **Inventory management**: Collect and equip weapons, armor, and accessories
- **Currency system**: Earn gold from defeating enemies to trade with merchants
- **Health system**: Visual HP display with heart indicators
- **Minimap**: Navigate the world using an ASCII minimap showing your location and surroundings

### World Areas
- **Forest Biome**: Start here with encounters against wildlife (geese, bears, bulls)
- **Plains**: Rolling plains connecting different regions
- **Tundra**: Icy wasteland with harsh conditions
- **Vengeful Village**: Trading hub in the plains
- **Icy Igloos**: Northern village in the tundra
- **Little Kingdom**: Major city with access to the Hidden Dungeon

### Voice Features
- **Text-to-Speech**: Hear game narration and descriptions read aloud
- **Voice Commands**: Speak commands to control your character
- **Offline operation**: No internet connection required after installation
- **Graceful fallback**: Automatically switches to text input if voice recognition fails

## Visuals
The game features colorful ASCII art, including:
- Game banner with stylized title
- Heart-based HP indicator (♥ for health, ♡ for empty)
- ASCII minimap showing world layout and current location
- Color-coded text for emphasis and readability

## Installation

### Prerequisites
- Python 3.x
- Virtual environment (recommended)

### Step 1: Install Python Dependencies

Activate your virtual environment (if using one) and install required packages:

```bash
pip install pyttsx3 vosk sounddevice numpy
```

### Step 2: Download Vosk Model

For voice input features, download the Vosk offline speech recognition model:

1. Download `vosk-model-small-en-us-0.15` from [alphacephei.com](https://alphacephei.com/vosk/models)
2. Extract the model to: `assets/models/vosk/vosk-model-small-en-us-0.15`
3. Create the directories if they don't exist

**Note:** The game works without voice features if you skip this step.

### Step 3: System Dependencies (Optional)

- **macOS**: May need to grant microphone permissions or install PortAudio:
  ```bash
  brew install portaudio
  ```
- **Linux**: For TTS, you may need:
  ```bash
  sudo apt-get install espeak
  ```
- **Windows**: No additional setup required (uses SAPI5 for TTS)

### Quick Start

Once installed, simply run:
```bash
python game.py
```

The game will automatically detect available features and continue without errors if voice/TTS is unavailable.

## Usage

### Starting the Game

Run the game:
```bash
python game.py
```

At startup you will be asked:
- **"Enable Text-To-Speech (y/n)?"**: Choose whether to hear game narration
- **"Enable Voice Input (y/n)?"**: Choose whether to use voice commands

### Game Controls

#### Basic Commands
- **GO [direction]**: Move in a direction (north, south, east, west, up, down)
- **TAKE [item]**: Pick up an item from the current room
- **DROP [item]**: Remove an item from your inventory
- **INVENTORY**: View your current items
- **INSPECT [item/enemy]**: Get details about an object or enemy
- **USE [item]**: Activate an item from your inventory
- **INTERACT [object]**: Interact with objects in the environment
- **WAIT**: Pass your turn (may trigger enemy encounters)
- **MAP**: Display the world map
- **HELP**: Show available commands

#### Combat Commands
- **ATTACK [enemy] normal**: Perform a standard attack
- **ATTACK [enemy] charge**: Charge up a powerful attack (takes 2 turns)
- **ATTACK [enemy] counter**: Counter-attack (effective if enemy is charging)
- **EVADE**: Guaranteed dodge of the next incoming attack

#### Voice Input

If voice input is enabled:
- The terminal shows a live ASCII sparkline of microphone peaks while listening
- Speak your command clearly
- Recognition stops on silence or timeout
- The recognized text is displayed back to you
- If recognition fails, the game falls back to keyboard input
- You can press 'S' or spacebar during typewriter text to skip ahead

## Technology Stack

### Core Dependencies
- **Python 3**: Programming language
- **pyttsx3**: Cross-platform TTS library for speech output
- **vosk**: Offline speech recognition (ASR)
- **sounddevice**: Audio I/O library for microphone access
- **numpy**: Numerical operations for audio processing

### Architecture
- **Modular design**: Separate modules for game logic, combat, player, enemies, items, and commands
- **Event-driven**: Turn-based system with room changes and combat events
- **Voice-first optional**: Game works with or without voice features

## Contributing

This is an academic project for Team 10. Contributions and suggestions are welcome. Please follow the existing code style and ensure all features work with both keyboard and voice input.

## Authors and Acknowledgment

Built by Team 10 at Cardiff University for a game development project.

**Acknowledgments:**
- Vosk project for providing offline speech recognition
- pyttsx3 developers for cross-platform text-to-speech
- Thanks to our project supervisors and testers

## License
MIT License

## Project Status
Currently in active development. Project deadline: Tuesday, 28th of October

## Troubleshooting

### Voice Input Issues
**Microphone not working:**
- Install PortAudio: `brew install portaudio` (macOS)
- Grant microphone permissions in system settings
- Verify device detection:
  ```bash
  python -c "import sounddevice as sd; print(sd.query_devices())"
  ```

### Speech Output Issues
**No speech output:**
- Ensure `pyttsx3` is installed correctly
- On Linux, you may need: `sudo apt-get install espeak`
- On Windows, check system audio is working
- Some environments require `nsss` backend on macOS

### Model/Setup Issues
**Model not found:**
- Verify Vosk model path: `assets/models/vosk/vosk-model-small-en-us-0.15`
- Re-download the model from [vosk models](https://alphacephei.com/vosk/models)
- Extract to the correct directory structure

### Gameplay Tips
- Start by exploring the Forest biome to level up
- Use merchants in cities to buy better equipment
- Save your gold for important upgrades
- Counter attacks are powerful when enemies charge
- Don't forget to equip better weapons and armor as you find them
- Visit the Little Kingdom for access to end-game content