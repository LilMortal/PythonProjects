#!/usr/bin/env python3
"""
Desktop Notifier App
A comprehensive desktop notification system with scheduling, reminders, and customization options.
Author: Assistant
Version: 1.0.0
Python: 3.10+
"""

import time
import threading
import json
import os
import argparse
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

# Cross-platform notifications
try:
    if sys.platform == "win32":
        import win10toast
        WINDOWS_AVAILABLE = True
    else:
        WINDOWS_AVAILABLE = False
except ImportError:
    WINDOWS_AVAILABLE = False

try:
    if sys.platform == "darwin":
        import subprocess
        MACOS_AVAILABLE = True
    else:
        MACOS_AVAILABLE = False
except ImportError:
    MACOS_AVAILABLE = False

try:
    if sys.platform.startswith("linux"):
        import subprocess
        LINUX_AVAILABLE = True
    else:
        LINUX_AVAILABLE = False
except ImportError:
    LINUX_AVAILABLE = False


class NotificationManager:
    """Handles cross-platform desktop notifications"""
    
    def __init__(self):
        self.toaster = None
        if WINDOWS_AVAILABLE:
            self.toaster = win10toast.ToastNotifier()
    
    def send_notification(self, title: str, message: str, duration: int = 10) -> bool:
        """
        Send a desktop notification across different platforms
        
        Args:
            title: Notification title
            message: Notification message
            duration: Duration in seconds (Windows only)
            
        Returns:
            bool: Success status
        """
        try:
            if sys.platform == "win32" and self.toaster:
                self.toaster.show_toast(title, message, duration=duration)
                return True
            elif sys.platform == "darwin" and MACOS_AVAILABLE:
                # macOS notification using osascript
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(["osascript", "-e", script], check=True)
                return True
            elif sys.platform.startswith("linux") and LINUX_AVAILABLE:
                # Linux notification using notify-send
                subprocess.run(["notify-send", title, message], check=True)
                return True
            else:
                # Fallback: print to console
                print(f"\n🔔 NOTIFICATION 🔔")
                print(f"Title: {title}")
                print(f"Message: {message}")
                print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 50)
                return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            # Fallback to console output
            print(f"\n🔔 NOTIFICATION 🔔")
            print(f"Title: {title}")
            print(f"Message: {message}")
            print("-" * 50)
            return False


class Reminder:
    """Represents a scheduled reminder"""
    
    def __init__(self, title: str, message: str, scheduled_time: datetime, 
                 repeat_interval: Optional[int] = None):
        self.title = title
        self.message = message
        self.scheduled_time = scheduled_time
        self.repeat_interval = repeat_interval  # minutes
        self.is_active = True
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert reminder to dictionary for JSON serialization"""
        return {
            'title': self.title,
            'message': self.message,
            'scheduled_time': self.scheduled_time.isoformat(),
            'repeat_interval': self.repeat_interval,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Reminder':
        """Create reminder from dictionary"""
        reminder = cls(
            title=data['title'],
            message=data['message'],
            scheduled_time=datetime.fromisoformat(data['scheduled_time']),
            repeat_interval=data.get('repeat_interval')
        )
        reminder.is_active = data.get('is_active', True)
        reminder.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        return reminder


class DesktopNotifierApp:
    """Main application class for the Desktop Notifier"""
    
    def __init__(self):
        self.notification_manager = NotificationManager()
        self.reminders: List[Reminder] = []
        self.data_file = "reminders.json"
        self.running = False
        self.load_reminders()
    
    def load_reminders(self) -> None:
        """Load reminders from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.reminders = [Reminder.from_dict(item) for item in data]
                print(f"Loaded {len(self.reminders)} reminders from {self.data_file}")
            except Exception as e:
                print(f"Error loading reminders: {e}")
    
    def save_reminders(self) -> None:
        """Save reminders to JSON file"""
        try:
            data = [reminder.to_dict() for reminder in self.reminders]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving reminders: {e}")
    
    def add_reminder(self, title: str, message: str, scheduled_time: datetime, 
                    repeat_interval: Optional[int] = None) -> None:
        """Add a new reminder"""
        reminder = Reminder(title, message, scheduled_time, repeat_interval)
        self.reminders.append(reminder)
        self.save_reminders()
        print(f"✅ Reminder added: '{title}' scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def list_reminders(self) -> None:
        """Display all active reminders"""
        active_reminders = [r for r in self.reminders if r.is_active]
        
        if not active_reminders:
            print("📋 No active reminders found.")
            return
        
        print(f"\n📋 Active Reminders ({len(active_reminders)}):")
        print("-" * 70)
        
        for i, reminder in enumerate(active_reminders, 1):
            status = "🔄 Repeating" if reminder.repeat_interval else "📅 One-time"
            repeat_info = f" (every {reminder.repeat_interval} min)" if reminder.repeat_interval else ""
            
            print(f"{i}. {reminder.title}")
            print(f"   Message: {reminder.message}")
            print(f"   Scheduled: {reminder.scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Type: {status}{repeat_info}")
            print()
    
    def delete_reminder(self, index: int) -> bool:
        """Delete a reminder by index"""
        active_reminders = [r for r in self.reminders if r.is_active]
        
        if 1 <= index <= len(active_reminders):
            reminder_to_delete = active_reminders[index - 1]
            reminder_to_delete.is_active = False
            self.save_reminders()
            print(f"🗑️  Deleted reminder: '{reminder_to_delete.title}'")
            return True
        else:
            print(f"❌ Invalid reminder index: {index}")
            return False
    
    def send_immediate_notification(self, title: str, message: str) -> None:
        """Send an immediate notification"""
        success = self.notification_manager.send_notification(title, message)
        if success:
            print(f"✅ Notification sent: '{title}'")
        else:
            print(f"❌ Failed to send notification: '{title}'")
    
    def check_reminders(self) -> None:
        """Check and trigger due reminders"""
        current_time = datetime.now()
        
        for reminder in self.reminders:
            if not reminder.is_active:
                continue
            
            # Check if reminder is due
            if current_time >= reminder.scheduled_time:
                # Send notification
                self.notification_manager.send_notification(reminder.title, reminder.message)
                print(f"🔔 Triggered reminder: '{reminder.title}' at {current_time.strftime('%H:%M:%S')}")
                
                # Handle repeating reminders
                if reminder.repeat_interval:
                    # Schedule next occurrence
                    reminder.scheduled_time += timedelta(minutes=reminder.repeat_interval)
                    print(f"🔄 Next occurrence: {reminder.scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    # Deactivate one-time reminders
                    reminder.is_active = False
        
        # Save changes
        self.save_reminders()
    
    def run_daemon(self) -> None:
        """Run the notification daemon"""
        print("🚀 Desktop Notifier daemon started!")
        print("Press Ctrl+C to stop the daemon")
        print("-" * 40)
        
        self.running = True
        
        try:
            while self.running:
                self.check_reminders()
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("\n👋 Stopping Desktop Notifier daemon...")
            self.running = False
    
    def parse_time_input(self, time_str: str) -> Optional[datetime]:
        """Parse various time input formats"""
        current_time = datetime.now()
        
        try:
            # Format: YYYY-MM-DD HH:MM
            if len(time_str) == 16 and ' ' in time_str:
                return datetime.strptime(time_str, '%Y-%m-%d %H:%M')
            
            # Format: HH:MM (today)
            elif len(time_str) == 5 and ':' in time_str:
                time_part = datetime.strptime(time_str, '%H:%M').time()
                scheduled_datetime = datetime.combine(current_time.date(), time_part)
                
                # If time has passed today, schedule for tomorrow
                if scheduled_datetime <= current_time:
                    scheduled_datetime += timedelta(days=1)
                
                return scheduled_datetime
            
            # Format: +Xm (X minutes from now)
            elif time_str.startswith('+') and time_str.endswith('m'):
                minutes = int(time_str[1:-1])
                return current_time + timedelta(minutes=minutes)
            
            # Format: +Xh (X hours from now)
            elif time_str.startswith('+') and time_str.endswith('h'):
                hours = int(time_str[1:-1])
                return current_time + timedelta(hours=hours)
            
            else:
                return None
        
        except ValueError:
            return None


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Desktop Notifier App - Schedule and manage desktop notifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python desktop_notifier.py notify "Meeting" "Team standup in 5 minutes"
  python desktop_notifier.py add "Lunch Break" "Time to eat!" "12:30"
  python desktop_notifier.py add "Water Break" "Stay hydrated!" "+30m" --repeat 60
  python desktop_notifier.py add "Daily Standup" "Meeting time!" "2024-06-22 09:00"
  python desktop_notifier.py list
  python desktop_notifier.py delete 1
  python desktop_notifier.py daemon

Time formats:
  "HH:MM"           - Today at specific time (or tomorrow if time passed)
  "YYYY-MM-DD HH:MM" - Specific date and time
  "+Xm"             - X minutes from now
  "+Xh"             - X hours from now
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Immediate notification command
    notify_parser = subparsers.add_parser('notify', help='Send immediate notification')
    notify_parser.add_argument('title', help='Notification title')
    notify_parser.add_argument('message', help='Notification message')
    
    # Add reminder command
    add_parser = subparsers.add_parser('add', help='Add scheduled reminder')
    add_parser.add_argument('title', help='Reminder title')
    add_parser.add_argument('message', help='Reminder message')
    add_parser.add_argument('time', help='Scheduled time (see time formats above)')
    add_parser.add_argument('--repeat', type=int, metavar='MINUTES',
                           help='Repeat interval in minutes')
    
    # List reminders command
    subparsers.add_parser('list', help='List all active reminders')
    
    # Delete reminder command
    delete_parser = subparsers.add_parser('delete', help='Delete reminder by index')
    delete_parser.add_argument('index', type=int, help='Reminder index (from list command)')
    
    # Daemon command
    subparsers.add_parser('daemon', help='Start notification daemon')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize app
    app = DesktopNotifierApp()
    
    # Handle commands
    if args.command == 'notify':
        app.send_immediate_notification(args.title, args.message)
    
    elif args.command == 'add':
        scheduled_time = app.parse_time_input(args.time)
        if scheduled_time is None:
            print(f"❌ Invalid time format: '{args.time}'")
            print("Use formats like: '14:30', '2024-06-22 14:30', '+30m', '+2h'")
            return
        
        app.add_reminder(args.title, args.message, scheduled_time, args.repeat)
    
    elif args.command == 'list':
        app.list_reminders()
    
    elif args.command == 'delete':
        app.delete_reminder(args.index)
    
    elif args.command == 'daemon':
        app.run_daemon()


if __name__ == "__main__":
    main()
