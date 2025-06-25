#!/usr/bin/env python3
"""
Speed Typing Test Application
A command-line tool to measure typing speed (WPM) and accuracy.
Author: Claude AI Assistant
Python Version: 3.8+
"""

import time
import random
import string
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple


class TypingTest:
    """Main class for the Speed Typing Test application."""
    
    def __init__(self):
        """Initialize the typing test with sample texts and settings."""
        self.sample_texts = [
            "The quick brown fox jumps over the lazy dog near the riverbank.",
            "Programming is the art of telling another human being what one wants the computer to do.",
            "Life is what happens to you while you are busy making other plans and dreams.",
            "The only way to do great work is to love what you do and pursue it with passion.",
            "Success is not final, failure is not fatal, it is the courage to continue that counts most.",
            "In the middle of difficulty lies opportunity waiting to be discovered by those who seek.",
            "The future belongs to those who believe in the beauty of their dreams and aspirations.",
            "Technology is best when it brings people together and makes their lives easier and better.",
            "Education is the most powerful weapon which you can use to change the world around you.",
            "The journey of a thousand miles begins with a single step taken in the right direction."
        ]
        
        self.difficulty_levels = {
            'easy': {'words': 5, 'complexity': 'simple'},
            'medium': {'words': 8, 'complexity': 'moderate'},
            'hard': {'words': 12, 'complexity': 'complex'}
        }
        
        self.results_file = "typing_results.json"
        
    def clear_screen(self):
        """Clear the terminal screen for better user experience."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("=" * 60)
        print("🎯 SPEED TYPING TEST")
        print("=" * 60)
        print("Welcome to the Speed Typing Test!")
        print("Test your typing speed and accuracy with various difficulty levels.")
        print("\nInstructions:")
        print("• Type the given text as quickly and accurately as possible")
        print("• Press Enter when you're done typing")
        print("• Your WPM (Words Per Minute) and accuracy will be calculated")
        print("• Results are automatically saved to track your progress")
        print("=" * 60)
    
    def get_random_text(self, difficulty: str = 'medium') -> str:
        """
        Generate or select text based on difficulty level.
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
            
        Returns:
            str: Text to be typed
        """
        if difficulty == 'easy':
            # Use shorter, simpler sentences
            easy_texts = [text for text in self.sample_texts if len(text.split()) <= 8]
            return random.choice(easy_texts if easy_texts else self.sample_texts[:3])
        
        elif difficulty == 'hard':
            # Create more complex text with punctuation and numbers
            base_text = random.choice(self.sample_texts)
            numbers = ''.join(random.choices(string.digits, k=3))
            symbols = random.choice(['!', '?', '.', ',', ';'])
            return f"{base_text} {numbers}{symbols}"
        
        else:  # medium
            return random.choice(self.sample_texts)
    
    def calculate_wpm(self, text: str, time_taken: float) -> float:
        """
        Calculate Words Per Minute (WPM).
        
        Args:
            text (str): The typed text
            time_taken (float): Time taken in seconds
            
        Returns:
            float: Words per minute
        """
        if time_taken <= 0:
            return 0.0
        
        word_count = len(text.split())
        minutes = time_taken / 60
        return round(word_count / minutes, 2)
    
    def calculate_accuracy(self, original: str, typed: str) -> Tuple[float, int, int]:
        """
        Calculate typing accuracy by comparing original and typed text.
        
        Args:
            original (str): Original text to be typed
            typed (str): User's typed text
            
        Returns:
            tuple: (accuracy_percentage, correct_chars, total_chars)
        """
        if not typed:
            return 0.0, 0, len(original)
        
        min_length = min(len(original), len(typed))
        correct_chars = sum(1 for i in range(min_length) if original[i] == typed[i])
        
        # Account for extra or missing characters
        total_chars = max(len(original), len(typed))
        accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0
        
        return round(accuracy, 2), correct_chars, total_chars
    
    def display_text_to_type(self, text: str):
        """
        Display the text that needs to be typed with formatting.
        
        Args:
            text (str): Text to display
        """
        print("\n" + "─" * 60)
        print("📝 TYPE THE FOLLOWING TEXT:")
        print("─" * 60)
        print(f"\n{text}\n")
        print("─" * 60)
        print("Start typing when ready (Press Enter when done):")
    
    def run_test(self, difficulty: str = 'medium') -> Dict:
        """
        Run a single typing test.
        
        Args:
            difficulty (str): Difficulty level
            
        Returns:
            dict: Test results
        """
        # Get text based on difficulty
        text_to_type = self.get_random_text(difficulty)
        
        # Display the text
        self.display_text_to_type(text_to_type)
        
        # Wait for user to start typing
        input("Press Enter when you're ready to start...")
        self.clear_screen()
        self.display_text_to_type(text_to_type)
        
        # Start timer and get user input
        start_time = time.time()
        try:
            user_input = input(">>> ")
        except KeyboardInterrupt:
            print("\n\nTest cancelled by user.")
            return {}
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        # Calculate results
        wpm = self.calculate_wpm(user_input, time_taken)
        accuracy, correct_chars, total_chars = self.calculate_accuracy(text_to_type, user_input)
        
        # Create results dictionary
        results = {
            'timestamp': datetime.now().isoformat(),
            'difficulty': difficulty,
            'original_text': text_to_type,
            'typed_text': user_input,
            'time_taken': round(time_taken, 2),
            'wpm': wpm,
            'accuracy': accuracy,
            'correct_characters': correct_chars,
            'total_characters': total_chars
        }
        
        return results
    
    def display_results(self, results: Dict):
        """
        Display test results in a formatted way.
        
        Args:
            results (dict): Test results to display
        """
        if not results:
            return
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        print(f"⏱️  Time Taken: {results['time_taken']} seconds")
        print(f"🚀 Speed: {results['wpm']} WPM")
        print(f"🎯 Accuracy: {results['accuracy']}%")
        print(f"✅ Correct Characters: {results['correct_characters']}/{results['total_characters']}")
        print(f"📈 Difficulty: {results['difficulty'].title()}")
        
        # Performance feedback
        if results['wpm'] >= 60:
            print("🏆 Excellent typing speed!")
        elif results['wpm'] >= 40:
            print("👍 Good typing speed!")
        elif results['wpm'] >= 20:
            print("📚 Keep practicing to improve!")
        else:
            print("🎯 Focus on accuracy first, speed will come!")
        
        print("=" * 60)
    
    def save_results(self, results: Dict):
        """
        Save test results to a JSON file.
        
        Args:
            results (dict): Test results to save
        """
        if not results:
            return
        
        try:
            # Load existing results
            if os.path.exists(self.results_file):
                with open(self.results_file, 'r') as f:
                    all_results = json.load(f)
            else:
                all_results = []
            
            # Add new result
            all_results.append(results)
            
            # Save back to file
            with open(self.results_file, 'w') as f:
                json.dump(all_results, f, indent=2)
            
            print(f"✅ Results saved to {self.results_file}")
            
        except Exception as e:
            print(f"⚠️  Error saving results: {e}")
    
    def show_statistics(self):
        """Display user's typing statistics from saved results."""
        try:
            if not os.path.exists(self.results_file):
                print("📊 No previous results found. Take a test first!")
                return
            
            with open(self.results_file, 'r') as f:
                all_results = json.load(f)
            
            if not all_results:
                print("📊 No results available.")
                return
            
            # Calculate statistics
            total_tests = len(all_results)
            avg_wpm = sum(r['wpm'] for r in all_results) / total_tests
            avg_accuracy = sum(r['accuracy'] for r in all_results) / total_tests
            best_wpm = max(r['wpm'] for r in all_results)
            best_accuracy = max(r['accuracy'] for r in all_results)
            
            print("\n" + "=" * 60)
            print("📈 YOUR TYPING STATISTICS")
            print("=" * 60)
            print(f"📝 Total Tests: {total_tests}")
            print(f"⚡ Average Speed: {avg_wpm:.1f} WPM")
            print(f"🎯 Average Accuracy: {avg_accuracy:.1f}%")
            print(f"🏆 Best Speed: {best_wpm} WPM")
            print(f"🎖️  Best Accuracy: {best_accuracy}%")
            print("=" * 60)
            
            # Show recent results
            print("\n🕐 RECENT RESULTS (Last 5):")
            recent_results = all_results[-5:]
            for i, result in enumerate(reversed(recent_results), 1):
                date = datetime.fromisoformat(result['timestamp']).strftime("%Y-%m-%d %H:%M")
                print(f"{i}. {date} | {result['wpm']} WPM | {result['accuracy']}% | {result['difficulty']}")
            
        except Exception as e:
            print(f"⚠️  Error loading statistics: {e}")
    
    def get_difficulty_choice(self) -> str:
        """
        Get difficulty choice from user.
        
        Returns:
            str: Selected difficulty level
        """
        print("\n🎚️  Select Difficulty Level:")
        print("1. Easy (Simple words, shorter text)")
        print("2. Medium (Standard sentences)")
        print("3. Hard (Complex text with numbers/symbols)")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                if choice == '1':
                    return 'easy'
                elif choice == '2':
                    return 'medium'
                elif choice == '3':
                    return 'hard'
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\n\nExiting...")
                return 'medium'
    
    def main_menu(self):
        """Display main menu and handle user choices."""
        while True:
            try:
                print("\n" + "🎯 MAIN MENU")
                print("1. Start Typing Test")
                print("2. View Statistics")
                print("3. Exit")
                
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == '1':
                    self.clear_screen()
                    difficulty = self.get_difficulty_choice()
                    self.clear_screen()
                    results = self.run_test(difficulty)
                    if results:
                        self.display_results(results)
                        self.save_results(results)
                
                elif choice == '2':
                    self.show_statistics()
                
                elif choice == '3':
                    print("\n👋 Thanks for using Speed Typing Test! Keep practicing!")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using Speed Typing Test!")
                break
            except Exception as e:
                print(f"⚠️  An error occurred: {e}")


def run_unit_tests():
    """Simple unit tests for the TypingTest class."""
    print("🧪 Running Unit Tests...")
    
    test = TypingTest()
    
    # Test WPM calculation
    wpm = test.calculate_wpm("hello world test", 60)  # 3 words in 60 seconds = 3 WPM
    assert wpm == 3.0, f"Expected 3.0, got {wpm}"
    print("✅ WPM calculation test passed")
    
    # Test accuracy calculation
    accuracy, correct, total = test.calculate_accuracy("hello", "hello")
    assert accuracy == 100.0, f"Expected 100.0, got {accuracy}"
    print("✅ Perfect accuracy test passed")
    
    accuracy, correct, total = test.calculate_accuracy("hello", "helo")
    assert accuracy == 80.0, f"Expected 80.0, got {accuracy}"
    print("✅ Partial accuracy test passed")
    
    # Test text generation
    text = test.get_random_text('easy')
    assert isinstance(text, str) and len(text) > 0, "Text generation failed"
    print("✅ Text generation test passed")
    
    print("🎉 All unit tests passed!")


if __name__ == "__main__":
    # Uncomment the next line to run unit tests
    # run_unit_tests()
    
    # Run the main application
    typing_test = TypingTest()
    typing_test.clear_screen()
    typing_test.display_welcome()
    typing_test.main_menu()
