#!/usr/bin/env python3
"""
FIND OUT, FIBONACCI - Interactive Fibonacci Sequence Generator
Author: Claude AI Assistant
Version: 1.0.0
Python Version: 3.8+

A comprehensive Fibonacci sequence generator with multiple modes and features.
"""

import sys
import time
import json
from typing import List, Generator, Tuple, Optional
from functools import lru_cache


class FibonacciGenerator:
    """A comprehensive Fibonacci sequence generator with multiple algorithms and features."""
    
    def __init__(self):
        self.cache = {}
        self.golden_ratio = (1 + 5**0.5) / 2
    
    def iterative(self, n: int) -> int:
        """Generate nth Fibonacci number using iterative approach (most efficient for large n)."""
        if n < 0:
            raise ValueError("Fibonacci sequence is not defined for negative numbers")
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    @lru_cache(maxsize=None)
    def recursive_cached(self, n: int) -> int:
        """Generate nth Fibonacci number using memoized recursion."""
        if n < 0:
            raise ValueError("Fibonacci sequence is not defined for negative numbers")
        if n <= 1:
            return n
        return self.recursive_cached(n - 1) + self.recursive_cached(n - 2)
    
    def binet_formula(self, n: int) -> int:
        """Generate nth Fibonacci number using Binet's formula (approximate for large n)."""
        if n < 0:
            raise ValueError("Fibonacci sequence is not defined for negative numbers")
        
        phi = self.golden_ratio
        psi = (1 - 5**0.5) / 2
        
        result = (phi**n - psi**n) / (5**0.5)
        return round(result)
    
    def matrix_power(self, n: int) -> int:
        """Generate nth Fibonacci number using matrix exponentiation (O(log n))."""
        if n < 0:
            raise ValueError("Fibonacci sequence is not defined for negative numbers")
        if n <= 1:
            return n
        
        def matrix_multiply(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
            return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                    [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
        
        def matrix_power_helper(matrix: List[List[int]], power: int) -> List[List[int]]:
            if power == 1:
                return matrix
            if power % 2 == 0:
                half = matrix_power_helper(matrix, power // 2)
                return matrix_multiply(half, half)
            else:
                return matrix_multiply(matrix, matrix_power_helper(matrix, power - 1))
        
        base_matrix = [[1, 1], [1, 0]]
        result_matrix = matrix_power_helper(base_matrix, n)
        return result_matrix[0][1]
    
    def sequence_generator(self, count: int) -> Generator[int, None, None]:
        """Generator that yields Fibonacci numbers up to count."""
        a, b = 0, 1
        for _ in range(count):
            yield a
            a, b = b, a + b
    
    def sequence_up_to_value(self, max_value: int) -> List[int]:
        """Generate Fibonacci sequence up to a maximum value."""
        sequence = []
        a, b = 0, 1
        while a <= max_value:
            sequence.append(a)
            a, b = b, a + b
        return sequence
    
    def is_fibonacci(self, num: int) -> bool:
        """Check if a number is a Fibonacci number using perfect square test."""
        if num < 0:
            return False
        
        # A number is Fibonacci if one of (5*n^2 + 4) or (5*n^2 - 4) is a perfect square
        def is_perfect_square(x: int) -> bool:
            root = int(x**0.5)
            return root * root == x
        
        return is_perfect_square(5 * num * num + 4) or is_perfect_square(5 * num * num - 4)
    
    def find_position(self, num: int) -> Optional[int]:
        """Find the position of a Fibonacci number in the sequence."""
        if not self.is_fibonacci(num):
            return None
        
        if num == 0:
            return 0
        if num == 1:
            return 1
        
        a, b, pos = 0, 1, 1
        while b < num:
            a, b = b, a + b
            pos += 1
        
        return pos if b == num else None


class FibonacciAnalyzer:
    """Analyzer for Fibonacci sequence properties and statistics."""
    
    @staticmethod
    def analyze_sequence(sequence: List[int]) -> dict:
        """Analyze properties of a Fibonacci sequence."""
        if not sequence:
            return {}
        
        analysis = {
            'count': len(sequence),
            'sum': sum(sequence),
            'max_value': max(sequence),
            'min_value': min(sequence),
            'even_count': sum(1 for x in sequence if x % 2 == 0),
            'odd_count': sum(1 for x in sequence if x % 2 == 1),
        }
        
        if len(sequence) > 1:
            analysis['average'] = analysis['sum'] / len(sequence)
            analysis['ratios'] = []
            for i in range(1, min(len(sequence), 11)):  # Show first 10 ratios
                if sequence[i-1] != 0:
                    ratio = sequence[i] / sequence[i-1]
                    analysis['ratios'].append(round(ratio, 6))
        
        return analysis
    
    @staticmethod
    def golden_ratio_approximation(n: int, fib_gen: FibonacciGenerator) -> float:
        """Calculate golden ratio approximation using F(n)/F(n-1)."""
        if n < 2:
            return 0.0
        
        fn = fib_gen.iterative(n)
        fn_1 = fib_gen.iterative(n - 1)
        
        return fn / fn_1 if fn_1 != 0 else 0.0


class FibonacciApp:
    """Main application class for the Fibonacci generator."""
    
    def __init__(self):
        self.generator = FibonacciGenerator()
        self.analyzer = FibonacciAnalyzer()
        self.history = []
    
    def display_banner(self):
        """Display application banner."""
        print("=" * 60)
        print("🌟 FIND OUT, FIBONACCI - Interactive Generator 🌟")
        print("=" * 60)
        print("Explore the fascinating world of Fibonacci numbers!")
        print()
    
    def display_menu(self):
        """Display main menu options."""
        menu_options = [
            "1. Generate nth Fibonacci number",
            "2. Generate Fibonacci sequence (first n numbers)",
            "3. Generate sequence up to a value",
            "4. Check if a number is Fibonacci",
            "5. Find position of Fibonacci number",
            "6. Analyze sequence properties",
            "7. Golden ratio approximation",
            "8. Performance comparison",
            "9. Save/Load results",
            "10. View history",
            "0. Exit"
        ]
        
        print("\n📋 Choose an option:")
        for option in menu_options:
            print(f"   {option}")
        print()
    
    def get_user_input(self, prompt: str, input_type: type = int, min_val: int = None, max_val: int = None):
        """Get validated user input."""
        while True:
            try:
                value = input(prompt).strip()
                if not value:
                    continue
                
                if input_type == int:
                    result = int(value)
                    if min_val is not None and result < min_val:
                        print(f"❌ Value must be at least {min_val}")
                        continue
                    if max_val is not None and result > max_val:
                        print(f"❌ Value must be at most {max_val}")
                        continue
                    return result
                else:
                    return input_type(value)
                    
            except ValueError:
                print(f"❌ Please enter a valid {input_type.__name__}")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)
    
    def generate_nth_fibonacci(self):
        """Generate nth Fibonacci number with algorithm choice."""
        print("\n🔢 Generate nth Fibonacci Number")
        print("-" * 40)
        
        n = self.get_user_input("Enter n (position): ", int, 0, 1000)
        
        print("\nChoose algorithm:")
        print("1. Iterative (recommended)")
        print("2. Recursive with memoization")
        print("3. Binet's formula")
        print("4. Matrix exponentiation")
        
        choice = self.get_user_input("Algorithm choice (1-4): ", int, 1, 4)
        
        algorithms = {
            1: ("Iterative", self.generator.iterative),
            2: ("Recursive (memoized)", self.generator.recursive_cached),
            3: ("Binet's formula", self.generator.binet_formula),
            4: ("Matrix exponentiation", self.generator.matrix_power)
        }
        
        name, method = algorithms[choice]
        
        try:
            start_time = time.time()
            result = method(n)
            end_time = time.time()
            
            print(f"\n✅ F({n}) = {result:,}")
            print(f"🕐 Algorithm: {name}")
            print(f"⏱️  Time taken: {(end_time - start_time)*1000:.3f} ms")
            
            self.history.append(f"F({n}) = {result:,} ({name})")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def generate_sequence(self):
        """Generate Fibonacci sequence."""
        print("\n📊 Generate Fibonacci Sequence")
        print("-" * 40)
        
        count = self.get_user_input("How many numbers? ", int, 1, 100)
        
        try:
            sequence = list(self.generator.sequence_generator(count))
            
            print(f"\n✅ First {count} Fibonacci numbers:")
            
            # Display in rows of 10
            for i in range(0, len(sequence), 10):
                row = sequence[i:i+10]
                formatted_row = [f"{num:,}" for num in row]
                print("  " + " ".join(f"{num:>12}" for num in formatted_row))
            
            # Show analysis
            analysis = self.analyzer.analyze_sequence(sequence)
            print(f"\n📈 Quick Analysis:")
            print(f"   Sum: {analysis['sum']:,}")
            print(f"   Max: {analysis['max_value']:,}")
            print(f"   Even numbers: {analysis['even_count']}")
            print(f"   Odd numbers: {analysis['odd_count']}")
            
            self.history.append(f"Generated sequence of {count} numbers")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def generate_up_to_value(self):
        """Generate sequence up to a maximum value."""
        print("\n🎯 Generate Sequence Up to Value")
        print("-" * 40)
        
        max_val = self.get_user_input("Maximum value: ", int, 0)
        
        try:
            sequence = self.generator.sequence_up_to_value(max_val)
            
            print(f"\n✅ Fibonacci numbers up to {max_val:,}:")
            
            # Display in rows of 10
            for i in range(0, len(sequence), 10):
                row = sequence[i:i+10]
                formatted_row = [f"{num:,}" for num in row]
                print("  " + " ".join(f"{num:>12}" for num in formatted_row))
            
            print(f"\n📊 Found {len(sequence)} Fibonacci numbers ≤ {max_val:,}")
            
            self.history.append(f"Generated sequence up to {max_val:,}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def check_fibonacci(self):
        """Check if a number is Fibonacci."""
        print("\n🔍 Check if Number is Fibonacci")
        print("-" * 40)
        
        num = self.get_user_input("Enter number to check: ", int, 0)
        
        try:
            is_fib = self.generator.is_fibonacci(num)
            
            if is_fib:
                position = self.generator.find_position(num)
                print(f"✅ {num:,} IS a Fibonacci number!")
                print(f"🎯 Position in sequence: F({position}) = {num:,}")
            else:
                print(f"❌ {num:,} is NOT a Fibonacci number")
            
            self.history.append(f"Checked {num:,}: {'Fibonacci' if is_fib else 'Not Fibonacci'}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def find_position(self):
        """Find position of a Fibonacci number."""
        print("\n📍 Find Position of Fibonacci Number")
        print("-" * 40)
        
        num = self.get_user_input("Enter Fibonacci number: ", int, 0)
        
        try:
            position = self.generator.find_position(num)
            
            if position is not None:
                print(f"✅ F({position}) = {num:,}")
                print(f"🎯 Position: {position}")
            else:
                print(f"❌ {num:,} is not a Fibonacci number")
            
            self.history.append(f"Found position of {num:,}: {position}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def analyze_sequence_interactive(self):
        """Interactive sequence analysis."""
        print("\n📊 Analyze Fibonacci Sequence")
        print("-" * 40)
        
        count = self.get_user_input("Number of terms to analyze: ", int, 2, 50)
        
        try:
            sequence = list(self.generator.sequence_generator(count))
            analysis = self.analyzer.analyze_sequence(sequence)
            
            print(f"\n✅ Analysis of first {count} Fibonacci numbers:")
            print("-" * 50)
            print(f"Count: {analysis['count']}")
            print(f"Sum: {analysis['sum']:,}")
            print(f"Maximum: {analysis['max_value']:,}")
            print(f"Average: {analysis.get('average', 0):.2f}")
            print(f"Even numbers: {analysis['even_count']}")
            print(f"Odd numbers: {analysis['odd_count']}")
            
            if 'ratios' in analysis and analysis['ratios']:
                print(f"\n🔢 Consecutive ratios (approaching golden ratio φ ≈ 1.618):")
                for i, ratio in enumerate(analysis['ratios'], 2):
                    print(f"   F({i})/F({i-1}) = {ratio}")
            
            self.history.append(f"Analyzed sequence of {count} numbers")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def golden_ratio_demo(self):
        """Demonstrate golden ratio approximation."""
        print("\n🌟 Golden Ratio Approximation")
        print("-" * 40)
        
        n = self.get_user_input("Calculate ratio for F(n)/F(n-1), enter n: ", int, 2, 50)
        
        try:
            ratio = self.analyzer.golden_ratio_approximation(n, self.generator)
            golden_ratio = (1 + 5**0.5) / 2
            error = abs(ratio - golden_ratio)
            
            print(f"\n✅ F({n})/F({n-1}) = {ratio:.10f}")
            print(f"🌟 Golden ratio φ = {golden_ratio:.10f}")
            print(f"📏 Error: {error:.10f}")
            print(f"🎯 Accuracy: {((1 - error/golden_ratio) * 100):.6f}%")
            
            self.history.append(f"Golden ratio approximation: {ratio:.6f}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def performance_comparison(self):
        """Compare performance of different algorithms."""
        print("\n⚡ Performance Comparison")
        print("-" * 40)
        
        n = self.get_user_input("Enter n for performance test: ", int, 10, 35)
        
        algorithms = [
            ("Iterative", self.generator.iterative),
            ("Recursive (memoized)", self.generator.recursive_cached),
            ("Matrix exponentiation", self.generator.matrix_power),
        ]
        
        print(f"\n🏁 Computing F({n}) with different algorithms:")
        print("-" * 50)
        
        results = []
        for name, method in algorithms:
            try:
                start_time = time.time()
                result = method(n)
                end_time = time.time()
                
                time_ms = (end_time - start_time) * 1000
                results.append((name, time_ms, result))
                print(f"{name:<25}: {time_ms:>8.3f} ms")
                
            except Exception as e:
                print(f"{name:<25}: ERROR - {e}")
        
        if results:
            fastest = min(results, key=lambda x: x[1])
            print(f"\n🏆 Fastest: {fastest[0]} ({fastest[1]:.3f} ms)")
            print(f"✅ Result: F({n}) = {fastest[2]:,}")
        
        self.history.append(f"Performance comparison for F({n})")
    
    def save_results(self):
        """Save results to file."""
        print("\n💾 Save Results")
        print("-" * 40)
        
        if not self.history:
            print("❌ No history to save!")
            return
        
        filename = input("Enter filename (or press Enter for 'fibonacci_results.json'): ").strip()
        if not filename:
            filename = "fibonacci_results.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            data = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'history': self.history
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Results saved to {filename}")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    
    def load_results(self):
        """Load results from file."""
        print("\n📂 Load Results")
        print("-" * 40)
        
        filename = input("Enter filename: ").strip()
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            print(f"✅ Loaded results from {data.get('timestamp', 'unknown time')}")
            print(f"📊 Found {len(data.get('history', []))} history entries")
            
            choice = input("Add to current history? (y/n): ").strip().lower()
            if choice == 'y':
                self.history.extend(data.get('history', []))
                print("✅ History merged!")
            
        except FileNotFoundError:
            print(f"❌ File '{filename}' not found")
        except Exception as e:
            print(f"❌ Error loading file: {e}")
    
    def view_history(self):
        """View calculation history."""
        print("\n📜 Calculation History")
        print("-" * 40)
        
        if not self.history:
            print("📭 No history available")
            return
        
        print(f"📊 {len(self.history)} entries found:")
        print()
        
        for i, entry in enumerate(self.history[-20:], 1):  # Show last 20 entries
            print(f"{i:2d}. {entry}")
        
        if len(self.history) > 20:
            print(f"\n... and {len(self.history) - 20} more entries")
    
    def run(self):
        """Main application loop."""
        self.display_banner()
        
        while True:
            self.display_menu()
            
            try:
                choice = self.get_user_input("Enter your choice (0-10): ", int, 0, 10)
                
                if choice == 0:
                    print("\n👋 Thank you for exploring Fibonacci numbers!")
                    print("🌟 Keep discovering the beauty of mathematics!")
                    break
                elif choice == 1:
                    self.generate_nth_fibonacci()
                elif choice == 2:
                    self.generate_sequence()
                elif choice == 3:
                    self.generate_up_to_value()
                elif choice == 4:
                    self.check_fibonacci()
                elif choice == 5:
                    self.find_position()
                elif choice == 6:
                    self.analyze_sequence_interactive()
                elif choice == 7:
                    self.golden_ratio_demo()
                elif choice == 8:
                    self.performance_comparison()
                elif choice == 9:
                    save_or_load = input("\nSave (s) or Load (l)? ").strip().lower()
                    if save_or_load == 's':
                        self.save_results()
                    elif save_or_load == 'l':
                        self.load_results()
                    else:
                        print("❌ Invalid choice")
                elif choice == 10:
                    self.view_history()
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")


def run_tests():
    """Simple unit tests for the Fibonacci generator."""
    print("🧪 Running Unit Tests...")
    print("-" * 30)
    
    fib = FibonacciGenerator()
    
    # Test cases: (input, expected_output)
    test_cases = [
        (0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5),
        (6, 8), (7, 13), (8, 21), (9, 34), (10, 55)
    ]
    
    algorithms = [
        ("Iterative", fib.iterative),
        ("Recursive", fib.recursive_cached),
        ("Matrix", fib.matrix_power),
        ("Binet", fib.binet_formula)
    ]
    
    for name, method in algorithms:
        print(f"\nTesting {name} algorithm:")
        passed = 0
        for n, expected in test_cases:
            try:
                result = method(n)
                if result == expected:
                    print(f"  ✅ F({n}) = {result}")
                    passed += 1
                else:
                    print(f"  ❌ F({n}) = {result}, expected {expected}")
            except Exception as e:
                print(f"  ❌ F({n}) failed: {e}")
        
        print(f"  📊 Passed: {passed}/{len(test_cases)} tests")
    
    # Test Fibonacci checking
    print(f"\nTesting Fibonacci number detection:")
    fib_numbers = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    non_fib_numbers = [4, 6, 7, 9, 10, 11, 12, 14, 15, 16]
    
    correct = 0
    total = 0
    
    for num in fib_numbers:
        is_fib = fib.is_fibonacci(num)
        if is_fib:
            correct += 1
        print(f"  {'✅' if is_fib else '❌'} {num} is Fibonacci: {is_fib}")
        total += 1
    
    for num in non_fib_numbers:
        is_fib = fib.is_fibonacci(num)
        if not is_fib:
            correct += 1
        print(f"  {'✅' if not is_fib else '❌'} {num} is Fibonacci: {is_fib}")
        total += 1
    
    print(f"  📊 Fibonacci detection accuracy: {correct}/{total}")
    print("\n🎉 Unit tests completed!")


if __name__ == "__main__":
    print("🚀 FIND OUT, FIBONACCI - Starting Application")
    
    # Check if user wants to run tests
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
        print("\n" + "="*50)
    
    # Run main application
    app = FibonacciApp()
    app.run()
