# Personal Task Manager 📋

A powerful command-line task management application built with Python that helps you organize, track, and manage your daily tasks efficiently.

## Overview

The Personal Task Manager is a lightweight, feature-rich CLI application that allows you to manage your to-do lists directly from the terminal. It provides all the essential features you need to stay organized: adding tasks, setting priorities, due dates, marking tasks as complete, and tracking your progress.

## Features ✨

- **Add Tasks**: Create new tasks with titles, descriptions, priorities, and due dates
- **List Tasks**: View your tasks with filtering options (by priority, completion status)
- **Complete Tasks**: Mark tasks as done with completion timestamps
- **Delete Tasks**: Remove tasks you no longer need
- **Priority System**: Organize tasks with high, medium, and low priorities
- **Due Date Tracking**: Set due dates and get overdue notifications
- **Task Statistics**: View comprehensive stats about your task completion
- **Data Persistence**: All tasks are saved locally in JSON format
- **Smart Sorting**: Tasks are automatically sorted by priority and due date
- **Error Handling**: Robust error handling with helpful messages
- **Unit Tests**: Built-in test suite for reliability

## Requirements

- **Python Version**: Python 3.8 or higher
- **Dependencies**: Uses only Python standard library (no external packages required!)
- **Operating System**: Cross-platform (Windows, macOS, Linux)

## Installation & Setup

### 1. Download the Project
```bash
# Option 1: Save the main.py file directly to your desired directory

# Option 2: If you have the project in a folder
cd personal-task-manager
```

### 2. Verify Python Installation
```bash
python --version
# or
python3 --version
```

### 3. Make the Script Executable (Optional - Unix/Linux/macOS)
```bash
chmod +x main.py
```

### 4. Run the Application
```bash
python main.py --help
```

## Usage Examples

### Adding Tasks
```bash
# Basic task
python main.py add "Buy groceries"

# Task with description and high priority
python main.py add "Finish project report" --description "Complete the Q4 analysis report" --priority high

# Task with due date
python main.py add "Doctor appointment" --due 2024-12-25 --priority high

# Task with all options
python main.py add "Plan vacation" --description "Research destinations and book flights" --priority medium --due 2024-12-30
```

### Listing Tasks
```bash
# List all pending tasks
python main.py list

# List all tasks (including completed)
python main.py list --all

# Filter by priority
python main.py list --priority high

# Combine filters
python main.py list --all --priority medium
```

### Managing Tasks
```bash
# Complete a task (use the ID from list command)
python main.py complete 1703123456789

# Delete a task
python main.py delete 1703123456789

# View statistics
python main.py stats
```

## Sample Output

### Adding a Task
```
$ python main.py add "Prepare presentation" --priority high --due 2024-12-28
✓ Task added successfully!
  ID: 1703123456789
  Title: Prepare presentation
  Priority: high
  Due: 2024-12-28
```

### Listing Tasks
```
$ python main.py list
==================================================
TASKS (3 found)
==================================================
○ [1703123456789] ↑ Prepare presentation (Due: 2024-12-28)
------------------------------
○ [1703123456790] → Buy groceries
    Get milk, bread, and vegetables
------------------------------
○ [1703123456791] ↓ Clean garage (Due: 2024-12-30)
------------------------------
```

### Task Statistics
```
$ python main.py stats
==============================
TASK STATISTICS
==============================
Total tasks:     5
Completed:       2
Pending:         3
Overdue:         1
Completion rate: 40.0%
```

## Data Storage

Tasks are automatically saved to a `tasks.json` file in the same directory as the script. The data structure includes:

- Task ID (unique timestamp-based identifier)
- Title and description
- Priority level (high/medium/low)
- Due date (optional)
- Completion status and timestamps
- Creation timestamp

## Testing

The application includes built-in unit tests. Run them with:

```bash
python main.py --test
```

## File Structure

```
personal-task-manager/
│
├── main.py          # Main application file
├── README.md        # This documentation
├── tasks.json       # Data file (created automatically)
└── requirements.txt # Empty (no external dependencies)
```

## Advanced Usage Tips

### Command Shortcuts
Most commands accept short flags:
- `--priority` can be shortened to `-p`
- `--description` can be shortened to `-d`
- `--all` can be shortened to `-a`

### Task ID Management
- Task IDs are displayed when you list tasks
- Copy the ID number from the list output to complete or delete tasks
- IDs are timestamp-based, so they're unique and sortable

### Priority System
- **High** (↑): Urgent, important tasks
- **Medium** (→): Regular tasks (default)
- **Low** (↓): Nice-to-have, less urgent tasks

### Due Date Format
Always use `YYYY-MM-DD` format for due dates:
- ✅ Correct: `2024-12-25`
- ❌ Wrong: `12/25/2024`, `Dec 25, 2024`

## Troubleshooting

### Common Issues

**"Command not found" error:**
- Make sure you're in the correct directory
- Try `python3 main.py` instead of `python main.py`

**Permission denied:**
- On Unix systems, run: `chmod +x main.py`

**Tasks not saving:**
- Check if you have write permissions in the directory
- Ensure the directory isn't read-only

**JSON decode error:**
- If `tasks.json` gets corrupted, delete it (you'll lose existing tasks)
- The app will create a new clean file

## Future Improvements / Next Steps

### Planned Enhancements
- **Categories/Tags**: Organize tasks by project or category
- **Search Functionality**: Find tasks by keyword
- **Recurring Tasks**: Support for daily/weekly/monthly tasks
- **Task Dependencies**: Link tasks that depend on others
- **Time Tracking**: Track time spent on tasks
- **Export Options**: Export to CSV, PDF, or other formats
- **Reminders**: System notifications for due tasks
- **Subtasks**: Break down complex tasks into smaller parts

### Integration Ideas
- **Calendar Integration**: Sync with Google Calendar or Outlook
- **Cloud Sync**: Backup tasks to cloud storage
- **Team Features**: Share tasks with team members
- **Mobile App**: Companion mobile application
- **Web Dashboard**: Browser-based interface

### Technical Improvements
- **Database Backend**: Migrate from JSON to SQLite for better performance
- **Configuration File**: User preferences and settings
- **Themes**: Customizable color schemes for output
- **Plugins**: Extensible architecture for custom features

## Converting to Other Formats

### Web Application
To convert this to a web app:
1. Use **Flask** or **FastAPI** for the backend
2. Create HTML templates for the UI
3. Replace CLI arguments with web forms
4. Use the existing `TaskManager` class as your data layer

### GUI Application
To create a desktop GUI:
1. Use **tkinter** (built into Python) for a simple GUI
2. Or **PyQt5/PySide2** for a more modern interface
3. Replace argument parsing with GUI event handlers
4. Keep the core `Task` and `TaskManager` classes unchanged

### Mobile App
For mobile development:
1. Use **Kivy** to create a cross-platform mobile app in Python
2. Or create a REST API and build native apps
3. The JSON data format is already mobile-friendly

## Contributing

This is a single-developer project, but here are ways to extend it:

1. **Fork the project** and add your own features
2. **Report bugs** by documenting the issue and steps to reproduce
3. **Suggest features** by describing the use case and benefits
4. **Optimize performance** for large numbers of tasks
5. **Add more test cases** to improve reliability

## License

This project is released under the MIT License - feel free to use, modify, and distribute as needed.

## Acknowledgments

- Built with Python's standard library for maximum compatibility
- Inspired by popular task management tools like Todoist and Any.do
- Thanks to the Python community for excellent documentation and examples

---

**Happy Task Managing! 🎯**

*For questions, issues, or suggestions, feel free to modify and extend this tool to fit your workflow.*
