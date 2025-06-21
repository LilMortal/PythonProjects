# 🎲 Number Guessing Game

A fun, interactive command-line number guessing game with multiple difficulty levels, intelligent hints, and comprehensive statistics tracking.

## 📋 Overview

This Python-based CLI game challenges players to guess a randomly generated number within a limited number of attempts. The game features four difficulty levels, smart hint system, persistent statistics tracking, and an engaging user interface with emojis and clear feedback.

## ✨ Features

### Core Gameplay
- **4 Difficulty Levels**: Easy (1-50), Medium (1-100), Hard (1-200), Expert (1-500)
- **Limited Attempts**: Varying attempts based on difficulty (5-10 attempts)
- **Intelligent Hint System**: Context-aware hints based on proximity to target
- **Input Validation**: Robust error handling for user inputs
- **Graceful Exit**: Type 'quit' anytime to exit gracefully

### Advanced Features
- **Statistics Tracking**: Persistent game statistics saved to JSON file
- **Performance Metrics**: Win rate, average guesses, best scores per difficulty
- **Game Timer**: Track how long each game takes
- **Guess History**: See all your guesses for each game
- **Best Score Tracking**: Personal best scores across all difficulties

### User Experience
- **Colorful Interface**: Emoji-rich CLI interface for better engagement
- **Clear Feedback**: Detailed hints and game state information
- **Menu System**: Easy navigation between game modes and statistics
- **Instructions**: Built-in how-to-play guide
- **Statistics Reset**: Option to reset all saved statistics

## 🚀 Setup and Installation

### Prerequisites
- Python 3.10 or higher
- No external dependencies required (uses only Python standard library)

### Installation
1. Download the `number_guessing_game.py` file
2. Make sure you have Python 3.10+ installed
3. No additional packages to install!

### Running the Game
```bash
# Method 1: Direct execution
python number_guessing_game.py

# Method 2: Make executable (Unix/Linux/Mac)
chmod +x number_guessing_game.py
./number_guessing_game.py

# Method 3: Using Python module
python -m py_compile number_guessing_game.py
python number_guessing_game.py
```

## 🎮 How to Play

### Quick Start
1. Run the game
2. Choose a difficulty level (1-4)
3. Start guessing the secret number
4. Use the hints to narrow down your guesses
5. Win by guessing the exact number within the attempt limit!

### Difficulty Levels
| Level  | Range   | Max Attempts | Best For |
|--------|---------|--------------|----------|
| Easy   | 1-50    | 10 attempts  | Beginners |
| Medium | 1-100   | 8 attempts   | Regular players |
| Hard   | 1-200   | 6 attempts   | Experienced players |
| Expert | 1-500   | 5 attempts   | Challenge seekers |

### Hint System
- 🔥 **Very close**: Within 5 numbers of the target
- 🌡️ **Getting warm**: Within 15 numbers of the target
- ❄️ **Getting colder**: Within 30 numbers of the target
- 🧊 **Way off**: More than 30 numbers away from target

### Pro Tips
- Use binary search strategy (start with middle of range)
- Pay close attention to the hints
- Keep track of your previous guesses
- Start with Medium difficulty to learn the game mechanics

## 📊 Example Usage

```
🎲 WELCOME TO THE NUMBER GUESSING GAME! 🎲
============================
Try to guess the secret number in as few attempts as possible!

🎯 Select Difficulty Level:
1. Easy     | Range: 1-50     | Max: 10 attempts
2. Medium   | Range: 1-100    | Max: 8 attempts
3. Hard     | Range: 1-200    | Max: 6 attempts
4. Expert   | Range: 1-500    | Max: 5 attempts

Enter your choice (1-4): 2

🎮 Starting Medium mode!
🎯 I'm thinking of a number between 1 and 100
🎲 You have 8 attempts to guess it!

--- Attempt 1/8 ---
Enter your guess (1-100) or 'quit' to exit: 50
💭 🌡️ Getting warm! Try higher!

--- Attempt 2/8 ---
Enter your guess (1-100) or 'quit' to exit: 75
💭 🔥 Very close! Go lower!

--- Attempt 3/8 ---
Enter your guess (1-100) or 'quit' to exit: 73
💭 🎉 PERFECT! You got it!

🎉 CONGRATULATIONS! 🎉
✅ You guessed 73 correctly!
📊 Attempts used: 3/8
⏱️ Time taken: 45.2 seconds
📈 Your guesses: 50 → 75 → 73
```

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Libraries Used**:
  - `random` - For generating random numbers
  - `time` - For game timing functionality
  - `json` - For persistent statistics storage
  - `os` - For file system operations
  - `typing` - For type hints and better code documentation

## 📁 File Structure

```
number_guessing_game.py    # Main game file (single file project)
game_stats.json           # Auto-generated statistics file
README.md                 # This documentation file
```

## 🚀 Future Enhancements

### Potential Improvements
1. **GUI Version**: Create a Tkinter-based graphical interface
2. **Web Interface**: Build a Flask/Django web version
3. **Multiplayer Mode**: Add competitive multiplayer functionality
4. **Custom Ranges**: Allow players to set custom number ranges
5. **Achievement System**: Add badges and achievements for milestones
6. **Sound Effects**: Add audio feedback for different game events
7. **Themes**: Different visual themes and color schemes
8. **Leaderboards**: Global or local leaderboards with high scores
9. **Hint Types**: Different types of hints (mathematical, visual, etc.)
10. **Game Modes**: Time attack, survival mode, reverse guessing

### Technical Enhancements
- **Database Integration**: Use SQLite for more robust statistics
- **Configuration File**: External config for game settings
- **Logging System**: Detailed logging for debugging and analytics
- **Unit Tests**: Comprehensive test suite
- **CLI Arguments**: Command-line arguments for different game modes
- **Export Statistics**: Export stats to CSV/Excel formats

## 🎯 Advanced Features Ideas

### Gameplay Variants
- **Reverse Mode**: Computer guesses your number
- **Team Mode**: Collaborative guessing with friends
- **Tournament Mode**: Bracket-style elimination games
- **Daily Challenge**: Special number of the day
- **Speed Round**: Multiple quick games with time pressure

### Educational Features
- **Math Mode**: Numbers based on mathematical sequences
- **Learning Stats**: Track improvement over time with graphs
- **Strategy Tips**: Built-in tutorial for optimal guessing strategies
- **Historical Data**: Long-term performance trends

## 🤝 Contributing

This is a single-file educational project, but here are ways to extend it:

1. Fork the project and add new features
2. Create themed versions (math, science, etc.)
3. Build GUI or web versions
4. Add localization for different languages
5. Create mobile app versions

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Credits

- Built with Python standard library only
- Inspired by classic number guessing games
- Emoji icons from Unicode standard
- Game design principles from classic CLI games

## 📞 Support

If you encounter any issues:
1. Check that you're using Python 3.10+
2. Ensure the script has proper file permissions
3. Verify that the directory is writable (for statistics file)

## 🎉 Changelog

### Version 1.0
- Initial release with core gameplay
- Four difficulty levels
- Statistics tracking
- Intelligent hint system
- Persistent data storage
- Complete CLI interface with menu system

---

**Happy Gaming! 🎮** 

Try to beat your best score and master all difficulty levels!