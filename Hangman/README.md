# 🎮 Hangman Game

A classic word-guessing game implemented in Python with a beautiful command-line interface, multiple difficulty levels, and comprehensive game statistics.

## 📋 Overview

This is a complete implementation of the traditional Hangman game where players guess letters to reveal a hidden word. The game features ASCII art hangman drawings, multiple difficulty levels, and detailed statistics tracking to enhance the gaming experience.

## ✨ Features

### 🎯 Core Game Features
- **Classic Hangman Gameplay**: Guess letters to reveal the hidden word
- **ASCII Art Hangman**: Visual representation of wrong guesses with detailed hangman drawings
- **Multiple Difficulty Levels**: 
  - Easy (3-4 letter words)
  - Medium (5-8 letter words) 
  - Hard (9+ letter words)
- **Extensive Word Database**: 60+ carefully curated words across all difficulty levels
- **Input Validation**: Robust error handling for all user inputs
- **Case Insensitive**: Accepts both uppercase and lowercase letters

### 🎮 User Interface Features
- **Clean Terminal Interface**: Professional-looking ASCII art and formatting
- **Screen Clearing**: Maintains clean display throughout gameplay
- **Interactive Menus**: Easy navigation with numbered menu options
- **Real-time Feedback**: Immediate response to correct/incorrect guesses
- **Game State Display**: Clear visualization of current word progress

### 📊 Advanced Features
- **Statistics Tracking**: 
  - Games played
  - Games won
  - Win rate percentage
  - Average guesses per game
- **Session Persistence**: Stats maintained throughout the game session
- **Smart Word Selection**: Random word selection from difficulty-appropriate lists
- **Graceful Exit**: Clean exit options with 'quit' command

## 🚀 Setup and Installation

### Prerequisites
- Python 3.10 or higher
- No external dependencies required (uses only Python standard library)

### Installation Steps

1. **Download the game file**:
   ```bash
   # Save the hangman.py file to your desired directory
   ```

2. **Make the file executable** (optional, for Unix-like systems):
   ```bash
   chmod +x hangman.py
   ```

3. **Run the game**:
   ```bash
   python hangman.py
   ```
   or
   ```bash
   python3 hangman.py
   ```

## 🎮 How to Play

### Basic Gameplay
1. **Start the game**: Run the Python file
2. **Choose difficulty**: Select from Easy, Medium, or Hard
3. **Guess letters**: Enter one letter at a time
4. **Win condition**: Guess all letters in the word before making 6 wrong guesses
5. **Lose condition**: Make 6 wrong guesses and the hangman is complete

### Game Commands
- **Letter guessing**: Type any letter (a-z)
- **Quit game**: Type 'quit' during gameplay
- **Menu navigation**: Use numbers (1-4) in menus

### Strategy Tips
- Start with common vowels: A, E, I, O, U
- Try frequent consonants: R, S, T, L, N
- Look for patterns as letters are revealed
- Consider word length and difficulty level

## 📱 Example Usage

```bash
$ python hangman.py

        ╔═══════════════════════════════════════╗
        ║          🎮 HANGMAN GAME 🎮           ║
        ║        Test Your Word Skills!         ║
        ╚═══════════════════════════════════════╝

🎮 MAIN MENU:
1. 🎯 Play Game
2. 📋 Instructions
3. 📊 View Statistics
4. 🚪 Exit

Enter your choice (1-4): 1

🎯 Choose difficulty level:
1. Easy (3-4 letter words)
2. Medium (5-8 letter words)
3. Hard (9+ letter words)

Enter your choice (1-3): 2

           -----
           |   |
           O   |
          /|   |
               |
               |
        =========

🎯 Difficulty: Medium
📝 Word: P _ _ _ _ N
❌ Wrong guesses: 3/6
💭 Guessed letters: A, E, I, O, P

🔤 Enter a letter (or 'quit' to exit): T
```

## 🛠️ Technical Details

### Tech Stack
- **Language**: Python 3.10+
- **Libraries**: 
  - `random` - Word selection
  - `string` - Input validation
  - `os` - Screen clearing
  - `sys` - Clean exit handling

### Code Structure
- **Object-Oriented Design**: Single `HangmanGame` class containing all game logic
- **Modular Functions**: Separate methods for each game aspect
- **Error Handling**: Comprehensive input validation and exception handling
- **Clean Code**: Well-commented, PEP 8 compliant Python code

### File Structure
```
hangman-game/
├── hangman.py          # Main game file (single file project)
└── README.md          # This documentation
```

## 🎯 Future Enhancement Ideas

### 🌟 Gameplay Enhancements
- **Custom Word Lists**: Allow users to add their own words
- **Hints System**: Provide category hints or definitions
- **Multiplayer Mode**: Two-player word challenges
- **Timed Mode**: Add time pressure for increased difficulty
- **Themed Word Sets**: Categories like animals, countries, movies

### 🖥️ Interface Improvements
- **GUI Version**: Create a Tkinter-based graphical interface
- **Web Version**: Convert to Flask web application
- **Mobile App**: Develop using Kivy or similar framework
- **Sound Effects**: Add audio feedback for correct/incorrect guesses

### 📊 Advanced Features
- **Persistent Statistics**: Save stats to file between sessions
- **Leaderboard System**: Track high scores and best performances
- **Achievement System**: Unlock achievements for various milestones
- **Difficulty Scaling**: Adaptive difficulty based on performance
- **Word Frequency Analysis**: Show statistics about guessed letters

### 🎨 Visual Enhancements
- **Colored Output**: Add terminal colors for better visual appeal
- **Animated Hangman**: ASCII animations for hangman drawing
- **Custom Themes**: Different visual themes for the game
- **Progress Bars**: Visual indicators for game progress

## 🔧 Customization Options

### Adding New Words
To add new words to the game, modify the `WORD_LISTS` dictionary in the `HangmanGame` class:

```python
WORD_LISTS = {
    'easy': ['your', 'new', 'easy', 'words'],
    'medium': ['your', 'medium', 'difficulty', 'words'],
    'hard': ['your', 'challenging', 'vocabulary', 'words']
}
```

### Adjusting Difficulty
- Change `max_wrong_guesses` to increase/decrease allowed mistakes
- Modify word lists to adjust difficulty curves
- Add new difficulty levels by extending the `WORD_LISTS` dictionary

### Visual Customization
- Modify `HANGMAN_STAGES` to change the ASCII art
- Update the title and menu displays
- Customize colors and formatting

## 🐛 Known Issues & Limitations

- **No Persistent Storage**: Statistics reset when the program closes
- **Terminal Dependent**: Requires terminal that supports ANSI escape codes
- **Single Language**: Currently only supports English words
- **Fixed Word Lists**: Limited to predefined words

## 🤝 Contributing

This is a single-file educational project. To contribute:

1. Fork or copy the project
2. Make your improvements
3. Test thoroughly
4. Share your enhanced version!

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🎖️ Credits

- **Game Design**: Classic Hangman game concept
- **ASCII Art**: Custom hangman drawings
- **Word Lists**: Curated from common English vocabulary
- **Implementation**: Created with Python standard library

## 📞 Support

If you encounter any issues:
1. Check that you're using Python 3.10+
2. Ensure your terminal supports text clearing
3. Verify the file has proper permissions
4. Try running with different Python commands (python vs python3)

---

**Enjoy playing Hangman! 🎮**

*Created with ❤️ and Python*
