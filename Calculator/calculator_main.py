#!/usr/bin/env python3
"""
Advanced Calculator - A comprehensive command-line calculator
Author: Assistant
Python Version: 3.8+
"""

import math
import re
import sys
from typing import Union, List, Tuple


class Calculator:
    """
    A comprehensive calculator class that supports basic arithmetic,
    scientific functions, and expression evaluation.
    """
    
    def __init__(self):
        self.history = []
        self.memory = 0
        
        # Define supported operations
        self.operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            '**': self.power,
            '^': self.power,
            '%': self.modulo,
            '//': self.floor_divide
        }
        
        # Define supported functions
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'log': math.log10,
            'ln': math.log,
            'sqrt': math.sqrt,
            'abs': abs,
            'ceil': math.ceil,
            'floor': math.floor,
            'round': round,
            'factorial': math.factorial
        }
        
        # Constants
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau
        }
    
    def add(self, a: float, b: float) -> float:
        """Addition operation"""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtraction operation"""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiplication operation"""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Division operation with zero-division check"""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
    
    def power(self, a: float, b: float) -> float:
        """Power operation"""
        try:
            return a ** b
        except OverflowError:
            raise ValueError("Result is too large to compute")
    
    def modulo(self, a: float, b: float) -> float:
        """Modulo operation"""
        if b == 0:
            raise ValueError("Modulo by zero is not allowed")
        return a % b
    
    def floor_divide(self, a: float, b: float) -> float:
        """Floor division operation"""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a // b
    
    def evaluate_expression(self, expression: str) -> float:
        """
        Safely evaluate mathematical expressions using eval with restricted globals
        """
        # Replace constants
        for const, value in self.constants.items():
            expression = expression.replace(const, str(value))
        
        # Replace ^ with ** for power operations
        expression = expression.replace('^', '**')
        
        # Create safe namespace for eval
        safe_dict = {
            "__builtins__": {},
            **self.functions,
            **self.constants
        }
        
        try:
            # Validate expression contains only allowed characters
            if not re.match(r'^[0-9+\-*/().^%\s\w]+$', expression):
                raise ValueError("Invalid characters in expression")
            
            result = eval(expression, safe_dict)
            return float(result)
        except (SyntaxError, NameError, TypeError) as e:
            raise ValueError(f"Invalid expression: {str(e)}")
        except ZeroDivisionError:
            raise ValueError("Division by zero is not allowed")
        except OverflowError:
            raise ValueError("Result is too large to compute")
    
    def calculate(self, expression: str) -> Tuple[float, str]:
        """
        Main calculation method that handles various input formats
        Returns tuple of (result, formatted_result_string)
        """
        expression = expression.strip().lower()
        
        # Handle special commands
        if expression in ['quit', 'exit', 'q']:
            return None, "Goodbye!"
        
        if expression in ['help', 'h']:
            return None, self.get_help()
        
        if expression == 'history':
            return None, self.get_history()
        
        if expression == 'clear':
            self.history.clear()
            return None, "History cleared"
        
        if expression.startswith('mem'):
            return self.handle_memory_operations(expression)
        
        try:
            # Evaluate the expression
            result = self.evaluate_expression(expression)
            
            # Store in history
            self.history.append(f"{expression} = {result}")
            
            # Format result
            if result.is_integer():
                formatted_result = f"{int(result)}"
            else:
                formatted_result = f"{result:.10g}"  # Remove trailing zeros
            
            return result, formatted_result
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            return None, error_msg
    
    def handle_memory_operations(self, expression: str) -> Tuple[float, str]:
        """Handle memory operations (store, recall, clear)"""
        parts = expression.split()
        
        if len(parts) == 1 and parts[0] == 'mem':
            return self.memory, f"Memory: {self.memory}"
        
        if len(parts) == 2:
            command, value_str = parts
            
            if command == 'mem+':
                try:
                    value = float(value_str)
                    self.memory += value
                    return self.memory, f"Memory: {self.memory} (added {value})"
                except ValueError:
                    return None, "Invalid number for memory operation"
            
            elif command == 'mem-':
                try:
                    value = float(value_str)
                    self.memory -= value
                    return self.memory, f"Memory: {self.memory} (subtracted {value})"
                except ValueError:
                    return None, "Invalid number for memory operation"
            
            elif command == 'mem=':
                try:
                    value = float(value_str)
                    self.memory = value
                    return self.memory, f"Memory set to: {self.memory}"
                except ValueError:
                    return None, "Invalid number for memory operation"
        
        if expression == 'mem clear':
            self.memory = 0
            return 0, "Memory cleared"
        
        return None, "Invalid memory command. Use: mem, mem+ <value>, mem- <value>, mem= <value>, mem clear"
    
    def get_help(self) -> str:
        """Return help information"""
        help_text = """
=== ADVANCED CALCULATOR HELP ===

Basic Operations:
  +, -, *, /          Basic arithmetic
  ** or ^             Power (e.g., 2^3 or 2**3)
  %                   Modulo
  //                  Floor division

Functions:
  sin(x), cos(x), tan(x)    Trigonometric functions
  asin(x), acos(x), atan(x) Inverse trigonometric functions
  log(x)                    Base-10 logarithm
  ln(x)                     Natural logarithm
  sqrt(x)                   Square root
  abs(x)                    Absolute value
  ceil(x), floor(x)         Ceiling and floor
  round(x)                  Round to nearest integer
  factorial(x)              Factorial

Constants:
  pi                  π (3.14159...)
  e                   Euler's number (2.71828...)
  tau                 2π (6.28318...)

Memory Operations:
  mem                 Show current memory value
  mem= <value>        Store value in memory
  mem+ <value>        Add to memory
  mem- <value>        Subtract from memory
  mem clear           Clear memory

Special Commands:
  history             Show calculation history
  clear               Clear history
  help or h           Show this help
  quit, exit, or q    Exit calculator

Examples:
  2 + 3 * 4
  sqrt(16) + log(100)
  sin(pi/2)
  2^10
  factorial(5)
        """
        return help_text.strip()
    
    def get_history(self) -> str:
        """Return calculation history"""
        if not self.history:
            return "No calculations in history"
        
        history_text = "=== CALCULATION HISTORY ===\n"
        for i, calc in enumerate(self.history[-10:], 1):  # Show last 10
            history_text += f"{i}. {calc}\n"
        
        if len(self.history) > 10:
            history_text += f"... and {len(self.history) - 10} more"
        
        return history_text.strip()


def main():
    """Main function to run the calculator"""
    calc = Calculator()
    
    print("🔢 Advanced Calculator")
    print("Type 'help' for instructions, 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            # Get user input
            user_input = input("calc> ").strip()
            
            if not user_input:
                continue
            
            # Calculate result
            result, output = calc.calculate(user_input)
            
            # Display result
            print(output)
            
            # Check for exit condition
            if result is None and output == "Goodbye!":
                break
                
        except KeyboardInterrupt:
            print("\n\nCalculator interrupted. Goodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


# Simple unit tests (uncomment to run)
def run_tests():
    """Basic unit tests for the calculator"""
    calc = Calculator()
    
    test_cases = [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("3 * 4", 12),
        ("15 / 3", 5),
        ("2 ** 3", 8),
        ("10 % 3", 1),
        ("sqrt(16)", 4),
        ("abs(-5)", 5),
        ("sin(0)", 0),
        ("log(100)", 2),
    ]
    
    print("Running tests...")
    passed = 0
    
    for expression, expected in test_cases:
        try:
            result, _ = calc.calculate(expression)
            if abs(result - expected) < 1e-10:  # Account for floating point precision
                print(f"✅ {expression} = {result}")
                passed += 1
            else:
                print(f"❌ {expression} = {result}, expected {expected}")
        except Exception as e:
            print(f"❌ {expression} failed with error: {e}")
    
    print(f"\nTests passed: {passed}/{len(test_cases)}")


if __name__ == "__main__":
    # Uncomment the next line to run tests instead of the main calculator
    # run_tests()
    main()
