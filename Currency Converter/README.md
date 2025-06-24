# 🌍 Currency Converter

A powerful command-line currency converter that provides real-time exchange rates for over 30 currencies. Built with Python 3.7+ using only standard libraries, this tool offers both interactive and command-line modes for quick currency conversions.

## 📋 Features

- **Real-time Exchange Rates**: Fetches live exchange rates from a reliable API
- **Smart Caching**: Caches exchange rates for 1 hour to reduce API calls and improve performance
- **Dual Modes**: 
  - Interactive mode for multiple conversions
  - Command-line mode for quick one-time conversions
- **Error Handling**: Comprehensive error handling for network issues and invalid inputs
- **30+ Currencies**: Supports major world currencies including USD, EUR, GBP, JPY, and more
- **Input Validation**: Validates currency codes and amounts with helpful error messages
- **Offline Capability**: Uses cached data when network is unavailable
- **Unit Tests**: Built-in test suite for reliability

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection (for fetching live rates)

### Installation

1. **Clone or Download** the project files:
   ```bash
   # Download main.py to your desired directory
   wget https://your-repo/main.py
   # or simply copy the main.py file
   ```

2. **No additional dependencies** required! The project uses only Python standard libraries.

### Running the Application

#### Interactive Mode (Recommended)
```bash
python main.py
```
This launches an interactive session where you can:
- Convert multiple currencies
- View supported currencies
- Get help with commands

#### Command-Line Mode (Quick Conversions)
```bash
python main.py <amount> <from_currency> <to_currency>
```

#### Run Tests
```bash
python main.py --test
```

## 💡 Usage Examples

### Interactive Mode Example
```
🌍 Currency Converter
========================================
Convert currencies with real-time exchange rates!
Type 'help' for commands or 'quit' to exit.

💰 Enter command (or 'help'): convert

💱 Currency Conversion
-------------------------
Enter amount: 100
From currency (e.g., USD): USD
To currency (e.g., EUR): EUR

🌐 Fetching live exchange rates for USD...
✅ Successfully fetched live exchange rates!

✅ Conversion Result:
   100.00 USD = 92.45 EUR
   Exchange Rate: 1 USD = 0.924500 EUR
```

### Command-Line Mode Examples
```bash
# Convert 100 USD to EUR
python main.py 100 USD EUR
# Output: 100.00 USD = 92.45 EUR

# Convert 50 GBP to JPY
python main.py 50 GBP JPY
# Output: 50.00 GBP = 7,231.50 JPY

# Convert 1000 EUR to CAD
python main.py 1000 EUR CAD
# Output: 1,000.00 EUR = 1,472.30 CAD
```

### Supported Commands (Interactive Mode)
- `convert` or `c` - Start currency conversion
- `list` or `l` - Display all supported currencies
- `help` or `h` - Show available commands
- `quit` or `q` - Exit the program

## 🌐 Supported Currencies

The converter supports 32 major world currencies:

| Americas | Europe | Asia-Pacific | Middle East/Africa |
|----------|---------|--------------|-------------------|
| USD 🇺🇸 | EUR 🇪🇺 | JPY 🇯🇵 | AED 🇦🇪 |
| CAD 🇨🇦 | GBP 🇬🇧 | AUD 🇦🇺 | SAR 🇸🇦 |
| BRL 🇧🇷 | CHF 🇨🇭 | CNY 🇨🇳 | ILS 🇮🇱 |
| MXN 🇲🇽 | SEK 🇸🇪 | KRW 🇰🇷 | ZAR 🇿🇦 |
| CLP 🇨🇱 | NOK 🇳🇴 | HKD 🇭🇰 | TRY 🇹🇷 |
| COP 🇨🇴 | DKK 🇩🇰 | SGD 🇸🇬 | |
| | PLN 🇵🇱 | NZD 🇳🇿 | |
| | CZK 🇨🇿 | INR 🇮🇳 | |
| | HUF 🇭🇺 | MYR 🇲🇾 | |
| | RON 🇷🇴 | PHP 🇵🇭 | |
| | RUB 🇷🇺 | | |

## 📁 Project Structure

```
currency-converter/
│
├── main.py                     # Main application file
├── README.md                   # This documentation
├── exchange_rates_cache.json   # Auto-generated cache file
└── requirements.txt            # Empty (no external dependencies)
```

## ⚙️ Technical Details

### Caching System
- Exchange rates are cached for 1 hour to improve performance
- Cache is stored in `exchange_rates_cache.json`
- Automatic fallback to cached data if network is unavailable

### API Integration
- Uses ExchangeRate-API (free tier) for real-time rates
- Base URL: `https://api.exchangerate-api.com/v4/latest/`
- Handles network timeouts and API errors gracefully

### Error Handling
- Network connectivity issues
- Invalid currency codes
- Malformed API responses
- File system errors (cache)
- User input validation

## 🔧 Customization

### Adding New Currencies
Edit the `supported_currencies` list in the `CurrencyConverter` class:

```python
self.supported_currencies = [
    'USD', 'EUR', 'GBP', 'JPY',  # existing currencies
    'NEW_CURRENCY_CODE',          # add new currency here
    # ... other currencies
]
```

### Changing Cache Duration
Modify the `cache_duration` in the `__init__` method:

```python
self.cache_duration = timedelta(hours=6)  # Cache for 6 hours
```

### Using Different API
Replace the `base_url` in the `CurrencyConverter` class:

```python
self.base_url = "https://your-preferred-api.com/latest/"
```

## 🧪 Testing

The project includes built-in unit tests:

```bash
# Run all tests
python main.py --test

# Run specific test functions (for developers)
python -c "import main; main.run_tests()"
```

Test coverage includes:
- Currency conversion logic
- Input validation functions
- Currency formatting
- Error handling scenarios

## 🚀 Future Improvements

### Phase 1 - Enhanced Features
- [ ] **Historical Exchange Rates**: Add support for historical rate queries
- [ ] **Currency Trends**: Show rate changes over time (daily, weekly, monthly)
- [ ] **Favorites**: Save frequently used currency pairs
- [ ] **Batch Conversion**: Convert multiple amounts at once
- [ ] **Configuration File**: Allow users to customize settings

### Phase 2 - User Interface
- [ ] **GUI Version**: Create a desktop application using tkinter or PyQt
- [ ] **Web Interface**: Build a Flask/Django web application
- [ ] **Mobile App**: Develop using Kivy or React Native
- [ ] **REST API**: Create an API server for other applications

### Phase 3 - Advanced Features
- [ ] **Cryptocurrency Support**: Add Bitcoin, Ethereum, and other cryptos
- [ ] **Rate Alerts**: Notify users when rates reach target values
- [ ] **Portfolio Tracking**: Track multiple currency holdings
- [ ] **Export Features**: Save conversion history to CSV/Excel
- [ ] **Multi-language Support**: Localization for different languages

### Phase 4 - Professional Features
- [ ] **Database Integration**: Store historical data and user preferences
- [ ] **User Accounts**: Personal conversion history and settings
- [ ] **Premium Features**: Advanced analytics and unlimited API calls
- [ ] **Enterprise Edition**: Bulk operations and team management

## 🌐 Converting to Web/GUI

### Web Application (Flask)
```python
# Add to requirements.txt:
# Flask==2.3.3

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
converter = CurrencyConverter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    result = converter.convert_currency(
        data['amount'], 
        data['from_currency'], 
        data['to_currency']
    )
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
```

### GUI Application (tkinter)
```python
import tkinter as tk
from tkinter import ttk, messagebox

class CurrencyConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.converter = CurrencyConverter()
        self.create_widgets()
    
    def create_widgets(self):
        # Amount input
        ttk.Label(self.root, text="Amount:").pack(pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.amount_var).pack(pady=5)
        
        # Currency dropdowns
        ttk.Label(self.root, text="From:").pack(pady=5)
        self.from_var = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.from_var, 
                    values=self.converter.get_supported_currencies()).pack(pady=5)
        
        # Convert button
        ttk.Button(self.root, text="Convert", 
                  command=self.convert_currency).pack(pady=10)

root = tk.Tk()
app = CurrencyConverterGUI(root)
root.mainloop()
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section below
2. Review the error messages for guidance
3. Ensure you have a stable internet connection
4. Verify your Python version (3.7+ required)

### Common Issues

**"Network error" message**: Check your internet connection and firewall settings.

**"Unsupported currency" error**: Use the `list` command to see all supported currencies.

**Cache file errors**: The application will continue to work without caching.

## 🙏 Acknowledgments

- **ExchangeRate-API** for providing free exchange rate data
- **Python Community** for excellent standard library documentation
- **Currency symbols** and flags used for documentation purposes

---

**Happy Converting! 💱**

*Last updated: June 2025*
