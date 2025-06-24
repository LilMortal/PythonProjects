# 🎮 Tic Tac Toe Game

A feature-rich, command-line implementation of the classic Tic Tac Toe game written in Python. This project includes both Player vs Player and Player vs AI modes with an intelligent AI opponent that uses the minimax algorithm.

## 📋 Project Description

This Tic Tac Toe game provides an interactive command-line experience with multiple game modes, statistics tracking, and a smart AI opponent. The game features clean code architecture, comprehensive error handling, and an intuitive user interface that makes it enjoyable for players of all ages.

## ✨ Features

- **Multiple Game Modes**: Player vs Player and Player vs AI
- **Intelligent AI**: Uses minimax algorithm with alpha-beta pruning for optimal gameplay
- **Flexible Input**: Accepts multiple input formats (comma-separated, space-separated, or concatenated)
- **Game Statistics**: Tracks wins, losses, and draws across multiple games
- **Error Handling**: Comprehensive input validation and error messages
- **Interactive Menu**: Easy-to-navigate main menu system
- **Instructions**: Built-in help system explaining how to play
- **Graceful Exit**: Option to quit at any time during gameplay
- **Unit Tests**: Built-in test suite to verify game functionality

## 🛠️ Installation & Setup

### Prerequisites

- **Python Version**: Python 3.7 or higher
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Dependencies**: None (uses only Python standard library)

### Installation Steps

1. **Download the game file**:
   ```bash
   # Option 1: Download directly
   curl -O https://example.com/main.py
   
   # Option 2: Clone if part of a repository
   git clone <repository-url>
   cd tic-tac-toe
   ```

2. **Verify Python installation**:
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Make the file executable** (optional, for Unix-like systems):
   ```bash
   chmod +x main.py
   ```

## 🚀 How to Run

### Basic Usage

```bash
python main.py
```

Or on some systems:

```bash
python3 main.py
```

### Running Tests

To run the built-in unit tests:

```bash
python main.py --test
```

### Direct Execution (Unix-like systems)

If you made the file executable:

```bash
./main.py
```

## 🎯 Example Usage

### Starting the Game

When you run the program, you'll see the main menu:

```
🎮 TIC TAC TOE GAME
====================
1. Player vs Player
2. Player vs AI
3. View Statistics
4. How to Play
5. Quit

Select an option (1-5):
```

### Game Board Display

The game board is displayed with clear coordinates:

```
   0   1   2
0  X |   | O
  -----------
1    | X |  
  -----------
2  O |   |  
```

### Making Moves

Players can input moves in several formats:
- `1,2` (comma-separated)
- `1 2` (space-separated)
- `12` (concatenated)

Example gameplay:
```
Player X, enter your move (row,col) or 'q' to quit: 1,1

   0   1   2
0    |   |  
  -----------
1    | X |  
  -----------
2    |   |  

AI is thinking...
AI plays: 0,0

   0   1   2
0  O |   |  
  -----------
1    | X |  
  -----------
2    |   |  
```

### Game Statistics

After playing several games:

```
📊 Game Statistics:
Player X wins: 3
Player O wins: 2
Draws: 1
Total games played: 6
```

## 🎮 Game Rules

1. **Objective**: Be the first player to get three of your marks in a row (horizontally, vertically, or diagonally)
2. **Players**: X always goes first
3. **Board**: 3×3 grid with positions numbered 0-2 for both rows and columns
4. **Winning**: Get three X's or O's in a row, column, or diagonal
5. **Draw**: If all 9 spaces are filled without a winner, the game is a draw

## 🤖 AI Features

The AI opponent includes several advanced features:

- **Minimax Algorithm**: Uses game theory to make optimal moves
- **Alpha-Beta Pruning**: Optimizes decision-making speed
- **Multiple Difficulty Levels**: Easy, Medium, and Hard (currently set to Hard)
- **Strategic Play**: The AI will always block winning moves and take wins when available

## 🧪 Testing

The game includes built-in unit tests that verify:

- Board initialization
- Move validation
- Win detection (horizontal, vertical, diagonal)
- Draw detection
- Game state management

Run tests with: `python main.py --test`

## 🔧 Code Structure

The project is organized using object-oriented programming principles:

- **TicTacToe Class**: Main game logic and state management
- **Game Logic Methods**: Move validation, win detection, board management
- **AI Methods**: Minimax algorithm implementation
- **User Interface Methods**: Menu system, input handling, display functions
- **Utility Functions**: Testing, statistics, helper methods

## 🚀 Future Improvements

### Potential Enhancements

1. **GUI Version**: Convert to a graphical interface using tkinter, pygame, or web-based
2. **Network Play**: Add multiplayer support over network
3. **Difficulty Levels**: Implement multiple AI difficulty settings
4. **Game Variants**: Add different board sizes (4×4, 5×5)
5. **Save/Load**: Implement game state persistence
6. **Themes**: Add visual themes and customization options
7. **Sound Effects**: Add audio feedback for moves and wins
8. **Tournament Mode**: Implement bracket-style tournaments
9. **Move History**: Track and display move history
10. **Undo Feature**: Allow players to undo recent moves

### Converting to GUI

To convert this to a GUI application, consider:

**Using tkinter (built-in)**:
```python
import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.buttons = []
        # ... implement GUI logic
```

**Using pygame**:
```python
import pygame
import sys

class TicTacToeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((300, 300))
        # ... implement game loop
```

**Web-based with Flask**:
```python
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('game.html')
```

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Classic Tic Tac Toe game rules and mechanics
- Minimax algorithm implementation inspired by game theory principles
- Python community for excellent documentation and resources
- Contributors and testers who helped improve the game

## 📞 Support

If you encounter any issues or have questions:

1. Check the built-in help system (option 4 in the main menu)
2. Run the test suite to verify installation (`python main.py --test`)
3. Review this README for common solutions
4. Create an issue in the project repository

---

**Happy Gaming! 🎮** Enjoy playing Tic Tac Toe and challenging the AI opponent!