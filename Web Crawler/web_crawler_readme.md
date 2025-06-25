# Web Crawler 🕷️

A comprehensive Python web crawler that extracts links, email addresses, and phone numbers from websites while respecting robots.txt rules and implementing intelligent rate limiting.

## 📖 Project Description

This web crawler is designed to systematically browse websites and extract valuable information including internal/external links, email addresses, and phone numbers. It implements breadth-first search crawling with configurable depth limits, respects website policies through robots.txt compliance, and includes robust error handling for production use.

The crawler is perfect for SEO analysis, lead generation, contact information extraction, website mapping, and competitive research while maintaining ethical crawling practices.

## ✨ Features

- **🎯 Smart Crawling**: Breadth-first search with configurable depth and page limits
- **🤖 Robots.txt Compliance**: Automatically checks and respects robots.txt rules
- **⚡ Rate Limiting**: Configurable delays between requests to avoid overwhelming servers
- **📧 Email Extraction**: Finds and collects email addresses using regex patterns
- **📞 Phone Extraction**: Detects various phone number formats (US-focused)
- **🔗 Link Discovery**: Extracts and normalizes both internal and external links
- **💾 Multiple Export Formats**: Save results in JSON or CSV format
- **📊 Detailed Reporting**: Comprehensive crawl summaries and statistics
- **🛡️ Error Handling**: Robust error handling with detailed logging
- **🧪 Built-in Tests**: Simple unit tests for core functionality

## 🔧 Requirements

- **Python Version**: 3.8 or higher
- **Dependencies**: Uses only Python standard library (no third-party packages required!)

### Optional Dependencies
For enhanced functionality, you can install:
```bash
# For advanced HTML parsing (optional)
pip install beautifulsoup4 lxml

# For better HTTP handling (optional)
pip install requests
```

## 🚀 Installation & Setup

1. **Clone or download** the project files:
   - `main.py` - The main crawler script
   - `README.md` - This documentation

2. **Verify Python version**:
   ```bash
   python --version
   # Should show Python 3.8 or higher
   ```

3. **Make the script executable** (Linux/Mac):
   ```bash
   chmod +x main.py
   ```

4. **Run basic tests** to ensure everything works:
   ```bash
   python main.py --test
   ```

## 🎮 Usage

### Basic Usage

```bash
# Crawl a single website
python main.py https://example.com

# Crawl multiple websites
python main.py https://site1.com https://site2.com https://site3.com
```

### Advanced Usage

```bash
# Deep crawl with custom settings
python main.py https://example.com \
  --depth 3 \
  --delay 2.0 \
  --max-pages 100 \
  --output csv \
  --filename my_crawl_results.csv

# Fast crawl for testing
python main.py https://example.com --depth 1 --delay 0.5 --max-pages 10
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `urls` | Starting URLs to crawl (required) | - |
| `--depth` | Maximum crawl depth | 2 |
| `--delay` | Delay between requests (seconds) | 1.0 |
| `--max-pages` | Maximum pages to crawl | 50 |
| `--output` | Output format (json/csv) | json |
| `--filename` | Custom output filename | auto-generated |
| `--no-summary` | Skip printing summary | False |

## 📋 Example Usage & Output

### Command
```bash
python main.py https://python.org --depth 2 --max-pages 20
```

### Sample Output
```
🚀 Starting crawl with max_depth=2, max_pages=20
⏱️  Delay between requests: 1.0s
------------------------------------------------------------
🔍 Crawling [1/20] (depth 0): https://python.org
✅ Found: 15 links, 2 emails, 1 phones
🔍 Crawling [2/20] (depth 1): https://python.org/about/
✅ Found: 8 links, 0 emails, 0 phones
...
------------------------------------------------------------
🎉 Crawl completed! Processed 20 pages
💾 Results saved to: crawl_results_20241225_143022.json

============================================================
📊 CRAWL SUMMARY
============================================================
Total pages processed: 20
Successful crawls: 18
Total links found: 145
Total emails found: 5
Total phone numbers found: 2
============================================================

🌐 Top Domains Crawled:
  python.org: 15 pages
  docs.python.org: 3 pages
  pypi.org: 2 pages
```

### Sample JSON Output
```json
[
  {
    "url": "https://python.org",
    "title": "Welcome to Python.org",
    "status_code": 200,
    "content_length": 52847,
    "links_found": 15,
    "emails_found": ["info@python.org", "webmaster@python.org"],
    "phone_numbers": ["+1-555-123-4567"],
    "crawl_time": "2024-12-25 14:30:22",
    "error_message": null
  }
]
```

## 🧪 Testing

Run the built-in tests:
```bash
python main.py --test
```

This will test:
- URL normalization
- Data extraction functions
- Basic crawler functionality

## 📁 Project Structure

```
web-crawler/
├── main.py          # Main crawler script (single file)
├── README.md        # This documentation
└── output/          # Generated results (created automatically)
    ├── crawl_results_YYYYMMDD_HHMMSS.json
    └── crawl_results_YYYYMMDD_HHMMSS.csv
```

## 🔒 Ethical Considerations

This crawler implements several ethical practices:

- **Robots.txt Compliance**: Always checks and respects robots.txt rules
- **Rate Limiting**: Prevents overwhelming target servers
- **User-Agent**: Identifies itself clearly in requests
- **Reasonable Defaults**: Conservative crawling limits by default
- **Error Handling**: Gracefully handles server errors and timeouts

**Please use responsibly and respect website terms of service!**

## 🐛 Troubleshooting

### Common Issues

1. **"Permission denied" errors**:
   - Check robots.txt compliance
   - Some sites block crawlers entirely

2. **SSL/HTTPS errors**:
   - Some older sites have SSL certificate issues
   - Try the HTTP version if available

3. **Encoding errors**:
   - The crawler handles most encoding issues automatically
   - Some very old sites may still cause problems

4. **Memory usage**:
   - Large crawls can consume significant memory
   - Reduce `--max-pages` for large sites

### Getting Help

If you encounter issues:
1. Run with `--test` to verify basic functionality
2. Try crawling a simple site like `https://example.com`
3. Check your internet connection and firewall settings
4. Reduce crawl parameters for testing

## 🚀 Future Improvements & Next Steps

### Planned Enhancements
- [ ] **GUI Version**: PyQt or Tkinter interface for non-technical users
- [ ] **Web Dashboard**: Flask/Django web interface with real-time progress
- [ ] **Database Storage**: SQLite/PostgreSQL integration for large crawls
- [ ] **Advanced Filtering**: Content-type filtering, size limits
- [ ] **Parallel Crawling**: Multi-threading for faster crawling
- [ ] **Export Formats**: XML, Excel, PDF report generation
- [ ] **Visualization**: Network graphs of crawled sites
- [ ] **API Integration**: RESTful API for programmatic access

### Converting to Web/GUI Version

#### Web Version (Flask)
```python
# Add to requirements.txt: flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('crawler.html')

@app.route('/crawl', methods=['POST'])
def start_crawl():
    data = request.json
    crawler = WebCrawler(data['depth'], data['delay'], data['max_pages'])
    results = crawler.crawl(data['urls'])
    return jsonify([asdict(r) for r in results])
```

#### GUI Version (Tkinter)
```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CrawlerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        # Add URL entry, buttons, progress bars, results display
        pass
    
    def start_crawl(self):
        # Run crawler in separate thread to prevent UI freezing
        pass
```

### Advanced Features to Add

1. **Content Analysis**: Keyword extraction, sentiment analysis
2. **Image Extraction**: Download and catalog images found
3. **Social Media Integration**: Extract social media links and handles
4. **SEO Analysis**: Meta tags, heading structure, page speed insights
5. **Duplicate Detection**: Identify and handle duplicate content
6. **Scheduled Crawling**: Cron-like scheduling for regular crawls
7. **Notification System**: Email alerts when crawls complete
8. **Data Validation**: Verify email addresses and phone numbers

## 📜 License & Credits

This project was created as an educational tool and example of Python web scraping best practices. Feel free to modify and extend it for your needs.

**Acknowledgments:**
- Python Software Foundation for the excellent standard library
- The web scraping community for best practices and ethical guidelines
- robots.txt specification contributors for standardizing crawler behavior

---

**⚠️ Disclaimer**: Always respect website terms of service and robots.txt files. This tool is for educational and legitimate business purposes only. Users are responsible for complying with applicable laws and website policies.

**🤝 Contributing**: Feel free to submit issues, feature requests, or pull requests to improve this crawler!
