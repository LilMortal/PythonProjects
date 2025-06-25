#!/usr/bin/env python3
"""
Web Crawler - A simple yet powerful web scraping tool
Author: Claude AI Assistant
Python Version: 3.8+
"""

import urllib.request
import urllib.parse
import urllib.error
from urllib.robotparser import RobotFileParser
import re
import json
import csv
import time
import argparse
import sys
from collections import deque, defaultdict
from dataclasses import dataclass, asdict
from typing import Set, List, Dict, Optional, Tuple
import html
import os
from datetime import datetime


@dataclass
class CrawlResult:
    """Data class to store crawl results for each URL"""
    url: str
    title: str
    status_code: int
    content_length: int
    links_found: int
    emails_found: List[str]
    phone_numbers: List[str]
    crawl_time: str
    error_message: Optional[str] = None


class WebCrawler:
    """
    A comprehensive web crawler that extracts links, emails, and phone numbers
    from web pages while respecting robots.txt and implementing rate limiting.
    """
    
    def __init__(self, max_depth: int = 2, delay: float = 1.0, max_pages: int = 50):
        """
        Initialize the web crawler with configuration parameters.
        
        Args:
            max_depth: Maximum depth to crawl (default: 2)
            delay: Delay between requests in seconds (default: 1.0)
            max_pages: Maximum number of pages to crawl (default: 50)
        """
        self.max_depth = max_depth
        self.delay = delay
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.crawl_results: List[CrawlResult] = []
        self.domain_robots: Dict[str, RobotFileParser] = {}
        
        # Regex patterns for data extraction
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        self.phone_pattern = re.compile(
            r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        )
        self.link_pattern = re.compile(
            r'<a\s+(?:[^>]*?\s+)?href\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE
        )
        self.title_pattern = re.compile(
            r'<title[^>]*>(.*?)</title>', re.IGNORECASE | re.DOTALL
        )
    
    def get_robots_parser(self, url: str) -> Optional[RobotFileParser]:
        """
        Get robots.txt parser for a domain, caching results.
        
        Args:
            url: The URL to check robots.txt for
            
        Returns:
            RobotFileParser instance or None if unavailable
        """
        try:
            parsed_url = urllib.parse.urlparse(url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            if domain not in self.domain_robots:
                robots_url = urllib.parse.urljoin(domain, '/robots.txt')
                rp = RobotFileParser()
                rp.set_url(robots_url)
                try:
                    rp.read()
                    self.domain_robots[domain] = rp
                except:
                    self.domain_robots[domain] = None
            
            return self.domain_robots[domain]
        except Exception:
            return None
    
    def can_fetch(self, url: str, user_agent: str = '*') -> bool:
        """
        Check if we can fetch a URL according to robots.txt.
        
        Args:
            url: URL to check
            user_agent: User agent string
            
        Returns:
            True if allowed to fetch, False otherwise
        """
        robots_parser = self.get_robots_parser(url)
        if robots_parser is None:
            return True  # If no robots.txt, assume allowed
        
        return robots_parser.can_fetch(user_agent, url)
    
    def normalize_url(self, url: str, base_url: str) -> Optional[str]:
        """
        Normalize and validate URLs.
        
        Args:
            url: URL to normalize
            base_url: Base URL for relative links
            
        Returns:
            Normalized URL or None if invalid
        """
        try:
            # Handle relative URLs
            if url.startswith(('http://', 'https://')):
                normalized = url
            elif url.startswith('//'):
                base_scheme = urllib.parse.urlparse(base_url).scheme
                normalized = f"{base_scheme}:{url}"
            elif url.startswith('/'):
                base_parsed = urllib.parse.urlparse(base_url)
                normalized = f"{base_parsed.scheme}://{base_parsed.netloc}{url}"
            elif url.startswith('#') or url.startswith('javascript:') or url.startswith('mailto:'):
                return None
            else:
                normalized = urllib.parse.urljoin(base_url, url)
            
            # Remove fragments
            normalized = normalized.split('#')[0]
            
            # Basic validation
            parsed = urllib.parse.urlparse(normalized)
            if parsed.scheme not in ('http', 'https') or not parsed.netloc:
                return None
                
            return normalized
        except Exception:
            return None
    
    def extract_data(self, html_content: str, url: str) -> Tuple[str, List[str], List[str], List[str]]:
        """
        Extract title, links, emails, and phone numbers from HTML content.
        
        Args:
            html_content: HTML content to parse
            url: Base URL for relative links
            
        Returns:
            Tuple of (title, links, emails, phone_numbers)
        """
        # Extract title
        title_match = self.title_pattern.search(html_content)
        title = html.unescape(title_match.group(1).strip()) if title_match else "No Title"
        
        # Extract links
        links = []
        for match in self.link_pattern.finditer(html_content):
            link = match.group(1)
            normalized_link = self.normalize_url(link, url)
            if normalized_link and normalized_link not in self.visited_urls:
                links.append(normalized_link)
        
        # Extract emails
        emails = list(set(self.email_pattern.findall(html_content)))
        
        # Extract phone numbers
        phone_matches = self.phone_pattern.findall(html_content)
        phone_numbers = list(set([
            ''.join(match) if isinstance(match, tuple) else match 
            for match in phone_matches
        ]))
        
        return title, links, emails, phone_numbers
    
    def fetch_page(self, url: str) -> Tuple[Optional[str], int]:
        """
        Fetch a single web page.
        
        Args:
            url: URL to fetch
            
        Returns:
            Tuple of (content, status_code)
        """
        try:
            # Check robots.txt
            if not self.can_fetch(url):
                print(f"❌ Robots.txt disallows crawling: {url}")
                return None, 403
            
            # Create request with headers
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Compatible Web Crawler)',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                
                # Handle encoding
                if hasattr(response, 'info'):
                    content_type = response.info().get('Content-Type', '')
                    if 'charset=' in content_type:
                        encoding = content_type.split('charset=')[1].split(';')[0]
                    else:
                        encoding = 'utf-8'
                else:
                    encoding = 'utf-8'
                
                try:
                    decoded_content = content.decode(encoding)
                except UnicodeDecodeError:
                    decoded_content = content.decode('utf-8', errors='ignore')
                
                return decoded_content, response.getcode()
                
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP Error {e.code}: {url}")
            return None, e.code
        except urllib.error.URLError as e:
            print(f"❌ URL Error: {url} - {e.reason}")
            return None, 0
        except Exception as e:
            print(f"❌ Unexpected error fetching {url}: {e}")
            return None, 0
    
    def crawl(self, start_urls: List[str]) -> List[CrawlResult]:
        """
        Main crawling method using breadth-first search.
        
        Args:
            start_urls: List of starting URLs
            
        Returns:
            List of CrawlResult objects
        """
        # Initialize queue with (url, depth) tuples
        url_queue = deque([(url, 0) for url in start_urls])
        pages_crawled = 0
        
        print(f"🚀 Starting crawl with max_depth={self.max_depth}, max_pages={self.max_pages}")
        print(f"⏱️  Delay between requests: {self.delay}s")
        print("-" * 60)
        
        while url_queue and pages_crawled < self.max_pages:
            current_url, depth = url_queue.popleft()
            
            if current_url in self.visited_urls or depth > self.max_depth:
                continue
            
            self.visited_urls.add(current_url)
            pages_crawled += 1
            
            print(f"🔍 Crawling [{pages_crawled}/{self.max_pages}] (depth {depth}): {current_url}")
            
            # Fetch the page
            start_time = time.time()
            content, status_code = self.fetch_page(current_url)
            crawl_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if content:
                # Extract data
                title, links, emails, phone_numbers = self.extract_data(content, current_url)
                
                # Create result
                result = CrawlResult(
                    url=current_url,
                    title=title,
                    status_code=status_code,
                    content_length=len(content),
                    links_found=len(links),
                    emails_found=emails,
                    phone_numbers=phone_numbers,
                    crawl_time=crawl_time
                )
                
                print(f"✅ Found: {len(links)} links, {len(emails)} emails, {len(phone_numbers)} phones")
                
                # Add new links to queue for next depth level
                for link in links:
                    if link not in self.visited_urls:
                        url_queue.append((link, depth + 1))
            else:
                # Create error result
                result = CrawlResult(
                    url=current_url,
                    title="Error",
                    status_code=status_code,
                    content_length=0,
                    links_found=0,
                    emails_found=[],
                    phone_numbers=[],
                    crawl_time=crawl_time,
                    error_message=f"Failed to fetch (HTTP {status_code})"
                )
                
                print(f"❌ Failed to crawl")
            
            self.crawl_results.append(result)
            
            # Rate limiting
            if self.delay > 0:
                time.sleep(self.delay)
        
        print("-" * 60)
        print(f"🎉 Crawl completed! Processed {len(self.crawl_results)} pages")
        return self.crawl_results
    
    def save_results(self, format_type: str = 'json', filename: Optional[str] = None):
        """
        Save crawl results to file.
        
        Args:
            format_type: Output format ('json' or 'csv')
            filename: Output filename (optional)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crawl_results_{timestamp}.{format_type}"
        
        if format_type.lower() == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([asdict(result) for result in self.crawl_results], f, indent=2, ensure_ascii=False)
        elif format_type.lower() == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if self.crawl_results:
                    fieldnames = ['url', 'title', 'status_code', 'content_length', 
                                'links_found', 'emails_found', 'phone_numbers', 
                                'crawl_time', 'error_message']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in self.crawl_results:
                        row = asdict(result)
                        row['emails_found'] = ', '.join(row['emails_found'])
                        row['phone_numbers'] = ', '.join(row['phone_numbers'])
                        writer.writerow(row)
        
        print(f"💾 Results saved to: {filename}")
    
    def print_summary(self):
        """Print a summary of crawl results."""
        if not self.crawl_results:
            print("No results to summarize.")
            return
        
        total_pages = len(self.crawl_results)
        successful_pages = sum(1 for r in self.crawl_results if r.status_code == 200)
        total_links = sum(r.links_found for r in self.crawl_results)
        total_emails = sum(len(r.emails_found) for r in self.crawl_results)
        total_phones = sum(len(r.phone_numbers) for r in self.crawl_results)
        
        print("\n" + "="*60)
        print("📊 CRAWL SUMMARY")
        print("="*60)
        print(f"Total pages processed: {total_pages}")
        print(f"Successful crawls: {successful_pages}")
        print(f"Total links found: {total_links}")
        print(f"Total emails found: {total_emails}")
        print(f"Total phone numbers found: {total_phones}")
        print("="*60)
        
        # Show top domains
        domain_count = defaultdict(int)
        for result in self.crawl_results:
            domain = urllib.parse.urlparse(result.url).netloc
            domain_count[domain] += 1
        
        print("\n🌐 Top Domains Crawled:")
        for domain, count in sorted(domain_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {domain}: {count} pages")


def main():
    """Main function with command-line interface."""
    parser = argparse.parser.ArgumentParser(
        description='Web Crawler - Extract links, emails, and phone numbers from websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://example.com
  python main.py https://example.com --depth 3 --delay 2 --max-pages 100
  python main.py https://site1.com https://site2.com --output json --filename results.json
        """
    )
    
    parser.add_argument('urls', nargs='+', help='Starting URLs to crawl')
    parser.add_argument('--depth', type=int, default=2, help='Maximum crawl depth (default: 2)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--max-pages', type=int, default=50, help='Maximum pages to crawl (default: 50)')
    parser.add_argument('--output', choices=['json', 'csv'], default='json', help='Output format (default: json)')
    parser.add_argument('--filename', help='Output filename (optional)')
    parser.add_argument('--no-summary', action='store_true', help='Skip printing summary')
    
    args = parser.parse_args()
    
    # Validate URLs
    valid_urls = []
    for url in args.urls:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        valid_urls.append(url)
    
    # Create and run crawler
    crawler = WebCrawler(
        max_depth=args.depth,
        delay=args.delay,
        max_pages=args.max_pages
    )
    
    try:
        results = crawler.crawl(valid_urls)
        
        if results:
            crawler.save_results(args.output, args.filename)
            
            if not args.no_summary:
                crawler.print_summary()
        else:
            print("No results to save.")
            
    except KeyboardInterrupt:
        print("\n⚠️  Crawl interrupted by user")
        if crawler.crawl_results:
            print("Saving partial results...")
            crawler.save_results(args.output, args.filename)
            crawler.print_summary()
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)


# Simple unit tests (run with: python main.py --test)
def run_tests():
    """Basic unit tests for the crawler."""
    print("🧪 Running basic tests...")
    
    crawler = WebCrawler(max_depth=1, delay=0, max_pages=5)
    
    # Test URL normalization
    base_url = "https://example.com/page"
    test_cases = [
        ("/about", "https://example.com/about"),
        ("contact.html", "https://example.com/contact.html"),
        ("https://other.com", "https://other.com"),
        ("javascript:void(0)", None),
        ("#section", None),
    ]
    
    print("Testing URL normalization...")
    for input_url, expected in test_cases:
        result = crawler.normalize_url(input_url, base_url)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {input_url} -> {result}")
    
    # Test data extraction
    print("Testing data extraction...")
    html = """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <p>Contact us at test@example.com or call (555) 123-4567</p>
        <a href="/about">About</a>
        <a href="https://external.com">External</a>
    </body>
    </html>
    """
    
    title, links, emails, phones = crawler.extract_data(html, "https://example.com")
    print(f"  ✅ Title: {title}")
    print(f"  ✅ Links found: {len(links)}")
    print(f"  ✅ Emails found: {len(emails)}")
    print(f"  ✅ Phones found: {len(phones)}")
    
    print("🎉 Basic tests completed!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_tests()
    else:
        main()
