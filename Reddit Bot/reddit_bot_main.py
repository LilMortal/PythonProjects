#!/usr/bin/env python3
"""
Reddit Bot - A comprehensive Reddit automation tool
Author: AI Assistant
Version: 1.0.0
Python Version: 3.8+

This bot can monitor subreddits, respond to posts, analyze sentiment,
and perform various Reddit-related automation tasks.
"""

import praw
import prawcore
import time
import json
import logging
import re
import random
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
import argparse
import sys
import os
from collections import defaultdict


# Configuration and Data Classes
@dataclass
class BotConfig:
    """Configuration class for Reddit Bot"""
    client_id: str
    client_secret: str
    user_agent: str
    username: str
    password: str
    target_subreddits: List[str]
    keywords: List[str]
    response_templates: List[str]
    max_comments_per_hour: int = 10
    min_delay_between_actions: int = 60
    dry_run: bool = False


class RedditBot:
    """
    A comprehensive Reddit bot for monitoring and interacting with Reddit content.
    
    Features:
    - Monitor multiple subreddits for specific keywords
    - Auto-respond to posts and comments
    - Sentiment analysis of posts
    - Rate limiting and spam prevention
    - Persistent storage of processed posts
    - Comprehensive logging
    """
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.reddit = None
        self.db_connection = None
        self.processed_posts: Set[str] = set()
        self.comment_count = 0
        self.last_comment_time = datetime.now()
        
        # Setup logging
        self.setup_logging()
        
        # Initialize database
        self.init_database()
        
        # Load processed posts from database
        self.load_processed_posts()
        
        # Initialize Reddit connection
        self.init_reddit_connection()
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('reddit_bot.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def init_database(self):
        """Initialize SQLite database for persistent storage"""
        try:
            self.db_connection = sqlite3.connect('reddit_bot.db')
            cursor = self.db_connection.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_posts (
                    post_id TEXT PRIMARY KEY,
                    subreddit TEXT,
                    title TEXT,
                    processed_at TIMESTAMP,
                    action_taken TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bot_stats (
                    date TEXT PRIMARY KEY,
                    posts_processed INTEGER,
                    comments_made INTEGER,
                    errors_encountered INTEGER
                )
            ''')
            
            self.db_connection.commit()
            self.logger.info("Database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            sys.exit(1)
    
    def init_reddit_connection(self):
        """Initialize Reddit API connection"""
        try:
            self.reddit = praw.Reddit(
                client_id=self.config.client_id,
                client_secret=self.config.client_secret,
                user_agent=self.config.user_agent,
                username=self.config.username,
                password=self.config.password
            )
            
            # Test the connection
            self.reddit.user.me()
            self.logger.info(f"Successfully connected to Reddit as {self.config.username}")
            
        except prawcore.exceptions.ResponseException as e:
            self.logger.error(f"Reddit authentication failed: {e}")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"Reddit connection failed: {e}")
            sys.exit(1)
    
    def load_processed_posts(self):
        """Load previously processed posts from database"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT post_id FROM processed_posts WHERE processed_at > ?",
                (datetime.now() - timedelta(days=7),)  # Only load recent posts
            )
            self.processed_posts = {row[0] for row in cursor.fetchall()}
            self.logger.info(f"Loaded {len(self.processed_posts)} previously processed posts")
        except Exception as e:
            self.logger.error(f"Failed to load processed posts: {e}")
    
    def save_processed_post(self, post_id: str, subreddit: str, title: str, action: str):
        """Save processed post to database"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO processed_posts VALUES (?, ?, ?, ?, ?)",
                (post_id, subreddit, title, datetime.now(), action)
            )
            self.db_connection.commit()
            self.processed_posts.add(post_id)
        except Exception as e:
            self.logger.error(f"Failed to save processed post: {e}")
    
    def contains_keywords(self, text: str) -> List[str]:
        """Check if text contains any of the configured keywords"""
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in self.config.keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Simple sentiment analysis based on keyword matching.
        In a real implementation, you might use NLTK or other libraries.
        """
        positive_words = ['good', 'great', 'awesome', 'excellent', 'amazing', 'love', 'best']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'sucks']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def generate_response(self, post_title: str, post_content: str, keywords_found: List[str]) -> str:
        """Generate an appropriate response based on the post content"""
        templates = self.config.response_templates
        
        if not templates:
            return f"Thanks for mentioning {', '.join(keywords_found)}! This is an automated response."
        
        # Select a random template and customize it
        template = random.choice(templates)
        
        # Replace placeholders in template
        response = template.replace("{keywords}", ", ".join(keywords_found))
        response = response.replace("{title}", post_title[:50] + "..." if len(post_title) > 50 else post_title)
        
        return response
    
    def can_make_comment(self) -> bool:
        """Check if bot can make a comment based on rate limiting"""
        now = datetime.now()
        
        # Reset counter if it's been more than an hour
        if now - self.last_comment_time > timedelta(hours=1):
            self.comment_count = 0
        
        # Check if we've exceeded the hourly limit
        if self.comment_count >= self.config.max_comments_per_hour:
            return False
        
        # Check minimum delay between actions
        if now - self.last_comment_time < timedelta(seconds=self.config.min_delay_between_actions):
            return False
        
        return True
    
    def make_comment(self, submission, response_text: str) -> bool:
        """Make a comment on a Reddit submission"""
        if self.config.dry_run:
            self.logger.info(f"[DRY RUN] Would comment on {submission.id}: {response_text}")
            return True
        
        try:
            if not self.can_make_comment():
                self.logger.info("Rate limit reached, skipping comment")
                return False
            
            submission.reply(response_text)
            self.comment_count += 1
            self.last_comment_time = datetime.now()
            self.logger.info(f"Successfully commented on post {submission.id}")
            return True
            
        except prawcore.exceptions.Forbidden:
            self.logger.error(f"Permission denied to comment on {submission.id}")
            return False
        except prawcore.exceptions.RateLimitExceeded as e:
            self.logger.warning(f"Rate limit exceeded: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to comment on {submission.id}: {e}")
            return False
    
    def process_submission(self, submission) -> bool:
        """Process a single Reddit submission"""
        try:
            # Skip if already processed
            if submission.id in self.processed_posts:
                return False
            
            # Combine title and selftext for keyword analysis
            full_text = f"{submission.title} {submission.selftext}"
            keywords_found = self.contains_keywords(full_text)
            
            if not keywords_found:
                self.save_processed_post(submission.id, submission.subreddit.display_name, 
                                       submission.title, "no_keywords")
                return False
            
            # Analyze sentiment
            sentiment = self.analyze_sentiment(full_text)
            
            self.logger.info(f"Found keywords {keywords_found} in post {submission.id} "
                           f"(sentiment: {sentiment})")
            
            # Generate and post response
            response = self.generate_response(submission.title, submission.selftext, keywords_found)
            
            if self.make_comment(submission, response):
                action = f"commented_keywords_{','.join(keywords_found)}_sentiment_{sentiment}"
                self.save_processed_post(submission.id, submission.subreddit.display_name,
                                       submission.title, action)
                return True
            else:
                self.save_processed_post(submission.id, submission.subreddit.display_name,
                                       submission.title, "comment_failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error processing submission {submission.id}: {e}")
            return False
    
    def monitor_subreddit(self, subreddit_name: str, limit: int = 25) -> Dict[str, int]:
        """Monitor a single subreddit for new posts"""
        stats = {"processed": 0, "commented": 0, "errors": 0}
        
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Monitor both new and hot posts
            submissions = list(subreddit.new(limit=limit//2)) + list(subreddit.hot(limit=limit//2))
            
            for submission in submissions:
                try:
                    stats["processed"] += 1
                    if self.process_submission(submission):
                        stats["commented"] += 1
                    
                    # Small delay between processing posts
                    time.sleep(2)
                    
                except Exception as e:
                    stats["errors"] += 1
                    self.logger.error(f"Error processing submission in {subreddit_name}: {e}")
            
            self.logger.info(f"Subreddit {subreddit_name}: {stats}")
            
        except prawcore.exceptions.Forbidden:
            self.logger.error(f"Access denied to subreddit {subreddit_name}")
            stats["errors"] += 1
        except prawcore.exceptions.NotFound:
            self.logger.error(f"Subreddit {subreddit_name} not found")
            stats["errors"] += 1
        except Exception as e:
            self.logger.error(f"Error monitoring subreddit {subreddit_name}: {e}")
            stats["errors"] += 1
        
        return stats
    
    def run_monitoring_cycle(self):
        """Run one complete monitoring cycle across all configured subreddits"""
        self.logger.info("Starting monitoring cycle")
        total_stats = defaultdict(int)
        
        for subreddit_name in self.config.target_subreddits:
            stats = self.monitor_subreddit(subreddit_name)
            for key, value in stats.items():
                total_stats[key] += value
            
            # Delay between subreddits to avoid overwhelming Reddit's servers
            time.sleep(10)
        
        self.logger.info(f"Monitoring cycle complete. Total stats: {dict(total_stats)}")
        return dict(total_stats)
    
    def run_continuous(self, cycle_interval: int = 300):
        """Run the bot continuously with specified interval between cycles"""
        self.logger.info(f"Starting continuous monitoring (cycle every {cycle_interval} seconds)")
        
        try:
            while True:
                stats = self.run_monitoring_cycle()
                
                # Save daily stats
                self.save_daily_stats(stats)
                
                self.logger.info(f"Sleeping for {cycle_interval} seconds...")
                time.sleep(cycle_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in continuous mode: {e}")
            raise
    
    def save_daily_stats(self, stats: Dict[str, int]):
        """Save daily statistics to database"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            cursor = self.db_connection.cursor()
            
            # Get existing stats for today
            cursor.execute("SELECT * FROM bot_stats WHERE date = ?", (today,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute(
                    "UPDATE bot_stats SET posts_processed = posts_processed + ?, "
                    "comments_made = comments_made + ?, errors_encountered = errors_encountered + ? "
                    "WHERE date = ?",
                    (stats.get('processed', 0), stats.get('commented', 0), 
                     stats.get('errors', 0), today)
                )
            else:
                # Insert new record
                cursor.execute(
                    "INSERT INTO bot_stats VALUES (?, ?, ?, ?)",
                    (today, stats.get('processed', 0), stats.get('commented', 0), 
                     stats.get('errors', 0))
                )
            
            self.db_connection.commit()
        except Exception as e:
            self.logger.error(f"Failed to save daily stats: {e}")
    
    def get_stats(self, days: int = 7) -> Dict:
        """Get bot statistics for the last N days"""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT * FROM bot_stats WHERE date >= ? ORDER BY date DESC",
                ((datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),)
            )
            
            stats = []
            total_processed = 0
            total_comments = 0
            total_errors = 0
            
            for row in cursor.fetchall():
                date, processed, comments, errors = row
                stats.append({
                    'date': date,
                    'processed': processed,
                    'comments': comments,
                    'errors': errors
                })
                total_processed += processed
                total_comments += comments
                total_errors += errors
            
            return {
                'daily_stats': stats,
                'totals': {
                    'processed': total_processed,
                    'comments': total_comments,
                    'errors': total_errors
                },
                'averages': {
                    'processed_per_day': total_processed / max(len(stats), 1),
                    'comments_per_day': total_comments / max(len(stats), 1),
                    'errors_per_day': total_errors / max(len(stats), 1)
                }
            }
        except Exception as e:
            self.logger.error(f"Failed to get stats: {e}")
            return {}
    
    def cleanup(self):
        """Cleanup resources"""
        if self.db_connection:
            self.db_connection.close()
        self.logger.info("Bot cleanup completed")


def load_config_from_file(config_path: str) -> BotConfig:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return BotConfig(**config_data)
    except FileNotFoundError:
        print(f"Configuration file {config_path} not found!")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in configuration file: {e}")
        return None
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None


def create_sample_config():
    """Create a sample configuration file"""
    sample_config = {
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
    
    with open('config.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print("Sample configuration file created: config.json")
    print("Please edit this file with your Reddit API credentials and preferences.")


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="Reddit Bot - Automated Reddit Interaction Tool")
    parser.add_argument('--config', '-c', default='config.json', 
                       help='Configuration file path (default: config.json)')
    parser.add_argument('--create-config', action='store_true',
                       help='Create a sample configuration file')
    parser.add_argument('--single-run', action='store_true',
                       help='Run once instead of continuously')
    parser.add_argument('--stats', action='store_true',
                       help='Show bot statistics')
    parser.add_argument('--dry-run', action='store_true',
                       help='Run in dry-run mode (no actual comments)')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    # Load configuration
    config = load_config_from_file(args.config)
    if not config:
        print("Failed to load configuration. Use --create-config to create a sample.")
        return
    
    # Override dry-run if specified in command line
    if args.dry_run:
        config.dry_run = True
    
    # Initialize bot
    try:
        bot = RedditBot(config)
        
        if args.stats:
            # Show statistics
            stats = bot.get_stats()
            print("\n=== Reddit Bot Statistics ===")
            print(f"Total posts processed: {stats['totals']['processed']}")
            print(f"Total comments made: {stats['totals']['comments']}")
            print(f"Total errors: {stats['totals']['errors']}")
            print(f"\nAverage per day:")
            print(f"  Posts processed: {stats['averages']['processed_per_day']:.1f}")
            print(f"  Comments made: {stats['averages']['comments_per_day']:.1f}")
            print(f"  Errors: {stats['averages']['errors_per_day']:.1f}")
            
        elif args.single_run:
            # Run once
            bot.run_monitoring_cycle()
        else:
            # Run continuously
            bot.run_continuous()
            
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Bot failed with error: {e}")
    finally:
        if 'bot' in locals():
            bot.cleanup()


if __name__ == "__main__":
    main()


# Simple unit tests (uncomment to run)
"""
import unittest
from unittest.mock import Mock, patch

class TestRedditBot(unittest.TestCase):
    def setUp(self):
        self.config = BotConfig(
            client_id="test",
            client_secret="test",
            user_agent="test",
            username="test",
            password="test",
            target_subreddits=["test"],
            keywords=["python", "bot"],
            response_templates=["Test response with {keywords}"],
            dry_run=True
        )
    
    def test_contains_keywords(self):
        bot = RedditBot(self.config)
        result = bot.contains_keywords("I love python programming")
        self.assertIn("python", result)
    
    def test_sentiment_analysis(self):
        bot = RedditBot(self.config)
        self.assertEqual(bot.analyze_sentiment("This is great!"), "positive")
        self.assertEqual(bot.analyze_sentiment("This is terrible!"), "negative")
        self.assertEqual(bot.analyze_sentiment("This is okay."), "neutral")
    
    def test_response_generation(self):
        bot = RedditBot(self.config)
        response = bot.generate_response("Test Post", "Content", ["python"])
        self.assertIn("python", response)

if __name__ == "__main__":
    # To run tests, uncomment the next line
    # unittest.main()
    main()
"""