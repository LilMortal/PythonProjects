#!/usr/bin/env python3
"""
Tic Tac Toe Game
A complete command-line implementation of the classic Tic Tac Toe game.
Supports both Player vs Player and Player vs AI modes.
"""

import random
import sys
from typing import List, Tuple, Optional


class TicTacToe:
    """
    A complete Tic Tac Toe game implementation with multiple game modes.
    """
    
    def __init__(self):
        """Initialize the game with an empty 3x3 board."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_mode = None
        self.game_stats = {'X': 0, 'O': 0, 'draws': 0}
    
    def display_board(self) -> None:
        """Display the current state of the game board."""
        print("\n   0   1   2")
        for i in range(3):
            print(f"{i}  {self.board[i][0]} | {self.board[i][1]} | {self.board[i][2]}")
            if i < 2:
                print("  -----------")
        print()
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move is valid.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            
        Returns:
            bool: True if move is valid, False otherwise
        """
        return (0 <= row <= 2 and 0 <= col <= 2 and 
                self.board[row][col] == ' ')
    
    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Make a move on the board.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            player (str): Player symbol ('X' or 'O')
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self) -> Optional[str]:
        """
        Check if there's a winner or if the game is a draw.
        
        Returns:
            str: 'X' or 'O' if there's a winner, 'draw' if it's a draw, None if game continues
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        # Check for draw
        if all(self.board[row][col] != ' ' for row in range(3) for col in range(3)):
            return 'draw'
        
        return None
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get all empty cells on the board.
        
        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples for empty cells
        """
        return [(row, col) for row in range(3) for col in range(3) 
                if self.board[row][col] == ' ']
    
    def minimax(self, depth: int, is_maximizing: bool, alpha: float = float('-inf'), 
                beta: float = float('inf')) -> int:
        """
        Minimax algorithm with alpha-beta pruning for AI decision making.
        
        Args:
            depth (int): Current depth in the game tree
            is_maximizing (bool): True if maximizing player's turn
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            
        Returns:
            int: Score of the position
        """
        winner = self.check_winner()
        
        if winner == 'O':  # AI wins
            return 10 - depth
        elif winner == 'X':  # Human wins
            return depth - 10
        elif winner == 'draw':
            return 0
        
        if is_maximizing:
            max_score = float('-inf')
            for row, col in self.get_empty_cells():
                self.board[row][col] = 'O'
                score = self.minimax(depth + 1, False, alpha, beta)
                self.board[row][col] = ' '
                max_score = max(score, max_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for row, col in self.get_empty_cells():
                self.board[row][col] = 'X'
                score = self.minimax(depth + 1, True, alpha, beta)
                self.board[row][col] = ' '
                min_score = min(score, min_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score
    
    def get_ai_move(self, difficulty: str = 'hard') -> Tuple[int, int]:
        """
        Get AI move based on difficulty level.
        
        Args:
            difficulty (str): 'easy', 'medium', or 'hard'
            
        Returns:
            Tuple[int, int]: (row, col) for AI's move
        """
        empty_cells = self.get_empty_cells()
        
        if difficulty == 'easy':
            return random.choice(empty_cells)
        elif difficulty == 'medium':
            # 70% chance of optimal move, 30% random
            if random.random() < 0.7:
                return self._get_best_move()
            else:
                return random.choice(empty_cells)
        else:  # hard
            return self._get_best_move()
    
    def _get_best_move(self) -> Tuple[int, int]:
        """Get the best move using minimax algorithm."""
        best_score = float('-inf')
        best_move = None
        
        for row, col in self.get_empty_cells():
            self.board[row][col] = 'O'
            score = self.minimax(0, False)
            self.board[row][col] = ' '
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move if best_move else random.choice(self.get_empty_cells())
    
    def get_player_move(self) -> Tuple[int, int]:
        """
        Get a valid move from the human player.
        
        Returns:
            Tuple[int, int]: (row, col) for player's move
        """
        while True:
            try:
                move_input = input(f"Player {self.current_player}, enter your move (row,col) or 'q' to quit: ").strip()
                
                if move_input.lower() == 'q':
                    print("Thanks for playing!")
                    sys.exit(0)
                
                # Parse input - accept formats like "1,2", "1 2", or "12"
                if ',' in move_input:
                    row, col = map(int, move_input.split(','))
                elif ' ' in move_input:
                    row, col = map(int, move_input.split())
                elif len(move_input) == 2 and move_input.isdigit():
                    row, col = int(move_input[0]), int(move_input[1])
                else:
                    raise ValueError("Invalid format")
                
                if self.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move! That position is already taken or out of bounds.")
                    
            except (ValueError, IndexError):
                print("Invalid input! Please enter row,col (e.g., '1,2') or 'q' to quit.")
    
    def reset_board(self) -> None:
        """Reset the board for a new game."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
    
    def display_stats(self) -> None:
        """Display current game statistics."""
        print(f"\n📊 Game Statistics:")
        print(f"Player X wins: {self.game_stats['X']}")
        print(f"Player O wins: {self.game_stats['O']}")
        print(f"Draws: {self.game_stats['draws']}")
        total_games = sum(self.game_stats.values())
        if total_games > 0:
            print(f"Total games played: {total_games}")
    
    def play_game(self) -> None:
        """Main game logic for a single game."""
        self.display_board()
        
        while True:
            winner = self.check_winner()
            if winner:
                if winner == 'draw':
                    print("🤝 It's a draw!")
                    self.game_stats['draws'] += 1
                else:
                    print(f"🎉 Player {winner} wins!")
                    self.game_stats[winner] += 1
                break
            
            # Handle player moves based on game mode
            if self.game_mode == 'pvp' or self.current_player == 'X':
                row, col = self.get_player_move()
            else:  # AI move
                print("AI is thinking...")
                row, col = self.get_ai_move('hard')
                print(f"AI plays: {row},{col}")
            
            if self.make_move(row, col, self.current_player):
                self.display_board()
                self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def main_menu(self) -> None:
        """Display main menu and handle user choices."""
        while True:
            print("\n🎮 TIC TAC TOE GAME")
            print("=" * 20)
            print("1. Player vs Player")
            print("2. Player vs AI")
            print("3. View Statistics")
            print("4. How to Play")
            print("5. Quit")
            
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == '1':
                self.game_mode = 'pvp'
                self.play_round()
            elif choice == '2':
                self.game_mode = 'pve'
                self.play_round()
            elif choice == '3':
                self.display_stats()
            elif choice == '4':
                self.show_instructions()
            elif choice == '5':
                print("Thanks for playing! 👋")
                break
            else:
                print("Invalid choice! Please select 1-5.")
    
    def play_round(self) -> None:
        """Play a round of games with option to continue."""
        while True:
            self.reset_board()
            print(f"\n🎯 Starting new game - {self.game_mode.upper()} mode")
            self.play_game()
            
            while True:
                play_again = input("\nPlay again? (y/n): ").strip().lower()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
    
    def show_instructions(self) -> None:
        """Display game instructions."""
        print("\n📖 HOW TO PLAY TIC TAC TOE")
        print("=" * 30)
        print("• The game is played on a 3x3 grid")
        print("• Players take turns placing X's and O's")
        print("• First player to get 3 in a row (horizontally, vertically, or diagonally) wins")
        print("• If all 9 squares are filled and no one wins, it's a draw")
        print("\n💡 INPUT FORMAT:")
        print("• Enter your move as row,col (e.g., '1,2')")
        print("• Rows and columns are numbered 0-2")
        print("• You can also use space separation (e.g., '1 2')")
        print("• Type 'q' during gameplay to quit")


def run_tests() -> None:
    """Simple unit tests for the TicTacToe class."""
    print("🧪 Running tests...")
    
    # Test 1: Board initialization
    game = TicTacToe()
    assert all(game.board[i][j] == ' ' for i in range(3) for j in range(3)), "Board should be empty"
    print("✅ Test 1 passed: Board initialization")
    
    # Test 2: Valid move
    assert game.is_valid_move(0, 0) == True, "Empty cell should be valid"
    assert game.make_move(0, 0, 'X') == True, "Should be able to make move"
    assert game.board[0][0] == 'X', "Move should be recorded"
    print("✅ Test 2 passed: Valid move")
    
    # Test 3: Invalid move
    assert game.is_valid_move(0, 0) == False, "Occupied cell should be invalid"
    assert game.make_move(0, 0, 'O') == False, "Should not be able to make move on occupied cell"
    print("✅ Test 3 passed: Invalid move")
    
    # Test 4: Win detection
    game.board = [['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
    assert game.check_winner() == 'X', "Should detect horizontal win"
    print("✅ Test 4 passed: Win detection")
    
    # Test 5: Draw detection
    game.board = [['X', 'O', 'X'], ['O', 'O', 'X'], ['O', 'X', 'O']]
    assert game.check_winner() == 'draw', "Should detect draw"
    print("✅ Test 5 passed: Draw detection")
    
    print("🎉 All tests passed!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
    else:
        game = TicTacToe()
        try:
            game.main_menu()
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing! 👋")
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please report this issue if it persists.")
