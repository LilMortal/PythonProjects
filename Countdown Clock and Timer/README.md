# 🕐 Countdown Clock and Timer

A versatile command-line countdown clock and timer application with multiple timer modes, progress visualization, and an intuitive interface. Perfect for productivity, cooking, workouts, or any time-based activities.

## 📖 Description

This Python application provides a comprehensive timing solution with three distinct modes: countdown timers for specific durations, stopwatch functionality for measuring elapsed time, and event countdowns for tracking time until specific dates. The application features a clean terminal interface with real-time progress bars, pause/resume functionality, and visual alerts when timers complete.

## ✨ Features

- **🎯 Multiple Timer Modes**
  - **Countdown Timer**: Set a specific duration and count down to zero
  - **Stopwatch**: Count up from zero with optional maximum time limit
  - **Event Countdown**: Count down to a specific date and time

- **⌨️ Interactive Controls**
  - Pause and resume functionality
  - Real-time display updates
  - Clean terminal interface with progress bars
  - Keyboard shortcuts for easy control

- **🎨 Visual Features**
  - Animated completion alerts
  - Progress bars showing timer completion percentage
  - Clear, formatted time display (HH:MM:SS)
  - Screen clearing for clean updates

- **🔧 Flexible Input Formats**
  - Time duration: `30` (seconds), `5:30` (MM:SS), `1:05:30` (HH:MM:SS)
  - Date/time: `2024-12-31 23:59:59`, `Dec 31 2024 11:59 PM`

- **💻 Command-Line Interface**
  - Interactive menu mode
  - Direct command-line arguments
  - Built-in help and examples

- **🧪 Built-in Testing**
  - Unit tests for core functionality
  - Input validation and error handling

## 🛠️ Requirements

- **Python Version**: Python 3.8 or higher
- **Dependencies**: None (uses only Python standard library)
- **Platform**: Cross-platform (Windows, macOS, Linux)

## 📦 Installation

1. **Download the files**:
   - Save `main.py` to your desired directory
   - No additional dependencies need to be installed

2. **Make the script executable** (optional, for Unix-like systems):
   ```bash
   chmod +x main.py
   ```

3. **Verify Python version**:
   ```bash
   python --version
   # or
   python3 --version
   ```

## 🚀 How to Run

### Interactive Mode (Recommended)
```bash
python main.py
```

This launches the interactive menu where you can choose your timer mode and configure settings through prompts.

### Command-Line Mode

**Countdown Timer:**
```bash
# 5-minute countdown
python main.py --countdown 300

# 10 minutes 30 seconds
python main.py --countdown 10:30

# 1 hour 5 minutes 30 seconds
python main.py --countdown 1:05:30
```

**Stopwatch:**
```bash
# Basic stopwatch
python main.py --stopwatch

# Stopwatch with 5-minute maximum
python main.py --stopwatch --max 5:00
```

**Event Countdown:**
```bash
# Countdown to New Year
python main.py --event "2024-12-31 23:59:59"

# Countdown to specific event
python main.py --event "Dec 25 2024 9:00 AM"
```

**Run Tests:**
```bash
python main.py --test
```

## 📝 Example Usage

### Example 1: Pomodoro Timer
```bash
python main.py --countdown 25:00
```
Perfect for 25-minute work sessions in the Pomodoro Technique.

### Example 2: Workout Timer
```bash
python main.py --stopwatch --max 30:00
```
Track your workout time with a 30-minute maximum.

### Example 3: Birthday Countdown
```bash
python main.py --event "2024-07-15 00:00:00"
```
Count down to a special birthday.

### Example 4: Interactive Cooking Timer
1. Run `python main.py`
2. Choose option 1 (Countdown Timer)
3. Enter `20:00` for a 20-minute cooking timer
4. Use SPACE to pause if needed

## ⌨️ Controls During Timer

- **SPACE**: Pause/Resume timer
- **Q**: Quit timer
- **R**: Reset timer
- **Ctrl+C**: Force quit application

## 🔧 Advanced Features

### Multiple Time Formats Supported

**Duration Input:**
- `30` → 30 seconds
- `5:30` → 5 minutes 30 seconds  
- `1:05:30` → 1 hour 5 minutes 30 seconds

**Date/Time Input:**
- `2024-12-31 23:59:59`
- `Dec 31 2024 11:59 PM`
- `31/12/2024 23:59`

### Error Handling
- Input validation for all time formats
- Graceful handling of invalid dates
- Clear error messages for troubleshooting

## 🧪 Testing

The application includes built-in unit tests:

```bash
python main.py --test
```

This tests:
- Time parsing functionality
- Time formatting
- Input validation

## 🌟 Future Improvements

### Potential Enhancements
- **🔊 Audio Alerts**: Add sound notifications when timers complete
- **📱 Desktop Notifications**: System tray notifications for timer completion
- **💾 Save Presets**: Save frequently used timer configurations
- **📊 Statistics**: Track timer usage and completion rates
- **🎨 Themes**: Multiple color schemes and display styles
- **⏰ Multiple Timers**: Run several timers simultaneously
- **📱 Mobile App**: Convert to mobile application
- **🌐 Web Interface**: Browser-based version

### Converting to GUI

**Using Tkinter:**
```python
import tkinter as tk
from tkinter import ttk

# Replace terminal interface with GUI widgets
# Use tk.after() for timer updates instead of time.sleep()
```

**Using PyQt/PySide:**
```python
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

# More advanced GUI with better styling options
```

**Web Version with Flask:**
```python
from flask import Flask, render_template
from flask_socketio import SocketIO

# Real-time web interface with WebSocket updates
```

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with Python's standard library for maximum compatibility
- Inspired by productivity techniques like Pomodoro Timing
- Designed for developers, students, and anyone who needs reliable timing tools

## 📞 Support

If you encounter any issues:

1. **Check Python Version**: Ensure you're using Python 3.8+
2. **Run Tests**: Use `python main.py --test` to verify functionality
3. **Check Input Format**: Verify your time/date format matches the examples
4. **Terminal Compatibility**: Some terminals may not support all display features

## 🚀 Quick Start

1. Download `main.py`
2. Open terminal/command prompt
3. Navigate to the file directory
4. Run `python main.py`
5. Choose your timer mode and start timing!

---

**Happy Timing!** ⏰✨
