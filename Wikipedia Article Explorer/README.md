# 🌟 Wikipedia Article Explorer

A powerful command-line tool that lets you discover and explore random Wikipedia articles, search for specific topics, and track your exploration journey. Perfect for learning something new every day or satisfying your curiosity about any topic!

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 Project Description

Wikipedia Article Explorer is an interactive Python application that connects to Wikipedia's API to fetch articles, providing an engaging way to discover knowledge. Whether you want to stumble upon random interesting topics or search for specific subjects, this tool makes Wikipedia exploration fun and organized.

The application maintains a session history of all articles you've explored, provides statistics about your interests, and allows you to save your discoveries for later reference.

## ✨ Features

- **🎲 Random Article Discovery**: Get completely random Wikipedia articles from any topic
- **🔍 Smart Search**: Search for articles using keywords and select from results
- **📖 Direct Article Access**: Fetch specific articles by title
- **📚 Session History**: Keep track of all articles explored in your session
- **📊 Exploration Statistics**: View stats about your interests and most explored categories
- **💾 Export Functionality**: Save your session data to JSON files for later reference
- **🎨 Beautiful CLI Interface**: Clean, emoji-rich interface with formatted output
- **⚡ Error Handling**: Robust error handling for network issues and invalid inputs
- **🔒 Safe & Reliable**: Uses official Wikipedia APIs with proper rate limiting

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Internet connection (for accessing Wikipedia API)

### Step 1: Download the Project

Save the `main.py` file to your desired directory.

### Step 2: Verify Python Version

```bash
python --version
# or
python3 --version
```

Make sure you have Python 3.8 or higher installed.

### Step 3: No Additional Dependencies Required!

This project uses only Python's standard library, so no additional packages need to be installed. Everything you need is built-in!

## 🏃 How to Run

Navigate to the project directory and run:

```bash
python main.py
```

Or on some systems:

```bash
python3 main.py
```

## 📖 Usage Examples

### Main Menu Interface
```
🌟 Wikipedia Article Explorer
1. Get random article
2. Search for article
3. Get article by title
4. Show session history
5. Show statistics
6. Save session to file
7. Help
8. Exit
------------------------------
Select an option (1-8):
```

### Example: Random Article Discovery
```
Select an option (1-8): 1
🎲 Fetching random article...
📖 Fetching article: Quantum Entanglement

================================================================================
📄 Quantum Entanglement
================================================================================
🔗 URL: https://en.wikipedia.org/wiki/Quantum_entanglement
🏷️  Categories: Quantum mechanics, Physics phenomena, Quantum information
⏰ Last modified: 2024-01-15

📝 Summary:
   Quantum entanglement is a phenomenon in quantum mechanics where particles
   become interconnected and the quantum state of each particle cannot be
   described independently...
--------------------------------------------------------------------------------
```

### Example: Search Functionality
```
Select an option (1-8): 2
Enter search query: space exploration

🔍 Searching for: space exploration
🔍 Found 5 results:
   1. Space exploration
   2. Timeline of space exploration
   3. Private spaceflight
   4. Mars exploration
   5. Space Race

Select article number (0 to cancel): 1
```

### Example: Session Statistics
```
Select an option (1-8): 5

📊 Session Statistics:
   Articles explored: 7
   Top categories: Science (3), History (2), Technology (2)
```

## 🛠️ Command Line Options

The application runs in interactive mode by default. Here are the available options:

| Option | Description |
|--------|-------------|
| 1 | Get a completely random Wikipedia article |
| 2 | Search for articles using keywords |
| 3 | Get a specific article by entering its exact title |
| 4 | View all articles explored in current session |
| 5 | Display statistics about your exploration patterns |
| 6 | Save your session history to a JSON file |
| 7 | Display detailed help information |
| 8 | Exit the application |

## 📁 File Structure

```
wikipedia-explorer/
├── main.py                 # Main application file
├── README.md              # This file
└── wikipedia_session_*.json # Generated session files (after saving)
```

## 🧪 Testing

The application includes basic unit tests. To run them, uncomment the test line in `main.py`:

```python
if __name__ == "__main__":
    run_tests()  # Uncomment this line
    main()
```

Then run:
```bash
python main.py
```

## 🔧 Configuration Options

You can modify these variables at the top of the `WikipediaExplorer` class:

- `base_url`: Wikipedia REST API endpoint
- `api_url`: Wikipedia API endpoint
- Search result limits
- Timeout values for network requests

## 🎯 Future Improvements / Next Steps

### Short-term Enhancements
- [ ] Add support for different Wikipedia language editions
- [ ] Implement article bookmarking/favorites system
- [ ] Add article reading time estimation
- [ ] Include article word count and statistics
- [ ] Add offline mode with cached articles

### Medium-term Features
- [ ] **GUI Version**: Create a desktop application using tkinter or PyQt
- [ ] **Web Interface**: Build a Flask/Django web version
- [ ] Image display support for article thumbnails
- [ ] Article comparison and similarity detection
- [ ] Export to different formats (PDF, HTML, Markdown)

### Advanced Features
- [ ] Machine learning-powered article recommendations
- [ ] Social features (share interesting articles)
- [ ] Integration with note-taking applications
- [ ] Voice-to-text search capabilities
- [ ] Accessibility improvements (screen reader support)

## 🌐 Converting to Web/GUI Version

### Web Version (Flask)
To convert this to a web application:

1. Install Flask: `pip install flask`
2. Create HTML templates for the interface
3. Convert the CLI methods to web routes
4. Use AJAX for dynamic content loading
5. Add CSS styling for better presentation

### GUI Version (tkinter)
To create a desktop GUI:

1. Import tkinter (included with Python)
2. Replace CLI inputs with GUI widgets
3. Create buttons for each main function
4. Add text areas for article display
5. Implement file dialogs for saving sessions

### Example GUI Structure:
```python
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class WikipediaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wikipedia Explorer")
        self.explorer = WikipediaExplorer()
        self.setup_ui()
    
    def setup_ui(self):
        # Create buttons, text areas, etc.
        pass
```

## 🤝 Contributing

This is a single-file educational project, but feel free to:

1. Fork the project
2. Add new features
3. Improve error handling
4. Enhance the user interface
5. Add more comprehensive tests

## 📋 Requirements Summary

- **Python Version**: 3.8 or higher
- **Dependencies**: None (uses standard library only)
- **Internet**: Required for Wikipedia API access
- **Platform**: Cross-platform (Windows, macOS, Linux)

## 🙏 Acknowledgments

- **Wikipedia**: For providing free access to their comprehensive API
- **Python Community**: For the excellent standard library that made this possible
- **Contributors**: Thanks to anyone who improves this project

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🆘 Troubleshooting

### Common Issues

**"Module not found" error**: Make sure you're using Python 3.8+
```bash
python --version
```

**Network timeout errors**: Check your internet connection and try again

**SSL certificate errors**: Update your Python installation or run:
```bash
pip install --upgrade certifi
```

**Permission errors when saving files**: Make sure you have write permissions in the current directory

### Getting Help

If you encounter issues:
1. Check that you're using Python 3.8 or higher
2. Ensure you have an active internet connection
3. Try running the built-in tests
4. Check the error messages for specific guidance

---

**Happy exploring! 🌟 Discover something amazing today!**
