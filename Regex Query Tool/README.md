# 🔍 Regex Query Tool

A comprehensive command-line regular expression testing and analysis tool built with Python. This tool provides multiple ways to test, validate, and analyze regular expressions with various output formats and advanced features.

## 📝 Description

The Regex Query Tool is designed to make working with regular expressions easier and more intuitive. Whether you're a beginner learning regex patterns or an experienced developer debugging complex expressions, this tool provides the functionality you need with a clean, user-friendly interface.

The tool supports pattern matching, text substitution, predefined common patterns, multiple output formats, and an interactive mode for exploratory regex work.

## ✨ Features

- **Pattern Matching**: Find all matches for regex patterns in text
- **Text Substitution**: Replace matched patterns with specified text
- **Predefined Patterns**: Built-in patterns for common use cases (email, phone, URL, etc.)
- **Multiple Output Formats**: Simple, detailed, JSON, and table formats
- **Regex Validation**: Validate patterns before execution
- **Flag Support**: Support for all Python regex flags (i, m, s, x, a, l)
- **Interactive Mode**: Real-time regex testing and exploration
- **Performance Metrics**: Execution time tracking
- **Error Handling**: Comprehensive error reporting and validation
- **Group Extraction**: Support for capturing groups and named groups

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- No external dependencies (uses only Python standard library)

### Setup
1. Clone or download the project files
2. Ensure Python 3.8+ is installed on your system
3. No additional installation required - ready to run!

```bash
# Check Python version
python --version

# Run the tool
python main.py --help
```

## 🎯 Usage

### Basic Command Line Usage

```bash
# Basic pattern matching
python main.py -p "\d+" -t "I have 123 apples and 456 oranges"

# Using flags (case insensitive)
python main.py -p "hello" -t "Hello World" -f "i"

# Detailed output format
python main.py -p "\w+" -t "Hello World" --format detailed

# JSON output format
python main.py -p "\d+" -t "Numbers: 1, 2, 3" --format json

# Using predefined patterns
python main.py -p "email" -t "Contact us at test@example.com" --predefined

# Text substitution
python main.py -p "\d+" -r "X" -t "Replace 123 with X" --substitute

# List all predefined patterns
python main.py --list-patterns
```

### Interactive Mode

```bash
# Start interactive mode
python main.py --interactive
```

In interactive mode, you can use these commands:
- `match <pattern> <text> [flags]` - Find matches
- `sub <pattern> <replacement> <text>` - Substitute text
- `validate <pattern>` - Validate a regex pattern
- `predefined` - List predefined patterns
- `use <pattern_name> <text>` - Use a predefined pattern
- `help` - Show available commands
- `quit` - Exit interactive mode

### Command Line Options

| Option | Description |
|--------|-------------|
| `-p, --pattern` | Regular expression pattern to use |
| `-t, --text` | Text to search in |
| `-f, --flags` | Regex flags (i, m, s, x, a, l) |
| `--format` | Output format: simple, detailed, json, table |
| `--predefined` | Use a predefined pattern by name |
| `--list-patterns` | List all available predefined patterns |
| `-r, --replace` | Replacement string for substitution |
| `--substitute` | Perform substitution instead of matching |
| `--count` | Maximum number of substitutions (0=all) |
| `--interactive` | Start interactive mode |

## 📋 Example Usage

### Example 1: Email Extraction
```bash
python main.py -p "email" -t "Contact john@example.com or support@company.org" --predefined --format detailed
```

**Output:**
```
==================================================
REGEX ANALYSIS RESULTS
==================================================
Pattern: \b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b
Flags: None
Execution time: 0.0001 seconds
Total matches: 2
--------------------------------------------------
Match #1:
  Text: 'john@example.com'
  Position: 8-23
  Length: 15 characters

Match #2:
  Text: 'support@company.org'
  Position: 27-46
  Length: 19 characters
```

### Example 2: Phone Number Validation
```bash
python main.py -p "phone" -t "Call us at (555) 123-4567 or 555.987.6543" --predefined
```

**Output:**
```
Found 2 match(es):
1. '(555) 123-4567' at position 11-26
2. '555.987.6543' at position 30-43
```

### Example 3: Text Substitution
```bash
python main.py -p "\d+" -r "[NUMBER]" -t "I have 5 cats and 3 dogs" --substitute
```

**Output:**
```
✅ Made 2 substitution(s)
Flags used: None
Result:
I have [NUMBER] cats and [NUMBER] dogs
```

### Example 4: JSON Output
```bash
python main.py -p "\b\w{4,}\b" -t "Find long words here" --format json
```

**Output:**
```json
{
  "pattern": "\\b\\w{4,}\\b",
  "flags": [],
  "execution_time": 0.0001,
  "total_matches": 2,
  "matches": [
    {
      "text": "Find",
      "start": 0,
      "end": 4,
      "groups": [],
      "named_groups": {}
    },
    {
      "text": "long",
      "start": 5,
      "end": 9,
      "groups": [],
      "named_groups": {}
    },
    {
      "text": "words",
      "start": 10,
      "end": 15,
      "groups": [],
      "named_groups": {}
    },
    {
      "text": "here",
      "start": 16,
      "end": 20,
      "groups": [],
      "named_groups": {}
    }
  ]
}
```

## 🎨 Predefined Patterns

The tool includes these built-in patterns:

| Pattern Name | Description | Example |
|--------------|-------------|---------|
| `email` | Email addresses | `user@example.com` |
| `phone` | Phone numbers | `(555) 123-4567` |
| `url` | Web URLs | `https://example.com` |
| `ipv4` | IPv4 addresses | `192.168.1.1` |
| `date_us` | US date format | `12/31/2023` |
| `time_24h` | 24-hour time | `14:30:00` |
| `hex_color` | Hex color codes | `#FF5733` |
| `credit_card` | Credit card numbers | `1234 5678 9012 3456` |
| `ssn` | Social Security Numbers | `123-45-6789` |
| `zip_code` | US ZIP codes | `12345-6789` |

## 🧪 Testing

The tool includes basic unit tests. To run them, uncomment the test lines at the bottom of `main.py`:

```python
# Uncomment these lines in main.py
run_tests()
sys.exit(0)
```

Then run:
```bash
python main.py
```

## 🎯 Future Improvements

- **Web Interface**: Convert to a web application using Flask/FastAPI
- **GUI Version**: Create a desktop GUI using Tkinter or PyQt
- **Pattern Library**: Expand predefined patterns with user contributions
- **Export Features**: Save results to files (CSV, Excel, etc.)
- **Regex Explanation**: Add pattern explanation and breakdown
- **Batch Processing**: Process multiple files at once
- **History Feature**: Save and recall previous queries
- **Syntax Highlighting**: Color-coded regex pattern display
- **Performance Benchmarking**: Compare different regex approaches
- **Pattern Optimization**: Suggest optimizations for slow patterns

## 🔧 Converting to Web/GUI Version

### Web Version (Flask)
To convert this to a web application:

1. Install Flask: `pip install flask`
2. Create a web interface with forms for pattern input
3. Use the existing `RegexQueryTool` class as the backend
4. Add JavaScript for real-time regex testing
5. Implement file upload for batch processing

### GUI Version (Tkinter)
To create a desktop GUI:

1. Use Tkinter (included with Python)
2. Create input fields for pattern and text
3. Add buttons for different operations
4. Use the existing tool class for processing
5. Display results in scrollable text areas

### Example GUI Structure:
```python
import tkinter as tk
from tkinter import ttk, scrolledtext

class RegexGUI:
    def __init__(self):
        self.tool = RegexQueryTool()
        self.setup_ui()
    
    def setup_ui(self):
        # Create main window
        # Add input fields
        # Add result display
        # Connect to existing tool methods
```

## 🤝 Contributing

This is a single-file project designed for learning and experimentation. Feel free to:

- Add new predefined patterns
- Improve output formatting
- Add new features
- Create tests for edge cases
- Optimize performance

## 📄 License

This project is provided as-is for educational and practical use. Feel free to modify and distribute.
