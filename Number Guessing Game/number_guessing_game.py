#!/usr/bin/env python3
"""
Number Guessing Game - A fun interactive CLI game
Author: Assistant
Version: 1.0
Python 3.10+ compatible
"""

import random
import time
import json
import os
from typing import Dict, List, Tuple, Optional

class NumberGuessingGame:
    """
    A comprehensive number guessing game with multiple difficulty levels,
    statistics tracking, and various game modes.
    """
    
    def __init__(self):
        self.stats_file = "game_stats.json"
        self.game_stats = self.load_stats()
        self.difficulty_levels = {
            1: {"name": "Easy", "range": (1, 50), "max_attempts": 10},
            2: {"name": "Medium", "range": (1, 100), "max_attempts": 8},
            3: {"name": "Hard", "range": (1, 200), "max_attempts": 6},
            4: {"name": "Expert", "range": (1, 500), "max_attempts": 5}
        }
    
    def load_stats(self) -> Dict:
        """Load game statistics from file or create new stats."""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        
        # Return default stats structure
        return {
            "games_played": 0,
            "games_won": 0,
            "total_guesses": 0,
            "best_score": {"difficulty": None, "guesses": float('inf')},
            "difficulty_stats": {
                "Easy": {"played": 0, "won": 0, "avg_guesses": 0},
                "Medium": {"played": 0, "won": 0, "avg_guesses": 0},
                "Hard": {"played": 0, "won": 0, "avg_guesses": 0},
                "Expert": {"played": 0, "won": 0, "avg_guesses": 0}
            }
        }
    
    def save_stats(self) -> None:
        """Save current game statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.game_stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Warning: Could not save stats - {e}")
    
    def update_stats(self, difficulty_name: str, won: bool, guesses: int) -> None:
        """Update game statistics after a game."""
        self.game_stats["games_played"] += 1
        self.game_stats["total_guesses"] += guesses
        
        if won:
            self.game_stats["games_won"] += 1
            
            # Update best score if this is better
            if (self.game_stats["best_score"]["difficulty"] is None or 
                guesses < self.game_stats["best_score"]["guesses"]):
                self.game_stats["best_score"] = {
                    "difficulty": difficulty_name,
                    "guesses": guesses
                }
        
        # Update difficulty-specific stats
        diff_stats = self.game_stats["difficulty_stats"][difficulty_name]
        diff_stats["played"] += 1
        
        if won:
            diff_stats["won"] += 1
        
        # Calculate average guesses for this difficulty
        if diff_stats["played"] > 0:
            total_guesses_diff = diff_stats.get("total_guesses", 0) + guesses
            diff_stats["total_guesses"] = total_guesses_diff
            diff_stats["avg_guesses"] = round(total_guesses_diff / diff_stats["played"], 1)
        
        self.save_stats()
    
    def display_welcome(self) -> None:
        """Display welcome message and game introduction."""
        print("\n" + "="*60)
        print("🎲 WELCOME TO THE NUMBER GUESSING GAME! 🎲")
        print("="*60)
        print("Try to guess the secret number in as few attempts as possible!")
        print("The game will give you hints after each guess.")
        print("="*60)
    
    def display_difficulty_menu(self) -> int:
        """Display difficulty selection menu and get user choice."""
        print("\n🎯 Select Difficulty Level:")
        print("-" * 30)
        
        for level, info in self.difficulty_levels.items():
            range_info = f"{info['range'][0]}-{info['range'][1]}"
            attempts_info = f"{info['max_attempts']} attempts"
            print(f"{level}. {info['name']:<8} | Range: {range_info:<8} | Max: {attempts_info}")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                choice = int(choice)
                
                if choice in self.difficulty_levels:
                    return choice
                else:
                    print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    def get_valid_guess(self, min_val: int, max_val: int) -> Optional[int]:
        """Get a valid guess from the user within the specified range."""
        while True:
            try:
                guess_input = input(f"\nEnter your guess ({min_val}-{max_val}) or 'quit' to exit: ").strip().lower()
                
                if guess_input == 'quit':
                    return None
                
                guess = int(guess_input)
                
                if min_val <= guess <= max_val:
                    return guess
                else:
                    print(f"❌ Please enter a number between {min_val} and {max_val}!")
                    
            except ValueError:
                print("❌ Please enter a valid number or 'quit'!")
    
    def give_hint(self, guess: int, target: int, attempt: int) -> str:
        """Provide intelligent hints based on the guess."""
        difference = abs(guess - target)
        
        if difference == 0:
            return "🎉 PERFECT! You got it!"
        elif difference <= 5:
            direction = "higher" if guess < target else "lower"
            return f"🔥 Very close! Go {direction}!"
        elif difference <= 15:
            direction = "higher" if guess < target else "lower"
            return f"🌡️  Getting warm! Try {direction}!"
        elif difference <= 30:
            direction = "higher" if guess < target else "lower"
            return f"❄️  Getting colder... Try {direction}!"
        else:
            direction = "much higher" if guess < target else "much lower"
            return f"🧊 Way off! Try {direction}!"
    
    def play_game(self, difficulty: int) -> Tuple[bool, int]:
        """Play a single game and return (won, attempts_used)."""
        level_info = self.difficulty_levels[difficulty]
        min_val, max_val = level_info["range"]
        max_attempts = level_info["max_attempts"]
        difficulty_name = level_info["name"]
        
        # Generate random number
        target_number = random.randint(min_val, max_val)
        
        print(f"\n🎮 Starting {difficulty_name} mode!")
        print(f"🎯 I'm thinking of a number between {min_val} and {max_val}")
        print(f"🎲 You have {max_attempts} attempts to guess it!")
        print(f"💡 Type 'quit' anytime to exit the game")
        
        start_time = time.time()
        attempts = 0
        guesses_history = []
        
        while attempts < max_attempts:
            attempts += 1
            print(f"\n--- Attempt {attempts}/{max_attempts} ---")
            
            guess = self.get_valid_guess(min_val, max_val)
            
            if guess is None:  # User wants to quit
                print(f"\n👋 Game ended! The number was {target_number}")
                return False, attempts - 1
            
            guesses_history.append(guess)
            
            if guess == target_number:
                end_time = time.time()
                game_time = round(end_time - start_time, 1)
                
                print(f"\n🎉 CONGRATULATIONS! 🎉")
                print(f"✅ You guessed {target_number} correctly!")
                print(f"📊 Attempts used: {attempts}/{max_attempts}")
                print(f"⏱️  Time taken: {game_time} seconds")
                print(f"📈 Your guesses: {' → '.join(map(str, guesses_history))}")
                
                return True, attempts
            else:
                hint = self.give_hint(guess, target_number, attempts)
                print(f"💭 {hint}")
                
                # Show remaining attempts
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"🔄 {remaining} attempts remaining")
        
        # Game over - no more attempts
        print(f"\n💥 GAME OVER! 💥")
        print(f"🎯 The number was: {target_number}")
        print(f"📈 Your guesses: {' → '.join(map(str, guesses_history))}")
        print("🍀 Better luck next time!")
        
        return False, max_attempts
    
    def display_stats(self) -> None:
        """Display comprehensive game statistics."""
        stats = self.game_stats
        
        print("\n" + "="*50)
        print("📊 GAME STATISTICS")
        print("="*50)
        
        if stats["games_played"] == 0:
            print("No games played yet. Start playing to see your stats!")
            return
        
        # Overall stats
        win_rate = round((stats["games_won"] / stats["games_played"]) * 100, 1)
        avg_guesses = round(stats["total_guesses"] / stats["games_played"], 1)
        
        print(f"🎮 Games Played: {stats['games_played']}")
        print(f"🏆 Games Won: {stats['games_won']}")
        print(f"📈 Win Rate: {win_rate}%")
        print(f"🎯 Average Guesses: {avg_guesses}")
        
        # Best score
        if stats["best_score"]["difficulty"]:
            print(f"🥇 Best Score: {stats['best_score']['guesses']} guesses ({stats['best_score']['difficulty']})")
        
        # Difficulty breakdown
        print("\n--- Difficulty Breakdown ---")
        for diff_name, diff_stats in stats["difficulty_stats"].items():
            if diff_stats["played"] > 0:
                diff_win_rate = round((diff_stats["won"] / diff_stats["played"]) * 100, 1)
                print(f"{diff_name:<8}: {diff_stats['played']} played, "
                      f"{diff_stats['won']} won ({diff_win_rate}%), "
                      f"avg: {diff_stats['avg_guesses']} guesses")
    
    def main_menu(self) -> bool:
        """Display main menu and handle user choice. Returns True to continue, False to exit."""
        print("\n" + "="*40)
        print("🎮 MAIN MENU")
        print("="*40)
        print("1. 🎯 Start New Game")
        print("2. 📊 View Statistics")
        print("3. 🔄 Reset Statistics")
        print("4. ❓ How to Play")
        print("5. 👋 Exit Game")
        
        while True:
            try:
                choice = input("\nSelect an option (1-5): ").strip()
                
                if choice == '1':
                    return True
                elif choice == '2':
                    self.display_stats()
                    input("\nPress Enter to continue...")
                    return True
                elif choice == '3':
                    self.reset_stats()
                    return True
                elif choice == '4':
                    self.show_instructions()
                    return True
                elif choice == '5':
                    return False
                else:
                    print("❌ Invalid choice! Please enter 1-5.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for playing!")
                return False
    
    def reset_stats(self) -> None:
        """Reset all game statistics."""
        confirm = input("\n⚠️  Are you sure you want to reset all statistics? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            self.game_stats = {
                "games_played": 0,
                "games_won": 0,
                "total_guesses": 0,
                "best_score": {"difficulty": None, "guesses": float('inf')},
                "difficulty_stats": {
                    "Easy": {"played": 0, "won": 0, "avg_guesses": 0},
                    "Medium": {"played": 0, "won": 0, "avg_guesses": 0},
                    "Hard": {"played": 0, "won": 0, "avg_guesses": 0},
                    "Expert": {"played": 0, "won": 0, "avg_guesses": 0}
                }
            }
            self.save_stats()
            print("✅ Statistics reset successfully!")
        else:
            print("❌ Reset cancelled.")
    
    def show_instructions(self) -> None:
        """Display game instructions and tips."""
        print("\n" + "="*50)
        print("❓ HOW TO PLAY")
        print("="*50)
        print("1. Choose a difficulty level (Easy, Medium, Hard, Expert)")
        print("2. The computer will think of a random number within the range")
        print("3. You have limited attempts to guess the number")
        print("4. After each guess, you'll get a hint:")
        print("   🔥 Very close - within 5 numbers")
        print("   🌡️  Getting warm - within 15 numbers")
        print("   ❄️  Getting colder - within 30 numbers")
        print("   🧊 Way off - more than 30 numbers away")
        print("5. Win by guessing the exact number!")
        print("\n💡 TIPS:")
        print("• Use binary search strategy for better results")
        print("• Pay attention to the hints - they're your best friend")
        print("• Start with medium difficulty to learn the game")
        print("• Type 'quit' during any guess to exit")
        
        input("\nPress Enter to continue...")
    
    def run(self) -> None:
        """Main game loop."""
        self.display_welcome()
        
        try:
            while True:
                if not self.main_menu():
                    break
                
                # Start new game
                difficulty = self.display_difficulty_menu()
                won, attempts = self.play_game(difficulty)
                
                # Update statistics
                difficulty_name = self.difficulty_levels[difficulty]["name"]
                self.update_stats(difficulty_name, won, attempts)
                
                # Ask if user wants to play again
                while True:
                    play_again = input("\n🎮 Play another game? (yes/no): ").strip().lower()
                    if play_again in ['yes', 'y', 'no', 'n']:
                        break
                    print("❌ Please enter 'yes' or 'no'")
                
                if play_again in ['no', 'n']:
                    break
        
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted by user.")
        
        finally:
            print("\n🎉 Thanks for playing the Number Guessing Game!")
            print("💾 Your statistics have been saved.")
            print("🎮 See you next time!")


def main():
    """Entry point of the application."""
    game = NumberGuessingGame()
    game.run()


if __name__ == "__main__":
    main()