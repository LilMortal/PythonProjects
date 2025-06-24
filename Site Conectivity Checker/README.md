# Site Connectivity Checker

A comprehensive Python tool to check website connectivity, health status, and performance metrics. This tool performs multiple layers of connectivity testing including DNS resolution, port accessibility, SSL certificate validation, and HTTP response analysis.

## 🚀 Features

- **DNS Resolution Testing** - Verify domain name resolution and measure response times
- **Port Connectivity Checking** - Test if HTTP/HTTPS ports are accessible
- **SSL Certificate Validation** - Check certificate validity, expiration dates, and issuer information
- **HTTP Response Analysis** - Get detailed HTTP status codes, response times, and headers
- **Batch Processing** - Check multiple sites at once from command line or file
- **Multiple Output Formats** - Generate reports in text or JSON format
- **Comprehensive Error Handling** - Detailed error messages for troubleshooting
- **Performance Metrics** - Response times, DNS resolution times, and connection speeds
- **Cross-Platform** - Works on Windows, macOS, and Linux

## 📋 Requirements

- **Python Version**: 3.8 or higher
- **Dependencies**: Uses only Python standard library (no external packages required!)

## 🛠️ Installation

1. **Clone or download** the project files:
   ```bash
   # Download the main.py file to your desired directory
   curl -O https://raw.githubusercontent.com/your-repo/site-checker/main/main.py
   ```

2. **Make the script executable** (Linux/macOS):
   ```bash
   chmod +x main.py
   ```

3. **Verify Python installation**:
   ```bash
   python --version  # Should show Python 3.8+
   ```

That's it! No additional dependencies needed.

## 🎯 How to Run

### Basic Usage

Check a single website:
```bash
python main.py google.com
```

Check multiple websites:
```bash
python main.py google.com github.com stackoverflow.com
```

### Advanced Usage

**Set custom timeout:**
```bash
python main.py -t 15 google.com
```

**Generate JSON report:**
```bash
python main.py --format json --output results.json google.com
```

**Batch check from file:**
```bash
python main.py --batch sites.txt
```

**Custom User-Agent:**
```bash
python main.py --user-agent "MyBot/1.0" example.com
```

### Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-t, --timeout` | Request timeout in seconds (default: 10) | `-t 15` |
| `-o, --output` | Save results to file | `-o report.txt` |
| `--format` | Output format: text or json | `--format json` |
| `--batch` | File with URLs (one per line) | `--batch sites.txt` |
| `--user-agent` | Custom User-Agent string | `--user-agent "MyBot/1.0"` |

## 📝 Example Usage

### Single Site Check
```bash
$ python main.py https://github.com

Checking connectivity for 1 site(s)...

[1/1] Checking: https://github.com
  → Checking DNS resolution...
    ✓ Resolved to: 140.82.114.4
  → Checking port 443 connectivity...
    ✓ Port 443 is accessible
  → Checking SSL certificate...
    ✓ SSL certificate valid (89 days remaining)
  → Checking HTTP response...
    ✓ HTTP 200 (342ms)
  → ✓ ONLINE

============================================================
SITE CONNECTIVITY REPORT
============================================================
Generated: 2025-06-24 10:30:15
Sites checked: 1

1. https://github.com
-----------------------
Status: ✓ ONLINE
IP Address: 140.82.114.4
DNS Resolution: 45.2ms
HTTP Status: 200
Response Time: 342ms
Server: GitHub.com
SSL Certificate: Valid (89 days)
```

### Batch File Example

Create a file named `sites.txt`:
```
google.com
github.com
stackoverflow.com
badexample.notarealsite
```

Run batch check:
```bash
$ python main.py --batch sites.txt --format json -o results.json

Loaded 4 URLs from sites.txt
Checking connectivity for 4 site(s)...

[1/4] Checking: https://google.com
  → ✓ ONLINE

[2/4] Checking: https://github.com
  → ✓ ONLINE

[3/4] Checking: https://stackoverflow.com
  → ✓ ONLINE

[4/4] Checking: https://badexample.notarealsite
  → ✗ OFFLINE

Results saved to: results.json
1 site(s) failed connectivity check.
```

## 🧪 Testing

Run the built-in unit tests:
```bash
python main.py --test
```

## 📊 Output Formats

### Text Format (Default)
- Human-readable format
- Easy to scan and understand
- Perfect for terminal output

### JSON Format
- Machine-readable structured data
- Includes all raw metrics
- Ideal for integration with other tools

Example JSON output structure:
```json
{
  "url": "https://example.com",
  "hostname": "example.com",
  "timestamp": "2025-06-24T10:30:15",
  "overall_success": true,
  "checks": {
    "dns": {
      "success": true,
      "ip_address": "93.184.216.34",
      "resolution_time_ms": 45.2
    },
    "port": {
      "success": true,
      "port": 443,
      "connection_time_ms": 120.5
    },
    "ssl": {
      "success": true,
      "days_until_expiry": 89,
      "is_expired": false
    },
    "http": {
      "success": true,
      "status_code": 200,
      "response_time_ms": 342.1,
      "content_type": "text/html"
    }
  }
}
```

## 🔧 Configuration

The tool can be customized through command-line arguments or by modifying the `SiteConnectivityChecker` class:

- **Timeout Settings**: Adjust connection timeouts for slow networks
- **User-Agent**: Customize the User-Agent string for specific requirements
- **SSL Validation**: Certificate checking can be extended for custom requirements

## 🚨 Troubleshooting

### Common Issues

**"DNS resolution failed"**
- Check if the domain name is correct
- Verify internet connection
- Try using a different DNS resolver

**"Port not accessible"**
- Website might be down
- Firewall blocking connections
- Try different ports (80 for HTTP, 443 for HTTPS)

**"SSL certificate errors"**
- Certificate might be expired
- Self-signed certificates not trusted
- Certificate chain issues

**"HTTP errors"**
- 404: Page not found
- 403: Access forbidden
- 500: Server error

### Debug Mode

For detailed debugging, modify the timeout and add verbose output:
```bash
python main.py -t 30 your-site.com
```

## 🎨 Converting to Web/GUI Version

### Web Version (Flask)
To convert this to a web application:

1. Install Flask: `pip install flask`
2. Create a web interface that calls the `SiteConnectivityChecker` class
3. Display results in HTML tables with CSS styling
4. Add AJAX for real-time updates

### GUI Version (Tkinter)
For a desktop GUI application:

1. Use Python's built-in `tkinter` library
2. Create input fields for URLs
3. Add progress bars for real-time feedback
4. Display results in a tree view or table widget

### Example Web Integration:
```python
from flask import Flask, render_template, request, jsonify
from main import SiteConnectivityChecker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_site():
    url = request.json['url']
    checker = SiteConnectivityChecker()
    result = checker.comprehensive_check(url)
    return jsonify(result)
```

## 🔮 Future Improvements

### Planned Features
- **Historical Tracking**: Store check results in a database for trend analysis
- **Monitoring Mode**: Continuous monitoring with alerts
- **Email Notifications**: Send alerts when sites go down
- **Performance Graphs**: Visualize response times over time
- **Custom Checks**: User-defined success criteria
- **API Endpoints**: RESTful API for integration
- **Docker Support**: Containerized deployment
- **Configuration Files**: YAML/JSON config files for advanced settings

### Enhancement Ideas
- **Multi-threading**: Parallel checks for faster batch processing
- **Proxy Support**: Check sites through different proxy servers
- **Mobile Optimization**: Responsive web interface
- **Slack/Discord Integration**: Send notifications to team channels
- **Custom Report Templates**: Branded reports for clients
- **Geographic Testing**: Check from multiple locations worldwide

## 📜 License

This project is released under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- Built with Python's excellent standard library
- Inspired by network monitoring tools like Pingdom and UptimeRobot
- Thanks to the Python community for continuous improvement of networking libraries

## 👥 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the example usage patterns
3. Run the built-in tests to verify functionality
4. Open an issue with detailed error messages and system information

---

**Version**: 1.0.0  
**Last Updated**: June 2025  
**Python Compatibility**: 3.8+  
**Platform Support**: Windows, macOS, Linux
