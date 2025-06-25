# 🧠 Interactive Quiz Application

A feature-rich command-line quiz application built in Python that tests your knowledge across multiple categories with scoring, progress tracking, and high score persistence.

## 📖 Project Description

This Interactive Quiz Application provides an engaging way to test your knowledge across different subjects. The app presents multiple-choice questions, tracks your progress in real-time, provides immediate feedback with explanations, and maintains high scores across sessions. Whether you're studying for exams, brushing up on general knowledge, or just having fun, this quiz app offers an educational and entertaining experience.

## ✨ Features

### Core Features
- **Multiple Categories**: Choose from General Knowledge, Science, and History
- **Customizable Quiz Length**: Select how many questions you want to answer
- **Real-time Progress Tracking**: See your current position in the quiz
- **Immediate Feedback**: Get instant results with explanations for each answer
- **Final Score Summary**: View detailed results including percentage and time taken
- **Answer Review**: Optional detailed review of all questions and answers after completion

### Advanced Features
- **High Score System**: Persistent high scores saved to JSON file
- **Performance Feedback**: Motivational messages based on your score
- **Randomized Questions**: Questions are randomly selected for each quiz session
- **Input Validation**: Robust error handling for all user inputs
- **Session Duration Tracking**: Monitor how long each quiz takes
- **Clean CLI Interface**: User-friendly command-line interface with clear navigation

## 🛠️ Installation & Setup

### Prerequisites
- **Python Version**: Python 3.7 or higher
- **Dependencies**: None (uses only standard library modules)

### Installation Steps

1. **Download the Files**
   ```bash
   # Save the main.py file to your desired directory
   # No additional installation required!
   ```

2. **Verify Python Installation**
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Make the Script Executable** (Optional, for Unix/Linux/macOS)
   ```bash
   chmod +x main.py
   ```

## 🚀 How to Run

### Basic Usage
```bash
python main.py
```

### Alternative Methods
```bash
# If you have multiple Python versions
python3 main.py

# If you made it executable (Unix/Linux/macOS)
./main.py
```

## 💡 Example Usage

### Sample Session Flow

```
============================================================
🧠 WELCOME TO THE INTERACTIVE QUIZ APP! 🧠
============================================================
Test your knowledge across different categories!
Answer multiple choice questions and track your progress.

📚 Available Categories:
------------------------------
1. General Knowledge (5 questions)
2. Science (5 questions)
3. History (5 questions)

Select a category (enter number): 1

📝 This category has 5 questions available.
How many questions would you like? (1-5): 3

🚀 Starting General Knowledge Quiz!
You'll be asked 3 questions.
Press Enter to begin...

============================================================
Question 1/3
============================================================
❓ What is the capital of France?

1. London
2. Berlin
3. Paris
4. Madrid

Your answer (enter number): 3
✅ Correct! Well done!
📖 Explanation: Paris has been the capital of France since 508 AD.

Press Enter to continue...

[Quiz continues...]

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
QUIZ COMPLETED!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉

📊 Your Results:
   Score: 2/3
   Percentage: 66.7%
   Duration: 1m 23s
   Category: General Knowledge

🥉 Not bad! Room for improvement!
```

### High Scores Display
```
🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆
HIGH SCORES
🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆

📚 General Knowledge:
   1. 100.0% (5/5) - 2m 15s - 2024-01-15 14:30:22
   2. 80.0% (4/5) - 1m 45s - 2024-01-15 14:25:10
```

## 🗂️ File Structure

```
quiz-app/
├── main.py              # Main application file
├── README.md            # This file
├── quiz_scores.json     # High scores (auto-generated)
└── requirements.txt     # Dependencies (optional)
```

## 🧪 Testing

The application includes basic unit tests that can be run by uncommenting the test code at the bottom of `main.py`:

```python
if __name__ == "__main__":
    # Uncomment the line below to run tests
    run_tests()  # <-- Uncomment this line
    
    # Run the main application
    # main()  # <-- Comment this line
```

Then run:
```bash
python main.py
```

## 🔧 Customization

### Adding New Questions
Modify the `_load_quiz_data()` method in the `QuizApp` class to add new questions:

```python
quiz_data = {
    "Your Category": [
        QuizQuestion(
            "Your question?",
            ["Option A", "Option B", "Option C", "Option D"],
            2,  # Index of correct answer (0-based)
            "Your explanation here"
        ),
        # Add more questions...
    ]
}
```

### Adding New Categories
Simply add a new key-value pair to the `quiz_data` dictionary with your category name and list of questions.

## 🚀 Future Improvements / Next Steps

### Immediate Enhancements
- **Question Import**: Load questions from external JSON/CSV files
- **Difficulty Levels**: Add easy, medium, hard question categories
- **Timer Mode**: Add time limits for questions or entire quizzes
- **Hints System**: Provide optional hints for difficult questions
- **Question Statistics**: Track which questions are most/least answered correctly

### Advanced Features
- **User Profiles**: Create and save individual user profiles
- **Multiplayer Mode**: Add competitive multiplayer functionality
- **Achievement System**: Unlock achievements for various milestones
- **Question Editor**: Built-in interface to add/edit questions
- **Export Results**: Save quiz results to PDF or other formats

### Technical Improvements
- **Database Integration**: Use SQLite or other database for data persistence
- **Configuration File**: External config file for app settings
- **Logging System**: Add comprehensive logging for debugging
- **API Integration**: Fetch questions from online quiz APIs
- **Performance Optimization**: Optimize for larger question databases

### Interface Upgrades
- **GUI Version**: Create a tkinter or PyQt desktop application
- **Web Version**: Convert to a Flask/Django web application
- **Mobile App**: Develop using frameworks like Kivy
- **Voice Interface**: Add text-to-speech and speech recognition
- **Rich Terminal UI**: Use libraries like `rich` or `textual` for better formatting

## 🌐 Converting to Web/GUI Version

### Web Application (Flask)
```python
# Install Flask: pip install flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
quiz_app = QuizApp()  # Your existing quiz logic

@app.route('/')
def home():
    return render_template('quiz.html')

@app.route('/api/categories')
def get_categories():
    return jsonify(list(quiz_app.categories.keys()))

# Add more routes for quiz functionality
```

### GUI Application (tkinter)
```python
import tkinter as tk
from tkinter import ttk, messagebox

class QuizGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interactive Quiz App")
        self.quiz_app = QuizApp()
        self.setup_ui()
    
    def setup_ui(self):
        # Create GUI elements
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(self.root, textvariable=self.category_var)
        category_combo['values'] = list(self.quiz_app.categories.keys())
        # Add more GUI elements...
```

## 📝 Requirements

### requirements.txt (Optional)
```
# This project uses only Python standard library
# No external dependencies required

# Optional enhancements (uncomment if needed):
# flask>=2.0.0          # For web version
# requests>=2.25.0      # For API integration
# rich>=10.0.0          # For enhanced terminal output
```

## 🙏 Acknowledgments

- **Python Standard Library**: Built using only built-in Python modules for maximum compatibility
- **Educational Content**: Sample questions cover fundamental knowledge across multiple subjects
- **Open Source**: Feel free to modify, distribute, and improve this application

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Some ways to contribute:
- Add more quiz questions and categories
- Improve the user interface and experience
- Add new features from the "Future Improvements" list
- Fix bugs and optimize performance
- Improve documentation and examples

---

**Happy Quizzing! 🧠✨**
