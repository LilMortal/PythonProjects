#!/usr/bin/env python3
"""
Currency Converter with Real-time Exchange Rates
A command-line tool for converting currencies using live exchange rates.

Author: Claude Assistant
Version: 1.0.0
Python Version: 3.7+
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import sys
import os


class CurrencyConverter:
    """
    Currency Converter class that fetches real-time exchange rates
    and provides conversion functionality.
    """
    
    def __init__(self):
        """Initialize the currency converter with default settings."""
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.cache_file = "exchange_rates_cache.json"
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        self.supported_currencies = [
            'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY',
            'SEK', 'NZD', 'MXN', 'SGD', 'HKD', 'NOK', 'KRW', 'TRY',
            'RUB', 'INR', 'BRL', 'ZAR', 'PLN', 'DKK', 'CZK', 'HUF',
            'ILS', 'CLP', 'PHP', 'AED', 'COP', 'SAR', 'MYR', 'RON'
        ]
    
    def fetch_exchange_rates(self, base_currency: str = 'USD') -> Optional[Dict]:
        """
        Fetch exchange rates from the API or cache.
        
        Args:
            base_currency (str): The base currency code (default: USD)
            
        Returns:
            Dict: Dictionary containing exchange rates or None if failed
        """
        # Check cache first
        cached_data = self._load_from_cache(base_currency)
        if cached_data:
            print(f"📊 Using cached exchange rates for {base_currency}")
            return cached_data
        
        # Fetch from API
        try:
            print(f"🌐 Fetching live exchange rates for {base_currency}...")
            url = f"{self.base_url}{base_currency}"
            
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            # Add timestamp for caching
            data['cached_at'] = datetime.now().isoformat()
            
            # Save to cache
            self._save_to_cache(base_currency, data)
            
            print("✅ Successfully fetched live exchange rates!")
            return data
            
        except urllib.error.URLError as e:
            print(f"❌ Network error: {e}")
            print("💡 Check your internet connection and try again.")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing response: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def _load_from_cache(self, base_currency: str) -> Optional[Dict]:
        """Load exchange rates from cache if valid."""
        try:
            if not os.path.exists(self.cache_file):
                return None
                
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
            
            if base_currency not in cache:
                return None
            
            cached_data = cache[base_currency]
            cached_time = datetime.fromisoformat(cached_data['cached_at'])
            
            # Check if cache is still valid
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data
                
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
            pass
        
        return None
    
    def _save_to_cache(self, base_currency: str, data: Dict):
        """Save exchange rates to cache."""
        try:
            cache = {}
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)
            
            cache[base_currency] = data
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Warning: Could not save to cache: {e}")
    
    def convert_currency(self, amount: float, from_currency: str, 
                        to_currency: str) -> Optional[float]:
        """
        Convert amount from one currency to another.
        
        Args:
            amount (float): Amount to convert
            from_currency (str): Source currency code
            to_currency (str): Target currency code
            
        Returns:
            float: Converted amount or None if conversion failed
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # Validate currency codes
        if from_currency not in self.supported_currencies:
            print(f"❌ Unsupported currency: {from_currency}")
            return None
            
        if to_currency not in self.supported_currencies:
            print(f"❌ Unsupported currency: {to_currency}")
            return None
        
        # Same currency conversion
        if from_currency == to_currency:
            return amount
        
        # Get exchange rates
        rates_data = self.fetch_exchange_rates(from_currency)
        if not rates_data:
            return None
        
        # Check if target currency is available
        if to_currency not in rates_data['rates']:
            print(f"❌ Exchange rate not available for {to_currency}")
            return None
        
        # Perform conversion
        exchange_rate = rates_data['rates'][to_currency]
        converted_amount = amount * exchange_rate
        
        return converted_amount
    
    def get_supported_currencies(self) -> List[str]:
        """Return list of supported currency codes."""
        return self.supported_currencies.copy()
    
    def display_supported_currencies(self):
        """Display all supported currencies in a formatted way."""
        print("\n💱 Supported Currencies:")
        print("=" * 50)
        
        currencies_per_row = 8
        for i in range(0, len(self.supported_currencies), currencies_per_row):
            row = self.supported_currencies[i:i + currencies_per_row]
            print("  ".join(f"{curr:>4}" for curr in row))
        
        print("=" * 50)
        print(f"Total: {len(self.supported_currencies)} currencies supported\n")


def validate_amount(amount_str: str) -> Optional[float]:
    """
    Validate and convert amount string to float.
    
    Args:
        amount_str (str): Amount as string
        
    Returns:
        float: Valid amount or None if invalid
    """
    try:
        amount = float(amount_str)
        if amount < 0:
            print("❌ Amount cannot be negative.")
            return None
        return amount
    except ValueError:
        print("❌ Invalid amount. Please enter a valid number.")
        return None


def validate_currency(currency: str, supported_currencies: List[str]) -> Optional[str]:
    """
    Validate currency code.
    
    Args:
        currency (str): Currency code to validate
        supported_currencies (List[str]): List of supported currencies
        
    Returns:
        str: Valid currency code or None if invalid
    """
    currency = currency.upper().strip()
    if currency in supported_currencies:
        return currency
    print(f"❌ '{currency}' is not a supported currency.")
    return None


def format_currency(amount: float, currency: str) -> str:
    """
    Format currency amount for display.
    
    Args:
        amount (float): Amount to format
        currency (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    return f"{amount:,.2f} {currency}"


def interactive_mode():
    """Run the currency converter in interactive mode."""
    converter = CurrencyConverter()
    
    print("🌍 Currency Converter")
    print("=" * 40)
    print("Convert currencies with real-time exchange rates!")
    print("Type 'help' for commands or 'quit' to exit.\n")
    
    while True:
        try:
            command = input("💰 Enter command (or 'help'): ").strip().lower()
            
            if command in ['quit', 'exit', 'q']:
                print("👋 Thank you for using Currency Converter!")
                break
                
            elif command in ['help', 'h']:
                print("\n📋 Available Commands:")
                print("  convert  - Convert between currencies")
                print("  list     - Show supported currencies")
                print("  quit     - Exit the program")
                print("  help     - Show this help message\n")
                
            elif command in ['list', 'currencies', 'l']:
                converter.display_supported_currencies()
                
            elif command in ['convert', 'c']:
                print("\n💱 Currency Conversion")
                print("-" * 25)
                
                # Get amount
                while True:
                    amount_input = input("Enter amount: ").strip()
                    amount = validate_amount(amount_input)
                    if amount is not None:
                        break
                
                # Get source currency
                while True:
                    from_curr = input("From currency (e.g., USD): ").strip()
                    from_currency = validate_currency(from_curr, converter.get_supported_currencies())
                    if from_currency:
                        break
                
                # Get target currency
                while True:
                    to_curr = input("To currency (e.g., EUR): ").strip()
                    to_currency = validate_currency(to_curr, converter.get_supported_currencies())
                    if to_currency:
                        break
                
                # Perform conversion
                result = converter.convert_currency(amount, from_currency, to_currency)
                
                if result is not None:
                    print(f"\n✅ Conversion Result:")
                    print(f"   {format_currency(amount, from_currency)} = {format_currency(result, to_currency)}")
                    
                    if from_currency != 'USD' and to_currency != 'USD':
                        rate = result / amount
                        print(f"   Exchange Rate: 1 {from_currency} = {rate:.6f} {to_currency}")
                else:
                    print("❌ Conversion failed. Please try again.")
                
                print()
                
            else:
                print("❌ Unknown command. Type 'help' for available commands.\n")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break


def command_line_mode(args):
    """Run the currency converter with command line arguments."""
    if len(args) != 4:
        print("❌ Usage: python main.py <amount> <from_currency> <to_currency>")
        print("   Example: python main.py 100 USD EUR")
        return
    
    try:
        amount = float(args[1])
        from_currency = args[2].upper()
        to_currency = args[3].upper()
        
        converter = CurrencyConverter()
        result = converter.convert_currency(amount, from_currency, to_currency)
        
        if result is not None:
            print(f"{format_currency(amount, from_currency)} = {format_currency(result, to_currency)}")
        else:
            print("❌ Conversion failed.")
            
    except ValueError:
        print("❌ Invalid amount. Please enter a valid number.")


def run_tests():
    """Run simple unit tests for the currency converter."""
    print("🧪 Running Tests...")
    print("=" * 30)
    
    converter = CurrencyConverter()
    
    # Test 1: Same currency conversion
    result = converter.convert_currency(100, 'USD', 'USD')
    assert result == 100, "Same currency conversion failed"
    print("✅ Test 1 passed: Same currency conversion")
    
    # Test 2: Validate amount function
    assert validate_amount("100") == 100.0, "Amount validation failed"
    assert validate_amount("-50") is None, "Negative amount validation failed"
    assert validate_amount("abc") is None, "Invalid amount validation failed"
    print("✅ Test 2 passed: Amount validation")
    
    # Test 3: Currency validation
    supported = ['USD', 'EUR', 'GBP']
    assert validate_currency('usd', supported) == 'USD', "Currency validation failed"
    assert validate_currency('xyz', supported) is None, "Invalid currency validation failed"
    print("✅ Test 3 passed: Currency validation")
    
    # Test 4: Currency formatting
    formatted = format_currency(1234.56, 'USD')
    assert formatted == "1,234.56 USD", "Currency formatting failed"
    print("✅ Test 4 passed: Currency formatting")
    
    print("\n🎉 All tests passed!")


def main():
    """Main function to run the currency converter."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            run_tests()
        else:
            command_line_mode(sys.argv)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()


# Additional test cases for development
"""
UNIT TESTS (for development reference):

def test_currency_converter():
    converter = CurrencyConverter()
    
    # Test supported currencies
    currencies = converter.get_supported_currencies()
    assert 'USD' in currencies
    assert 'EUR' in currencies
    assert len(currencies) > 10
    
    # Test same currency conversion
    result = converter.convert_currency(100, 'USD', 'USD')
    assert result == 100
    
    # Test invalid currency
    result = converter.convert_currency(100, 'INVALID', 'USD')
    assert result is None

def test_validation_functions():
    # Test amount validation
    assert validate_amount('100') == 100.0
    assert validate_amount('100.50') == 100.50
    assert validate_amount('-50') is None
    assert validate_amount('abc') is None
    
    # Test currency validation
    supported = ['USD', 'EUR', 'GBP']
    assert validate_currency('USD', supported) == 'USD'
    assert validate_currency('usd', supported) == 'USD'  # Case insensitive
    assert validate_currency('INVALID', supported) is None

def test_formatting():
    # Test currency formatting
    assert format_currency(1000, 'USD') == '1,000.00 USD'
    assert format_currency(1234.56, 'EUR') == '1,234.56 EUR'

# Run tests with: python -c "import main; main.run_tests()"
"""