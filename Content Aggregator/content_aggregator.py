#!/usr/bin/env python3
"""
Content Aggregator - A simple RSS feed aggregator
Fetches and displays articles from multiple RSS feeds with filtering and export options.

Author: Content Aggregator
Version: 1.0.0
Python Version: 3.8+
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import json
import csv
import re
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import argparse
import sys
import time


@dataclass
class Article:
    """Data class representing a news article."""
    title: str
    link: str
    description: str
    pub_date: str
    source: str
    category: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert article to dictionary."""
        return asdict(self)


class FeedParser:
    """RSS/Atom feed parser with error handling."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def fetch_feed(self, url: str) -> Optional[str]:
        """
        Fetch RSS feed content from URL.
        
        Args:
            url: RSS feed URL
            
        Returns:
            Feed content as string or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Content-Aggregator/1.0 (Python RSS Reader)',
                'Accept': 'application/rss+xml, application/xml, text/xml'
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                return response.read().decode('utf-8', errors='ignore')
                
        except urllib.error.URLError as e:
            print(f"Error fetching {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching {url}: {e}")
            return None
    
    def parse_rss(self, content: str, source_name: str) -> List[Article]:
        """
        Parse RSS feed content into Article objects.
        
        Args:
            content: RSS XML content
            source_name: Name of the source feed
            
        Returns:
            List of Article objects
        """
        articles = []
        
        try:
            root = ET.fromstring(content)
            
            # Handle RSS 2.0 format
            if root.tag == 'rss' or root.find('.//item') is not None:
                items = root.findall('.//item')
                for item in items:
                    article = self._parse_rss_item(item, source_name)
                    if article:
                        articles.append(article)
            
            # Handle Atom format
            elif root.tag.endswith('feed') or root.find('.//{http://www.w3.org/2005/Atom}entry') is not None:
                entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
                for entry in entries:
                    article = self._parse_atom_entry(entry, source_name)
                    if article:
                        articles.append(article)
                        
        except ET.ParseError as e:
            print(f"Error parsing XML for {source_name}: {e}")
        except Exception as e:
            print(f"Unexpected error parsing {source_name}: {e}")
            
        return articles
    
    def _parse_rss_item(self, item: ET.Element, source_name: str) -> Optional[Article]:
        """Parse RSS item element into Article."""
        try:
            title = self._get_text(item.find('title'), 'No Title')
            link = self._get_text(item.find('link'), '')
            description = self._get_text(item.find('description'), 'No Description')
            pub_date = self._get_text(item.find('pubDate'), '')
            category = self._get_text(item.find('category'), '')
            
            # Clean up description (remove HTML tags)
            description = self._clean_html(description)
            
            return Article(
                title=title,
                link=link,
                description=description[:300] + '...' if len(description) > 300 else description,
                pub_date=pub_date,
                source=source_name,
                category=category
            )
        except Exception as e:
            print(f"Error parsing RSS item: {e}")
            return None
    
    def _parse_atom_entry(self, entry: ET.Element, source_name: str) -> Optional[Article]:
        """Parse Atom entry element into Article."""
        try:
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            title = self._get_text(entry.find('atom:title', ns), 'No Title')
            link_elem = entry.find('atom:link', ns)
            link = link_elem.get('href', '') if link_elem is not None else ''
            
            summary = self._get_text(entry.find('atom:summary', ns), '')
            content = self._get_text(entry.find('atom:content', ns), '')
            description = summary or content or 'No Description'
            
            pub_date = self._get_text(entry.find('atom:published', ns), 
                                    self._get_text(entry.find('atom:updated', ns), ''))
            
            category_elem = entry.find('atom:category', ns)
            category = category_elem.get('term', '') if category_elem is not None else ''
            
            # Clean up description
            description = self._clean_html(description)
            
            return Article(
                title=title,
                link=link,
                description=description[:300] + '...' if len(description) > 300 else description,
                pub_date=pub_date,
                source=source_name,
                category=category
            )
        except Exception as e:
            print(f"Error parsing Atom entry: {e}")
            return None
    
    def _get_text(self, element: Optional[ET.Element], default: str = '') -> str:
        """Safely extract text from XML element."""
        return element.text.strip() if element is not None and element.text else default
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from text."""
        # Simple HTML tag removal
        clean = re.sub(r'<[^>]+>', '', text)
        # Clean up extra whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean


class ContentAggregator:
    """Main content aggregator class."""
    
    def __init__(self):
        self.parser = FeedParser()
        self.articles: List[Article] = []
        
        # Default feeds - you can modify these
        self.default_feeds = {
            'BBC News': 'http://feeds.bbci.co.uk/news/rss.xml',
            'TechCrunch': 'https://techcrunch.com/feed/',
            'Reuters': 'https://www.reutersagency.com/feed/?best-topics=tech',
            'Hacker News': 'https://hnrss.org/frontpage',
        }
    
    def load_feeds_from_file(self, filename: str) -> Dict[str, str]:
        """
        Load feed URLs from a JSON file.
        
        Args:
            filename: Path to JSON file containing feeds
            
        Returns:
            Dictionary of feed name -> URL mappings
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Feed file {filename} not found. Using default feeds.")
            return self.default_feeds
        except json.JSONDecodeError as e:
            print(f"Error parsing feed file: {e}")
            return self.default_feeds
    
    def fetch_all_articles(self, feeds: Dict[str, str], max_articles_per_feed: int = 10) -> None:
        """
        Fetch articles from all provided feeds.
        
        Args:
            feeds: Dictionary of feed name -> URL mappings
            max_articles_per_feed: Maximum articles to fetch per feed
        """
        self.articles = []
        total_feeds = len(feeds)
        
        print(f"Fetching articles from {total_feeds} feeds...")
        
        for i, (name, url) in enumerate(feeds.items(), 1):
            print(f"[{i}/{total_feeds}] Fetching from {name}...")
            
            content = self.parser.fetch_feed(url)
            if content:
                feed_articles = self.parser.parse_rss(content, name)
                # Limit articles per feed
                if len(feed_articles) > max_articles_per_feed:
                    feed_articles = feed_articles[:max_articles_per_feed]
                
                self.articles.extend(feed_articles)
                print(f"  ✓ Found {len(feed_articles)} articles")
            else:
                print(f"  ✗ Failed to fetch from {name}")
            
            # Small delay to be respectful to servers
            time.sleep(0.5)
        
        print(f"\nTotal articles fetched: {len(self.articles)}")
    
    def filter_articles(self, keyword: str = '', category: str = '', 
                       source: str = '') -> List[Article]:
        """
        Filter articles based on keywords, category, or source.
        
        Args:
            keyword: Filter by keyword in title or description
            category: Filter by category
            source: Filter by source name
            
        Returns:
            Filtered list of articles
        """
        filtered = self.articles
        
        if keyword:
            keyword_lower = keyword.lower()
            filtered = [a for a in filtered if 
                       keyword_lower in a.title.lower() or 
                       keyword_lower in a.description.lower()]
        
        if category:
            category_lower = category.lower()
            filtered = [a for a in filtered if 
                       category_lower in a.category.lower()]
        
        if source:
            source_lower = source.lower()
            filtered = [a for a in filtered if 
                       source_lower in a.source.lower()]
        
        return filtered
    
    def display_articles(self, articles: List[Article], limit: int = 20) -> None:
        """
        Display articles in a formatted way.
        
        Args:
            articles: List of articles to display
            limit: Maximum number of articles to display
        """
        if not articles:
            print("No articles found.")
            return
        
        print(f"\n{'='*80}")
        print(f"DISPLAYING {min(len(articles), limit)} OF {len(articles)} ARTICLES")
        print(f"{'='*80}")
        
        for i, article in enumerate(articles[:limit], 1):
            print(f"\n[{i}] {article.title}")
            print(f"Source: {article.source}")
            if article.category:
                print(f"Category: {article.category}")
            if article.pub_date:
                print(f"Published: {article.pub_date}")
            print(f"Description: {article.description}")
            print(f"Link: {article.link}")
            print("-" * 80)
    
    def export_articles(self, articles: List[Article], filename: str, 
                       format_type: str = 'json') -> None:
        """
        Export articles to file.
        
        Args:
            articles: List of articles to export
            filename: Output filename
            format_type: Export format ('json' or 'csv')
        """
        try:
            if format_type.lower() == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump([article.to_dict() for article in articles], 
                             f, indent=2, ensure_ascii=False)
            
            elif format_type.lower() == 'csv':
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    if articles:
                        writer = csv.DictWriter(f, fieldnames=articles[0].to_dict().keys())
                        writer.writeheader()
                        for article in articles:
                            writer.writerow(article.to_dict())
            
            print(f"Exported {len(articles)} articles to {filename}")
            
        except Exception as e:
            print(f"Error exporting articles: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about fetched articles."""
        if not self.articles:
            return {}
        
        sources = {}
        categories = {}
        
        for article in self.articles:
            sources[article.source] = sources.get(article.source, 0) + 1
            if article.category:
                categories[article.category] = categories.get(article.category, 0) + 1
        
        return {
            'total_articles': len(self.articles),
            'sources': sources,
            'categories': categories,
            'articles_with_categories': sum(1 for a in self.articles if a.category)
        }


def create_sample_feeds_file():
    """Create a sample feeds.json file."""
    sample_feeds = {
        "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
        "TechCrunch": "https://techcrunch.com/feed/",
        "Reuters Tech": "https://www.reutersagency.com/feed/?best-topics=tech",
        "Hacker News": "https://hnrss.org/frontpage",
        "Python.org News": "https://www.python.org/jobs/feed/rss/",
        "NASA News": "https://www.nasa.gov/rss/dyn/breaking_news.rss"
    }
    
    with open('feeds.json', 'w', encoding='utf-8') as f:
        json.dump(sample_feeds, f, indent=2)
    
    print("Created sample feeds.json file")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Content Aggregator - Fetch and display articles from RSS feeds'
    )
    
    parser.add_argument('--feeds', '-f', 
                       help='JSON file containing feed URLs (default: feeds.json)')
    parser.add_argument('--keyword', '-k', 
                       help='Filter articles by keyword')
    parser.add_argument('--category', '-c', 
                       help='Filter articles by category')
    parser.add_argument('--source', '-s', 
                       help='Filter articles by source')
    parser.add_argument('--limit', '-l', type=int, default=20,
                       help='Maximum articles to display (default: 20)')
    parser.add_argument('--export', '-e', 
                       help='Export articles to file (specify filename)')
    parser.add_argument('--format', choices=['json', 'csv'], default='json',
                       help='Export format (default: json)')
    parser.add_argument('--max-per-feed', type=int, default=10,
                       help='Maximum articles per feed (default: 10)')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics about fetched articles')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create sample feeds.json file')
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_feeds_file()
        return
    
    # Initialize aggregator
    aggregator = ContentAggregator()
    
    # Load feeds
    if args.feeds:
        feeds = aggregator.load_feeds_from_file(args.feeds)
    else:
        feeds = aggregator.load_feeds_from_file('feeds.json')
    
    # Fetch articles
    aggregator.fetch_all_articles(feeds, args.max_per_feed)
    
    # Filter articles if requested
    articles = aggregator.filter_articles(
        keyword=args.keyword or '',
        category=args.category or '',
        source=args.source or ''
    )
    
    # Display statistics if requested
    if args.stats:
        stats = aggregator.get_statistics()
        print(f"\n{'='*50}")
        print("STATISTICS")
        print(f"{'='*50}")
        print(f"Total articles: {stats.get('total_articles', 0)}")
        print(f"Articles with categories: {stats.get('articles_with_categories', 0)}")
        
        print("\nArticles by source:")
        for source, count in stats.get('sources', {}).items():
            print(f"  {source}: {count}")
        
        if stats.get('categories'):
            print("\nArticles by category:")
            for category, count in sorted(stats.get('categories', {}).items()):
                print(f"  {category}: {count}")
    
    # Export if requested
    if args.export:
        aggregator.export_articles(articles, args.export, args.format)
    
    # Display articles
    aggregator.display_articles(articles, args.limit)


# Simple unit tests
def run_tests():
    """Run basic unit tests."""
    print("Running basic tests...")
    
    # Test Article class
    article = Article(
        title="Test Title",
        link="https://example.com",
        description="Test description",
        pub_date="2024-01-01",
        source="Test Source"
    )
    
    assert article.title == "Test Title"
    assert article.to_dict()['title'] == "Test Title"
    print("✓ Article class test passed")
    
    # Test FeedParser
    parser = FeedParser()
    
    # Test HTML cleaning
    test_html = "<p>This is <b>bold</b> text with <a href='#'>links</a></p>"
    cleaned = parser._clean_html(test_html)
    assert "<" not in cleaned and ">" not in cleaned
    print("✓ HTML cleaning test passed")
    
    # Test ContentAggregator
    aggregator = ContentAggregator()
    assert len(aggregator.articles) == 0
    print("✓ ContentAggregator initialization test passed")
    
    print("All tests passed!")


if __name__ == "__main__":
    # Uncomment the line below to run tests
    # run_tests()
    
    main()
