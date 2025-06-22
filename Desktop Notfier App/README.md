# 🔔 Desktop Notifier App

A comprehensive cross-platform desktop notification system that allows you to schedule reminders, send immediate notifications, and manage recurring alerts - all from a simple command-line interface.

## ✨ Features

### Core Functionality
- **Immediate Notifications**: Send instant desktop notifications with custom titles and messages
- **Scheduled Reminders**: Schedule notifications for specific dates and times
- **Recurring Reminders**: Set up repeating notifications with custom intervals
- **Flexible Time Parsing**: Multiple time input formats for ease of use
- **Persistent Storage**: Reminders are saved to JSON and persist across sessions
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Daemon Mode**: Background service that continuously monitors and triggers reminders

### Advanced Features
- **Smart Time Scheduling**: Automatically schedules for next day if time has passed
- **Reminder Management**: List, view, and delete active reminders
- **Error Handling**: Graceful handling of invalid inputs and system errors
- **Console Fallback**: Falls back to console output if system notifications fail
- **Data Persistence**: All reminders are automatically saved to `reminders.json`

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Operating System: Windows 10+, macOS 10.14+, or Linux with notification support

### Installation

1. **Download the script**:
   ```bash
   # Save the desktop_notifier.py file to your desired directory
   ```

2. **Install optional dependencies** (for enhanced Windows support):
   ```bash
   pip install win10toast  # Windows only - for native toast notifications
   ```
   
   > **Note**: The app works without additional dependencies using built-in system commands, but `win10toast` provides better Windows integration.

3. **Make executable** (Linux/macOS):
   ```bash
   chmod +x desktop_notifier.py
   ```

## 📖 Usage Guide

### Command Structure
```bash
python desktop_notifier.py <command> [arguments]
```

### Available Commands

#### 1. Send Immediate Notification
```bash
python desktop_notifier.py notify "Meeting Alert" "Team standup starts in 5 minutes"
```

#### 2. Schedule a One-Time Reminder
```bash
# Schedule for today at 2:30 PM
python desktop_notifier.py add "Lunch Break" "Time to eat!" "14:30"

# Schedule for specific date and time
python desktop_notifier.py add "Doctor Appointment" "Don't forget!" "2024-06-25 10:00"

# Schedule 30 minutes from now
python desktop_notifier.py add "Coffee Break" "Take a break!" "+30m"

# Schedule 2 hours from now
python desktop_notifier.py add "Project Deadline" "Submit report" "+2h"
```

#### 3. Schedule Recurring Reminders
```bash
# Water reminder every 60 minutes
python desktop_notifier.py add "Hydration" "Drink water!" "+5m" --repeat 60

# Daily standup reminder
python desktop_notifier.py add "Daily Meeting" "Time for standup!" "09:00" --repeat 1440
```

#### 4. List All Active Reminders
```bash
python desktop_notifier.py list
```

#### 5. Delete a Reminder
```bash
# Delete reminder by index (get index from 'list' command)
python desktop_notifier.py delete 1
```

#### 6. Start Daemon Mode
```bash
# Run continuously in background
python desktop_notifier.py daemon
```

### Time Format Options

| Format | Example | Description |
|--------|---------|-------------|
| `HH:MM` | `14:30` | Today at 2:30 PM (or tomorrow if time passed) |
| `YYYY-MM-DD HH:MM` | `2024-06-25 14:30` | Specific date and time |
| `+Xm` | `+30m` | X minutes from now |
| `+Xh` | `+2h` | X hours from now |

## 💡 Example Use Cases

### Personal Productivity
```bash
# Morning routine
python desktop_notifier.py add "Morning Exercise" "Time to work out!" "07:00" --repeat 1440

# Work breaks
python desktop_notifier.py add "Pomodoro Break" "Take a 5-minute break!" "+25m" --repeat 30

# Evening wind-down
python desktop_notifier.py add "Digital Sunset" "Put devices away" "21:00"
```

### Work & Meetings
```bash
# Meeting preparation
python desktop_notifier.py add "Team Meeting" "Prepare slides and agenda" "2024-06-25 13:45"

# Deadline reminders
python desktop_notifier.py add "Project Due" "Final review needed!" "2024-06-30 16:00"

# Regular check-ins
python desktop_notifier.py add "Status Update" "Send weekly report" "17:00" --repeat 10080
```

### Health & Wellness
```bash
# Hydration reminders
python desktop_notifier.py add "Water Break" "Stay hydrated! 💧" "+1h" --repeat 60

# Posture checks
python desktop_notifier.py add "Posture Check" "Sit up straight!" "+30m" --repeat 45

# Medication reminders
python desktop_notifier.py add "Medicine" "Take evening medication" "20:00" --repeat 1440
```

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Core Libraries**: 
  - `datetime` - Time handling and scheduling
  - `threading` - Background daemon operation
  - `json` - Data persistence
  - `argparse` - Command-line interface
  - `subprocess` - System notification integration
- **Optional Dependencies**:
  - `win10toast` - Enhanced Windows notifications
- **Platform Integration**:
  - **Windows**: Native toast notifications via `win10toast` or Windows API
  - **macOS**: AppleScript integration via `osascript`
  - **Linux**: `notify-send` command integration

## 📁 File Structure

```
desktop_notifier.py     # Main application file
reminders.json          # Auto-generated data file (stores reminders)
README.md              # This documentation
```

## 🔧 Configuration

### Data Storage
- Reminders are automatically saved to `reminders.json` in the same directory
- The file is created automatically on first use
- Manual editing is supported (valid JSON format required)

### Notification Behavior
- **Check Interval**: Daemon checks for due reminders every 30 seconds
- **Notification Duration**: 10 seconds on Windows (system default on other platforms)
- **Fallback**: Console output if system notifications fail

## 🚀 Future Enhancements

### Short-term Improvements
- [ ] **GUI Interface**: Tkinter-based graphical interface for easier management
- [ ] **Sound Alerts**: Audio notifications with custom sounds
- [ ] **Priority Levels**: High/medium/low priority reminders with different styles
- [ ] **Snooze Functionality**: Delay reminders by 5/10/15 minutes
- [ ] **Categories**: Organize reminders by type (work, personal, health)

### Advanced Features
- [ ] **Web Interface**: Flask-based web dashboard for remote management
- [ ] **Email Integration**: Send email notifications as backup
- [ ] **Calendar Sync**: Import events from Google Calendar, Outlook
- [ ] **Smart Scheduling**: AI-suggested optimal reminder times
- [ ] **Team Notifications**: Share reminders across team members
- [ ] **Mobile App**: Companion mobile app for notifications

### Technical Improvements
- [ ] **Database Support**: SQLite integration for better data management
- [ ] **Logging System**: Comprehensive logging with rotation
- [ ] **Plugin System**: Custom notification handlers
- [ ] **REST API**: RESTful API for third-party integrations
- [ ] **Configuration File**: YAML/TOML configuration options

## 🐛 Troubleshooting

### Common Issues

**Notifications not appearing**:
- Ensure notification permissions are enabled in system settings
- On Linux, install `libnotify-bin`: `sudo apt-get install libnotify-bin`
- Check if notification daemon is running in background mode

**Time parsing errors**:
- Use 24-hour format for times (14:30 instead of 2:30 PM)
- Ensure date format is YYYY-MM-DD
- Use +Xm or +Xh for relative times

**Permission errors**:
- Ensure write permissions in the script directory
- Run with appropriate user privileges

### Platform-Specific Notes

**Windows**:
- Install `win10toast` for native notifications: `pip install win10toast`
- Notifications appear in Action Center

**macOS**:
- Notifications appear in Notification Center
- Terminal may need notification permissions (System Preferences > Security & Privacy)

**Linux**:
- Requires `notify-send` command (usually pre-installed)
- GNOME/KDE desktop environments recommended

## 📝 Contributing

This is a single-file project designed for simplicity and portability. To contribute:

1. Test thoroughly on your platform
2. Maintain Python 3.10+ compatibility
3. Keep all functionality in the single file
4. Add comprehensive error handling
5. Update documentation for new features

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with Python's robust standard library
- Cross-platform notification support inspired by various OS notification systems
- Command-line interface design following Unix philosophy
- Thanks to the Python community for excellent documentation and examples

---

**Need help?** Run `python desktop_notifier.py --help` for quick command reference or create an issue for bug reports and feature requests.
