# 🎲 Dice Rolling Simulator

A comprehensive and interactive command-line dice rolling application with multiple game modes, custom dice support, and statistical tracking. Perfect for tabletop gaming, probability experiments, or just having fun with dice!

## ✨ Features

### Core Rolling Modes
- **Standard Dice Rolling** - Roll any number of dice with any number of sides
- **Advantage/Disadvantage** - Roll two dice and take the higher (advantage) or lower (disadvantage) result
- **Modified Rolls** - Add or subtract modifiers to your dice rolls
- **Drop Lowest** - Roll multiple dice and drop the lowest results (great for D&D ability scores)
- **Exploding Dice** - Dice that "explode" and roll again when they hit maximum values
- **Custom Dice** - Create and save dice with custom face values

### Game-Specific Quick Rolls
- **D&D Integration** - Ability scores (4d6 drop lowest), attack rolls (1d20), damage rolls
- **Board Games** - Monopoly (2d6), Yahtzee (5d6), Risk attacks (3d6)
- **Party Games** - Farkle (6d6) and more

### Advanced Features
- **Roll History** - Track all your rolls with timestamps
- **Statistics** - View detailed statistics about your rolling patterns
- **Animated Rolling** - Fun visual dice rolling animation
- **Error Handling** - Robust input validation and error management
- **Custom Dice Library** - Save and reuse custom dice configurations

## 🚀 Setup and Installation

### Requirements
- Python 3.10 or higher
- No external dependencies required (uses only Python standard library)

### Installation
1. Download the `dice_simulator.py` file
2. Make it executable (optional):
   ```bash
   chmod +x dice_simulator.py
   ```

### Running the Application
```bash
python dice_simulator.py
```

Or if you made it executable:
```bash
./dice_simulator.py
```

## 📖 Usage Examples

### Basic Usage
When you run the application, you'll see an interactive menu with numbered options. Simply enter the number corresponding to your desired action.

### Example Session
```
🎲 DICE ROLLING SIMULATOR 🎲
==================================================
1. Roll Standard Dice
2. Roll with Advantage/Disadvantage
...

Choose an option (0-11): 1
Number of sides (default 6): 20
Number of dice (default 1): 2

🎲 Rolling... ⚃

🎲 Standard Roll (2d20)
   Rolls: [15, 8]
   Total: 23
```

### Sample Custom Dice Creation
```
Choose an option (0-11): 6
Enter name for custom dice: Fudge
Enter face values separated by spaces (e.g., 1 3 5 7 9): -1 -1 0 0 1 1
✅ Custom dice 'Fudge' created with faces: [-1, -1, 0, 0, 1, 1]
```

### Quick Roll Examples
The application includes preset configurations for popular games:
- **D&D Ability Scores**: Automatically rolls 4d6 and drops the lowest
- **Yahtzee**: Rolls 5d6 for the classic dice game
- **Monopoly**: Rolls 2d6 for board game movement

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Libraries Used**:
  - `random` - For dice rolling mechanics
  - `time` - For timestamps and animations
  - `sys` - For clean application exit
  - `typing` - For type hints and better code documentation

## 🎯 Code Structure

The application is built around a main `DiceSimulator` class that handles:
- Different rolling algorithms
- History tracking
- Statistics calculation
- Custom dice management

Key components:
- **DiceSimulator Class**: Core functionality for all dice rolling operations
- **Animation Functions**: Visual feedback for rolling actions
- **Menu Systems**: Interactive CLI navigation
- **Input Validation**: Robust error handling and user input validation

## 📊 Statistics Features

The application tracks comprehensive statistics including:
- Total number of roll sessions
- Total individual dice rolled
- Average roll value across all dice
- Highest and lowest individual rolls
- Most frequently rolled number
- Complete roll history with timestamps

## 🎮 Gaming Applications

Perfect for:
- **Tabletop RPGs** (D&D, Pathfinder, etc.)
- **Board Games** (Risk, Monopoly, Yahtzee)
- **Probability Learning** and statistical analysis
- **Game Development** testing and prototyping
- **Educational Purposes** for teaching probability

## 🚀 Future Enhancement Ideas

### Planned Features
- **GUI Version** using Tkinter for visual interface
- **Web Interface** using Flask for browser-based rolling
- **Discord Bot** integration for online gaming groups
- **Dice Notation Parser** (e.g., "3d6+2", "1d20 advantage")
- **Roll Macros** for saving complex roll combinations
- **Probability Calculator** for analyzing odds
- **Export Functionality** for saving roll history to files

### Advanced Features
- **Multiple Dice Sets** for different characters/scenarios
- **Dice Bag Simulation** with limited dice quantities
- **Tournament Mode** for competitive rolling
- **Sound Effects** for enhanced experience
- **Custom Themes** and visual customization
- **API Integration** for online dice rolling services

### Technical Improvements
- **Configuration File** support for saving preferences
- **Plugin System** for custom rolling modes
- **Multi-language Support** for international users
- **Performance Optimization** for handling large numbers of dice
- **Unit Tests** for code reliability

## 🤝 Contributing

This is a single-file educational project, but contributions and improvements are welcome! Consider:

1. **Bug Reports**: If you find any issues with the dice rolling logic
2. **Feature Suggestions**: Ideas for new rolling modes or game integrations
3. **Code Improvements**: Better algorithms, error handling, or user experience
4. **Documentation**: Improvements to this README or inline code comments

## 📝 License

This project is open source and available for educational and personal use. Feel free to modify, distribute, and use in your own projects.

## 🎲 Credits

- **Dice Unicode Characters**: Uses Unicode dice symbols (⚀⚁⚂⚃⚄⚅) for rolling animation
- **Game Mechanics**: Inspired by popular tabletop games and RPG systems
- **Python Community**: Built using Python's excellent standard library

## 📞 Support

If you encounter any issues:
1. Check that you're using Python 3.10 or higher
2. Ensure the file has proper permissions to execute
3. Verify all input follows the requested format (numbers, spaces, etc.)

## 🎯 Quick Start Checklist

- [ ] Download `dice_simulator.py`
- [ ] Ensure Python 3.10+ is installed
- [ ] Run `python dice_simulator.py`
- [ ] Try rolling some standard dice (option 1)
- [ ] Explore the quick rolls menu (option 10)
- [ ] Create a custom dice (option 6)
- [ ] Check your roll history (option 8)
- [ ] View your statistics (option 9)

---

**Ready to roll?** Download the file and start your dice rolling adventure! 🎲✨
