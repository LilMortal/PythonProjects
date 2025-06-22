#!/usr/bin/env python3
"""
Hangman Game - A classic word guessing game
Author: Claude AI
Python 3.10+ Compatible
"""

import random
import string
import os
import sys

class HangmanGame:
    """Main Hangman game class that handles all game logic"""
    
    # ASCII art for hangman stages
    HANGMAN_STAGES = [
        """
           -----
           |   |
               |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """
    ]
    
    # Default word lists by difficulty
    WORD_LISTS = {
        'easy': [
            'cat', 'dog', 'car', 'sun', 'hat', 'pen', 'cup', 'bag', 'key', 'box',
            'run', 'red', 'blue', 'book', 'tree', 'fish', 'bird', 'moon', 'star', 'home'
        ],
        'medium': [
            'python', 'guitar', 'flower', 'rocket', 'bridge', 'castle', 'jungle', 'wizard',
            'dragon', 'rainbow', 'puzzle', 'monkey', 'elephant', 'diamond', 'treasure',
            'mountain', 'adventure', 'kitchen', 'garden', 'camera'
        ],
        'hard': [
            'programming', 'extraordinary', 'mysterious', 'encyclopedia', 'archaeology',
            'metamorphosis', 'synchronization', 'pharmaceutical', 'entrepreneurship',
            'unconventional', 'characteristics', 'responsibilities', 'telecommunications',
            'environmental', 'international', 'revolutionary', 'sophisticated', 'magnificent',
            'incomprehensible', 'unquestionably'
        ]
    }
    
    def __init__(self):
        """Initialize the game with default settings"""
        self.word = ""
        self.guessed_word = []
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.game_over = False
        self.won = False
        self.difficulty = 'medium'
        self.stats = {'games_played': 0, 'games_won': 0, 'total_guesses': 0}
    
    def clear_screen(self):
        """Clear the terminal screen for better UI"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_title(self):
        """Display the game title with ASCII art"""
        title = """
        ╔═══════════════════════════════════════╗
        ║          🎮 HANGMAN GAME 🎮           ║
        ║        Test Your Word Skills!         ║
        ╚═══════════════════════════════════════╝
        """
        print(title)
    
    def get_difficulty(self):
        """Get difficulty level from user"""
        while True:
            print("\n🎯 Choose difficulty level:")
            print("1. Easy (3-4 letter words)")
            print("2. Medium (5-8 letter words)")
            print("3. Hard (9+ letter words)")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                self.difficulty = 'easy'
                break
            elif choice == '2':
                self.difficulty = 'medium'
                break
            elif choice == '3':
                self.difficulty = 'hard'
                break
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.")
    
    def choose_word(self):
        """Choose a random word based on difficulty"""
        word_list = self.WORD_LISTS[self.difficulty]
        self.word = random.choice(word_list).upper()
        self.guessed_word = ['_' for _ in self.word]
    
    def display_game_state(self):
        """Display current game state including hangman, word, and guesses"""
        self.clear_screen()
        self.display_title()
        
        # Display hangman
        print(self.HANGMAN_STAGES[self.wrong_guesses])
        
        # Display difficulty and word progress
        print(f"🎯 Difficulty: {self.difficulty.capitalize()}")
        print(f"📝 Word: {' '.join(self.guessed_word)}")
        print(f"❌ Wrong guesses: {self.wrong_guesses}/{self.max_wrong_guesses}")
        
        # Display guessed letters
        if self.guessed_letters:
            sorted_guesses = sorted(list(self.guessed_letters))
            print(f"💭 Guessed letters: {', '.join(sorted_guesses)}")
        
        print("\n" + "="*50)
    
    def get_guess(self):
        """Get and validate user's letter guess"""
        while True:
            guess = input("\n🔤 Enter a letter (or 'quit' to exit): ").strip().upper()
            
            # Check for quit command
            if guess.lower() == 'quit':
                return None
            
            # Validate input
            if len(guess) != 1:
                print("❌ Please enter exactly one letter!")
                continue
            
            if not guess.isalpha():
                print("❌ Please enter a valid letter!")
                continue
            
            if guess in self.guessed_letters:
                print("❌ You already guessed that letter!")
                continue
            
            return guess
    
    def process_guess(self, guess):
        """Process the user's guess and update game state"""
        self.guessed_letters.add(guess)
        self.stats['total_guesses'] += 1
        
        if guess in self.word:
            # Correct guess - reveal letter(s)
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.guessed_word[i] = letter
            print(f"✅ Great! '{guess}' is in the word!")
            
            # Check if word is complete
            if '_' not in self.guessed_word:
                self.won = True
                self.game_over = True
        else:
            # Wrong guess
            self.wrong_guesses += 1
            print(f"❌ Sorry! '{guess}' is not in the word.")
            
            # Check if game is lost
            if self.wrong_guesses >= self.max_wrong_guesses:
                self.game_over = True
        
        # Small pause for user to see the message
        input("\nPress Enter to continue...")
    
    def display_end_game(self):
        """Display end game message and statistics"""
        self.display_game_state()
        
        if self.won:
            print("🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"💡 The word was: {self.word}")
            print(f"🎯 You guessed it with {len(self.guessed_letters)} total guesses!")
        else:
            print("💀 GAME OVER! 💀")
            print(f"💡 The word was: {self.word}")
            print("Better luck next time!")
        
        # Update and display stats
        self.stats['games_played'] += 1
        if self.won:
            self.stats['games_won'] += 1
        
        self.display_stats()
    
    def display_stats(self):
        """Display game statistics"""
        win_rate = (self.stats['games_won'] / self.stats['games_played'] * 100) if self.stats['games_played'] > 0 else 0
        avg_guesses = (self.stats['total_guesses'] / self.stats['games_played']) if self.stats['games_played'] > 0 else 0
        
        print(f"\n📊 GAME STATISTICS:")
        print(f"🎮 Games played: {self.stats['games_played']}")
        print(f"🏆 Games won: {self.stats['games_won']}")
        print(f"📈 Win rate: {win_rate:.1f}%")
        print(f"🔤 Average guesses per game: {avg_guesses:.1f}")
    
    def play_again(self):
        """Ask if user wants to play again"""
        while True:
            choice = input("\n🔄 Would you like to play again? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' for yes or 'n' for no.")
    
    def reset_game(self):
        """Reset game state for a new game"""
        self.word = ""
        self.guessed_word = []
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.won = False
    
    def display_instructions(self):
        """Display game instructions"""
        instructions = """
        📋 HOW TO PLAY HANGMAN:
        
        🎯 Objective: Guess the hidden word letter by letter
        
        📝 Rules:
        • You have 6 wrong guesses before the game ends
        • Each wrong guess adds a part to the hangman
        • Guess letters one at a time
        • Win by guessing all letters before the hangman is complete
        
        💡 Tips:
        • Start with common vowels (A, E, I, O, U)
        • Try common consonants (R, S, T, L, N)
        • Look for letter patterns as the word is revealed
        
        🎮 Commands:
        • Type any letter to make a guess
        • Type 'quit' during the game to exit
        
        Good luck and have fun! 🍀
        """
        print(instructions)
        input("\nPress Enter to start playing...")
    
    def main_menu(self):
        """Display main menu and handle user choice"""
        while True:
            self.clear_screen()
            self.display_title()
            
            print("🎮 MAIN MENU:")
            print("1. 🎯 Play Game")
            print("2. 📋 Instructions")
            print("3. 📊 View Statistics")
            print("4. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                return 'play'
            elif choice == '2':
                self.display_instructions()
            elif choice == '3':
                self.display_stats()
                input("\nPress Enter to continue...")
            elif choice == '4':
                return 'exit'
            else:
                print("❌ Invalid choice! Please enter 1-4.")
                input("Press Enter to continue...")
    
    def run(self):
        """Main game loop"""
        print("🎮 Welcome to Hangman!")
        
        while True:
            menu_choice = self.main_menu()
            
            if menu_choice == 'exit':
                self.clear_screen()
                print("👋 Thanks for playing Hangman!")
                print("🎮 Game created with Python")
                sys.exit(0)
            
            elif menu_choice == 'play':
                self.reset_game()
                self.get_difficulty()
                self.choose_word()
                
                # Main game loop
                while not self.game_over:
                    self.display_game_state()
                    guess = self.get_guess()
                    
                    if guess is None:  # User chose to quit
                        print("👋 Thanks for playing!")
                        return
                    
                    self.process_guess(guess)
                
                # Game ended
                self.display_end_game()
                
                if not self.play_again():
                    self.clear_screen()
                    print("👋 Thanks for playing Hangman!")
                    print("🎮 Game created with Python")
                    break

def main():
    """Main function to start the game"""
    try:
        game = HangmanGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the game.")

if __name__ == "__main__":
    main()
