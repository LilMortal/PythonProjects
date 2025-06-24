# 🗓️ Leap It! - Advanced Leap Year Calculator

A comprehensive Python tool for leap year calculations, analysis, and exploration. More than just a simple leap year checker - it's a complete toolkit for understanding leap years!

## 📋 Project Description

Leap It! is an educational and practical tool that goes beyond basic leap year checking. It provides detailed analysis, statistics, and interactive features to help users understand leap years and their patterns throughout history and into the future.

The project demonstrates clean Python coding practices, object-oriented design, command-line interface development, and comprehensive error handling.

## ✨ Features

- **Single Year Check**: Determine if any year is a leap year with detailed information
- **Range Analysis**: Analyze leap year patterns across any date range
- **Interactive Mode**: User-friendly menu-driven interface
- **Command-Line Interface**: Quick operations via command-line arguments
- **Statistical Analysis**: Comprehensive statistics about leap year distribution
- **Next/Previous Finder**: Find the nearest leap years to any given year
- **Current Year Quick Check**: Instantly check if the current year is a leap year
- **Visual Output**: Clean, formatted output with emojis and ASCII art
- **Error Handling**: Robust input validation and error messages
- **Unit Tests**: Built-in testing functionality

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- No third-party packages required (uses only standard library)

### Installation Steps

1. **Download the project files**:
   ```bash
   # Save main.py and README.md to your desired directory
   mkdir leap-it
   cd leap-it
   # Copy the main.py file content to main.py
   ```

2. **Make the script executable** (optional, for Unix/Linux/macOS):
   ```bash
   chmod +x main.py
   ```

3. **Verify Python version**:
   ```bash
   python --version
   # Should show Python 3.10 or higher
   ```

## 🚀 How to Run

### Interactive Mode (Recommended)
```bash
python main.py
```

This launches the interactive menu where you can:
- Check individual years
- Analyze date ranges  
- Quick-check the current year
- Find leap years around a specific year

### Command-Line Options

**Check a specific year**:
```bash
python main.py -y 2024
python main.py --year 2000
```

**Analyze a range of years**:
```bash
python main.py -r 2000 2030
python main.py --range 1900 2000
```

**Check current year**:
```bash
python main.py -c
python main.py --current
```

**View help**:
```bash
python main.py -h
python main.py --help
```

## 📝 Example Usage

### Interactive Mode Example
```
    ╔═══════════════════════════════════════╗
    ║              🗓️  LEAP IT! 🗓️             ║
    ║        Advanced Leap Year Tool        ║
    ║              Version 1.0              ║
    ╚═══════════════════════════════════════╝

🎯 Choose an option:
1. Check a single year
2. Analyze a range of years
3. Quick check current year
4. Find leap years around a specific year
5. Exit

Enter your choice (1-5): 1
Enter a year: 2024

📅 Year Analysis: 2024
========================================
Leap Year: ✅ YES
Days in February: 29
🎉 This year has an extra day (February 29th)!

Next leap year: 2028
Previous leap year: 2020
```

### Command-Line Example
```bash
$ python main.py -r 2020 2030

📊 Leap Year Analysis: 2020 - 2030
==================================================
Total years analyzed: 11
Leap years found: 3
Percentage of leap years: 27.27%
Average gap between leap years: 3.7 years
First leap year: 2020
Last leap year: 2028

🗓️ All leap years in range:
   2020 2024 2028
```

## 🧪 Running Tests

The project includes built-in unit tests. To run them:

1. Open `main.py` in a text editor
2. Uncomment the line `# run_tests()` near the bottom (line 369)
3. Run the script:
   ```bash
   python main.py
   ```

The tests will run before the main application starts.

## 📁 Project Structure

```
leap-it/
├── main.py           # Main application file
├── README.md         # This documentation
└── requirements.txt  # Empty (no external dependencies)
```

## 🎓 Educational Value

This project demonstrates:
- **Object-Oriented Programming**: Clean class design with `LeapYearAnalyzer` and `LeapItCLI`
- **Algorithm Implementation**: Both custom and built-in leap year calculation methods
- **CLI Development**: Using `argparse` for command-line interfaces
- **Error Handling**: Comprehensive input validation and exception handling
- **Code Documentation**: Detailed docstrings and comments
- **Testing**: Built-in unit tests for validation
- **User Experience**: Interactive menus and formatted output

## 🚀 Future Improvements

Here are some ideas to extend this project:

### Easy Enhancements
- Add date calculations (e.g., "What day of the week was February 29, 2000?")
- Export results to CSV or JSON files
- Add more statistical analysis (leap year frequency over centuries)
- Include historical context about calendar reforms

### Medium Enhancements
- **Web Interface**: Convert to Flask/Django web application
- **GUI Version**: Create a tkinter or PyQt desktop application
- **Calendar Visualization**: Generate visual calendars showing leap years
- **API Mode**: Create REST API endpoints for leap year data

### Advanced Features
- **Database Integration**: Store and query historical leap year data
- **Plotting**: Generate graphs showing leap year distribution over time
- **Internationalization**: Support for different calendar systems
- **Performance Optimization**: Handle very large date ranges efficiently

## 🌐 Converting to Web/GUI

### Web Version (Flask)
```python
# Basic Flask structure to get you started
from flask import Flask, render_template, request
from main import LeapYearAnalyzer

app = Flask(__name__)
analyzer = LeapYearAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_year():
    year = int(request.form['year'])
    is_leap = analyzer.is_leap_year(year)
    return render_template('result.html', year=year, is_leap=is_leap)
```

### GUI Version (tkinter)
```python
# Basic tkinter structure
import tkinter as tk
from main import LeapYearAnalyzer

class LeapYearGUI:
    def __init__(self):
        self.analyzer = LeapYearAnalyzer()
        self.root = tk.Tk()
        self.root.title("Leap It! GUI")
        # Add widgets here
        
    def check_year(self):
        # Implementation here
        pass
```

## 📄 License

This project is created as an educational example and is free to use, modify, and distribute.

## 🙏 Acknowledgments

- **Calendar Algorithm**: Based on the Gregorian calendar leap year rules
- **Python Community**: For excellent documentation and standard library
- **Educational Purpose**: Designed to demonstrate Python best practices

## 📞 Support

This is an educational project. For questions about Python programming concepts demonstrated here, consult:
- [Python Official Documentation](https://docs.python.org/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/) for advanced tutorials

## 🎯 Learning Objectives

After exploring this project, you should understand:
- How to structure a complete Python application
- Object-oriented programming principles
- Command-line argument parsing
- Interactive user interfaces in Python
- Error handling and input validation
- Unit testing basics
- Code documentation practices

---

**Happy leap year calculating! 🗓️✨**
