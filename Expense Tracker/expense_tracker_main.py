#!/usr/bin/env python3
"""
Expense Tracker - A simple command-line expense tracking application
Author: Claude AI Assistant
Version: 1.0.0
Python Version: 3.8+
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import argparse


class ExpenseTracker:
    """Main class for managing expenses with file-based persistence."""
    
    def __init__(self, data_file: str = "expenses.json"):
        """
        Initialize the expense tracker.
        
        Args:
            data_file (str): Path to the JSON file for storing expense data
        """
        self.data_file = data_file
        self.expenses = self._load_expenses()
        
    def _load_expenses(self) -> List[Dict]:
        """
        Load expenses from JSON file.
        
        Returns:
            List[Dict]: List of expense dictionaries
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load expenses from {self.data_file}: {e}")
            return []
    
    def _save_expenses(self) -> bool:
        """
        Save expenses to JSON file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.expenses, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error: Could not save expenses to {self.data_file}: {e}")
            return False
    
    def add_expense(self, amount: float, category: str, description: str = "", date: str = None) -> bool:
        """
        Add a new expense.
        
        Args:
            amount (float): Expense amount
            category (str): Expense category
            description (str): Optional description
            date (str): Date in YYYY-MM-DD format (defaults to today)
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate amount
        if amount <= 0:
            print("Error: Amount must be positive")
            return False
        
        # Validate and format date
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("Error: Date must be in YYYY-MM-DD format")
                return False
        
        # Create expense record
        expense = {
            "id": len(self.expenses) + 1,
            "amount": round(amount, 2),
            "category": category.strip().title(),
            "description": description.strip(),
            "date": date,
            "created_at": datetime.now().isoformat()
        }
        
        self.expenses.append(expense)
        
        if self._save_expenses():
            print(f"✅ Added expense: ${amount:.2f} for {category}")
            return True
        return False
    
    def list_expenses(self, category: str = None, days: int = None) -> None:
        """
        List expenses with optional filtering.
        
        Args:
            category (str): Filter by category
            days (int): Show expenses from last N days
        """
        filtered_expenses = self.expenses.copy()
        
        # Filter by category
        if category:
            filtered_expenses = [e for e in filtered_expenses 
                               if e['category'].lower() == category.lower()]
        
        # Filter by date range
        if days:
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            filtered_expenses = [e for e in filtered_expenses if e['date'] >= cutoff_date]
        
        if not filtered_expenses:
            print("No expenses found matching your criteria.")
            return
        
        # Sort by date (newest first)
        filtered_expenses.sort(key=lambda x: x['date'], reverse=True)
        
        print(f"\n📊 Expenses {'for ' + category if category else ''}"
              f"{'from last ' + str(days) + ' days' if days else ''}:")
        print("-" * 80)
        print(f"{'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<30}")
        print("-" * 80)
        
        total = 0
        for expense in filtered_expenses:
            print(f"{expense['date']:<12} {expense['category']:<15} "
                  f"${expense['amount']:<9.2f} {expense['description'][:29]:<30}")
            total += expense['amount']
        
        print("-" * 80)
        print(f"{'Total:':<39} ${total:.2f}")
    
    def get_summary(self, days: int = 30) -> None:
        """
        Display expense summary by category.
        
        Args:
            days (int): Number of days to include in summary
        """
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        # Filter expenses by date range
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        recent_expenses = [e for e in self.expenses if e['date'] >= cutoff_date]
        
        if not recent_expenses:
            print(f"No expenses found in the last {days} days.")
            return
        
        # Calculate totals by category
        category_totals: Dict[str, float] = {}
        total_amount = 0
        
        for expense in recent_expenses:
            category = expense['category']
            amount = expense['amount']
            category_totals[category] = category_totals.get(category, 0) + amount
            total_amount += amount
        
        # Sort categories by amount (highest first)
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\n📈 Expense Summary (Last {days} days):")
        print("-" * 50)
        print(f"{'Category':<20} {'Amount':<12} {'Percentage':<12}")
        print("-" * 50)
        
        for category, amount in sorted_categories:
            percentage = (amount / total_amount) * 100 if total_amount > 0 else 0
            print(f"{category:<20} ${amount:<11.2f} {percentage:<11.1f}%")
        
        print("-" * 50)
        print(f"{'Total:':<20} ${total_amount:.2f}")
        
        # Additional statistics
        avg_per_day = total_amount / days if days > 0 else 0
        print(f"\n📊 Statistics:")
        print(f"Total expenses: {len(recent_expenses)}")
        print(f"Average per day: ${avg_per_day:.2f}")
        print(f"Largest expense: ${max(e['amount'] for e in recent_expenses):.2f}")
    
    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense by ID.
        
        Args:
            expense_id (int): ID of the expense to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        for i, expense in enumerate(self.expenses):
            if expense['id'] == expense_id:
                deleted_expense = self.expenses.pop(i)
                if self._save_expenses():
                    print(f"✅ Deleted expense: ${deleted_expense['amount']:.2f} "
                          f"for {deleted_expense['category']}")
                    return True
                return False
        
        print(f"Error: No expense found with ID {expense_id}")
        return False
    
    def get_categories(self) -> List[str]:
        """
        Get list of all unique categories.
        
        Returns:
            List[str]: Sorted list of unique categories
        """
        categories = set(expense['category'] for expense in self.expenses)
        return sorted(list(categories))


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Expense Tracker - Track your daily expenses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add 25.50 Food "Lunch at restaurant"
  python main.py add 100 Transport --date 2024-01-15
  python main.py list
  python main.py list --category Food
  python main.py list --days 7
  python main.py summary
  python main.py summary --days 90
  python main.py delete 1
  python main.py categories
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add expense command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('amount', type=float, help='Expense amount')
    add_parser.add_argument('category', help='Expense category')
    add_parser.add_argument('description', nargs='?', default='', help='Expense description')
    add_parser.add_argument('--date', help='Date (YYYY-MM-DD format, defaults to today)')
    
    # List expenses command
    list_parser = subparsers.add_parser('list', help='List expenses')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--days', type=int, help='Show expenses from last N days')
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show expense summary')
    summary_parser.add_argument('--days', type=int, default=30, help='Number of days for summary (default: 30)')
    
    # Delete expense command
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('id', type=int, help='Expense ID to delete')
    
    # Categories command
    subparsers.add_parser('categories', help='List all categories')
    
    # Interactive mode command
    subparsers.add_parser('interactive', help='Start interactive mode')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = ExpenseTracker()
    
    # Handle commands
    if args.command == 'add':
        tracker.add_expense(args.amount, args.category, args.description, args.date)
    
    elif args.command == 'list':
        tracker.list_expenses(args.category, args.days)
    
    elif args.command == 'summary':
        tracker.get_summary(args.days)
    
    elif args.command == 'delete':
        tracker.delete_expense(args.id)
    
    elif args.command == 'categories':
        categories = tracker.get_categories()
        if categories:
            print("📂 Available categories:")
            for category in categories:
                print(f"  • {category}")
        else:
            print("No categories found. Add some expenses first!")
    
    elif args.command == 'interactive':
        interactive_mode(tracker)
    
    else:
        # If no command provided, show help
        parser.print_help()


def interactive_mode(tracker: ExpenseTracker):
    """Interactive mode for easier expense management."""
    print("\n🎯 Welcome to Expense Tracker Interactive Mode!")
    print("Type 'help' for available commands or 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("expense-tracker> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using Expense Tracker!")
                break
            
            if user_input.lower() == 'help':
                print("""
Available commands:
  add <amount> <category> [description]  - Add new expense
  list [category] [days]                 - List expenses
  summary [days]                         - Show summary
  delete <id>                           - Delete expense
  categories                            - Show categories
  quit                                  - Exit interactive mode
                """)
                continue
            
            # Parse command
            parts = user_input.split()
            command = parts[0].lower()
            
            if command == 'add' and len(parts) >= 3:
                try:
                    amount = float(parts[1])
                    category = parts[2]
                    description = ' '.join(parts[3:]) if len(parts) > 3 else ''
                    tracker.add_expense(amount, category, description)
                except ValueError:
                    print("Error: Invalid amount. Please enter a number.")
            
            elif command == 'list':
                category = parts[1] if len(parts) > 1 and not parts[1].isdigit() else None
                days = None
                if len(parts) > 1 and parts[-1].isdigit():
                    days = int(parts[-1])
                tracker.list_expenses(category, days)
            
            elif command == 'summary':
                days = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 30
                tracker.get_summary(days)
            
            elif command == 'delete' and len(parts) == 2:
                try:
                    expense_id = int(parts[1])
                    tracker.delete_expense(expense_id)
                except ValueError:
                    print("Error: Invalid ID. Please enter a number.")
            
            elif command == 'categories':
                categories = tracker.get_categories()
                if categories:
                    print("📂 Available categories:")
                    for cat in categories:
                        print(f"  • {cat}")
                else:
                    print("No categories found.")
            
            else:
                print("❌ Invalid command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n👋 Thanks for using Expense Tracker!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


# Simple unit tests (can be run by uncommenting the test functions)
def test_expense_tracker():
    """Basic unit tests for ExpenseTracker class."""
    # Create a test tracker with temporary file
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file.close()
    
    tracker = ExpenseTracker(temp_file.name)
    
    # Test adding expense
    assert tracker.add_expense(25.50, "Food", "Test meal")
    assert len(tracker.expenses) == 1
    assert tracker.expenses[0]['amount'] == 25.50
    assert tracker.expenses[0]['category'] == "Food"
    
    # Test invalid amount
    assert not tracker.add_expense(-10, "Food", "Invalid")
    assert len(tracker.expenses) == 1  # Should not add invalid expense
    
    # Test categories
    categories = tracker.get_categories()
    assert "Food" in categories
    
    # Clean up
    os.unlink(temp_file.name)
    print("✅ All tests passed!")


if __name__ == "__main__":
    # Uncomment the next line to run tests
    # test_expense_tracker()
    
    main()
