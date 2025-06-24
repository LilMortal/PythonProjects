# 🔢 Advanced Calculator

A comprehensive command-line calculator built in Python that supports basic arithmetic, scientific functions, memory operations, and expression evaluation. Perfect for quick calculations, mathematical operations, and educational purposes.

## 📋 Project Description

This Advanced Calculator is a feature-rich, interactive command-line application that goes beyond simple arithmetic. It provides a user-friendly interface for performing complex mathematical calculations, including trigonometric functions, logarithms, and memory operations. The calculator maintains a history of calculations and includes comprehensive error handling to ensure reliable operation.

## ✨ Features

### Basic Operations
- **Arithmetic**: Addition (+), Subtraction (-), Multiplication (*), Division (/)
- **Advanced Math**: Power (** or ^), Modulo (%), Floor Division (//)
- **Order of Operations**: Proper precedence handling with parentheses support

### Scientific Functions
- **Trigonometric**: sin, cos, tan, asin, acos, atan
- **Logarithmic**: log (base-10), ln (natural logarithm)
- **Mathematical**: sqrt, abs, ceil, floor, round, factorial

### Memory Operations
- Store values in memory
- Add to or subtract from memory
- Recall memory contents
- Clear memory

### Additional Features
- **Constants**: Built-in support for π (pi), e, and τ (tau)
- **History**: Track and display previous calculations
- **Error Handling**: Comprehensive validation and error messages
- **Help System**: Built-in documentation and examples
- **Expression Evaluation**: Support for complex mathematical expressions

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- No external dependencies required (uses only standard library)

### Installation Steps

1. **Download the project files**
   ```bash
   # Create a new directory for the project
   mkdir advanced-calculator
   cd advanced-calculator
   ```

2. **Save the Python file**
   - Copy the `main.py` code into a file named `main.py`

3. **Make the file executable (optional)**
   ```bash
   chmod +x main.py
   ```

### Dependencies
This project uses only Python standard library modules:
- `math` - Mathematical functions
- `re` - Regular expressions for input validation
- `sys` - System-specific parameters
- `typing` - Type hints for better code documentation

No `requirements.txt` is needed as no third-party packages are required.

## 🚀 How to Run

### Start the Calculator
```bash
python main.py
```

### Alternative Method
```bash
python3 main.py
```

The calculator will start with a welcome message and prompt you for input.

## 📖 Usage Examples

### Basic Arithmetic
```
calc> 2 + 3 * 4
14

calc> (15 + 5) / 4
5.0

calc> 2^10
1024
```

### Scientific Functions
```
calc> sqrt(16)
4

calc> sin(pi/2)
1.0

calc> log(100)
2.0

calc> factorial(5)
120
```

### Memory Operations
```
calc> mem= 10
Memory set to: 10.0

calc> mem+ 5
Memory: 15.0 (added 5.0)

calc> mem
Memory: 15.0
```

### Using Constants
```
calc> pi * 2
6.283185307179586

calc> e^2
7.38905609893065
```

### Special Commands
```
calc> help          # Show help information
calc> history       # Display calculation history
calc> clear         # Clear history
calc> quit          # Exit calculator
```

## 🎮 Interactive Features

### Command Prompt
The calculator uses a `calc>` prompt for easy identification and professional appearance.

### Error Handling
- Division by zero protection
- Invalid expression detection
- Overflow handling for large numbers
- Clear error messages for user guidance

### History Management
- Automatic storage of successful calculations
- Display last 10 calculations
- History clearing functionality

## 🧪 Testing

The project includes built-in unit tests. To run them:

1. **Edit the main.py file**
   - Uncomment the line `# run_tests()` at the bottom
   - Comment out the `main()` line

2. **Run tests**
   ```bash
   python main.py
   ```

Expected output:
```
Running tests...
✅ 2 + 3 = 5.0
✅ 10 - 4 = 6.0
✅ 3 * 4 = 12.0
...
Tests passed: 10/10
```

## 🔧 Code Structure

```
main.py
├── Calculator Class
│   ├── Basic Operations (add, subtract, multiply, divide)
│   ├── Expression Evaluation
│   ├── Memory Management
│   ├── History Tracking
│   └── Help System
├── Main Function (User Interface)
└── Unit Tests
```

## 🚀 Future Improvements

### Potential Enhancements
1. **Graphical User Interface (GUI)**
   - Convert to tkinter or PyQt application
   - Add button-based interface
   - Visual history display

2. **Web Interface**
   - Flask/Django web application
   - REST API for calculations
   - Browser-based interface

3. **Advanced Features**
   - Variable storage and manipulation
   - Function definition and execution
   - Plotting capabilities with matplotlib
   - Unit conversion utilities

4. **File Operations**
   - Save/load calculation sessions
   - Export history to CSV/JSON
   - Configuration file support

5. **Enhanced Scientific Functions**
   - Matrix operations
   - Statistical functions
   - Complex number support
   - Calculus operations (derivatives, integrals)

### Converting to GUI Version

To create a GUI version using tkinter:

```python
import tkinter as tk
from tkinter import ttk

class CalculatorGUI:
    def __init__(self, root):
        self.calc = Calculator()
        self.root = root
        self.setup_gui()
    
    def setup_gui(self):
        # Create input field
        self.entry = tk.Entry(root, width=30, font=('Arial', 12))
        self.entry.pack(pady=10)
        
        # Create calculate button
        calc_btn = tk.Button(root, text="Calculate", 
                           command=self.calculate)
        calc_btn.pack(pady=5)
        
        # Create result display
        self.result_label = tk.Label(root, text="Result: ", 
                                   font=('Arial', 12))
        self.result_label.pack(pady=10)

root = tk.Tk()
root.title("Advanced Calculator")
app = CalculatorGUI(root)
root.mainloop()
```

### Converting to Web Version

To create a web version using Flask:

```python
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
calc = Calculator()

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    expression = request.json['expression']
    result, output = calc.calculate(expression)
    return jsonify({'result': result, 'output': output})

if __name__ == '__main__':
    app.run(debug=True)
```

## 📝 Credits & Acknowledgments

- Built using Python standard library
- Mathematical functions provided by Python's `math` module
- Inspired by scientific calculators and programming language REPLs
- Error handling patterns adapted from Python best practices

## 📄 License

This project is open source and available for educational and personal use. Feel free to modify and distribute as needed.

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Include tests for new functionality
5. Submit a pull request

## 📞 Support

For questions or issues:
- Review the built-in help system (`help` command)
- Check the examples in this README
- Examine the code comments for implementation details

---

**Enjoy calculating! 🧮**
