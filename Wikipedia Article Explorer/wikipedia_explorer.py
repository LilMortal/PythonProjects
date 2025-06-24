#!/usr/bin/env python3
"""
Wikipedia Article Explorer
A command-line tool to fetch and explore random Wikipedia articles.

Author: Claude AI Assistant
Version: 1.0.0
Python Version: 3.8+
"""

import json
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class WikipediaExplorer:
    """Main class for exploring Wikipedia articles."""
    
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/api/rest_v1"
        self.api_url = "https://en.wikipedia.org/w/api.php"
        self.session_history = []
        
    def get_random_article(self) -> Optional[Dict]:
        """
        Fetch a random Wikipedia article.
        
        Returns:
            Dict containing article data or None if failed
        """
        try:
            # Get random article title
            random_url = f"{self.api_url}?action=query&format=json&list=random&rnnamespace=0&rnlimit=1"
            
            print("🎲 Fetching random article...")
            with urllib.request.urlopen(random_url, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            if not data.get('query', {}).get('random'):
                print("❌ No random article found")
                return None
                
            title = data['query']['random'][0]['title']
            return self.get_article_by_title(title)
            
        except urllib.error.URLError as e:
            print(f"❌ Network error: {e}")
            return None
        except json.JSONDecodeError:
            print("❌ Failed to parse response")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def get_article_by_title(self, title: str) -> Optional[Dict]:
        """
        Fetch a specific Wikipedia article by title.
        
        Args:
            title: The title of the Wikipedia article
            
        Returns:
            Dict containing article data or None if failed
        """
        try:
            # Clean and encode title
            clean_title = title.strip().replace(' ', '_')
            encoded_title = urllib.parse.quote(clean_title)
            
            # Get article summary
            summary_url = f"{self.base_url}/page/summary/{encoded_title}"
            
            print(f"📖 Fetching article: {title}")
            with urllib.request.urlopen(summary_url, timeout=10) as response:
                article_data = json.loads(response.read().decode())
            
            # Get additional metadata
            metadata = self._get_article_metadata(title)
            
            # Combine data
            result = {
                'title': article_data.get('title', title),
                'extract': article_data.get('extract', 'No summary available'),
                'url': article_data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                'thumbnail': article_data.get('thumbnail', {}).get('source', ''),
                'lang': article_data.get('lang', 'en'),
                'timestamp': datetime.now().isoformat(),
                **metadata
            }
            
            # Add to session history
            self.session_history.append(result)
            return result
            
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"❌ Article '{title}' not found")
            else:
                print(f"❌ HTTP error {e.code}: {e.reason}")
            return None
        except Exception as e:
            print(f"❌ Error fetching article: {e}")
            return None
    
    def _get_article_metadata(self, title: str) -> Dict:
        """Get additional metadata for an article."""
        try:
            metadata_url = f"{self.api_url}?action=query&format=json&prop=info|categories&titles={urllib.parse.quote(title)}&inprop=url"
            
            with urllib.request.urlopen(metadata_url, timeout=5) as response:
                data = json.loads(response.read().decode())
            
            pages = data.get('query', {}).get('pages', {})
            if not pages:
                return {}
            
            page_data = next(iter(pages.values()))
            categories = [cat['title'].replace('Category:', '') 
                         for cat in page_data.get('categories', [])]
            
            return {
                'page_id': page_data.get('pageid', 0),
                'last_modified': page_data.get('touched', ''),
                'categories': categories[:5]  # Limit to first 5 categories
            }
            
        except Exception:
            return {}
    
    def search_articles(self, query: str, limit: int = 5) -> List[str]:
        """
        Search for Wikipedia articles by query.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of article titles
        """
        try:
            encoded_query = urllib.parse.quote(query)
            search_url = f"{self.api_url}?action=query&format=json&list=search&srsearch={encoded_query}&srlimit={limit}"
            
            print(f"🔍 Searching for: {query}")
            with urllib.request.urlopen(search_url, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            results = data.get('query', {}).get('search', [])
            return [result['title'] for result in results]
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    def display_article(self, article_data: Dict) -> None:
        """Display article information in a formatted way."""
        print("\n" + "="*80)
        print(f"📄 {article_data['title']}")
        print("="*80)
        
        # Basic info
        print(f"🔗 URL: {article_data['url']}")
        if article_data.get('categories'):
            print(f"🏷️  Categories: {', '.join(article_data['categories'])}")
        
        print(f"⏰ Last modified: {article_data.get('last_modified', 'Unknown')[:10]}")
        
        # Summary
        print(f"\n📝 Summary:")
        summary = article_data['extract']
        # Wrap text to 80 characters
        words = summary.split()
        line = ""
        for word in words:
            if len(line + word) > 77:
                print(f"   {line}")
                line = word + " "
            else:
                line += word + " "
        if line:
            print(f"   {line}")
        
        print("\n" + "-"*80)
    
    def save_session_history(self, filename: str = None) -> bool:
        """Save session history to a JSON file."""
        if not self.session_history:
            print("❌ No articles in session history")
            return False
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wikipedia_session_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.session_history, f, indent=2, ensure_ascii=False)
            print(f"💾 Session saved to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            return False
    
    def show_statistics(self) -> None:
        """Display session statistics."""
        if not self.session_history:
            print("📊 No articles explored yet")
            return
        
        print(f"\n📊 Session Statistics:")
        print(f"   Articles explored: {len(self.session_history)}")
        
        # Most common categories
        all_categories = []
        for article in self.session_history:
            all_categories.extend(article.get('categories', []))
        
        if all_categories:
            category_counts = {}
            for cat in all_categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            print(f"   Top categories: {', '.join([f'{cat} ({count})' for cat, count in top_categories])}")


def display_menu() -> None:
    """Display the main menu."""
    print("\n🌟 Wikipedia Article Explorer")
    print("1. Get random article")
    print("2. Search for article")
    print("3. Get article by title")
    print("4. Show session history")
    print("5. Show statistics")
    print("6. Save session to file")
    print("7. Help")
    print("8. Exit")
    print("-" * 30)


def display_help() -> None:
    """Display help information."""
    print("\n📚 Help - Wikipedia Article Explorer")
    print("=" * 50)
    print("This tool helps you explore Wikipedia articles with the following features:")
    print("\n🎲 Random Article: Fetches a completely random Wikipedia article")
    print("🔍 Search: Find articles by searching for keywords")
    print("📖 By Title: Get a specific article if you know its title")
    print("📊 Statistics: View your exploration session stats")
    print("💾 Save Session: Export your explored articles to a JSON file")
    print("\n💡 Tips:")
    print("- Articles are automatically added to your session history")
    print("- Use search to find articles on topics you're interested in")
    print("- Save your session to review articles later")
    print("-" * 50)


def get_user_input(prompt: str, validator=None) -> str:
    """Get user input with optional validation."""
    while True:
        try:
            user_input = input(f"{prompt}: ").strip()
            if not user_input:
                print("❌ Input cannot be empty")
                continue
            if validator and not validator(user_input):
                print("❌ Invalid input format")
                continue
            return user_input
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except EOFError:
            sys.exit(0)


def main():
    """Main application loop."""
    explorer = WikipediaExplorer()
    
    print("🌟 Welcome to Wikipedia Article Explorer!")
    print("Discover interesting articles from the world's largest encyclopedia")
    
    while True:
        try:
            display_menu()
            choice = input("Select an option (1-8): ").strip()
            
            if choice == '1':
                article = explorer.get_random_article()
                if article:
                    explorer.display_article(article)
                    
            elif choice == '2':
                query = get_user_input("Enter search query")
                results = explorer.search_articles(query)
                
                if results:
                    print(f"\n🔍 Found {len(results)} results:")
                    for i, title in enumerate(results, 1):
                        print(f"   {i}. {title}")
                    
                    try:
                        selection = int(input("\nSelect article number (0 to cancel): "))
                        if 1 <= selection <= len(results):
                            article = explorer.get_article_by_title(results[selection-1])
                            if article:
                                explorer.display_article(article)
                        elif selection != 0:
                            print("❌ Invalid selection")
                    except ValueError:
                        print("❌ Please enter a valid number")
                else:
                    print("❌ No results found")
                    
            elif choice == '3':
                title = get_user_input("Enter article title")
                article = explorer.get_article_by_title(title)
                if article:
                    explorer.display_article(article)
                    
            elif choice == '4':
                if explorer.session_history:
                    print(f"\n📚 Session History ({len(explorer.session_history)} articles):")
                    for i, article in enumerate(explorer.session_history, 1):
                        print(f"   {i}. {article['title']}")
                else:
                    print("\n📚 No articles in session history")
                    
            elif choice == '5':
                explorer.show_statistics()
                
            elif choice == '6':
                filename = input("Enter filename (press Enter for auto-generated): ").strip()
                explorer.save_session_history(filename if filename else None)
                
            elif choice == '7':
                display_help()
                
            elif choice == '8':
                print("👋 Thank you for using Wikipedia Article Explorer!")
                if explorer.session_history:
                    save = input("Save session before exit? (y/n): ").strip().lower()
                    if save == 'y':
                        explorer.save_session_history()
                break
                
            else:
                print("❌ Invalid option. Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
            print("Please try again or report this issue.")


# Simple unit tests (can be moved to separate file)
def run_tests():
    """Run basic unit tests."""
    print("🧪 Running basic tests...")
    
    explorer = WikipediaExplorer()
    
    # Test URL construction
    assert explorer.base_url == "https://en.wikipedia.org/api/rest_v1"
    assert explorer.api_url == "https://en.wikipedia.org/w/api.php"
    
    # Test search functionality (requires internet)
    try:
        results = explorer.search_articles("Python programming", limit=3)
        assert isinstance(results, list)
        print("✅ Search test passed")
    except:
        print("⚠️ Search test skipped (no internet connection)")
    
    print("🧪 Basic tests completed")


if __name__ == "__main__":
    # Uncomment the next line to run tests
    # run_tests()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ This script requires Python 3.8 or higher")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    main()