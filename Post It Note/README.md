# 🗒️ Post-it Notes Manager

A feature-rich command-line application for managing digital sticky notes. Create, organize, search, and manage your notes with colors and timestamps - all from your terminal!

## 📋 Project Description

Post-it Notes Manager is a Python-based CLI tool that brings the simplicity of physical sticky notes to your digital workspace. Whether you need to jot down quick reminders, organize tasks, or keep track of important information, this tool provides an intuitive interface for managing your notes efficiently.

The application stores all notes in a local JSON file, making it lightweight, portable, and completely offline. Perfect for developers, students, writers, or anyone who loves the simplicity of sticky notes but wants the power of digital organization.

## ✨ Features

- **📝 Create Notes**: Add notes with titles, content, and color coding
- **📚 List & View**: Display all notes or filter by color, view detailed note content
- **🔍 Search**: Find notes by searching through titles and content
- **✏️ Update**: Modify existing notes (title, content, or color)
- **🗑️ Delete**: Remove notes you no longer need
- **🎨 Color Coding**: Organize notes with 6 different colors (yellow, blue, green, pink, orange, purple)
- **📊 Statistics**: View summary statistics about your notes collection
- **💾 Auto-Save**: All changes are automatically saved to JSON file
- **🕐 Timestamps**: Track when notes were created and last updated
- **🖥️ Interactive Mode**: Run without arguments for a guided experience
- **⚡ Command-Line Mode**: Direct commands for power users
- **🧪 Unit Tests**: Built-in test suite for reliability

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+** (uses standard library only, no external dependencies!)
- Any operating system (Windows, macOS, Linux)

### Installation Steps

1. **Download the application**:
   ```bash
   # Save the main.py file to your desired directory
   curl -o main.py [URL_TO_RAW_FILE] # or manually download
   ```

2. **Make it executable** (optional, for Unix-like systems):
   ```bash
   chmod +x main.py
   ```

3. **Verify installation**:
   ```bash
   python main.py help
   ```

### No Dependencies Required!
This project uses only Python's standard library, so no `pip install` or virtual environment setup is needed.

## 🚀 How to Run

### Interactive Mode (Recommended for beginners)
```bash
python main.py
```
This starts the interactive mode where you can type commands and get guided prompts.

### Command-Line Mode (For power users)
```bash
# General syntax
python main.py <command> [arguments]

# Examples
python main.py create
python main.py list
python main.py view 1
python main.py search "meeting"
python main.py delete 5
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Create a new note (interactive) | `python main.py create` |
| `list [color]` | List all notes or filter by color | `python main.py list blue` |
| `view <id>` | View a specific note by ID | `python main.py view 1` |
| `search <query>` | Search notes by title/content | `python main.py search "project"` |
| `update <id>` | Update an existing note | `python main.py update 3` |
| `delete <id>` | Delete a note by ID | `python main.py delete 2` |
| `stats` | Show notes statistics | `python main.py stats` |
| `help` | Display help information | `python main.py help` |
| `exit` | Exit interactive mode | `exit` (in interactive mode) |

## 📖 Example Usage

### Creating Your First Note
```bash
$ python main.py create
📝 Creating a new note...
Enter note title: Project Meeting Notes
Enter note content (press Enter twice to finish):
- Discuss Q3 roadmap
- Review budget allocation
- Plan team building event

Available colors: yellow, blue, green, pink, orange, purple
Enter color (default: yellow): blue
✅ Note created successfully! (ID: 1)
```

### Listing Notes
```bash
$ python main.py list
📚 Your Notes (3 total):
============================================================
# 1 | 🎨 blue     | Project Meeting Notes          | 2024-06-24 10:30:15
# 2 | 🎨 yellow   | Grocery List                   | 2024-06-24 11:45:22
# 3 | 🎨 green    | Book Recommendations           | 2024-06-24 14:20:33
============================================================
💡 Use 'view <id>' to see full content or 'help' for more options
```

### Viewing a Specific Note
```bash
$ python main.py view 1
==================================================
📝 Note #1 - Project Meeting Notes
==================================================
- Discuss Q3 roadmap
- Review budget allocation  
- Plan team building event
📅 Created: 2024-06-24 10:30:15
🎨 Color: blue
==================================================
```

### Searching Notes
```bash
$ python main.py search "meeting"
🔍 Search results for 'meeting' (1 found):
============================================================
# 1 | Project Meeting Notes                    | blue
============================================================
```

### Interactive Mode Example
```bash
$ python main.py
🗒️  Welcome to Post-it Notes Manager!
Type 'help' for available commands or 'exit' to quit.

📝 > list
📚 Your Notes (2 total):
...

📝 > create
📝 Creating a new note...
Enter note title: Daily Tasks
...

📝 > stats
📊 Notes Statistics
==============================
Total Notes: 3
Data File: notes_data.json

Notes by Color:
  🎨 Blue: 1
  🎨 Green: 1
  🎨 Yellow: 1
==============================

📝 > exit
👋 Goodbye!
```

## 🗂️ File Structure

```
your-project-folder/
├── main.py           # Main application file
├── notes_data.json   # Auto-created data file (stores your notes)
└── README.md         # This documentation
```

The `notes_data.json` file is automatically created when you add your first note. It contains all your notes data in a structured JSON format.

## 🧪 Testing

The application includes built-in unit tests to ensure reliability:

```bash
# Run the test suite
python main.py test
```

Expected output:
```
🧪 Running unit tests...
✅ Note creation test passed
✅ Manager create test passed
✅ Manager find test passed
✅ Manager update test passed
✅ Manager delete test passed
🎉 All tests passed!
```

## 🔧 Configuration

### Custom Data File Location
You can specify a custom location for your notes data file:

```bash
python main.py --data-file /path/to/my/notes.json list
```

### Color Options
Available colors for notes:
- `yellow` (default)
- `blue`
- `green` 
- `pink`
- `orange`
- `purple`

## 🚀 Future Improvements / Next Steps

### Planned Enhancements
- **📱 GUI Version**: Desktop application using tkinter or PyQt
- **🌐 Web Interface**: Flask/Django web app for browser access
- **☁️ Cloud Sync**: Integration with cloud storage services
- **📎 File Attachments**: Ability to attach files to notes
- **🏷️ Tags System**: Advanced categorization beyond colors
- **📅 Due Dates**: Add deadline tracking to notes
- **🔒 Encryption**: Optional password protection for sensitive notes
- **📤 Export Options**: Export to PDF, HTML, or Markdown formats
- **🔔 Reminders**: Desktop notifications for important notes
- **📊 Advanced Analytics**: Usage patterns and productivity insights

### Converting to GUI Application

To convert this to a desktop GUI application:

1. **Using tkinter** (built into Python):
   ```python
   import tkinter as tk
   from tkinter import ttk, messagebox, scrolledtext
   # Wrap the PostItNotesManager class with GUI components
   ```

2. **Using PyQt5/6** (more advanced):
   ```bash
   pip install PyQt6
   # Create modern Qt-based interface
   ```

### Converting to Web Application

To create a web version:

1. **Using Flask** (simple):
   ```python
   from flask import Flask, render_template, request, jsonify
   # Create REST API endpoints for CRUD operations
   ```

2. **Using Django** (full-featured):
   ```bash
   django-admin startproject postit_notes
   # Create models, views, and templates
   ```

### Mobile App Development
- **React Native**: Cross-platform mobile app
- **Flutter**: Google's mobile development framework
- **Progressive Web App**: Mobile-optimized web interface

## 🤝 Contributing

Found a bug or have a feature request? Here's how you can contribute:

1. Test the application thoroughly
2. Report issues with detailed reproduction steps
3. Suggest new features or improvements
4. Share your experience and use cases

## 📜 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- Inspired by the simplicity and effectiveness of physical Post-it notes
- Built with Python's excellent standard library
- Thanks to the community for feature suggestions and testing

---

**Happy Note-Taking! 📝✨**

*Made with ❤️ for productivity enthusiasts everywhere*
