# Content Aggregator

A powerful and flexible RSS feed aggregator that fetches, filters, and displays articles from multiple news sources and blogs. Stay updated with your favorite content sources in one convenient place.

## Description

Content Aggregator is a command-line tool that automatically fetches articles from RSS and Atom feeds, allowing you to aggregate content from multiple sources like news websites, blogs, and other publications. It provides filtering capabilities, export options, and statistical analysis of your aggregated content.

Perfect for developers, researchers, journalists, or anyone who wants to stay informed by monitoring multiple content sources efficiently.

## Features

- **Multi-format Support**: Handles both RSS 2.0 and Atom feed formats
- **Flexible Feed Management**: Load feeds from JSON configuration files or use built-in defaults
- **Smart Filtering**: Filter articles by keywords, categories, or sources
- **Export Capabilities**: Export articles to JSON or CSV formats
- **Statistics Dashboard**: View detailed statistics about your aggregated content
- **Error Handling**: Robust error handling for network issues and malformed feeds
- **Rate Limiting**: Respectful delays between requests to avoid overwhelming servers
- **HTML Cleanup**: Automatically removes HTML tags from article descriptions
- **Customizable Display**: Control how many articles to display and fetch per feed

## Requirements

- **Python Version**: Python 3.8 or higher
- **Dependencies**: Uses only Python standard library (no external dependencies required!)

## Installation

1. **Clone or download** the project files:
   ```bash
   # If using git
   git clone <repository-url>
   cd content-aggregator
   
   # Or simply download main.py and place it in your desired directory
   ```

2. **Verify Python version**:
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

3. **Make the script executable** (optional, on Unix-like systems):
   ```bash
   chmod +x main.py
   ```

## Configuration

### Setting Up Feed Sources

1. **Create a sample feeds configuration**:
   ```bash
   python main.py --create-sample
   ```
   This creates a `feeds.json` file with default feed sources.

2. **Customize your feeds** by editing `feeds.json`:
   ```json
   {
     "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
     "TechCrunch": "https://techcrunch.com/feed/",
     "Your Blog": "https://yourblog.com/rss",
     "Custom Source": "https://example.com/feed.xml"
   }
   ```

## Usage

### Basic Usage

Run the aggregator with default settings:
```bash
python main.py
```

This will:
- Load feeds from `feeds.json` (or use defaults if file doesn't exist)
- Fetch up to 10 articles per feed
- Display the first 20 articles

### Command-Line Options

```bash
python main.py [OPTIONS]
```

#### Options:

- `--feeds FILE` or `-f FILE`: Specify custom feeds JSON file
- `--keyword WORD` or `-k WORD`: Filter articles containing keyword
- `--category CAT` or `-c CAT`: Filter articles by category
- `--source SOURCE` or `-s SOURCE`: Filter articles by source name
- `--limit N` or `-l N`: Maximum articles to display (default: 20)
- `--export FILE` or `-e FILE`: Export articles to file
- `--format FORMAT`: Export format - 'json' or 'csv' (default: json)
- `--max-per-feed N`: Maximum articles per feed (default: 10)
- `--stats`: Show statistics about fetched articles
- `--create-sample`: Create sample feeds.json file

### Example Commands

1. **Basic fetch and display**:
   ```bash
   python main.py
   ```

2. **Filter by keyword**:
   ```bash
   python main.py --keyword "artificial intelligence"
   ```

3. **Filter by source**:
   ```bash
   python main.py --source "TechCrunch"
   ```

4. **Export articles to JSON**:
   ```bash
   python main.py --export articles.json --format json
   ```

5. **Show statistics**:
   ```bash
   python main.py --stats
   ```

6. **Limit display and fetch amounts**:
   ```bash
   python main.py --limit 10 --max-per-feed 5
   ```

7. **Use custom feeds file**:
   ```bash
   python main.py --feeds my_custom_feeds.json
   ```

8. **Complex filtering and export**:
   ```bash
   python main.py --keyword "python" --limit 15 --export python_articles.csv --format csv --stats
   ```

### Sample Output

```
Fetching articles from 4 feeds...
[1/4] Fetching from BBC News...
  ✓ Found 10 articles
[2/4] Fetching from TechCrunch...
  ✓ Found 10 articles
[3/4] Fetching from Reuters Tech...
  ✓ Found 8 articles
[4/4] Fetching from Hacker News...
  ✓ Found 10 articles

Total articles fetched: 38

================================================================================
DISPLAYING 20 OF 38 ARTICLES
================================================================================

[1] Breaking: New AI Breakthrough Announced
Source: TechCrunch
Category: Technology
Published: Mon, 25 Jun 2024 10:30:00 GMT
Description: Researchers have developed a new machine learning algorithm that...
Link: https://techcrunch.com/2024/06/25/ai-breakthrough
--------------------------------------------------------------------------------

[2] Global Markets React to Economic News
Source: BBC News
Published: Mon, 25 Jun 2024 09:15:00 GMT
Description: Stock markets worldwide showed mixed reactions following...
Link: https://bbc.com/news/business-12345678
--------------------------------------------------------------------------------
```

## File Structure

```
content-aggregator/
├── main.py              # Main application file
├── feeds.json           # Feed configuration (created by --create-sample)
├── README.md           # This file
└── exported_files/     # Directory for exported articles (created as needed)
    ├── articles.json
    └── articles.csv
```

## Error Handling

The application handles various error scenarios gracefully:

- **Network timeouts**: 10-second timeout per feed request
- **Invalid URLs**: Skips malformed or unreachable feeds
- **Malformed XML**: Continues processing other feeds if one fails
- **Missing files**: Uses default feeds if configuration file is missing
- **Permission errors**: Provides clear error messages for file operations

## Advanced Features

### Custom Feed Parser

The application includes a robust feed parser that:
- Automatically detects RSS vs Atom formats
- Handles various XML namespaces
- Cleans HTML content from descriptions
- Extracts metadata like publication dates and categories

### Statistics Dashboard

Use `--stats` to see detailed analytics:
- Total articles fetched
- Articles per source
- Category distribution
- Articles with categorization

### Export Formats

**JSON Export** (default):
```json
[
  {
    "title": "Article Title",
    "link": "https://example.com/article",
    "description": "Article description...",
    "pub_date": "Mon, 25 Jun 2024 10:30:00 GMT",
    "source": "Source Name",
    "category": "Technology"
  }
]
```

**CSV Export**:
```csv
title,link,description,pub_date,source,category
"Article Title","https://example.com","Description...","Mon, 25 Jun 2024","Source","Tech"
```

## Troubleshooting

### Common Issues

1. **"No articles found"**:
   - Check your internet connection
   - Verify feed URLs are valid and accessible
   - Some feeds might be temporarily unavailable

2. **"Error parsing XML"**:
   - The feed might have malformed XML
   - Try fetching individual feeds to identify the problematic one

3. **"Permission denied" when exporting**:
   - Check write permissions in the target directory
   - Ensure the export path is valid

4. **Slow performance**:
   - Reduce `--max-per-feed` value
   - Use `--limit` to display fewer articles
   - Some feeds might be slow to respond

### Finding RSS Feeds

Most websites provide RSS feeds. Common locations:
- `/rss.xml`
- `/feed.xml`
- `/rss/`
- `/feed/`

Look for RSS icons (🔶) on websites or check the page source for `<link rel="alternate" type="application/rss+xml">` tags.

## Future Improvements

### Planned Features
- **Web Interface**: Convert to a Flask/FastAPI web application
- **Database Storage**: Store articles in SQLite for persistence
- **Scheduled Fetching**: Cron-like scheduling for automatic updates
- **Email Notifications**: Send digest emails for new articles
- **Full-text Search**: Elasticsearch integration for advanced search
- **Duplicate Detection**: Identify and merge duplicate articles
- **Content Summarization**: AI-powered article summarization
- **Mobile App**: React Native or Flutter mobile application

### Enhancement Ideas
- **GUI Version**: Tkinter or PyQt desktop application
- **RSS Discovery**: Automatic RSS feed discovery from websites
- **Social Media Integration**: Twitter, Reddit feed support
- **Content Filtering**: Machine learning-based content classification
- **Reading List**: Save articles for later reading
- **OPML Support**: Import/export feed lists in OPML format
- **Webhook Support**: Real-time notifications via webhooks

## Converting to Web Application

To convert this to a web application:

1. **Install Flask**:
   ```bash
   pip install flask
   ```

2. **Create a basic web interface**:
   ```python
   from flask import Flask, render_template, request
   from main import ContentAggregator
   
   app = Flask(__name__)
   
   @app.route('/')
   def index():
       aggregator = ContentAggregator()
       # ... (implement web logic)
       return render_template('index.html', articles=articles)
   ```

3. **Add HTML templates** in `templates/` directory
4. **Add CSS styling** in `static/` directory

## Testing

Basic unit tests are included in the main file. To run them:

```python
# Uncomment the line in main.py:
# run_tests()

python main.py
```

For comprehensive testing, consider using pytest:
```bash
pip install pytest
pytest test_content_aggregator.py
```

## Contributing

Feel free to contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with Python's excellent standard library
- Inspired by RSS readers like Feedly and NewsBlur
- Thanks to the RSS/Atom specification maintainers
- Special thanks to all the websites providing RSS feeds

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the example commands and usage patterns
3. Ensure your Python version meets the requirements
4. Verify your internet connection and feed URLs

---

**Happy aggregating!** 📰✨
