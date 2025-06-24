#!/usr/bin/env python3
"""
Leap It! - Advanced Leap Year Calculator and Analyzer
A comprehensive tool for leap year calculations, analysis, and exploration.

Author: Claude AI Assistant
Version: 1.0.0
Python: 3.10+
"""

import calendar
import datetime
from typing import List, Tuple, Dict
import argparse
import sys


class LeapYearAnalyzer:
    """
    A comprehensive leap year analyzer with multiple calculation methods
    and analysis features.
    """
    
    def __init__(self):
        self.current_year = datetime.datetime.now().year
    
    def is_leap_year(self, year: int) -> bool:
        """
        Determine if a year is a leap year using the standard algorithm.
        
        Rules:
        - Divisible by 4: potential leap year
        - Divisible by 100: not a leap year (exception)
        - Divisible by 400: leap year (exception to the exception)
        
        Args:
            year (int): Year to check
            
        Returns:
            bool: True if leap year, False otherwise
        """
        if not isinstance(year, int):
            raise TypeError("Year must be an integer")
        
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def is_leap_year_builtin(self, year: int) -> bool:
        """
        Alternative method using Python's built-in calendar module.
        
        Args:
            year (int): Year to check
            
        Returns:
            bool: True if leap year, False otherwise
        """
        return calendar.isleap(year)
    
    def get_leap_years_in_range(self, start_year: int, end_year: int) -> List[int]:
        """
        Get all leap years within a specified range.
        
        Args:
            start_year (int): Starting year (inclusive)
            end_year (int): Ending year (inclusive)
            
        Returns:
            List[int]: List of leap years in the range
        """
        if start_year > end_year:
            raise ValueError("Start year must be less than or equal to end year")
        
        return [year for year in range(start_year, end_year + 1) 
                if self.is_leap_year(year)]
    
    def next_leap_year(self, year: int) -> int:
        """
        Find the next leap year after the given year.
        
        Args:
            year (int): Reference year
            
        Returns:
            int: Next leap year
        """
        year += 1
        while not self.is_leap_year(year):
            year += 1
        return year
    
    def previous_leap_year(self, year: int) -> int:
        """
        Find the previous leap year before the given year.
        
        Args:
            year (int): Reference year
            
        Returns:
            int: Previous leap year
        """
        year -= 1
        while not self.is_leap_year(year) and year > 0:
            year -= 1
        return year if year > 0 else None
    
    def days_in_february(self, year: int) -> int:
        """
        Get the number of days in February for a given year.
        
        Args:
            year (int): Year to check
            
        Returns:
            int: 29 if leap year, 28 otherwise
        """
        return 29 if self.is_leap_year(year) else 28
    
    def leap_year_statistics(self, start_year: int, end_year: int) -> Dict[str, any]:
        """
        Generate comprehensive statistics about leap years in a range.
        
        Args:
            start_year (int): Starting year
            end_year (int): Ending year
            
        Returns:
            Dict: Statistics about leap years
        """
        leap_years = self.get_leap_years_in_range(start_year, end_year)
        total_years = end_year - start_year + 1
        
        return {
            'total_years': total_years,
            'leap_years_count': len(leap_years),
            'leap_years': leap_years,
            'percentage': (len(leap_years) / total_years) * 100,
            'average_gap': (total_years / len(leap_years)) if leap_years else 0,
            'first_leap': leap_years[0] if leap_years else None,
            'last_leap': leap_years[-1] if leap_years else None
        }


class LeapItCLI:
    """Command-line interface for the Leap It! application."""
    
    def __init__(self):
        self.analyzer = LeapYearAnalyzer()
    
    def display_banner(self):
        """Display the application banner."""
        banner = """
    ╔═══════════════════════════════════════╗
    ║              🗓️  LEAP IT! 🗓️             ║
    ║        Advanced Leap Year Tool        ║
    ║              Version 1.0              ║
    ╚═══════════════════════════════════════╝
        """
        print(banner)
    
    def check_single_year(self, year: int):
        """Check if a single year is a leap year and provide details."""
        try:
            is_leap = self.analyzer.is_leap_year(year)
            days_feb = self.analyzer.days_in_february(year)
            
            print(f"\n📅 Year Analysis: {year}")
            print("=" * 40)
            print(f"Leap Year: {'✅ YES' if is_leap else '❌ NO'}")
            print(f"Days in February: {days_feb}")
            
            if is_leap:
                print("🎉 This year has an extra day (February 29th)!")
            
            # Show next and previous leap years
            next_leap = self.analyzer.next_leap_year(year)
            prev_leap = self.analyzer.previous_leap_year(year)
            
            print(f"\nNext leap year: {next_leap}")
            if prev_leap:
                print(f"Previous leap year: {prev_leap}")
            
        except (TypeError, ValueError) as e:
            print(f"❌ Error: {e}")
    
    def analyze_range(self, start_year: int, end_year: int):
        """Analyze leap years in a range."""
        try:
            stats = self.analyzer.leap_year_statistics(start_year, end_year)
            
            print(f"\n📊 Leap Year Analysis: {start_year} - {end_year}")
            print("=" * 50)
            print(f"Total years analyzed: {stats['total_years']}")
            print(f"Leap years found: {stats['leap_years_count']}")
            print(f"Percentage of leap years: {stats['percentage']:.2f}%")
            print(f"Average gap between leap years: {stats['average_gap']:.1f} years")
            
            if stats['leap_years']:
                print(f"First leap year: {stats['first_leap']}")
                print(f"Last leap year: {stats['last_leap']}")
                
                print(f"\n🗓️ All leap years in range:")
                # Display leap years in rows of 10
                leap_years = stats['leap_years']
                for i in range(0, len(leap_years), 10):
                    row = leap_years[i:i+10]
                    print("   " + " ".join(f"{year:4d}" for year in row))
            
        except (TypeError, ValueError) as e:
            print(f"❌ Error: {e}")
    
    def interactive_mode(self):
        """Run the application in interactive mode."""
        self.display_banner()
        
        while True:
            print("\n🎯 Choose an option:")
            print("1. Check a single year")
            print("2. Analyze a range of years")
            print("3. Quick check current year")
            print("4. Find leap years around a specific year")
            print("5. Exit")
            
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == '1':
                    year = int(input("Enter a year: "))
                    self.check_single_year(year)
                
                elif choice == '2':
                    start = int(input("Enter start year: "))
                    end = int(input("Enter end year: "))
                    self.analyze_range(start, end)
                
                elif choice == '3':
                    current_year = datetime.datetime.now().year
                    self.check_single_year(current_year)
                
                elif choice == '4':
                    year = int(input("Enter a reference year: "))
                    print(f"\n🔍 Leap years around {year}:")
                    leap_years = self.analyzer.get_leap_years_in_range(year - 10, year + 10)
                    print("   " + " ".join(f"{y:4d}" for y in leap_years))
                
                elif choice == '5':
                    print("\n👋 Thanks for using Leap It! Goodbye!")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter 1-5.")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
    
    def run_with_args(self, args):
        """Run the application with command-line arguments."""
        if args.year:
            self.check_single_year(args.year)
        elif args.range:
            start, end = args.range
            self.analyze_range(start, end)
        elif args.current:
            current_year = datetime.datetime.now().year
            self.check_single_year(current_year)
        else:
            self.interactive_mode()


def create_argument_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Leap It! - Advanced Leap Year Calculator and Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode
  python main.py -y 2024           # Check specific year
  python main.py -r 2000 2030      # Analyze range
  python main.py -c                # Check current year
        """
    )
    
    parser.add_argument(
        '-y', '--year',
        type=int,
        help='Check if a specific year is a leap year'
    )
    
    parser.add_argument(
        '-r', '--range',
        nargs=2,
        type=int,
        metavar=('START', 'END'),
        help='Analyze leap years in a range (start end)'
    )
    
    parser.add_argument(
        '-c', '--current',
        action='store_true',
        help='Check if the current year is a leap year'
    )
    
    return parser


# Simple unit tests (can be run by uncommenting the test section)
def run_tests():
    """
    Simple unit tests for the LeapYearAnalyzer class.
    Uncomment the test_leap_it() call at the bottom to run tests.
    """
    analyzer = LeapYearAnalyzer()
    
    # Test cases: (year, expected_result)
    test_cases = [
        (2000, True),   # Divisible by 400
        (1900, False),  # Divisible by 100 but not 400
        (2004, True),   # Divisible by 4 but not 100
        (2001, False),  # Not divisible by 4
        (2024, True),   # Current leap year
        (2023, False),  # Recent non-leap year
    ]
    
    print("🧪 Running Unit Tests...")
    print("=" * 30)
    
    all_passed = True
    for year, expected in test_cases:
        result = analyzer.is_leap_year(year)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{year}: {status} (Expected: {expected}, Got: {result})")
        if result != expected:
            all_passed = False
    
    # Test range functionality
    leap_years_2000_2010 = analyzer.get_leap_years_in_range(2000, 2010)
    expected_leaps = [2000, 2004, 2008]
    range_test_pass = leap_years_2000_2010 == expected_leaps
    status = "✅ PASS" if range_test_pass else "❌ FAIL"
    print(f"Range test (2000-2010): {status}")
    if not range_test_pass:
        all_passed = False
    
    print("=" * 30)
    print(f"Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed


def main():
    """Main function to run the Leap It! application."""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    cli = LeapItCLI()
    cli.run_with_args(args)


if __name__ == "__main__":
    # Uncomment the next line to run unit tests
    # run_tests()
    
    main()
