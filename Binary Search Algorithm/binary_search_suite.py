#!/usr/bin/env python3
"""
Binary Search Algorithm Suite
A comprehensive implementation of binary search with multiple practical applications.

Author: AI Assistant
Python Version: 3.10+
"""

import random
import time
from typing import List, Optional, Union, Tuple


class BinarySearchSuite:
    """
    A comprehensive binary search implementation with multiple applications.
    Includes standard search, range finding, and practical use cases.
    """
    
    def __init__(self):
        self.comparisons = 0  # Track number of comparisons for analysis
    
    def reset_comparisons(self):
        """Reset the comparison counter."""
        self.comparisons = 0
    
    def binary_search_basic(self, arr: List[int], target: int) -> int:
        """
        Basic binary search implementation.
        
        Args:
            arr: Sorted list of integers
            target: Value to search for
            
        Returns:
            Index of target if found, -1 otherwise
        """
        self.reset_comparisons()
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            self.comparisons += 1
            
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1
    
    def binary_search_recursive(self, arr: List[int], target: int, left: int = 0, right: int = None) -> int:
        """
        Recursive binary search implementation.
        
        Args:
            arr: Sorted list of integers
            target: Value to search for
            left: Left boundary (default: 0)
            right: Right boundary (default: len(arr) - 1)
            
        Returns:
            Index of target if found, -1 otherwise
        """
        if right is None:
            right = len(arr) - 1
            self.reset_comparisons()
        
        if left > right:
            return -1
        
        mid = (left + right) // 2
        self.comparisons += 1
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return self.binary_search_recursive(arr, target, mid + 1, right)
        else:
            return self.binary_search_recursive(arr, target, left, mid - 1)
    
    def find_first_occurrence(self, arr: List[int], target: int) -> int:
        """
        Find the first occurrence of target in a sorted array with duplicates.
        
        Args:
            arr: Sorted list of integers (may contain duplicates)
            target: Value to search for
            
        Returns:
            Index of first occurrence, -1 if not found
        """
        self.reset_comparisons()
        left, right = 0, len(arr) - 1
        result = -1
        
        while left <= right:
            mid = (left + right) // 2
            self.comparisons += 1
            
            if arr[mid] == target:
                result = mid
                right = mid - 1  # Continue searching left for first occurrence
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    def find_last_occurrence(self, arr: List[int], target: int) -> int:
        """
        Find the last occurrence of target in a sorted array with duplicates.
        
        Args:
            arr: Sorted list of integers (may contain duplicates)
            target: Value to search for
            
        Returns:
            Index of last occurrence, -1 if not found
        """
        self.reset_comparisons()
        left, right = 0, len(arr) - 1
        result = -1
        
        while left <= right:
            mid = (left + right) // 2
            self.comparisons += 1
            
            if arr[mid] == target:
                result = mid
                left = mid + 1  # Continue searching right for last occurrence
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    def search_range(self, arr: List[int], target: int) -> Tuple[int, int]:
        """
        Find the range (first and last occurrence) of target.
        
        Args:
            arr: Sorted list of integers
            target: Value to search for
            
        Returns:
            Tuple of (first_index, last_index) or (-1, -1) if not found
        """
        first = self.find_first_occurrence(arr, target)
        if first == -1:
            return (-1, -1)
        
        last = self.find_last_occurrence(arr, target)
        return (first, last)
    
    def search_insert_position(self, arr: List[int], target: int) -> int:
        """
        Find the position where target should be inserted to maintain sorted order.
        
        Args:
            arr: Sorted list of integers
            target: Value to find insertion position for
            
        Returns:
            Index where target should be inserted
        """
        self.reset_comparisons()
        left, right = 0, len(arr)
        
        while left < right:
            mid = (left + right) // 2
            self.comparisons += 1
            
            if arr[mid] < target:
                left = mid + 1
            else:
                right = mid
        
        return left
    
    def search_in_rotated_array(self, arr: List[int], target: int) -> int:
        """
        Search in a rotated sorted array.
        
        Args:
            arr: Rotated sorted array
            target: Value to search for
            
        Returns:
            Index of target if found, -1 otherwise
        """
        self.reset_comparisons()
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            self.comparisons += 1
            
            if arr[mid] == target:
                return mid
            
            # Check which half is sorted
            if arr[left] <= arr[mid]:  # Left half is sorted
                if arr[left] <= target < arr[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:  # Right half is sorted
                if arr[mid] < target <= arr[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return -1


class NumberGuessingGame:
    """A number guessing game that demonstrates binary search optimization."""
    
    def __init__(self, min_num: int = 1, max_num: int = 100):
        self.min_num = min_num
        self.max_num = max_num
        self.secret_number = random.randint(min_num, max_num)
        self.attempts = 0
        self.max_attempts = self._calculate_max_attempts()
    
    def _calculate_max_attempts(self) -> int:
        """Calculate theoretical maximum attempts needed using binary search."""
        import math
        return math.ceil(math.log2(self.max_num - self.min_num + 1))
    
    def make_guess(self, guess: int) -> str:
        """
        Make a guess and get feedback.
        
        Args:
            guess: The guessed number
            
        Returns:
            Feedback string
        """
        self.attempts += 1
        
        if guess == self.secret_number:
            return "correct"
        elif guess < self.secret_number:
            return "higher"
        else:
            return "lower"
    
    def get_optimal_guess(self, low: int, high: int) -> int:
        """Get the optimal next guess using binary search strategy."""
        return (low + high) // 2
    
    def reset_game(self):
        """Reset the game with a new secret number."""
        self.secret_number = random.randint(self.min_num, self.max_num)
        self.attempts = 0


def generate_test_data(size: int, max_value: int = 1000, allow_duplicates: bool = False) -> List[int]:
    """
    Generate test data for binary search demonstrations.
    
    Args:
        size: Number of elements
        max_value: Maximum value in the array
        allow_duplicates: Whether to allow duplicate values
        
    Returns:
        Sorted list of integers
    """
    if allow_duplicates:
        data = [random.randint(1, max_value // 2) for _ in range(size)]
    else:
        data = random.sample(range(1, max_value + 1), min(size, max_value))
    
    return sorted(data)


def demonstrate_performance():
    """Demonstrate the performance advantage of binary search over linear search."""
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON: Binary Search vs Linear Search")
    print("="*60)
    
    sizes = [1000, 10000, 100000]
    bs = BinarySearchSuite()
    
    for size in sizes:
        print(f"\nArray size: {size:,} elements")
        test_array = list(range(size))
        target = random.randint(0, size - 1)
        
        # Binary search timing
        start_time = time.time()
        bs_result = bs.binary_search_basic(test_array, target)
        bs_time = time.time() - start_time
        bs_comparisons = bs.comparisons
        
        # Linear search timing
        start_time = time.time()
        ls_result = -1
        ls_comparisons = 0
        for i, val in enumerate(test_array):
            ls_comparisons += 1
            if val == target:
                ls_result = i
                break
        ls_time = time.time() - start_time
        
        print(f"  Target: {target}")
        print(f"  Binary Search: {bs_time:.6f}s, {bs_comparisons} comparisons")
        print(f"  Linear Search: {ls_time:.6f}s, {ls_comparisons} comparisons")
        print(f"  Speed improvement: {ls_time/bs_time:.1f}x faster")
        print(f"  Comparison reduction: {ls_comparisons/bs_comparisons:.1f}x fewer")


def interactive_search_demo():
    """Interactive demonstration of various binary search algorithms."""
    bs = BinarySearchSuite()
    
    while True:
        print("\n" + "="*50)
        print("BINARY SEARCH ALGORITHM SUITE")
        print("="*50)
        print("1. Basic Binary Search")
        print("2. Recursive Binary Search")
        print("3. Find First/Last Occurrence")
        print("4. Search Range")
        print("5. Find Insert Position")
        print("6. Search in Rotated Array")
        print("7. Number Guessing Game")
        print("8. Performance Comparison")
        print("9. Generate Custom Test Data")
        print("0. Exit")
        
        try:
            choice = input("\nSelect an option (0-9): ").strip()
            
            if choice == '0':
                print("Thank you for using Binary Search Suite!")
                break
            
            elif choice == '1' or choice == '2':
                print(f"\n--- {'Basic' if choice == '1' else 'Recursive'} Binary Search ---")
                
                # Get array input
                print("Enter a sorted array (space-separated integers):")
                arr_input = input("Array: ").strip()
                if not arr_input:
                    arr = generate_test_data(20)
                    print(f"Using generated array: {arr}")
                else:
                    arr = list(map(int, arr_input.split()))
                
                target = int(input("Enter target value: "))
                
                if choice == '1':
                    result = bs.binary_search_basic(arr, target)
                else:
                    result = bs.binary_search_recursive(arr, target)
                
                if result != -1:
                    print(f"✓ Target {target} found at index {result}")
                else:
                    print(f"✗ Target {target} not found")
                print(f"Comparisons made: {bs.comparisons}")
            
            elif choice == '3':
                print("\n--- Find First/Last Occurrence ---")
                
                # Create array with duplicates
                base_arr = generate_test_data(15, allow_duplicates=True)
                print(f"Array with duplicates: {base_arr}")
                
                target = int(input("Enter target value: "))
                
                first = bs.find_first_occurrence(base_arr, target)
                last = bs.find_last_occurrence(base_arr, target)
                
                if first != -1:
                    print(f"✓ First occurrence at index {first}")
                    print(f"✓ Last occurrence at index {last}")
                    print(f"✓ Total occurrences: {last - first + 1}")
                else:
                    print(f"✗ Target {target} not found")
            
            elif choice == '4':
                print("\n--- Search Range ---")
                
                base_arr = generate_test_data(15, allow_duplicates=True)
                print(f"Array: {base_arr}")
                
                target = int(input("Enter target value: "))
                first, last = bs.search_range(base_arr, target)
                
                if first != -1:
                    print(f"✓ Range: [{first}, {last}]")
                    print(f"✓ Total occurrences: {last - first + 1}")
                else:
                    print(f"✗ Target {target} not found")
            
            elif choice == '5':
                print("\n--- Find Insert Position ---")
                
                arr = generate_test_data(15)
                print(f"Sorted array: {arr}")
                
                target = int(input("Enter value to insert: "))
                position = bs.search_insert_position(arr, target)
                
                print(f"✓ Insert position: {position}")
                arr.insert(position, target)
                print(f"✓ Array after insertion: {arr}")
            
            elif choice == '6':
                print("\n--- Search in Rotated Array ---")
                
                # Create rotated array
                original = list(range(1, 11))
                rotate_point = random.randint(1, 8)
                rotated = original[rotate_point:] + original[:rotate_point]
                
                print(f"Original sorted array: {original}")
                print(f"Rotated array: {rotated}")
                
                target = int(input("Enter target value: "))
                result = bs.search_in_rotated_array(rotated, target)
                
                if result != -1:
                    print(f"✓ Target {target} found at index {result}")
                else:
                    print(f"✗ Target {target} not found")
                print(f"Comparisons made: {bs.comparisons}")
            
            elif choice == '7':
                print("\n--- Number Guessing Game ---")
                print("I'll think of a number between 1 and 100.")
                print("Use binary search strategy for optimal guessing!")
                
                game = NumberGuessingGame()
                low, high = 1, 100
                
                print(f"Maximum attempts needed with binary search: {game.max_attempts}")
                print("Hint: Always guess the middle value of your current range.\n")
                
                while True:
                    optimal_guess = game.get_optimal_guess(low, high)
                    print(f"Optimal next guess: {optimal_guess} (range: {low}-{high})")
                    
                    try:
                        guess = int(input(f"Attempt {game.attempts + 1}: Enter your guess: "))
                        feedback = game.make_guess(guess)
                        
                        if feedback == "correct":
                            print(f"🎉 Congratulations! You found {game.secret_number} in {game.attempts} attempts!")
                            if game.attempts <= game.max_attempts:
                                print("✓ You used optimal or near-optimal strategy!")
                            break
                        elif feedback == "higher":
                            print("📈 Go higher!")
                            low = guess + 1
                        else:
                            print("📉 Go lower!")
                            high = guess - 1
                            
                    except ValueError:
                        print("Please enter a valid number.")
            
            elif choice == '8':
                demonstrate_performance()
            
            elif choice == '9':
                print("\n--- Generate Custom Test Data ---")
                try:
                    size = int(input("Enter array size: "))
                    max_val = int(input("Enter maximum value: "))
                    allow_dup = input("Allow duplicates? (y/n): ").lower().startswith('y')
                    
                    custom_array = generate_test_data(size, max_val, allow_dup)
                    print(f"Generated array: {custom_array}")
                    
                except ValueError:
                    print("Please enter valid numbers.")
            
            else:
                print("Invalid option. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
        
        input("\nPress Enter to continue...")


def main():
    """Main function to run the Binary Search Algorithm Suite."""
    print("🔍 Welcome to the Binary Search Algorithm Suite!")
    print("This program demonstrates various binary search implementations and applications.")
    
    try:
        interactive_search_demo()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please restart the program.")


if __name__ == "__main__":
    main()