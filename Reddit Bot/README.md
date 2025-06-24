# Reddit Bot 🤖

A comprehensive Reddit automation tool that monitors subreddits, responds to posts based on keywords, and provides detailed analytics. This bot is designed for educational purposes and community engagement while respecting Reddit's API guidelines and rate limits.

## 📋 Project Description

This Reddit Bot automatically monitors multiple subreddits for posts containing specific keywords and can respond with customizable templates. It includes features like sentiment analysis, rate limiting, persistent storage, and comprehensive logging to ensure responsible and effective Reddit interaction.

## ✨ Features

- **Multi-Subreddit Monitoring**: Monitor multiple subreddits simultaneously
- **Keyword Detection**: Automatically detect posts containing specified keywords
- **Smart Responses**: Generate contextual responses using customizable templates
- **Sentiment Analysis**: Basic sentiment analysis of posts (positive/negative/neutral)
- **Rate Limiting**: Built-in rate limiting to respect Reddit's API guidelines
- **Persistent Storage**: SQLite database to track processed posts and statistics
- **Comprehensive Logging**: Detailed logging with both file and console output
- **Dry Run Mode**: Test the bot without actually posting comments
- **Statistics Dashboard**: Track bot performance and activity over time
- **Error Handling**: Robust error handling for network issues and API errors
- **Continuous Operation**: Can run continuously with configurable cycle intervals

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Reddit account with API access
- Reddit application credentials (client ID and secret)

### Step 1: Install Dependencies

```bash
pip install praw prawcore
```

### Step 2: Create Reddit Application

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Note down your client ID and client secret

### Step 3: Download the Bot

Save the `main.py` file to your desired directory.

### Step 4: Create Configuration File

Run the bot with the `--create-config` flag to generate a sample configuration:

```bash
python main.py --create-config
```

This creates a `config.json` file that you need to edit with your credentials:

```json
{
  "client_id": "your_reddit_app_client_id",
  "client_secret": "your_reddit_app_client_secret",
  "user_agent": "RedditBot/1.0.0 (by /u/yourusername)",
  "username": "your_reddit_username",
  "password": "your_reddit_password",
  "target_subreddits": ["test", "learnpython", "programming"],
  "keywords": ["python", "bot", "automation", "help"],
  "response_templates": [
    "Thanks for mentioning {keywords}! Here's some helpful information...",
    "I noticed you mentioned {keywords}. Hope this helps!",
    "Great post about {keywords}! Thanks for sharing."
  ],
  "max_comments_per_hour": 10,
  "min_delay_between_actions": 60,
  "dry_run": true
}
```

### Step 5: Configure Your Bot

Edit the `config.json` file with:
- Your Reddit API credentials
- Target subreddits to monitor
- Keywords to look for
- Custom response templates
- Rate limiting preferences

## 🚀 How to Run

### Basic Usage

```bash
# Run the bot continuously (default mode)
python main.py

# Run once and exit
python main.py --single-run

# Run in dry-run mode (no actual comments)
python main.py --dry-run

# Show bot statistics
python main.py --stats

# Use custom configuration file
python main.py --config my_config.json
```

### Command Line Options

- `--config`, `-c`: Specify configuration file path (default: config.json)
- `--create-config`: Create a sample configuration file
- `--single-run`: Run once instead of continuously
- `--stats`: Show bot statistics
- `--dry-run`: Run in dry-run mode (no actual comments)

## 📊 Example Usage

### Configuration Example

```json
{
  "target_subreddits": ["learnpython", "Python", "programming"],
  "keywords": ["beginner", "help", "tutorial", "learning"],
  "response_templates": [
    "Welcome to the Python community! For {keywords}, I recommend checking out the official documentation.",
    "Great question about {keywords}! Here are some resources that might help..."
  ],
  "max_comments_per_hour": 5,
  "dry_run": false
}
```

### Sample Output

```
2025-06-24 10:30:15 - INFO - Successfully connected to Reddit as YourBot
2025-06-24 10:30:16 - INFO - Starting monitoring cycle
2025-06-24 10:30:20 - INFO - Found keywords ['python', 'help'] in post abc123 (sentiment: neutral)
2025-06-24 10:30:25 - INFO - Successfully commented on post abc123
2025-06-24 10:30:30 - INFO - Subreddit learnpython: {'processed': 15, 'commented': 2, 'errors': 0}
2025-06-24 10:30:45 - INFO - Monitoring cycle complete. Total stats: {'processed': 45, 'commented': 3, 'errors': 0}
```

### Statistics Example

```bash
$ python main.py --stats

=== Reddit Bot Statistics ===
Total posts processed: 1,247
Total comments made: 89
Total errors: 3

Average per day:
  Posts processed: 178.1
  Comments made: 12.7
  Errors: 0.4
```

## 📁 Generated Files

The bot creates several files during operation:

- `reddit_bot.db`: SQLite database storing processed posts and statistics
- `reddit_bot.log`: Detailed log file of all bot activities
- `config.json`: Configuration file (created with --create-config)

## ⚠️ Important Notes

### Reddit API Guidelines

- **Rate Limiting**: The bot includes built-in rate limiting (default: 10 comments/hour)
- **Respectful Usage**: Always use descriptive user agents and avoid spam
- **Community Rules**: Ensure your bot complies with subreddit rules
- **Testing**: Always test with dry-run mode first

### Best Practices

1. Start with `dry_run: true` to test your configuration
2. Use conservative rate limits initially
3. Monitor logs for errors and adjust accordingly
4. Ensure your responses add value to discussions
5. Regularly check that your bot isn't being downvoted heavily

## 🔧 Customization

### Adding New Features

The bot is designed to be easily extensible:

```python
# Add custom sentiment analysis
def advanced_sentiment_analysis(self, text):
    # Implement your custom logic
    pass

# Add custom response logic
def generate_smart_response(self, post):
    # Implement context-aware responses
    pass
```

### Configuration Options

- `max_comments_per_hour`: Maximum comments per hour (default: 10)
- `min_delay_between_actions`: Minimum seconds between actions (default: 60)
- `dry_run`: Test mode without actual posting (default: true)
- `target_subreddits`: List of subreddits to monitor
- `keywords`: Keywords to search for in posts
- `response_templates`: Template responses with {keywords} placeholder

## 🧪 Testing

The bot includes basic unit tests at the bottom of the main file. To run tests:

1. Uncomment the test section at the bottom of `main.py`
2. Run: `python main.py` (will run tests instead of main program)

Example test:
```python
def test_contains_keywords(self):
    bot = RedditBot(self.config)
    result = bot.contains_keywords("I love python programming")
    self.assertIn("python", result)
```

## 🌐 Converting to Web/GUI Version

### Web Version (Flask)

To convert this to a web application:

1. Install Flask: `pip install flask`
2. Create a web interface for configuration
3. Add endpoints for statistics and control
4. Run the bot in a separate thread

```python
from flask import Flask, render_template, jsonify
import threading

app = Flask(__name__)
bot_thread = None

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    return jsonify(bot.get_stats())

@app.route('/api/start')
def start_bot():
    global bot_thread
    if not bot_thread or not bot_thread.is_alive():
        bot_thread = threading.Thread(target=bot.run_continuous)
        bot_thread.start()
    return jsonify({'status': 'started'})
```

### GUI Version (Tkinter)

For a desktop GUI application:

1. Use tkinter (included with Python)
2. Create forms for configuration
3. Add real-time
