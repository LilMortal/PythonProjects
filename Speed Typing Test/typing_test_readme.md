# 🎯 Speed Typing Test

A comprehensive command-line application to measure and improve your typing speed and accuracy. Test your WPM (Words Per Minute) with multiple difficulty levels and track your progress over time!

## 📋 Project Description

This Speed Typing Test is designed to help users improve their typing skills through engaging practice sessions. The application provides real-time feedback on typing speed and accuracy, supports multiple difficulty levels, and maintains a history of your performance to track improvement over time.

## ✨ Features

- **Multiple Difficulty Levels**: Choose from Easy, Medium, or Hard difficulty levels
- **Real-time Performance Metrics**: Get instant feedback on WPM and accuracy percentage
- **Progress Tracking**: Automatic saving of test results with detailed statistics
- **Performance Analytics**: View your typing statistics including averages and personal bests
- **Clean Interface**: User-friendly command-line interface with clear instructions
- **Error Handling**: Robust error handling for various edge cases
- **Cross-platform**: Works on Windows, macOS, and Linux
- **No External Dependencies**: Uses only Python standard library

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- No additional packages required (uses only standard library)

### Installation Steps

1. **Clone or Download**: Save the `main.py` file to your desired directory

2. **Verify Python Version**:
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Make the script executable** (Optional, for Unix-like systems):
   ```bash
   chmod +x main.py
   ```

## 🚀 How to Run

### Basic Usage
```bash
python main.py
```

### Alternative (if python3 is required):
```bash
python3 main.py
```

## 📱 Example Usage

### Starting the Application
```
=========================================================
🎯 SPEED TYPING TEST  
=========================================================
Welcome to the Speed Typing Test!
Test your typing speed and accuracy with various difficulty levels.

Instructions:
• Type the given text as quickly and accurately as possible
• Press Enter when you're done typing  
• Your WPM (Words Per Minute) and accuracy will be calculated
• Results are automatically saved to track your progress
=========================================================

🎯 MAIN MENU
1. Start Typing Test
2. View Statistics  
3. Exit

Enter your choice (1-3): 1
```

### Difficulty Selection
```
🎚️  Select Difficulty Level:
1. Easy (Simple words, shorter text)
2. Medium (Standard sentences)
3. Hard (Complex text with numbers/symbols)

Enter your choice (1-3): 2
```

### During the Test
```
────────────────────────────────────────────────────────
📝 TYPE THE FOLLOWING TEXT:
────────────────────────────────────────────────────────

The quick brown fox jumps over the lazy dog near the riverbank.

────────────────────────────────────────────────────────
Start typing when ready (Press Enter when done):
>>> The quick brown fox jumps over the lazy dog near the riverbank.
```

### Results Display
```
============================================================
📊 TEST RESULTS
============================================================
⏱️  Time Taken: 12.34 seconds
🚀 Speed: 42.5 WPM
🎯 Accuracy: 96.2%
✅ Correct Characters: 75/78
📈 Difficulty: Medium
👍 Good typing speed!
============================================================
✅ Results saved to typing_results.json
```

### Statistics View
```
============================================================
📈 YOUR TYPING STATISTICS
============================================================
📝 Total Tests: 15
⚡ Average Speed: 38.7 WPM
🎯 Average Accuracy: 94.3%
🏆 Best Speed: 52.1 WPM
🎖️  Best Accuracy: 100.0%
============================================================

🕐 RECENT RESULTS (Last 5):
1. 2024-01-15 14:30 | 42.5 WPM | 96.2% | medium
2. 2024-01-15 14:25 | 38.9 WPM | 92.1% | easy
3. 2024-01-15 14:20 | 45.2 WPM | 98.5% | medium
4. 2024-01-15 14:15 | 35.7 WPM | 89.3% | hard
5. 2024-01-15 14:10 | 40.1 WPM | 95.8% | medium
```

## 📁 Generated Files

The application creates the following files:

- **`typing_results.json`**: Contains all your test results and statistics in JSON format
  - Automatically created after your first test
  - Stores timestamp, difficulty, original text, typed text, performance metrics
  - Used for generating statistics and tracking progress

## 🧪 Testing

The application includes built-in unit tests. To run them:

1. Open `main.py` and uncomment the line:
   ```python
   run_unit_tests()
   ```

2. Run the script:
   ```bash
   python main.py
   ```

The tests will verify:
- WPM calculation accuracy
- Text accuracy measurement
- Text generation functionality

## 🎨 Customization Options

### Adding Custom Texts
Edit the `sample_texts` list in the `TypingTest` class to add your own practice texts:

```python
self.sample_texts = [
    "Your custom text here...",
    "Another practice sentence...",
    # Add more texts as needed
]
```

### Modifying Difficulty Levels
Adjust the difficulty parameters in the `difficulty_levels` dictionary:

```python
self.difficulty_levels = {
    'easy': {'words': 5, 'complexity': 'simple'},
    'medium': {'words': 8, 'complexity': 'moderate'},
    'hard': {'words': 12, 'complexity': 'complex'}
}
```

## 🌐 Converting to Web/GUI Version

### Web Version (Flask)
To create a web version, you could:
1. Install Flask: `pip install flask`
2. Create HTML templates for the typing interface
3. Use JavaScript for real-time typing detection
4. Convert the core logic to web routes

### GUI Version (Tkinter)
For a desktop GUI version:
1. Use Python's built-in `tkinter` library
2. Create a window with text display and input field
3. Add buttons for different difficulty levels
4. Display results in popup windows or separate frames

### Modern Web Version (FastAPI + React)
For a modern web application:
1. Backend: FastAPI for REST API
2. Frontend: React with real-time typing detection
3. Database: SQLite or PostgreSQL for storing results
4. Deployment: Docker containers

## 🚀 Future Improvements

### Planned Features
- [ ] **Multiplayer Mode**: Compete with friends in real-time
- [ ] **Custom Text Import**: Upload your own texts or documents
- [ ] **Typing Lessons**: Structured lessons for different skill levels
- [ ] **Visual Progress Charts**: Graphical representation of improvement
- [ ] **Sound Effects**: Audio feedback for correct/incorrect typing
- [ ] **Themes**: Different color schemes and display modes

### Advanced Features
- [ ] **Machine Learning**: Personalized difficulty adjustment based on performance
- [ ] **Error Analysis**: Detailed breakdown of common typing mistakes
- [ ] **Leaderboards**: Compare your scores with other users
- [ ] **Mobile App**: React Native or Flutter version
- [ ] **Voice Commands**: Start/stop tests with voice commands

### Technical Improvements
- [ ] **Database Integration**: Replace JSON file with proper database
- [ ] **Configuration File**: External config for customizable settings
- [ ] **Logging System**: Detailed logging for debugging and analytics
- [ ] **Plugin System**: Allow third-party extensions
- [ ] **API Endpoints**: RESTful API for integration with other apps

## 🤝 Contributing

Feel free to contribute to this project by:
1. Reporting bugs or issues
2. Suggesting new features
3. Submitting pull requests with improvements
4. Adding new sample texts
5. Creating translations for different languages

## 📄 License

This project is open-source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- **Typing Test Inspiration**: Based on popular online typing test platforms
- **Python Community**: For excellent documentation and libraries
- **Test Texts**: Sample sentences chosen for balanced difficulty and engagement
- **Users**: Thanks to all future users who will help improve this application

## 🆘 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running the script
**Solution**: Ensure you're using Python 3.8+ and all imports are from standard library

**Issue**: Results file not saving
**Solution**: Check write permissions in the current directory

**Issue**: Application crashes during input
**Solution**: Try using Python 3 instead of Python 2: `python3 main.py`

**Issue**: Text display formatting issues
**Solution**: Ensure your terminal supports UTF-8 encoding

### Getting Help

If you encounter any issues:
1. Check that you're using Python 3.8 or higher
2. Ensure you have write permissions in the script directory
3. Try running the unit tests to verify functionality
4. Check the generated `typing_results.json` file for any corruption

---

**Happy Typing! 🎯✨**

Start improving your typing skills today and track your progress over ti