#!/usr/bin/env python3
"""
Rock Paper Scissors Game
A command-line implementation of the classic Rock Paper Scissors game.
Includes single player vs computer and multiplayer modes.
"""

import random
import sys
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


class RockPaperScissorsGame:
    """Main game class handling all Rock Paper Scissors logic."""
    
    # Game constants
    CHOICES = ['rock', 'paper', 'scissors']
    WINNING_COMBINATIONS = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    def __init__(self):
        """Initialize the game with empty statistics."""
        self.stats = {
            'player_wins': 0,
            'computer_wins': 0,
            'ties': 0,
            'total_games': 0
        }
        self.game_history: List[Dict] = []
    
    def display_welcome(self) -> None:
        """Display welcome message and game rules."""
        print("=" * 50)
        print("🎮 WELCOME TO ROCK PAPER SCISSORS! 🎮")
        print("=" * 50)
        print("\nGame Rules:")
        print("• Rock crushes Scissors")
        print("• Scissors cuts Paper")
        print("• Paper covers Rock")
        print("\nChoices: rock, paper, scissors")
        print("Commands: 'quit' to exit, 'stats' to see statistics")
        print("=" * 50)
    
    def get_player_choice(self, player_name: str = "Player") -> Optional[str]:
        """
        Get and validate player choice.
        
        Args:
            player_name: Name of the player making the choice
            
        Returns:
            Valid choice string or None if quitting
        """
        while True:
            try:
                choice = input(f"\n{player_name}, enter your choice: ").lower().strip()
                
                # Handle special commands
                if choice == 'quit':
                    return None
                elif choice == 'stats':
                    self.display_stats()
                    continue
                elif choice in self.CHOICES:
                    return choice
                else:
                    print(f"❌ Invalid choice! Please enter: {', '.join(self.CHOICES)}")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n\n👋 Thanks for playing!")
                return None
    
    def get_computer_choice(self) -> str:
        """Generate random computer choice."""
        return random.choice(self.CHOICES)
    
    def determine_winner(self, player_choice: str, computer_choice: str) -> str:
        """
        Determine the winner of a round.
        
        Args:
            player_choice: Player's choice
            computer_choice: Computer's choice
            
        Returns:
            'player', 'computer', or 'tie'
        """
        if player_choice == computer_choice:
            return 'tie'
        elif self.WINNING_COMBINATIONS[player_choice] == computer_choice:
            return 'player'
        else:
            return 'computer'
    
    def display_round_result(self, player_choice: str, computer_choice: str, 
                           winner: str, player_name: str = "Player") -> None:
        """Display the result of a single round."""
        print(f"\n{player_name}: {player_choice.capitalize()}")
        print(f"Computer: {computer_choice.capitalize()}")
        print("-" * 30)
        
        if winner == 'tie':
            print("🤝 It's a tie!")
        elif winner == 'player':
            print(f"🎉 {player_name} wins this round!")
        else:
            print("🤖 Computer wins this round!")
    
    def update_stats(self, winner: str) -> None:
        """Update game statistics."""
        self.stats['total_games'] += 1
        if winner == 'player':
            self.stats['player_wins'] += 1
        elif winner == 'computer':
            self.stats['computer_wins'] += 1
        else:
            self.stats['ties'] += 1
    
    def display_stats(self) -> None:
        """Display current game statistics."""
        print("\n" + "=" * 30)
        print("📊 GAME STATISTICS")
        print("=" * 30)
        print(f"Total Games: {self.stats['total_games']}")
        print(f"Player Wins: {self.stats['player_wins']}")
        print(f"Computer Wins: {self.stats['computer_wins']}")
        print(f"Ties: {self.stats['ties']}")
        
        if self.stats['total_games'] > 0:
            win_rate = (self.stats['player_wins'] / self.stats['total_games']) * 100
            print(f"Win Rate: {win_rate:.1f}%")
        print("=" * 30)
    
    def play_single_round(self, player_name: str = "Player") -> bool:
        """
        Play a single round of the game.
        
        Args:
            player_name: Name of the player
            
        Returns:
            True to continue playing, False to quit
        """
        # Get player choice
        player_choice = self.get_player_choice(player_name)
        if player_choice is None:
            return False
        
        # Get computer choice
        computer_choice = self.get_computer_choice()
        
        # Determine winner
        winner = self.determine_winner(player_choice, computer_choice)
        
        # Display results
        self.display_round_result(player_choice, computer_choice, winner, player_name)
        
        # Update statistics
        self.update_stats(winner)
        
        # Store game history
        self.game_history.append({
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'winner': winner,
            'player_name': player_name
        })
        
        return True
    
    def play_multiplayer_round(self, player1_name: str, player2_name: str) -> bool:
        """
        Play a multiplayer round (no computer).
        
        Args:
            player1_name: Name of first player
            player2_name: Name of second player
            
        Returns:
            True to continue playing, False to quit
        """
        # Get both players' choices
        print(f"\n{player1_name}'s turn:")
        player1_choice = self.get_player_choice(player1_name)
        if player1_choice is None:
            return False
        
        print(f"\n{player2_name}'s turn:")
        player2_choice = self.get_player_choice(player2_name)
        if player2_choice is None:
            return False
        
        # Determine winner
        print(f"\n{player1_name}: {player1_choice.capitalize()}")
        print(f"{player2_name}: {player2_choice.capitalize()}")
        print("-" * 30)
        
        if player1_choice == player2_choice:
            print("🤝 It's a tie!")
        elif self.WINNING_COMBINATIONS[player1_choice] == player2_choice:
            print(f"🎉 {player1_name} wins this round!")
        else:
            print(f"🎉 {player2_name} wins this round!")
        
        return True
    
    def play_best_of_series(self, rounds: int = 3) -> None:
        """
        Play a best-of-N series.
        
        Args:
            rounds: Number of rounds to play (must be odd)
        """
        if rounds % 2 == 0:
            rounds += 1  # Make it odd
        
        print(f"\n🏆 Best of {rounds} series starting!")
        wins_needed = (rounds // 2) + 1
        
        player_series_wins = 0
        computer_series_wins = 0
        round_num = 1
        
        while (player_series_wins < wins_needed and 
               computer_series_wins < wins_needed and 
               round_num <= rounds):
            
            print(f"\n--- Round {round_num} ---")
            print(f"Score: Player {player_series_wins} - {computer_series_wins} Computer")
            
            if not self.play_single_round():
                break
            
            # Check last game result
            if self.game_history[-1]['winner'] == 'player':
                player_series_wins += 1
            elif self.game_history[-1]['winner'] == 'computer':
                computer_series_wins += 1
            
            round_num += 1
        
        # Announce series winner
        print(f"\n🏆 SERIES COMPLETE!")
        print(f"Final Score: Player {player_series_wins} - {computer_series_wins} Computer")
        
        if player_series_wins > computer_series_wins:
            print("🎉 Player wins the series!")
        elif computer_series_wins > player_series_wins:
            print("🤖 Computer wins the series!")
        else:
            print("🤝 Series tied!")
    
    def run_game(self) -> None:
        """Main game loop."""
        self.display_welcome()
        
        while True:
            print("\n" + "=" * 30)
            print("GAME MODES:")
            print("1. Single Player (vs Computer)")
            print("2. Multiplayer (2 Players)")
            print("3. Best of 3 Series")
            print("4. Best of 5 Series")
            print("5. View Statistics")
            print("6. Quit")
            print("=" * 30)
            
            try:
                choice = input("Select game mode (1-6): ").strip()
                
                if choice == '1':
                    # Single player mode
                    print("\n🎮 Single Player Mode")
                    while self.play_single_round():
                        pass
                
                elif choice == '2':
                    # Multiplayer mode
                    print("\n👥 Multiplayer Mode")
                    player1 = input("Enter Player 1 name: ").strip() or "Player 1"
                    player2 = input("Enter Player 2 name: ").strip() or "Player 2"
                    
                    while self.play_multiplayer_round(player1, player2):
                        pass
                
                elif choice == '3':
                    # Best of 3
                    self.play_best_of_series(3)
                
                elif choice == '4':
                    # Best of 5
                    self.play_best_of_series(5)
                
                elif choice == '5':
                    # View statistics
                    self.display_stats()
                
                elif choice == '6':
                    # Quit
                    break
                
                else:
                    print("❌ Invalid choice! Please enter 1-6.")
                    
            except (EOFError, KeyboardInterrupt):
                break
        
        # Final statistics
        if self.stats['total_games'] > 0:
            print("\n" + "=" * 40)
            print("🏁 FINAL GAME SUMMARY")
            print("=" * 40)
            self.display_stats()
        
        print("\n👋 Thanks for playing Rock Paper Scissors!")


def main():
    """Main function to run the game."""
    try:
        game = RockPaperScissorsGame()
        game.run_game()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


# Simple unit tests (can be run by uncommenting)
def run_tests():
    """Basic unit tests for the game logic."""
    print("Running basic tests...")
    
    game = RockPaperScissorsGame()
    
    # Test winner determination
    assert game.determine_winner('rock', 'scissors') == 'player'
    assert game.determine_winner('scissors', 'paper') == 'player'
    assert game.determine_winner('paper', 'rock') == 'player'
    assert game.determine_winner('rock', 'paper') == 'computer'
    assert game.determine_winner('rock', 'rock') == 'tie'
    
    # Test stats update
    game.update_stats('player')
    assert game.stats['player_wins'] == 1
    assert game.stats['total_games'] == 1
    
    game.update_stats('tie')
    assert game.stats['ties'] == 1
    assert game.stats['total_games'] == 2
    
    print("✅ All tests passed!")


if __name__ == "__main__":
    # Uncomment the line below to run tests
    # run_tests()
    
    main()