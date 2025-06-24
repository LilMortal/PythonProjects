#!/usr/bin/env python3
"""
Word Guessing Game - A fun interactive word puzzle game
Similar to Wordle but with customizable features and difficulty levels.

Author: Claude Assistant
Version: 1.0
Python Version: 3.7+
"""

import random
import string
import json
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime


class WordGame:
    """Main game class for the word guessing game."""
    
    def __init__(self, word_length: int = 5, max_attempts: int = 6):
        """
        Initialize the game with specified parameters.
        
        Args:
            word_length: Length of the word to guess (default: 5)
            max_attempts: Maximum number of attempts allowed (default: 6)
        """
        self.word_length = word_length
        self.max_attempts = max_attempts
        self.current_word = ""
        self.attempts = 0
        self.guessed_words = []
        self.game_over = False
        self.won = False
        self.stats = self._load_stats()
        
        # Color codes for terminal output
        self.colors = {
            'correct': '\033[92m',     # Green
            'partial': '\033[93m',     # Yellow
            'incorrect': '\033[91m',   # Red
            'reset': '\033[0m',        # Reset
            'bold': '\033[1m'          # Bold
        }
        
        # Word lists for different difficulties
        self.word_lists = {
            3: ['cat', 'dog', 'run', 'sun', 'hat', 'bat', 'car', 'far', 'war', 'bar'],
            4: ['code', 'game', 'play', 'word', 'quiz', 'test', 'help', 'home', 'love', 'time'],
            5: ['world', 'house', 'money', 'power', 'light', 'music', 'heart', 'brain', 'smile', 'dance'],
            6: ['python', 'gaming', 'coding', 'forest', 'bottle', 'carpet', 'finger', 'garden', 'juggle', 'laptop'],
            7: ['rainbow', 'pattern', 'history', 'journey', 'kitchen', 'morning', 'picture', 'science', 'trouble', 'welcome']
        }
    
    def _load_stats(self) -> Dict:
        """Load game statistics from file."""
        stats_file = 'game_stats.json'
        default_stats = {
            'games_played': 0,
            'games_won': 0,
            'win_percentage': 0.0,
            'current_streak': 0,
            'max_streak': 0,
            'guess_distribution': {str(i): 0 for i in range(1, 7)}
        }
        
        try:
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        
        return default_stats
    
    def _save_stats(self):
        """Save game statistics to file."""
        try:
            with open('game_stats.json', 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError:
            print("Warning: Could not save game statistics.")
    
    def _get_random_word(self) -> str:
        """Get a random word based on the specified word length."""
        if self.word_length in self.word_lists:
            return random.choice(self.word_lists[self.word_length]).upper()
        else:
            # Generate a random word if length not in predefined lists
            return ''.join(random.choices(string.ascii_uppercase, k=self.word_length))
    
    def start_new_game(self):
        """Start a new game session."""
        self.current_word = self._get_random_word()
        self.attempts = 0
        self.guessed_words = []
        self.game_over = False
        self.won = False
        
        print(f"\n{self.colors['bold']}🎯 Welcome to Word Guessing Game! 🎯{self.colors['reset']}")
        print(f"Guess the {self.word_length}-letter word!")
        print(f"You have {self.max_attempts} attempts.")
        print(f"Enter your guess (or 'quit' to exit, 'hint' for a hint):\n")
    
    def _validate_guess(self, guess: str) -> Tuple[bool, str]:
        """
        Validate the user's guess.
        
        Args:
            guess: The user's guess
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(guess) != self.word_length:
            return False, f"Word must be exactly {self.word_length} letters long."
        
        if not guess.isalpha():
            return False, "Word must contain only letters."
        
        return True, ""
    
    def _analyze_guess(self, guess: str) -> List[str]:
        """
        Analyze the guess and return color-coded feedback.
        
        Args:
            guess: The user's guess
            
        Returns:
            List of color codes for each letter
        """
        guess = guess.upper()
        result = ['incorrect'] * len(guess)
        word_chars = list(self.current_word)
        
        # First pass: mark correct positions
        for i, char in enumerate(guess):
            if char == self.current_word[i]:
                result[i] = 'correct'
                word_chars[i] = None  # Mark as used
        
        # Second pass: mark partial matches
        for i, char in enumerate(guess):
            if result[i] == 'incorrect' and char in word_chars:
                result[i] = 'partial'
                word_chars[word_chars.index(char)] = None  # Mark as used
        
        return result
    
    def _display_guess_result(self, guess: str, analysis: List[str]):
        """Display the guess result with colors."""
        colored_guess = ""
        for i, char in enumerate(guess.upper()):
            color = self.colors[analysis[i]]
            colored_guess += f"{color}{char}{self.colors['reset']}"
        
        print(f"Guess {self.attempts}: {colored_guess}")
        
        # Display legend
        legend = (f"{self.colors['correct']}Green = Correct position{self.colors['reset']} | "
                 f"{self.colors['partial']}Yellow = Wrong position{self.colors['reset']} | "
                 f"{self.colors['incorrect']}Red = Not in word{self.colors['reset']}")
        print(f"Legend: {legend}\n")
    
    def _give_hint(self):
        """Provide a hint to the player."""
        if self.attempts == 0:
            hint_pos = 0
        else:
            # Reveal a random position that hasn't been guessed correctly
            revealed_positions = set()
            for guess_data in self.guessed_words:
                guess, analysis = guess_data
                for i, status in enumerate(analysis):
                    if status == 'correct':
                        revealed_positions.add(i)
            
            unrevealed = [i for i in range(self.word_length) if i not in revealed_positions]
            if unrevealed:
                hint_pos = random.choice(unrevealed)
            else:
                print("No more hints available!")
                return
        
        hint_letter = self.current_word[hint_pos]
        print(f"💡 Hint: Position {hint_pos + 1} is '{hint_letter}'")
    
    def make_guess(self, guess: str) -> bool:
        """
        Process a player's guess.
        
        Args:
            guess: The player's guess
            
        Returns:
            True if game should continue, False if game is over
        """
        # Handle special commands
        if guess.lower() == 'quit':
            print("Thanks for playing! 👋")
            return False
        
        if guess.lower() == 'hint':
            self._give_hint()
            return True
        
        # Validate guess
        is_valid, error_msg = self._validate_guess(guess)
        if not is_valid:
            print(f"❌ {error_msg}")
            return True
        
        # Process guess
        self.attempts += 1
        analysis = self._analyze_guess(guess)
        self.guessed_words.append((guess.upper(), analysis))
        
        # Display result
        self._display_guess_result(guess, analysis)
        
        # Check win condition
        if guess.upper() == self.current_word:
            self.won = True
            self.game_over = True
            print(f"🎉 Congratulations! You guessed '{self.current_word}' in {self.attempts} attempts!")
            self._update_stats(won=True)
            return False
        
        # Check lose condition
        if self.attempts >= self.max_attempts:
            self.game_over = True
            print(f"💀 Game Over! The word was '{self.current_word}'")
            print(f"Better luck next time!")
            self._update_stats(won=False)
            return False
        
        # Game continues
        remaining = self.max_attempts - self.attempts
        print(f"Attempts remaining: {remaining}")
        return True
    
    def _update_stats(self, won: bool):
        """Update game statistics."""
        self.stats['games_played'] += 1
        
        if won:
            self.stats['games_won'] += 1
            self.stats['current_streak'] += 1
            self.stats['max_streak'] = max(self.stats['max_streak'], self.stats['current_streak'])
            self.stats['guess_distribution'][str(self.attempts)] += 1
        else:
            self.stats['current_streak'] = 0
        
        self.stats['win_percentage'] = (self.stats['games_won'] / self.stats['games_played']) * 100
        self._save_stats()
    
    def display_stats(self):
        """Display game statistics."""
        print(f"\n{self.colors['bold']}📊 Game Statistics 📊{self.colors['reset']}")
        print(f"Games Played: {self.stats['games_played']}")
        print(f"Games Won: {self.stats['games_won']}")
        print(f"Win Percentage: {self.stats['win_percentage']:.1f}%")
        print(f"Current Streak: {self.stats['current_streak']}")
        print(f"Max Streak: {self.stats['max_streak']}")
        
        print(f"\n{self.colors['bold']}Guess Distribution:{self.colors['reset']}")
        for attempt, count in self.stats['guess_distribution'].items():
            bar = '█' * count if count > 0 else ''
            print(f"{attempt}: {bar} ({count})")


def get_difficulty_settings() -> Tuple[int, int]:
    """Get difficulty settings from user."""
    print("\n🎮 Choose Difficulty Level:")
    print("1. Easy (3 letters, 8 attempts)")
    print("2. Normal (5 letters, 6 attempts)")
    print("3. Hard (6 letters, 5 attempts)")
    print("4. Expert (7 letters, 4 attempts)")
    print("5. Custom")
    
    while True:
        try:
            choice = input("Enter choice (1-5): ").strip()
            
            if choice == '1':
                return 3, 8
            elif choice == '2':
                return 5, 6
            elif choice == '3':
                return 6, 5
            elif choice == '4':
                return 7, 4
            elif choice == '5':
                word_length = int(input("Word length (3-10): "))
                max_attempts = int(input("Max attempts (3-10): "))
                
                if not (3 <= word_length <= 10) or not (3 <= max_attempts <= 10):
                    print("Invalid range. Please use 3-10 for both values.")
                    continue
                
                return word_length, max_attempts
            else:
                print("Please enter a valid choice (1-5).")
        
        except (ValueError, KeyboardInterrupt):
            print("Invalid input. Please try again.")


def main():
    """Main game loop."""
    print("🎯 Word Guessing Game 🎯")
    print("=" * 30)
    
    try:
        while True:
            # Get game settings
            word_length, max_attempts = get_difficulty_settings()
            
            # Create and start game
            game = WordGame(word_length, max_attempts)
            game.start_new_game()
            
            # Game loop
            while True:
                try:
                    guess = input(f"Enter your guess ({game.word_length} letters): ").strip()
                    
                    if not game.make_guess(guess):
                        break
                        
                except KeyboardInterrupt:
                    print("\n\nGame interrupted. Thanks for playing! 👋")
                    return
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue
            
            # Show stats
            game.display_stats()
            
            # Ask to play again
            while True:
                try:
                    play_again = input("\nPlay again? (y/n): ").strip().lower()
                    if play_again in ['y', 'yes']:
                        break
                    elif play_again in ['n', 'no']:
                        print("Thanks for playing! 👋")
                        return
                    else:
                        print("Please enter 'y' for yes or 'n' for no.")
                except KeyboardInterrupt:
                    print("\nThanks for playing! 👋")
                    return
    
    except KeyboardInterrupt:
        print("\nThanks for playing! 👋")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Simple unit tests (can be run by uncommenting and running this section)
def run_tests():
    """Run basic unit tests for the game."""
    print("Running tests...")
    
    # Test word validation
    game = WordGame(5, 6)
    
    # Test valid word
    valid, msg = game._validate_guess("hello")
    assert valid == True, "Valid word should pass validation"
    
    # Test invalid length
    valid, msg = game._validate_guess("hi")
    assert valid == False, "Short word should fail validation"
    
    # Test non-alpha characters
    valid, msg = game._validate_guess("hel12")
    assert valid == False, "Word with numbers should fail validation"
    
    # Test guess analysis
    game.current_word = "HELLO"
    analysis = game._analyze_guess("HELLO")
    assert analysis == ['correct'] * 5, "Perfect guess should be all correct"
    
    analysis = game._analyze_guess("WORLD")
    expected = ['incorrect', 'incorrect', 'incorrect', 'partial', 'incorrect']
    assert analysis == expected, f"Analysis should be {expected}, got {analysis}"
    
    print("All tests passed! ✅")


if __name__ == "__main__":
    # Uncomment the line below to run tests
    # run_tests()
    
    main()
