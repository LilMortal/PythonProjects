# 🎯 Word Guessing Game

A fun and interactive command-line word guessing game similar to Wordle, but with customizable difficulty levels and enhanced features. Test your vocabulary and deduction skills by guessing the hidden word within a limited number of attempts!

## 📖 Project Description

This Word Guessing Game is a Python-based puzzle game where players attempt to guess a hidden word by making educated guesses. The game provides color-coded feedback for each guess:
- **Green**: Letter is correct and in the right position
- **Yellow**: Letter is in the word but in the wrong position  
- **Red**: Letter is not in the word at all

The game features multiple difficulty levels, persistent statistics tracking, hints system, and a clean terminal interface with colored output.

## ✨ Features

- **Multiple Difficulty Levels**: Choose from Easy (3 letters) to Expert (7 letters) or create custom settings
- **Color-Coded Feedback**: Visual feedback using terminal colors for better user experience
- **Statistics Tracking**: Persistent game statistics including win percentage, streaks, and guess distribution
- **Hint System**: Get helpful hints when you're stuck
- **Input Validation**: Robust error handling and input validation
- **Customizable Settings**: Adjust word length and maximum attempts
- **Clean Interface**: User-friendly command-line interface with clear instructions
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Terminal/Command prompt with color support (most modern terminals)

### Setup Instructions

1. **Download the game files**:
   - Save `main.py` to your desired directory
   - Optionally save this README.md file for reference

2. **Navigate to the game directory**:
   ```bash
   cd path/to/word-guessing-game
   ```

3. **No additional dependencies required** - the game uses only Python standard library modules!

## 🚀 How to Run

Run the game using Python:

```bash
python main.py
```

Or if you have Python 3 specifically:

```bash
python3 main.py
```

## 🎮 How to Play

1. **Choose Difficulty**: Select from preset difficulty levels or create custom settings
2. **Start Guessing**: Enter words of the specified length
3. **Analyze Feedback**: Use the color-coded feedback to refine your next guess
4. **Use Hints**: Type 'hint' to reveal a letter position when stuck
5. **Win or Learn**: Either guess the word correctly or learn from the reveal!

### Example Gameplay

```
🎯 Welcome to Word Guessing Game! 🎯
Guess the 5-letter word!
You have 6 attempts.

Enter your guess (5 letters): house
Guess 1: H🟩O🟨U🟥S🟥E🟥
Legend: Green = Correct position | Yellow = Wrong position | Red = Not in word

Enter your guess (5 letters): world
Guess 2: W🟥O🟨R🟩L🟥D🟥
Legend: Green = Correct position | Yellow = Wrong position | Red = Not in word

Enter your guess (5 letters): horse
🎉 Congratulations! You guessed 'HORSE' in 3 attempts!
```

### Special Commands

- **`hint`**: Get a hint revealing one letter position
- **`quit`**: Exit the current game

## 📊 Game Statistics

The game automatically tracks and saves your statistics:

- **Games Played**: Total number of games
- **Games Won**: Number of successful games
- **Win Percentage**: Success rate
- **Current Streak**: Current winning streak
- **Max Streak**: Best winning streak achieved
- **Guess Distribution**: How many attempts you typically need

Statistics are saved in `game_stats.json` and persist between game sessions.

## 🔧 Configuration

### Difficulty Levels

1. **Easy**: 3 letters, 8 attempts
2. **Normal**: 5 letters, 6 attempts (classic Wordle style)
3. **Hard**: 6 letters, 5 attempts
4. **Expert**: 7 letters, 4 attempts
5. **Custom**: Set your own word length (3-10) and attempts (3-10)

### Customization Options

You can modify the game by editing these variables in the `WordGame` class:

- `word_lists`: Add your own word collections for different lengths
- `colors`: Customize the color scheme
- `max_attempts`: Change default attempt limits
- `word_length`: Adjust default word lengths

## 🧪 Testing

The game includes basic unit tests. To run them:

1. Uncomment the test line in `main.py`:
   ```python
   # Uncomment the line below to run tests
   run_tests()  # Remove the # to enable
   ```

2. Run the file:
   ```bash
   python main.py
   ```

## 🌟 Future Improvements

### Planned Enhancements
- **Web Interface**: Convert to a web-based game using Flask or Django
- **GUI Version**: Create a desktop version using tkinter or PyQt
- **Multiplayer Mode**: Add competitive multiplayer functionality
- **Word Categories**: Themed word lists (animals, countries, technology, etc.)
- **Daily Challenges**: Implement daily puzzle mode like Wordle
- **Difficulty Progression**: Adaptive difficulty based on performance
- **Sound Effects**: Add audio feedback for better engagement
- **Export Statistics**: Save/export detailed game statistics

### Converting to Web Version

To convert this to a web application:

1. **Use Flask/Django**: Create web routes for game logic
2. **HTML/CSS Frontend**: Replace terminal colors with CSS styling
3. **JavaScript Interactivity**: Handle user input and dynamic updates
4. **Database Storage**: Replace JSON file with proper database
5. **User Accounts**: Add registration and login functionality

### Converting to GUI Version

To create a desktop GUI version:

1. **Choose Framework**: tkinter (built-in) or PyQt/PySide
2. **Design Layout**: Create input fields, game board, and statistics panel
3. **Event Handling**: Replace command-line input with button clicks
4. **Visual Feedback**: Use colored text/backgrounds instead of terminal colors

## 🏆 Credits

- **Game Design**: Inspired by Wordle and classic word guessing games
- **Development**: Created as a comprehensive Python learning project
- **Color Support**: Uses ANSI escape codes for terminal colors

## 📝 License

This project is open source and available for educational purposes. Feel free to modify, distribute, and enhance the code for your own learning and projects.

---

**Enjoy the game and happy guessing! 🎯**

For questions, suggestions, or bug reports, feel free to reach out or modify the code to suit your needs!