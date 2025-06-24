#!/usr/bin/env python3
"""
Random Password Generator
A secure and customizable password generator with various options.

Author: Claude AI Assistant
Version: 1.0.0
Python Version: 3.8+
"""

import random
import string
import secrets
import argparse
import sys
from typing import List, Set


class PasswordGenerator:
    """
    A secure password generator with customizable options.
    Uses Python's secrets module for cryptographically secure random generation.
    """
    
    def __init__(self):
        """Initialize the password generator with default character sets."""
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.ambiguous_chars = "0O1lI"  # Characters that might be confused
    
    def generate_password(self, 
                         length: int = 12,
                         include_uppercase: bool = True,
                         include_lowercase: bool = True,
                         include_digits: bool = True,
                         include_special: bool = True,
                         exclude_ambiguous: bool = False,
                         custom_chars: str = "") -> str:
        """
        Generate a random password with specified criteria.
        
        Args:
            length (int): Length of the password (minimum 4)
            include_uppercase (bool): Include uppercase letters
            include_lowercase (bool): Include lowercase letters
            include_digits (bool): Include digits
            include_special (bool): Include special characters
            exclude_ambiguous (bool): Exclude ambiguous characters (0, O, 1, l, I)
            custom_chars (str): Additional custom characters to include
            
        Returns:
            str: Generated password
            
        Raises:
            ValueError: If invalid parameters are provided
        """
        # Validate input parameters
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        if not any([include_uppercase, include_lowercase, include_digits, include_special]) and not custom_chars:
            raise ValueError("At least one character type must be selected")
        
        # Build character pool
        char_pool = ""
        required_chars = []
        
        if include_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            char_pool += chars
            required_chars.append(secrets.choice(chars))
        
        if include_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            char_pool += chars
            required_chars.append(secrets.choice(chars))
        
        if include_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            char_pool += chars
            required_chars.append(secrets.choice(chars))
        
        if include_special:
            char_pool += self.special_chars
            required_chars.append(secrets.choice(self.special_chars))
        
        if custom_chars:
            char_pool += custom_chars
        
        # Generate password ensuring at least one character from each selected type
        password_chars = required_chars.copy()
        
        # Fill remaining positions with random characters from the pool
        for _ in range(length - len(required_chars)):
            password_chars.append(secrets.choice(char_pool))
        
        # Shuffle the password to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_multiple_passwords(self, count: int, **kwargs) -> List[str]:
        """
        Generate multiple passwords with the same criteria.
        
        Args:
            count (int): Number of passwords to generate
            **kwargs: Password generation parameters
            
        Returns:
            List[str]: List of generated passwords
        """
        if count < 1:
            raise ValueError("Count must be at least 1")
        
        return [self.generate_password(**kwargs) for _ in range(count)]
    
    def check_password_strength(self, password: str) -> dict:
        """
        Analyze password strength and provide feedback.
        
        Args:
            password (str): Password to analyze
            
        Returns:
            dict: Dictionary containing strength analysis
        """
        analysis = {
            'length': len(password),
            'has_lowercase': any(c.islower() for c in password),
            'has_uppercase': any(c.isupper() for c in password),
            'has_digits': any(c.isdigit() for c in password),
            'has_special': any(c in self.special_chars for c in password),
            'unique_chars': len(set(password)),
            'strength_score': 0,
            'strength_level': 'Very Weak'
        }
        
        # Calculate strength score
        if analysis['length'] >= 8:
            analysis['strength_score'] += 2
        if analysis['length'] >= 12:
            analysis['strength_score'] += 1
        if analysis['has_lowercase']:
            analysis['strength_score'] += 1
        if analysis['has_uppercase']:
            analysis['strength_score'] += 1
        if analysis['has_digits']:
            analysis['strength_score'] += 1
        if analysis['has_special']:
            analysis['strength_score'] += 2
        if analysis['unique_chars'] / len(password) > 0.7:
            analysis['strength_score'] += 1
        
        # Determine strength level
        if analysis['strength_score'] >= 8:
            analysis['strength_level'] = 'Very Strong'
        elif analysis['strength_score'] >= 6:
            analysis['strength_level'] = 'Strong'
        elif analysis['strength_score'] >= 4:
            analysis['strength_level'] = 'Medium'
        elif analysis['strength_score'] >= 2:
            analysis['strength_level'] = 'Weak'
        
        return analysis


def print_password_analysis(analysis: dict) -> None:
    """Print formatted password strength analysis."""
    print(f"\n📊 Password Analysis:")
    print(f"Length: {analysis['length']} characters")
    print(f"Lowercase letters: {'✓' if analysis['has_lowercase'] else '✗'}")
    print(f"Uppercase letters: {'✓' if analysis['has_uppercase'] else '✗'}")
    print(f"Digits: {'✓' if analysis['has_digits'] else '✗'}")
    print(f"Special characters: {'✓' if analysis['has_special'] else '✗'}")
    print(f"Unique characters: {analysis['unique_chars']}")
    print(f"Strength: {analysis['strength_level']} ({analysis['strength_score']}/9)")


def interactive_mode():
    """Run the password generator in interactive mode."""
    print("🔐 Interactive Password Generator")
    print("=" * 40)
    
    generator = PasswordGenerator()
    
    while True:
        try:
            print("\nPassword Options:")
            length = int(input("Password length (default 12): ") or "12")
            
            include_upper = input("Include uppercase letters? (Y/n): ").lower() != 'n'
            include_lower = input("Include lowercase letters? (Y/n): ").lower() != 'n'
            include_digits = input("Include digits? (Y/n): ").lower() != 'n'
            include_special = input("Include special characters? (Y/n): ").lower() != 'n'
            exclude_ambiguous = input("Exclude ambiguous characters (0,O,1,l,I)? (y/N): ").lower() == 'y'
            
            count = int(input("Number of passwords to generate (default 1): ") or "1")
            
            # Generate passwords
            passwords = generator.generate_multiple_passwords(
                count=count,
                length=length,
                include_uppercase=include_upper,
                include_lowercase=include_lower,
                include_digits=include_digits,
                include_special=include_special,
                exclude_ambiguous=exclude_ambiguous
            )
            
            print(f"\n🔑 Generated Password{'s' if count > 1 else ''}:")
            for i, password in enumerate(passwords, 1):
                print(f"{i}: {password}")
                
                # Show analysis for single password
                if count == 1:
                    analysis = generator.check_password_strength(password)
                    print_password_analysis(analysis)
            
            # Ask to continue
            if input("\nGenerate another password? (Y/n): ").lower() == 'n':
                break
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break


def main():
    """Main function to handle command-line arguments and run the generator."""
    parser = argparse.ArgumentParser(
        description="Generate secure random passwords with customizable options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Interactive mode
  python main.py -l 16                    # Generate 16-character password
  python main.py -l 12 --no-special      # No special characters
  python main.py -l 20 -c 5              # Generate 5 passwords
  python main.py --exclude-ambiguous     # Exclude confusing characters
  python main.py --analyze "MyPassword123!"  # Analyze password strength
        """
    )
    
    parser.add_argument('-l', '--length', type=int, default=12,
                       help='Password length (default: 12)')
    parser.add_argument('--no-uppercase', action='store_true',
                       help='Exclude uppercase letters')
    parser.add_argument('--no-lowercase', action='store_true',
                       help='Exclude lowercase letters')
    parser.add_argument('--no-digits', action='store_true',
                       help='Exclude digits')
    parser.add_argument('--no-special', action='store_true',
                       help='Exclude special characters')
    parser.add_argument('--exclude-ambiguous', action='store_true',
                       help='Exclude ambiguous characters (0,O,1,l,I)')
    parser.add_argument('-c', '--count', type=int, default=1,
                       help='Number of passwords to generate (default: 1)')
    parser.add_argument('--custom-chars', type=str, default="",
                       help='Additional custom characters to include')
    parser.add_argument('--analyze', type=str,
                       help='Analyze the strength of a given password')
    parser.add_argument('--interactive', action='store_true',
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    # Handle password analysis
    if args.analyze:
        analysis = generator.check_password_strength(args.analyze)
        print(f"Password: {args.analyze}")
        print_password_analysis(analysis)
        return
    
    # Handle interactive mode
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
    try:
        # Generate passwords with command-line arguments
        passwords = generator.generate_multiple_passwords(
            count=args.count,
            length=args.length,
            include_uppercase=not args.no_uppercase,
            include_lowercase=not args.no_lowercase,
            include_digits=not args.no_digits,
            include_special=not args.no_special,
            exclude_ambiguous=args.exclude_ambiguous,
            custom_chars=args.custom_chars
        )
        
        print(f"🔑 Generated Password{'s' if args.count > 1 else ''}:")
        for i, password in enumerate(passwords, 1):
            if args.count > 1:
                print(f"{i}: {password}")
            else:
                print(password)
        
        # Show analysis for single password
        if args.count == 1:
            analysis = generator.check_password_strength(passwords[0])
            print_password_analysis(analysis)
            
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


# Simple unit tests (can be run with: python -m doctest main.py)
def run_tests():
    """
    Simple test functions to verify password generator functionality.
    
    >>> generator = PasswordGenerator()
    >>> password = generator.generate_password(length=10)
    >>> len(password) == 10
    True
    >>> password = generator.generate_password(length=8, include_special=False)
    >>> any(c in generator.special_chars for c in password)
    False
    >>> passwords = generator.generate_multiple_passwords(3, length=8)
    >>> len(passwords) == 3
    True
    >>> all(len(p) == 8 for p in passwords)
    True
    >>> analysis = generator.check_password_strength("Password123!")
    >>> analysis['has_uppercase'] and analysis['has_lowercase'] and analysis['has_digits'] and analysis['has_special']
    True
    """
    pass


if __name__ == "__main__":
    main()