#!/usr/bin/env python3
"""
Advanced Alarm Clock Application
A feature-rich command-line alarm clock with multiple alarms, snooze, and custom sounds.
Author: Claude
Date: 2025
"""

import time
import datetime
import threading
import json
import os
import sys
import argparse
from typing import List, Dict, Optional
import winsound if sys.platform == "win32" else None

# For non-Windows systems, we'll use a simple beep alternative
try:
    import subprocess
except ImportError:
    subprocess = None


class AlarmSound:
    """Handles alarm sound playback across different platforms"""
    
    @staticmethod
    def play_sound(sound_type: str = "beep", duration: int = 1000, frequency: int = 1000):
        """
        Play alarm sound based on platform
        
        Args:
            sound_type: Type of sound ("beep", "chime", "urgent")
            duration: Duration in milliseconds
            frequency: Frequency in Hz (for beep sounds)
        """
        try:
            if sys.platform == "win32" and winsound:
                if sound_type == "beep":
                    winsound.Beep(frequency, duration)
                elif sound_type == "chime":
                    # Play multiple tones for chime effect
                    for freq in [523, 659, 784, 1047]:  # C, E, G, C notes
                        winsound.Beep(freq, 200)
                        time.sleep(0.1)
                elif sound_type == "urgent":
                    # Rapid beeping for urgent alarms
                    for _ in range(5):
                        winsound.Beep(800, 200)
                        time.sleep(0.1)
                        winsound.Beep(1200, 200)
                        time.sleep(0.1)
            else:
                # For Unix-like systems, use system bell or alternative
                if subprocess:
                    try:
                        # Try to use system bell
                        subprocess.run(["printf", "\\a"], check=False)
                    except:
                        pass
                # Fallback: print bell character
                print("\a" * 3, end="", flush=True)
        except Exception as e:
            print(f"Could not play sound: {e}")
            print("\a🔔 ALARM! 🔔\a")  # Visual + audio fallback


class Alarm:
    """Represents a single alarm with its properties"""
    
    def __init__(self, alarm_id: str, time_str: str, label: str = "", 
                 sound_type: str = "beep", enabled: bool = True, 
                 repeat_days: List[str] = None):
        """
        Initialize an alarm
        
        Args:
            alarm_id: Unique identifier for the alarm
            time_str: Time in HH:MM format
            label: Optional label for the alarm
            sound_type: Type of alarm sound
            enabled: Whether the alarm is active
            repeat_days: List of days to repeat (Mon, Tue, etc.)
        """
        self.id = alarm_id
        self.time_str = time_str
        self.label = label
        self.sound_type = sound_type
        self.enabled = enabled
        self.repeat_days = repeat_days or []
        self.snoozed_until = None
        
        # Validate and parse time
        try:
            self.hour, self.minute = map(int, time_str.split(':'))
            if not (0 <= self.hour <= 23 and 0 <= self.minute <= 59):
                raise ValueError("Invalid time range")
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}. Use HH:MM format.")
    
    def should_trigger(self, current_time: datetime.datetime) -> bool:
        """Check if alarm should trigger at current time"""
        if not self.enabled:
            return False
        
        # Check if currently snoozed
        if self.snoozed_until and current_time < self.snoozed_until:
            return False
        
        # Reset snooze if time has passed
        if self.snoozed_until and current_time >= self.snoozed_until:
            self.snoozed_until = None
        
        # Check time match
        if current_time.hour != self.hour or current_time.minute != self.minute:
            return False
        
        # Check day of week if repeat days are set
        if self.repeat_days:
            day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            current_day = day_names[current_time.weekday()]
            return current_day in self.repeat_days
        
        return True
    
    def snooze(self, minutes: int = 5):
        """Snooze the alarm for specified minutes"""
        self.snoozed_until = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    
    def to_dict(self) -> Dict:
        """Convert alarm to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'time_str': self.time_str,
            'label': self.label,
            'sound_type': self.sound_type,
            'enabled': self.enabled,
            'repeat_days': self.repeat_days
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Alarm':
        """Create alarm from dictionary"""
        return cls(
            data['id'],
            data['time_str'],
            data.get('label', ''),
            data.get('sound_type', 'beep'),
            data.get('enabled', True),
            data.get('repeat_days', [])
        )
    
    def __str__(self) -> str:
        """String representation of alarm"""
        status = "ON" if self.enabled else "OFF"
        repeat_info = f" (Repeats: {', '.join(self.repeat_days)})" if self.repeat_days else ""
        snooze_info = f" [Snoozed until {self.snoozed_until.strftime('%H:%M')}]" if self.snoozed_until else ""
        return f"[{self.id}] {self.time_str} - {self.label or 'Unnamed'} ({status}){repeat_info}{snooze_info}"


class AlarmClock:
    """Main alarm clock application"""
    
    def __init__(self, config_file: str = "alarms.json"):
        """Initialize alarm clock with configuration file"""
        self.config_file = config_file
        self.alarms: Dict[str, Alarm] = {}
        self.running = False
        self.alarm_thread = None
        self.load_alarms()
    
    def load_alarms(self):
        """Load alarms from configuration file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    for alarm_data in data.get('alarms', []):
                        alarm = Alarm.from_dict(alarm_data)
                        self.alarms[alarm.id] = alarm
                print(f"Loaded {len(self.alarms)} alarms from {self.config_file}")
        except Exception as e:
            print(f"Error loading alarms: {e}")
    
    def save_alarms(self):
        """Save alarms to configuration file"""
        try:
            data = {
                'alarms': [alarm.to_dict() for alarm in self.alarms.values()]
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Alarms saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving alarms: {e}")
    
    def add_alarm(self, time_str: str, label: str = "", sound_type: str = "beep", 
                  repeat_days: List[str] = None) -> str:
        """Add a new alarm"""
        alarm_id = f"alarm_{len(self.alarms) + 1:03d}"
        
        try:
            alarm = Alarm(alarm_id, time_str, label, sound_type, True, repeat_days)
            self.alarms[alarm_id] = alarm
            self.save_alarms()
            print(f"✅ Added alarm: {alarm}")
            return alarm_id
        except ValueError as e:
            print(f"❌ Error adding alarm: {e}")
            return ""
    
    def remove_alarm(self, alarm_id: str) -> bool:
        """Remove an alarm by ID"""
        if alarm_id in self.alarms:
            removed_alarm = self.alarms.pop(alarm_id)
            self.save_alarms()
            print(f"🗑️ Removed alarm: {removed_alarm}")
            return True
        else:
            print(f"❌ Alarm {alarm_id} not found")
            return False
    
    def toggle_alarm(self, alarm_id: str) -> bool:
        """Toggle alarm on/off"""
        if alarm_id in self.alarms:
            alarm = self.alarms[alarm_id]
            alarm.enabled = not alarm.enabled
            self.save_alarms()
            status = "enabled" if alarm.enabled else "disabled"
            print(f"🔄 Alarm {alarm_id} {status}")
            return True
        else:
            print(f"❌ Alarm {alarm_id} not found")
            return False
    
    def list_alarms(self):
        """Display all alarms"""
        if not self.alarms:
            print("📝 No alarms set")
            return
        
        print("📋 Current Alarms:")
        print("-" * 50)
        for alarm in sorted(self.alarms.values(), key=lambda a: (a.hour, a.minute)):
            print(f"  {alarm}")
    
    def snooze_alarm(self, alarm_id: str, minutes: int = 5):
        """Snooze a specific alarm"""
        if alarm_id in self.alarms:
            self.alarms[alarm_id].snooze(minutes)
            print(f"😴 Alarm {alarm_id} snoozed for {minutes} minutes")
        else:
            print(f"❌ Alarm {alarm_id} not found")
    
    def check_alarms(self):
        """Check and trigger alarms - runs in separate thread"""
        last_minute = -1
        
        while self.running:
            try:
                current_time = datetime.datetime.now()
                current_minute = current_time.minute
                
                # Only check once per minute
                if current_minute != last_minute:
                    last_minute = current_minute
                    
                    for alarm in self.alarms.values():
                        if alarm.should_trigger(current_time):
                            self.trigger_alarm(alarm)
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"Error in alarm checking: {e}")
                time.sleep(5)
    
    def trigger_alarm(self, alarm: Alarm):
        """Trigger an alarm"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n🚨 ALARM TRIGGERED! 🚨")
        print(f"⏰ Time: {current_time}")
        print(f"📌 Label: {alarm.label or 'Unnamed Alarm'}")
        print(f"🔔 Sound: {alarm.sound_type}")
        print("-" * 40)
        
        # Play alarm sound
        AlarmSound.play_sound(alarm.sound_type)
        
        # Provide user options
        print("Options:")
        print("  's' + Enter: Snooze for 5 minutes")
        print("  'd' + Enter: Dismiss alarm")
        print("  'q' + Enter: Quit alarm clock")
        
        # Wait for user input with timeout
        self.handle_alarm_response(alarm)
    
    def handle_alarm_response(self, alarm: Alarm):
        """Handle user response to alarm"""
        try:
            # In a real implementation, you might want to use select() or threading
            # for non-blocking input, but for simplicity, we'll use basic input
            print(f"Alarm {alarm.id} is ringing! Enter command (s/d/q): ", end="")
            
            # Simple implementation - in practice, you'd want non-blocking input
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Input timeout")
            
            # Set timeout for input (Unix-like systems only)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(30)  # 30 second timeout
            
            try:
                response = input().lower().strip()
                if hasattr(signal, 'SIGALRM'):
                    signal.alarm(0)  # Cancel timeout
                
                if response == 's':
                    alarm.snooze(5)
                    print("😴 Alarm snoozed for 5 minutes")
                elif response == 'd':
                    print("✅ Alarm dismissed")
                elif response == 'q':
                    print("👋 Shutting down alarm clock...")
                    self.stop()
                else:
                    print("✅ Alarm dismissed (default)")
                    
            except (TimeoutError, EOFError):
                print("\n⏰ No response - alarm auto-dismissed")
                
        except Exception as e:
            print(f"Error handling alarm response: {e}")
            print("✅ Alarm dismissed due to error")
    
    def start(self):
        """Start the alarm clock"""
        if self.running:
            print("⚠️ Alarm clock is already running")
            return
        
        self.running = True
        self.alarm_thread = threading.Thread(target=self.check_alarms, daemon=True)
        self.alarm_thread.start()
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🚀 Alarm clock started at {current_time}")
        print("💡 Tip: Use Ctrl+C to stop the alarm clock")
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping alarm clock...")
            self.stop()
    
    def stop(self):
        """Stop the alarm clock"""
        self.running = False
        if self.alarm_thread:
            self.alarm_thread.join(timeout=2)
        print("✅ Alarm clock stopped")


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(description="Advanced Alarm Clock")
    parser.add_argument('--config', default='alarms.json', 
                       help='Configuration file path (default: alarms.json)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add alarm command
    add_parser = subparsers.add_parser('add', help='Add a new alarm')
    add_parser.add_argument('time', help='Alarm time in HH:MM format')
    add_parser.add_argument('--label', default='', help='Alarm label')
    add_parser.add_argument('--sound', choices=['beep', 'chime', 'urgent'], 
                           default='beep', help='Alarm sound type')
    add_parser.add_argument('--repeat', nargs='*', 
                           choices=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                           help='Days to repeat the alarm')
    
    # List alarms command
    subparsers.add_parser('list', help='List all alarms')
    
    # Remove alarm command
    remove_parser = subparsers.add_parser('remove', help='Remove an alarm')
    remove_parser.add_argument('alarm_id', help='Alarm ID to remove')
    
    # Toggle alarm command
    toggle_parser = subparsers.add_parser('toggle', help='Toggle alarm on/off')
    toggle_parser.add_argument('alarm_id', help='Alarm ID to toggle')
    
    # Start alarm clock command
    subparsers.add_parser('start', help='Start the alarm clock')
    
    # Interactive mode command
    subparsers.add_parser('interactive', help='Start interactive mode')
    
    args = parser.parse_args()
    
    # Initialize alarm clock
    alarm_clock = AlarmClock(args.config)
    
    if args.command == 'add':
        alarm_clock.add_alarm(args.time, args.label, args.sound, args.repeat)
    
    elif args.command == 'list':
        alarm_clock.list_alarms()
    
    elif args.command == 'remove':
        alarm_clock.remove_alarm(args.alarm_id)
    
    elif args.command == 'toggle':
        alarm_clock.toggle_alarm(args.alarm_id)
    
    elif args.command == 'start':
        alarm_clock.list_alarms()
        print("\n" + "="*50)
        alarm_clock.start()
    
    elif args.command == 'interactive':
        interactive_mode(alarm_clock)
    
    else:
        # No command provided, show help and start interactive mode
        parser.print_help()
        print("\n" + "="*50)
        print("Starting interactive mode...")
        interactive_mode(alarm_clock)


def interactive_mode(alarm_clock: AlarmClock):
    """Interactive command-line interface"""
    print("\n🕐 Welcome to Advanced Alarm Clock!")
    print("Type 'help' for available commands")
    
    while True:
        try:
            command = input("\nalarm> ").strip().lower()
            
            if command in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            elif command == 'help':
                print("\nAvailable commands:")
                print("  add <time> [label] - Add alarm (e.g., 'add 07:30 Wake up')")
                print("  list - List all alarms")
                print("  remove <id> - Remove alarm by ID")
                print("  toggle <id> - Toggle alarm on/off")
                print("  start - Start alarm monitoring")
                print("  status - Show current time and alarm status")
                print("  help - Show this help")
                print("  quit - Exit the program")
            
            elif command == 'list':
                alarm_clock.list_alarms()
            
            elif command == 'start':
                alarm_clock.list_alarms()
                print("\nStarting alarm clock... (Press Ctrl+C to stop)")
                alarm_clock.start()
            
            elif command == 'status':
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"⏰ Current time: {current_time}")
                print(f"📊 Total alarms: {len(alarm_clock.alarms)}")
                active_alarms = sum(1 for a in alarm_clock.alarms.values() if a.enabled)
                print(f"✅ Active alarms: {active_alarms}")
            
            elif command.startswith('add '):
                parts = command.split(' ', 2)
                if len(parts) >= 2:
                    time_str = parts[1]
                    label = parts[2] if len(parts) > 2 else ""
                    alarm_clock.add_alarm(time_str, label)
                else:
                    print("❌ Usage: add <time> [label]")
            
            elif command.startswith('remove '):
                parts = command.split()
                if len(parts) >= 2:
                    alarm_clock.remove_alarm(parts[1])
                else:
                    print("❌ Usage: remove <alarm_id>")
            
            elif command.startswith('toggle '):
                parts = command.split()
                if len(parts) >= 2:
                    alarm_clock.toggle_alarm(parts[1])
                else:
                    print("❌ Usage: toggle <alarm_id>")
            
            elif command == '':
                continue
            
            else:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n🛑 Interrupted. Type 'quit' to exit.")
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


# Simple unit tests (can be run with python -m pytest main.py)
def test_alarm_creation():
    """Test alarm creation and validation"""
    # Valid alarm
    alarm = Alarm("test_001", "07:30", "Morning alarm")
    assert alarm.hour == 7
    assert alarm.minute == 30
    assert alarm.enabled == True
    
    # Invalid time format should raise ValueError
    try:
        Alarm("test_002", "25:70", "Invalid")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_alarm_trigger():
    """Test alarm triggering logic"""
    alarm = Alarm("test_001", "07:30", "Test")
    
    # Create a datetime for 7:30 AM today
    trigger_time = datetime.datetime.now().replace(hour=7, minute=30, second=0, microsecond=0)
    assert alarm.should_trigger(trigger_time) == True
    
    # Different time should not trigger
    no_trigger_time = datetime.datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    assert alarm.should_trigger(no_trigger_time) == False


if __name__ == "__main__":
    # Run tests if called with --test
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running basic tests...")
        test_alarm_creation()
        test_alarm_trigger()
        print("✅ All tests passed!")
    else:
        main()
