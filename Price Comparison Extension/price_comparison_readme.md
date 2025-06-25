# 🛒 Price Comparison Tool

A powerful command-line Python application that helps you compare prices across multiple e-commerce websites. Simply provide product URLs and get instant price comparisons to find the best deals!

## 📋 Project Description

The Price Comparison Tool is designed to save you time and money by automatically extracting product prices from various online retailers. It scrapes product information including names, prices, availability, and provides a comprehensive comparison with savings calculations.

**Key Benefits:**
- Compare prices across multiple websites instantly
- Identify the best deals and potential savings
- Save comparison results for future reference
- Extensible architecture for adding new retailers

## ✨ Features

- **Multi-site Support**: Works with Amazon, eBay, and generic e-commerce sites
- **Smart Price Extraction**: Uses advanced regex patterns to find prices in various formats
- **Intelligent Sorting**: Automatically sorts results by price (lowest to highest)
- **Savings Calculator**: Shows potential savings and percentage differences
- **Data Export**: Save results to JSON format for record-keeping
- **Demo Mode**: Test the tool with sample data
- **Interactive Mode**: Add URLs one by one with real-time feedback
- **Rate Limiting**: Configurable delays between requests to be respectful to websites
- **Error Handling**: Robust error handling for network issues and parsing failures
- **Multiple Currency Support**: Handles USD, EUR, GBP, and other common currencies

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Internet connection for web scraping

### Step 1: Download the Files
Save both `main.py` and this `README.md` to your project directory.

### Step 2: Install Dependencies
This project uses only Python standard libraries, so no additional packages are required!

```bash
# Optional: Create a virtual environment
python -m venv price_comparison_env
source price_comparison_env/bin/activate  # On Windows: price_comparison_env\Scripts\activate

# The project is ready to run!
```

### Step 3: Make the Script Executable (Optional)
```bash
chmod +x main.py
```

## 🚀 How to Run

### Basic Usage
```bash
python main.py --help
```

### Demo Mode (Recommended for first run)
```bash
python main.py --demo
```

### Compare Specific URLs
```bash
python main.py --urls "https://amazon.com/product1" "https://ebay.com/product2"
```

### Interactive Mode
```bash
python main.py --interactive
```

### Advanced Usage
```bash
# Custom output file and delay
python main.py --urls "url1" "url2" --output my_comparison.json --delay 2.0

# Batch comparison with custom settings
python main.py --urls \
  "https://site1.com/product" \
  "https://site2.com/product" \
  "https://site3.com/product" \
  --delay 1.5 \
  --output laptop_prices.json
```

## 📖 Example Usage

### Example 1: Demo Mode
```bash
$ python main.py --demo

🛒 Price Comparison Tool v1.0
========================================
Running with demo data...
Demo data loaded successfully!

================================================================================
PRICE COMPARISON RESULTS
================================================================================

1. Sample Laptop Computer...
   Site: Store2
   Price: $849.99 USD
   Availability: In Stock
   URL: https://example-store2.com/laptop

2. Sample Laptop Computer...
   Site: Store1
   Price: $899.99 USD
   Availability: In Stock
   URL: https://example-store1.com/laptop

3. Sample Laptop Computer...
   Site: Store3
   Price: $925.00 USD
   Availability: Limited Stock
   URL: https://example-store3.com/laptop

==================================================
BEST DEAL: Store2 - $849.99
SAVINGS: $75.01 (8.1%)
==================================================

Results saved to price_comparison.json
```

### Example 2: Interactive Mode
```bash
$ python main.py --interactive

🛒 Price Comparison Tool v1.0
========================================
Interactive mode - Enter URLs one by one (empty line to finish):
Enter product URL: https://example-shop.com/smartphone
Fetching price from: https://example-shop.com/smartphone
✓ Found: Latest Smartphone Model - $599.99
Enter product URL: 

================================================================================
PRICE COMPARISON RESULTS
================================================================================
...
```

## 📊 Output Format

### Console Output
- Real-time feedback during URL processing
- Sorted price comparison table
- Best deal identification with savings calculation
- Clear success/error indicators

### JSON Export
```json
{
  "timestamp": "2025-01-15T10:30:45.123456",
  "total_products": 3,
  "products": [
    {
      "name": "Product Name",
      "price": 299.99,
      "currency": "USD",
      "url": "https://example.com/product",
      "site": "Example Store",
      "availability": "In Stock",
      "timestamp": "2025-01-15T10:30:45.123456"
    }
  ]
}
```

## 🧪 Testing

The project includes built-in unit tests. Run them with:

```bash
# Run individual test functions (basic testing)
python -c "from main import test_product_info_creation; test_product_info_creation(); print('✓ ProductInfo test passed')"

# Or install pytest for comprehensive testing
pip install pytest
python -m pytest main.py -v
```

## 🔧 Configuration Options

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--urls` | List of product URLs to compare | None | `--urls "url1" "url2"` |
| `--demo` | Run with sample data | False | `--demo` |
| `--interactive` | Interactive URL input mode | False | `--interactive` |
| `--output` | Output JSON filename | `price_comparison.json` | `--output results.json` |
| `--delay` | Delay between requests (seconds) | 1.0 | `--delay 2.5` |

## 🌐 Web/GUI Version Guide

### Converting to a Web Application

1. **Flask Web App**:
```bash
pip install flask
```
Create a simple web interface where users can input URLs and view results in a browser.

2. **Streamlit Dashboard**:
```bash
pip install streamlit
```
Build an interactive dashboard with real-time price tracking charts.

3. **FastAPI REST API**:
```bash
pip install fastapi uvicorn
```
Create a REST API for integration with other applications.

### Converting to a GUI Application

1. **Tkinter (Built-in)**:
No additional packages needed. Create a desktop application with forms and result displays.

2. **PyQt5/PySide2**:
```bash
pip install PyQt5
```
Build a professional desktop application with advanced UI components.

3. **Kivy (Cross-platform)**:
```bash
pip install kivy
```
Create applications that work on desktop, mobile, and tablets.

## 🚀 Future Improvements

### Planned Features
- **Browser Extension**: Chrome/Firefox extension for one-click price comparison
- **Price History Tracking**: Database storage with historical price trends
- **Email Alerts**: Automated notifications when prices drop
- **More Retailers**: Support for Walmart, Best Buy, Target, and international sites
- **Product Matching**: AI-powered product matching across different sites
- **Price Prediction**: Machine learning models to predict future price trends
- **Mobile App**: Native iOS/Android applications
- **Wishlist Management**: Save and track favorite products

### Technical Enhancements
- **Database Integration**: PostgreSQL/MongoDB for data persistence
- **Caching System**: Redis cache for improved performance
- **Async Processing**: Concurrent price fetching for faster results
- **API Rate Limiting**: Sophisticated request throttling
- **Proxy Support**: Rotate IP addresses to avoid blocking
- **Image Recognition**: Compare products using visual similarity
- **Selenium Integration**: Handle JavaScript-heavy sites
- **Docker Containerization**: Easy deployment and scaling

### Business Features
- **Price Drop Alerts**: Email/SMS notifications
- **Deal Sharing**: Social media integration
- **Affiliate Links**: Monetization through referral programs
- **Bulk Processing**: Handle large product catalogs
- **Analytics Dashboard**: Price trend analysis and insights

## ⚠️ Important Notes

### Ethical Web Scraping
- The tool includes respectful delays between requests
- Always check website robots.txt and terms of service
- Consider using official APIs when available
- Don't overload servers with excessive requests

### Limitations
- Some sites may block automated requests
- JavaScript-heavy sites might not work perfectly
- Prices may change between checks
- Product matching across sites can be challenging

### Legal Considerations
- Web scraping laws vary by jurisdiction
- Use responsibly and respect website terms
- Consider reaching out to sites for API access
- Don't use for commercial purposes without permission

## 🙏 Credits & Acknowledgments

- Built with Python's powerful standard libraries
- Regex patterns inspired by common e-commerce structures
- Architecture designed for extensibility and maintainability
- Thanks to the Python community for excellent documentation

## 📄 License

This project is open source and available under the MIT License. Feel free to modify and distribute as needed.

## 🐛 Troubleshooting

### Common Issues

**"Could not extract price from URL"**
- The website might be blocking requests
- Try increasing the delay with `--delay 3`
- Check if the URL is accessible in your browser

**"Error fetching URL"**
- Check your internet connection
- Verify the URL is correct and accessible
- Some sites may require specific headers

**"No products found for comparison"**
- Ensure URLs are valid product pages
- Try the demo mode first: `python main.py --demo`
- Check that products have visible prices

### Getting Help
1. Run `python main.py --help` for usage information
2. Try demo mode to verify installation: `python main.py --demo`
3. Check Python version: `python --version` (requires 3.8+)
4. Verify internet connectivity

---

**Happy price hunting! 🛍️💰**

*Find the best deals and save money with intelligent price comparison.*