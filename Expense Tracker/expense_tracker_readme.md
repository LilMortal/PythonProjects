# 💰 Expense Tracker

A simple, yet powerful command-line expense tracking application built in Python. Track your daily expenses, categorize them, and get insights into your spending patterns with easy-to-use commands and an interactive mode.

## 📋 Project Description

Expense Tracker is a lightweight, file-based expense management tool that helps you keep track of your personal finances. All data is stored locally in a JSON file, ensuring your financial information stays private and secure. The application provides both command-line interface and interactive mode for maximum flexibility.

## ✨ Features

- **Add Expenses**: Record expenses with amount, category, description, and date
- **List & Filter**: View expenses with filtering by category or date range
- **Smart Categorization**: Automatic category title-case formatting
- **Summary Reports**: Get spending summaries by category with percentages
- **Interactive Mode**: User-friendly interactive interface for easy expense management
- **Data Persistence**: All data saved in local JSON file
- **Input Validation**: Comprehensive error handling and data validation
- **Date Flexibility**: Add expenses for any date or default to today
- **Statistics**: View spending statistics including averages and totals
- **Category Management**: View all unique spending categories
- **Delete Functionality**: Remove incorrect or unwanted expense entries

## 🛠️ Requirements

- **Python Version**: Python 3.8 or higher
- **Dependencies**: Only standard library modules (no external packages required)
- **Operating System**: Cross-platform (Windows, macOS, Linux)

## 📦 Installation & Setup

1. **Download the file**: Save the `main.py` file to your desired directory

2. **Make it executable** (Linux/macOS):
   ```bash
   chmod +x main.py
   ```

3. **Verify Python version**:
   ```bash
   python --version
   # or
   python3 --version
   ```

4. **Test the installation**:
   ```bash
   python main.py --help
   ```

## 🚀 How to Run

### Basic Usage
```bash
python main.py [command] [arguments]
```

### Available Commands

#### Add Expenses
```bash
# Add expense with description
python main.py add 25.50 Food "Lunch at restaurant"

# Add expense for specific date
python main.py add 100 Transport --date 2024-01-15

# Add simple expense
python main.py add 50 Entertainment
```

#### List Expenses
```bash
# List all expenses
python main.py list

# Filter by category
python main.py list --category Food

# Show last 7 days
python main.py list --days 7

# Combine filters
python main.py list --category Transport --days 30
```

#### View Summary
```bash
# Summary for last 30 days (default)
python main.py summary

# Summary for last 90 days
python main.py summary --days 90
```

#### Manage Data
```bash
# Delete expense by ID
python main.py delete 1

# View all categories
python main.py categories
```

#### Interactive Mode
```bash
# Start interactive mode
python main.py interactive
```

## 📊 Example Usage

### Adding Your First Expenses
```bash
$ python main.py add 4.50 Coffee "Morning latte"
✅ Added expense: $4.50 for Coffee

$ python main.py add 12.99 Food "Subway sandwich"
✅ Added expense: $12.99 for Food

$ python main.py add 45.00 Gas "Fill up tank"
✅ Added expense: $45.00 for Gas
```

### Viewing Your Expenses
```bash
$ python main.py list

📊 Expenses :
--------------------------------------------------------------------------------
Date         Category        Amount     Description                   
--------------------------------------------------------------------------------
2024-01-20   Gas             $45.00     Fill up tank                  
2024-01-20   Food            $12.99     Subway sandwich               
2024-01-20   Coffee          $4.50      Morning latte                 
--------------------------------------------------------------------------------
Total:                       $62.49
```

### Getting Spending Summary
```bash
$ python main.py summary --days 7

📈 Expense Summary (Last 7 days):
--------------------------------------------------
Category             Amount       Percentage   
--------------------------------------------------
Gas                  $45.00       72.0%        
Food                 $12.99       20.8%        
Coffee               $4.50        7.2%         
--------------------------------------------------
Total:               $62.49

📊 Statistics:
Total expenses: 3
Average per day: $8.93
Largest expense: $45.00
```

### Interactive Mode Example
```bash
$ python main.py interactive

🎯 Welcome to Expense Tracker Interactive Mode!
Type 'help' for available commands or 'quit' to exit.

expense-tracker> add 8.99 Food Pizza slice
✅ Added expense: $8.99 for Food

expense-tracker> summary
📈 Expense Summary (Last 30 days):
[... summary output ...]

expense-tracker> quit
👋 Thanks for using Expense Tracker!
```

## 📁 File Structure

```
expense-tracker/
│
├── main.py          # Main application file
├── README.md        # This documentation file
└── expenses.json    # Data file (created automatically)
```

## 🔧 Configuration

The application uses a JSON file (`expenses.json`) to store all expense data. This file is created automatically in the same directory as `main.py` when you add your first expense.

### Data Format
Each expense is stored with the following structure:
```json
{
  "id": 1,
  "amount": 25.50,
  "category": "Food",
  "description": "Lunch at restaurant",
  "date": "2024-01-20",
  "created_at": "2024-01-20T14:30:00.123456"
}
```

## 🧪 Testing

The application includes basic unit tests. To run them:

1. Uncomment the test line in `main.py`:
   ```python
   # Change this line:
   # test_expense_tracker()
   
   # To this:
   test_expense_tracker()
   ```

2. Run the tests:
   ```bash
   python main.py
   ```

## 🌐 Converting to Web/GUI Version

### Web Version with Flask
To convert this to a web application:

1. Install Flask: `pip install flask`
2. Create HTML templates for the interface
3. Convert the ExpenseTracker methods to Flask routes
4. Use AJAX for dynamic updates
5. Consider using a database instead of JSON for better performance

### GUI Version with Tkinter
To create a desktop GUI version:

1. Import tkinter (included with Python)
2. Create main window with entry fields for expenses
3. Add buttons for different operations
4. Use treeview widget to display expense lists
5. Add menu bar for advanced features

### Database Version
For more robust data storage:

1. Replace JSON with SQLite: `import sqlite3`
2. Create proper database schema
3. Add data migration functionality
4. Implement backup and restore features

## 🚀 Future Improvements

### Core Features
- **Budget Management**: Set monthly budgets per category with alerts
- **Recurring Expenses**: Add support for automatic recurring expenses
- **Multi-Currency**: Support for different currencies with conversion
- **Import/Export**: CSV/Excel import/export functionality
- **Backup System**: Automatic data backup and restore

### Advanced Analytics
- **Spending Trends**: Visual charts showing spending patterns over time
- **Predictive Analysis**: Forecast future spending based on history
- **Goal Tracking**: Set and track financial goals
- **Comparison Reports**: Month-over-month and year-over-year comparisons

### User Experience
- **Configuration File**: Customizable settings and preferences
- **Themes**: Different color schemes and display options
- **Search Functionality**: Advanced search with multiple criteria
- **Undo/Redo**: Ability to undo recent actions
- **Data Validation**: Enhanced input validation and error messages

### Integration Features
- **Cloud Sync**: Synchronize data across multiple devices
- **Mobile App**: Companion mobile application
- **Bank Integration**: Import transactions from bank statements
- **Receipt Scanning**: OCR functionality for receipt processing

## 📚 Acknowledgments

- Built with Python's standard library for maximum compatibility
- Inspired by popular expense tracking applications
- Designed with privacy and simplicity in mind
- Uses JSON for human-readable data storage

## 📄 License

This project is open source and available under the MIT License. Feel free to modify and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Some areas for improvement:
- Additional export formats
- Enhanced reporting features
- Better error handling
- Performance optimizations
- User interface improvements

---

**Happy Expense Tracking! 💰**

*Remember: The best expense tracker is the one you actually use. Start simple, stay consistent!*