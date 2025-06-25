# 🗂️ Python File Explorer

A powerful command-line file manager built with Python that provides an intuitive interface for navigating and managing files and directories on your system.

## 📖 Project Description

Python File Explorer is a cross-platform command-line application that brings file management capabilities directly to your terminal. It offers a user-friendly interface with familiar commands for navigation, file operations, and search functionality. The application supports both Windows and Unix-like systems and provides visual indicators, formatted output, and comprehensive error handling.

## ✨ Features

- **Directory Navigation**: Navigate through directories with `cd`, `back`, and `forward` commands
- **File Listing**: Display directory contents with detailed information (type, size, modification date, permissions)
- **File Operations**: Create, delete, copy, and move files and directories
- **Search Functionality**: Find files using patterns with support for recursive searching
- **History Navigation**: Navigate back and forward through previously visited directories
- **Hidden Files Support**: Toggle display of hidden files and directories
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Visual Indicators**: Icons and formatting for better readability
- **File Size Formatting**: Human-readable file sizes (B, KB, MB, GB, TB)
- **Interactive Prompts**: Confirmation prompts for destructive operations

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- No third-party packages required (uses only standard library)

### Installation Steps

1. **Download the project files**
   ```bash
   # Create a new directory for the project
   mkdir python-file-explorer
   cd python-file-explorer
   ```

2. **Save the main.py file**
   - Copy the provided `main.py` code into a file named `main.py`

3. **Make the file executable (Unix/Linux/macOS)**
   ```bash
   chmod +x main.py
   ```

### Dependencies
This project uses only Python standard library modules:
- `os` - Operating system interface
- `sys` - System-specific parameters
- `shutil` - High-level file operations
- `stat` - File status
- `datetime` - Date and time handling
- `fnmatch` - Unix filename pattern matching
- `pathlib` - Object-oriented filesystem paths

## 🚀 How to Run

### Basic Usage
```bash
python main.py
```

### Running Tests (Optional)
Uncomment the test line in the `if __name__ == "__main__":` section:
```python
run_tests()  # Uncomment this line
```

Then run:
```bash
python main.py
```

## 📚 Example Usage

### Starting the Application
```
$ python main.py
🗂️  Python File Explorer
Type 'help' for commands or 'exit' to quit.

[current-directory]>
```

### Basic Navigation
```bash
# List current directory contents
[home]> ls

# Change to a directory
[home]> cd Documents

# Go back to parent directory
[Documents]> cd ..

# Show current directory path
[home]> pwd
Current directory: /home/user
```

### File Operations
```bash
# Create a new file
[Documents]> touch myfile.txt
File 'myfile.txt' created successfully.

# Create a new directory
[Documents]> mkdir projects
Directory 'projects' created successfully.

# Copy a file
[Documents]> cp myfile.txt backup.txt
'myfile.txt' copied to 'backup.txt' successfully.

# Move/rename a file
[Documents]> mv backup.txt mybackup.txt
'backup.txt' moved to 'mybackup.txt' successfully.

# Delete a file (with confirmation)
[Documents]> rm myfile.txt
Delete file 'myfile.txt'? This cannot be undone! (y/N): y
File 'myfile.txt' deleted successfully.
```

### Search Operations
```bash
# Find files in current directory
[Documents]> find *.txt

# Recursive search
[Documents]> find -r *.py
Found 3 matches:
  📄 script.py
  📁 projects/main.py
  📄 utils/helper.py
```

### Directory Listing Example Output
```
📁 Current Directory: /home/user/Documents
================================================================================
Type   Name                           Size       Modified          Permissions
--------------------------------------------------------------------------------
DIR    📁 .. (parent)                -          -                 -
DIR    📁 projects                   -          2024-01-15 14:30  drwxr-xr-x
FILE   📄 document.pdf               2.3 MB     2024-01-14 09:15  -rw-r--r--
FILE   📄 notes.txt                  1.2 KB     2024-01-15 16:45  -rw-r--r--
LINK   🔗 shortcut                   -          2024-01-10 11:20  lrwxrwxrwx
```

## 🎯 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `ls` or `list` | List directory contents | `ls` |
| `ls -a` | List all files including hidden | `ls -a` |
| `cd <dir>` | Change directory | `cd projects` |
| `cd ..` | Go to parent directory | `cd ..` |
| `pwd` | Print current directory | `pwd` |
| `back` | Go back in history | `back` |
| `forward` | Go forward in history | `forward` |
| `touch <file>` | Create empty file | `touch newfile.txt` |
| `mkdir <dir>` | Create directory | `mkdir newfolder` |
| `rm <name>` | Delete file/directory | `rm oldfile.txt` |
| `cp <src> <dst>` | Copy file/directory | `cp file1.txt file2.txt` |
| `mv <src> <dst>` | Move/rename item | `mv old.txt new.txt` |
| `find <pattern>` | Search in current directory | `find *.py` |
| `find -r <pattern>` | Recursive search | `find -r *.txt` |
| `clear` | Clear screen | `clear` |
| `help` | Show help information | `help` |
| `exit` or `quit` | Exit the program | `exit` |

## 🔄 Future Improvements

### Planned Enhancements
- **File Editing**: Integrate with default text editors for file editing
- **Archive Support**: Add support for creating and extracting ZIP/TAR archives
- **File Permissions**: Advanced permission management commands
- **Configuration File**: User preferences and custom settings
- **Bookmarks**: Save and quickly navigate to favorite directories
- **File Preview**: Preview text files and images directly in terminal
- **Batch Operations**: Support for multiple file operations
- **Plugin System**: Extensible architecture for custom commands

### Web/GUI Conversion Guide

#### Converting to Web Application
To convert this into a web application:

1. **Framework Selection**: Use Flask or FastAPI for the backend
2. **Frontend**: Create an HTML interface with JavaScript for file operations
3. **File Upload/Download**: Implement file transfer capabilities
4. **Security**: Add authentication and path sanitization
5. **WebSocket**: For real-time directory updates

Example Flask structure:
```python
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
explorer = FileExplorer()

@app.route('/')
def index():
    return render_template('file_explorer.html')

@app.route('/api/list')
def api_list():
    items = explorer.list_directory()
    return jsonify([item.name for item in items])
```

#### Converting to GUI Application
To create a desktop GUI version:

1. **Tkinter Version**: Use Python's built-in GUI library
   ```python
   import tkinter as tk
   from tkinter import ttk, filedialog, messagebox
   ```

2. **PyQt/PySide Version**: For more advanced GUI features
   ```python
   from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
   ```

3. **Key Components**:
   - Tree view for directory structure
   - File list panel
   - Toolbar with common operations
   - Status bar for current path
   - Context menus for file operations

## 🧪 Testing

The application includes basic unit tests that can be enabled by uncommenting the test call in the main section. The tests cover:

- File size formatting functionality
- Directory accessibility
- Directory listing operations

To run tests:
```python
# In main.py, uncomment:
run_tests()
```

## 📄 License

This project is released under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- Built using Python's standard library for maximum compatibility
- Inspired by traditional command-line file managers like `mc` (Midnight Commander)
- Icons and visual elements designed for terminal compatibility
- Cross-platform design tested on Windows, macOS, and Linux

## 🐛 Known Issues

- Large directories may take time to load
- Some special characters in filenames might not display correctly in all terminals
- Windows path handling may vary between different terminal emulators

## 📞 Support

If you encounter issues or have suggestions:
1. Check that you're using Python 3.8+
2. Ensure you have proper file system permissions
3. Try running in a different terminal if display issues occur
4. For recursive operations on large directories, be patient as they may take time

---

**Happy file exploring! 🗂️✨**