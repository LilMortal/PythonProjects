#!/usr/bin/env python3
"""
Countdown Clock and Timer Application
A versatile command-line timer with multiple modes and features.

Author: Claude AI
Version: 1.0.0
Python: 3.8+
"""

import time
import datetime
import argparse
import sys
import os
import threading
from typing import Optional, Tuple


class CountdownTimer:
    """Main countdown timer class with multiple timer modes."""
    
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.start_time = None
        self.pause_time = None
        self.total_paused_time = 0
        
    def clear_screen(self):
        """Clear the terminal screen for better display."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_time(self, seconds: int) -> str:
        """Format seconds into HH:MM:SS format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def parse_time_input(self, time_str: str) -> int:
        """
        Parse time input in various formats and return total seconds.
        Supports: 
        - "30" (30 seconds)
        - "5:30" (5 minutes 30 seconds)
        - "1:05:30" (1 hour 5 minutes 30 seconds)
        """
        try:
            parts = time_str.split(':')
            if len(parts) == 1:
                # Just seconds
                return int(parts[0])
            elif len(parts) == 2:
                # Minutes:seconds
                minutes, seconds = map(int, parts)
                return minutes * 60 + seconds
            elif len(parts) == 3:
                # Hours:minutes:seconds
                hours, minutes, seconds = map(int, parts)
                return hours * 3600 + minutes * 60 + seconds
            else:
                raise ValueError("Invalid time format")
        except ValueError:
            raise ValueError("Time must be in format: seconds, MM:SS, or HH:MM:SS")
    
    def parse_datetime_input(self, datetime_str: str) -> datetime.datetime:
        """
        Parse datetime input in various formats.
        Supports:
        - "2024-12-31 23:59:59"
        - "Dec 31 2024 11:59 PM"
        - "31/12/2024 23:59"
        """
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d/%m/%Y %H:%M:%S",
            "%d/%m/%Y %H:%M",
            "%b %d %Y %I:%M %p",
            "%B %d %Y %I:%M %p"
        ]
        
        for fmt in formats:
            try:
                return datetime.datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse datetime: {datetime_str}")
    
    def display_timer(self, remaining_seconds: int, total_seconds: int, timer_type: str):
        """Display the timer with progress information."""
        self.clear_screen()
        
        # Header
        print("=" * 50)
        print(f"🕐 {timer_type.upper()} TIMER")
        print("=" * 50)
        
        # Time display
        time_str = self.format_time(remaining_seconds)
        print(f"\n⏰ Time Remaining: {time_str}")
        
        # Progress bar
        if total_seconds > 0:
            progress = (total_seconds - remaining_seconds) / total_seconds
            bar_length = 30
            filled_length = int(bar_length * progress)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            percentage = progress * 100
            print(f"📊 Progress: [{bar}] {percentage:.1f}%")
        
        # Status
        status = "⏸️  PAUSED" if self.is_paused else "▶️  RUNNING"
        print(f"\n🔄 Status: {status}")
        
        # Controls
        print("\n" + "─" * 50)
        print("⌨️  Controls:")
        print("   [SPACE] - Pause/Resume")
        print("   [Q] - Quit")
        print("   [R] - Reset")
        print("─" * 50)
    
    def countdown_timer(self, total_seconds: int):
        """Run a countdown timer for specified duration."""
        print(f"\n🚀 Starting countdown timer for {self.format_time(total_seconds)}")
        print("Press ENTER to start...")
        input()
        
        self.is_running = True
        self.start_time = time.time()
        remaining_seconds = total_seconds
        
        try:
            while remaining_seconds > 0 and self.is_running:
                self.display_timer(remaining_seconds, total_seconds, "Countdown")
                
                # Wait 1 second or until interrupted
                time.sleep(1)
                
                if not self.is_paused:
                    remaining_seconds -= 1
            
            if remaining_seconds <= 0:
                self.timer_finished("Countdown")
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Timer stopped by user.")
    
    def count_up_timer(self, max_seconds: Optional[int] = None):
        """Run a count-up timer (stopwatch mode)."""
        print(f"\n🚀 Starting stopwatch timer")
        if max_seconds:
            print(f"Will stop at {self.format_time(max_seconds)}")
        print("Press ENTER to start...")
        input()
        
        self.is_running = True
        self.start_time = time.time()
        elapsed_seconds = 0
        
        try:
            while self.is_running:
                display_max = max_seconds if max_seconds else elapsed_seconds + 3600
                self.display_timer(display_max - elapsed_seconds, display_max, "Stopwatch")
                
                # Check if we've reached the maximum
                if max_seconds and elapsed_seconds >= max_seconds:
                    self.timer_finished("Stopwatch")
                    break
                
                time.sleep(1)
                
                if not self.is_paused:
                    elapsed_seconds += 1
            
        except KeyboardInterrupt:
            print(f"\n\n⏹️  Stopwatch stopped. Total time: {self.format_time(elapsed_seconds)}")
    
    def countdown_to_datetime(self, target_datetime: datetime.datetime):
        """Count down to a specific date and time."""
        now = datetime.datetime.now()
        
        if target_datetime <= now:
            print("❌ Target date/time must be in the future!")
            return
        
        print(f"\n🎯 Counting down to: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Press ENTER to start...")
        input()
        
        self.is_running = True
        
        try:
            while self.is_running:
                now = datetime.datetime.now()
                time_diff = target_datetime - now
                
                if time_diff.total_seconds() <= 0:
                    self.timer_finished("Event Countdown")
                    break
                
                total_seconds = int(time_diff.total_seconds())
                remaining_seconds = total_seconds
                
                self.display_timer(remaining_seconds, total_seconds, "Event Countdown")
                time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Countdown stopped by user.")
    
    def timer_finished(self, timer_type: str):
        """Handle timer completion with alert."""
        self.clear_screen()
        
        # Alert animation
        for _ in range(5):
            print("\n" * 10)
            print("🔥" * 20)
            print("🚨 TIME'S UP! 🚨".center(40))
            print(f"🏁 {timer_type} Complete! 🏁".center(40))
            print("🔥" * 20)
            time.sleep(0.5)
            self.clear_screen()
            time.sleep(0.5)
        
        # Final message
        print("\n" * 5)
        print("⭐" * 50)
        print("🎉 TIMER COMPLETED! 🎉".center(50))
        print("⭐" * 50)
        print(f"\n✅ {timer_type} finished at {datetime.datetime.now().strftime('%H:%M:%S')}")
        print("\nPress ENTER to continue...")
        input()
    
    def interactive_mode(self):
        """Run the timer in interactive mode with menu."""
        while True:
            self.clear_screen()
            print("🕐 COUNTDOWN CLOCK & TIMER")
            print("=" * 40)
            print("\n📋 Choose timer mode:")
            print("1. ⏰ Countdown Timer (duration)")
            print("2. 🔢 Stopwatch (count up)")
            print("3. 📅 Event Countdown (to date/time)")
            print("4. 🚪 Exit")
            
            try:
                choice = input("\n👉 Enter your choice (1-4): ").strip()
                
                if choice == '1':
                    duration_str = input("\n⏰ Enter duration (seconds, MM:SS, or HH:MM:SS): ")
                    duration = self.parse_time_input(duration_str)
                    self.countdown_timer(duration)
                
                elif choice == '2':
                    has_limit = input("\n🔢 Set maximum time? (y/n): ").lower().startswith('y')
                    max_time = None
                    if has_limit:
                        max_str = input("Enter maximum time (seconds, MM:SS, or HH:MM:SS): ")
                        max_time = self.parse_time_input(max_str)
                    self.count_up_timer(max_time)
                
                elif choice == '3':
                    datetime_str = input("\n📅 Enter target date/time (YYYY-MM-DD HH:MM:SS): ")
                    target_dt = self.parse_datetime_input(datetime_str)
                    self.countdown_to_datetime(target_dt)
                
                elif choice == '4':
                    print("\n👋 Goodbye!")
                    break
                
                else:
                    print("\n❌ Invalid choice. Please try again.")
                    time.sleep(2)
            
            except (ValueError, KeyboardInterrupt) as e:
                print(f"\n❌ Error: {e}")
                print("Press ENTER to continue...")
                input()
            
            # Reset timer state
            self.is_running = False
            self.is_paused = False


def run_tests():
    """Simple unit tests for the timer functionality."""
    print("🧪 Running tests...")
    
    timer = CountdownTimer()
    
    # Test time parsing
    test_cases = [
        ("30", 30),
        ("5:30", 330),
        ("1:05:30", 3930),
    ]
    
    for input_str, expected in test_cases:
        result = timer.parse_time_input(input_str)
        assert result == expected, f"Expected {expected}, got {result} for input '{input_str}'"
        print(f"✅ Time parsing test passed: '{input_str}' -> {result}s")
    
    # Test time formatting
    format_tests = [
        (30, "00:00:30"),
        (330, "00:05:30"),
        (3930, "01:05:30"),
    ]
    
    for seconds, expected in format_tests:
        result = timer.format_time(seconds)
        assert result == expected, f"Expected '{expected}', got '{result}' for {seconds}s"
        print(f"✅ Time formatting test passed: {seconds}s -> '{result}'")
    
    print("🎉 All tests passed!")


def main():
    """Main function to handle command-line arguments and run the timer."""
    parser = argparse.ArgumentParser(
        description="Countdown Clock and Timer Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Interactive mode
  python main.py --countdown 300          # 5-minute countdown
  python main.py --countdown 10:30        # 10 minutes 30 seconds
  python main.py --stopwatch              # Stopwatch mode
  python main.py --stopwatch --max 5:00   # 5-minute maximum stopwatch
  python main.py --event "2024-12-31 23:59:59"  # Countdown to New Year
  python main.py --test                   # Run unit tests
        """
    )
    
    parser.add_argument('--countdown', '-c', 
                       help='Start countdown timer (format: seconds, MM:SS, or HH:MM:SS)')
    parser.add_argument('--stopwatch', '-s', action='store_true',
                       help='Start stopwatch timer')
    parser.add_argument('--max', '-m',
                       help='Maximum time for stopwatch (format: seconds, MM:SS, or HH:MM:SS)')
    parser.add_argument('--event', '-e',
                       help='Countdown to specific date/time (format: YYYY-MM-DD HH:MM:SS)')
    parser.add_argument('--test', '-t', action='store_true',
                       help='Run unit tests')
    
    args = parser.parse_args()
    timer = CountdownTimer()
    
    try:
        if args.test:
            run_tests()
        elif args.countdown:
            duration = timer.parse_time_input(args.countdown)
            timer.countdown_timer(duration)
        elif args.stopwatch:
            max_time = None
            if args.max:
                max_time = timer.parse_time_input(args.max)
            timer.count_up_timer(max_time)
        elif args.event:
            target_dt = timer.parse_datetime_input(args.event)
            timer.countdown_to_datetime(target_dt)
        else:
            # No arguments provided, run interactive mode
            timer.interactive_mode()
    
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Timer application closed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
