# 🎮 Rock Paper Scissors Game

A feature-rich command-line implementation of the classic Rock Paper Scissors game written in Python. This project includes multiple game modes, statistics tracking, and a clean, user-friendly interface.

## 📝 Project Description

This Rock Paper Scissors game brings the timeless classic to your terminal with enhanced features and multiple play modes. Whether you want a quick game against the computer, challenge a friend, or play a competitive best-of series, this implementation has you covered. The game includes comprehensive statistics tracking, input validation, and error handling for a smooth gaming experience.

## ✨ Features

- **Multiple Game Modes:**
  - Single Player vs Computer
  - Multiplayer (2 Players)
  - Best of 3 Series
  - Best of 5 Series

- **Smart Game Logic:**
  - Robust input validation
  - Case-insensitive input handling
  - Graceful error handling

- **Statistics Tracking:**
  - Win/loss/tie counts
  - Win rate percentage
  - Game history storage
  - Real-time statistics display

- **User Experience:**
  - Clear game rules and instructions
  - Colorful emoji feedback
  - Interactive menu system
  - Graceful exit handling

- **Code Quality:**
  - Well-documented code with docstrings
  - Type hints for better code clarity
  - Modular class-based design
  - Built-in unit tests

## 🔧 Installation

### Prerequisites
- Python 3.7 or higher

### Setup Instructions

1. **Clone or download the project:**
   ```bash
   # If using git
   git clone <repository-url>
   cd rock-paper-scissors
   
   # Or simply download the main.py file
   ```

2. **No additional dependencies required!**
   This project uses only Python standard libraries, so no pip installations are needed.

3. **Make the script executable (optional):**
   ```bash
   chmod +x main.py
   ```

## 🚀 How to Run

### Basic Usage
```bash
python main.py
```

### Alternative (if executable permission set)
```bash
./main.py
```

## 📖 Example Usage

### Starting the Game
```
==================================================
🎮 WELCOME TO ROCK PAPER SCISSORS! 🎮
==================================================

Game Rules:
• Rock crushes Scissors
• Scissors cuts Paper
• Paper covers Rock

Choices: rock, paper, scissors
Commands: 'quit' to exit, 'stats' to see statistics
==================================================

==============================
GAME MODES:
1. Single Player (vs Computer)
2. Multiplayer (2 Players)
3. Best of 3 Series
4. Best of 5 Series
5. View Statistics
6. Quit
==============================
Select game mode (1-6): 1
```

### Single Player Game
```
🎮 Single Player Mode

Player, enter your choice: rock

Player: Rock
Computer: Scissors
------------------------------
🎉 Player wins this round!

Player, enter your choice: stats

==============================
📊 GAME STATISTICS
==============================
Total Games: 1
Player Wins: 1
Computer Wins: 0
Ties: 0
Win Rate: 100.0%
==============================
```

### Best of Series
```
Select game mode (1-6): 3

🏆 Best of 3 series starting!

--- Round 1 ---
Score: Player 0 - 0 Computer

Player, enter your choice: paper

Player: Paper
Computer: Rock
------------------------------
🎉 Player wins this round!

--- Round 2 ---
Score: Player 1 - 0 Computer
...
```

## 🎯 Available Commands

During gameplay, you can use these commands:
- **rock, paper, scissors** - Make your move
- **stats** - View current game statistics
- **quit** - Exit the game gracefully

## 🧪 Running Tests

The project includes basic unit tests. To run them:

1. Open `main.py` in a text editor
2. Uncomment the line `# run_tests()` at the bottom of the file
3. Run the script:
   ```bash
   python main.py
   ```

The tests will run first, followed by the main game.

## 🔮 Future Improvements

Here are some potential enhancements for the project:

### Short-term Enhancements
- [ ] Add Rock Paper Scissors Lizard Spock variant
- [ ] Implement difficulty levels for computer AI
- [ ] Add colored terminal output support
- [ ] Save/load game statistics to file
- [ ] Add tournament mode for multiple players

### Medium-term Enhancements
- [ ] **Web Version**: Convert to a Flask web application
- [ ] **GUI Version**: Create a Tkinter or PyQt desktop application
- [ ] Add sound effects and animations
- [ ] Implement online multiplayer with websockets
- [ ] Add user profiles and achievements

### Advanced Features
- [ ] Machine learning AI that adapts to player patterns
- [ ] Database integration for persistent statistics
- [ ] RESTful API for game integration
- [ ] Mobile app version using Kivy
- [ ] Discord bot integration

## 🌐 Converting to Web/GUI

### Web Version (Flask)
To convert this to a web application:
1. Install Flask: `pip install flask`
2. Create HTML templates for the game interface
3. Convert game logic to handle HTTP requests
4. Use JavaScript for real-time interactions

### GUI Version (Tkinter)
To create a desktop GUI:
1. Import tkinter (included with Python)
2. Design the main game window with buttons
3. Connect button clicks to game methods
4. Add result display labels

### Example GUI starter code:
```python
import tkinter as tk
from tkinter import ttk

class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.game = RockPaperScissorsGame()
        # Add GUI elements here
        
    def on_choice_click(self, choice):
        # Handle button clicks
        pass
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements! Some areas where contributions would be welcome:

- Additional game variants
- UI/UX improvements
- Performance optimizations
- Extended test coverage
- Documentation improvements

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a demonstration of clean Python programming practices, featuring object-oriented design, comprehensive error handling, and user-friendly interfaces.

---

**Happy Gaming! 🎮** May the odds be ever in your favor!