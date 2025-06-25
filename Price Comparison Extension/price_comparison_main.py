#!/usr/bin/env python3
"""
Price Comparison Tool
A command-line application to compare prices across multiple e-commerce platforms.

Author: Claude AI Assistant
Version: 1.0.0
Python: 3.8+
"""

import re
import json
import time
import argparse
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error
from dataclasses import dataclass, asdict


@dataclass
class ProductInfo:
    """Data class to store product information"""
    name: str
    price: float
    currency: str
    url: str
    site: str
    availability: str = "Unknown"
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class PriceExtractor:
    """Base class for price extraction from different websites"""
    
    def __init__(self, site_name: str):
        self.site_name = site_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_page(self, url: str) -> str:
        """Fetch webpage content with error handling"""
        try:
            request = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except urllib.error.URLError as e:
            print(f"Error fetching {url}: {e}")
            return ""
        except Exception as e:
            print(f"Unexpected error fetching {url}: {e}")
            return ""
    
    def extract_price(self, html: str) -> Tuple[Optional[float], str]:
        """Extract price from HTML content - to be overridden by subclasses"""
        # Generic price extraction using common patterns
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',  # $XX.XX format
            r'(\d+(?:\.\d{2})?)\s*USD',  # XX.XX USD format
            r'Price:\s*\$?(\d+(?:\.\d{2})?)',  # Price: $XX.XX
            r'(?:£|€|¥)(\d+(?:[\.,]\d{2})?)',  # Other currencies
        ]
        
        for pattern in price_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                try:
                    price = float(matches[0].replace(',', ''))
                    return price, 'USD'
                except ValueError:
                    continue
        
        return None, 'USD'
    
    def extract_product_name(self, html: str) -> str:
        """Extract product name from HTML content"""
        # Look for common title patterns
        title_patterns = [
            r'<title[^>]*>([^<]+)</title>',
            r'<h1[^>]*>([^<]+)</h1>',
            r'property=["\']og:title["\'][^>]*content=["\']([^"\']+)["\']',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                title = match.group(1).strip()
                # Clean up common suffixes
                title = re.sub(r'\s*[-|]\s*.*$', '', title)
                return title[:100]  # Limit length
        
        return "Product"
    
    def get_product_info(self, url: str) -> Optional[ProductInfo]:
        """Get complete product information from URL"""
        html = self.fetch_page(url)
        if not html:
            return None
        
        price, currency = self.extract_price(html)
        if price is None:
            return None
        
        name = self.extract_product_name(html)
        availability = "In Stock" if price else "Out of Stock"
        
        return ProductInfo(
            name=name,
            price=price,
            currency=currency,
            url=url,
            site=self.site_name,
            availability=availability
        )


class AmazonExtractor(PriceExtractor):
    """Specialized extractor for Amazon-like sites"""
    
    def __init__(self):
        super().__init__("Amazon")
    
    def extract_price(self, html: str) -> Tuple[Optional[float], str]:
        # Amazon-specific price patterns
        amazon_patterns = [
            r'price_inside_buybox[^>]*>\$?([0-9,]+\.?\d*)',
            r'priceblock_[^>]*>\$?([0-9,]+\.?\d*)',
            r'a-price-whole[^>]*>([0-9,]+)',
            r'\$([0-9,]+\.?\d*)',
        ]
        
        for pattern in amazon_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                try:
                    price_str = matches[0].replace(',', '')
                    price = float(price_str)
                    return price, 'USD'
                except ValueError:
                    continue
        
        return super().extract_price(html)


class EbayExtractor(PriceExtractor):
    """Specialized extractor for eBay-like sites"""
    
    def __init__(self):
        super().__init__("eBay")
    
    def extract_price(self, html: str) -> Tuple[Optional[float], str]:
        # eBay-specific price patterns
        ebay_patterns = [
            r'notranslate[^>]*>\$?([0-9,]+\.?\d*)',
            r'u-flL[^>]*>\$?([0-9,]+\.?\d*)',
            r'price[^>]*>\$?([0-9,]+\.?\d*)',
        ]
        
        for pattern in ebay_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                try:
                    price_str = matches[0].replace(',', '')
                    price = float(price_str)
                    return price, 'USD'
                except ValueError:
                    continue
        
        return super().extract_price(html)


class PriceComparator:
    """Main class to handle price comparison logic"""
    
    def __init__(self):
        self.extractors = {
            'amazon.com': AmazonExtractor(),
            'ebay.com': EbayExtractor(),
            'default': PriceExtractor('Generic')
        }
        self.results: List[ProductInfo] = []
    
    def get_extractor(self, url: str) -> PriceExtractor:
        """Get appropriate extractor based on URL domain"""
        domain = urlparse(url).netloc.lower()
        
        for site_domain, extractor in self.extractors.items():
            if site_domain in domain:
                return extractor
        
        return self.extractors['default']
    
    def add_url(self, url: str) -> bool:
        """Add a URL for price comparison"""
        print(f"Fetching price from: {url}")
        
        extractor = self.get_extractor(url)
        product_info = extractor.get_product_info(url)
        
        if product_info:
            self.results.append(product_info)
            print(f"✓ Found: {product_info.name} - ${product_info.price}")
            return True
        else:
            print(f"✗ Could not extract price from {url}")
            return False
    
    def compare_prices(self) -> None:
        """Display price comparison results"""
        if not self.results:
            print("No products found for comparison.")
            return
        
        print("\n" + "="*80)
        print("PRICE COMPARISON RESULTS")
        print("="*80)
        
        # Sort by price
        sorted_results = sorted(self.results, key=lambda x: x.price)
        
        for i, product in enumerate(sorted_results, 1):
            print(f"\n{i}. {product.name[:50]}...")
            print(f"   Site: {product.site}")
            print(f"   Price: ${product.price:.2f} {product.currency}")
            print(f"   Availability: {product.availability}")
            print(f"   URL: {product.url}")
        
        if len(sorted_results) > 1:
            cheapest = sorted_results[0]
            most_expensive = sorted_results[-1]
            savings = most_expensive.price - cheapest.price
            
            print(f"\n{'='*50}")
            print(f"BEST DEAL: {cheapest.site} - ${cheapest.price:.2f}")
            print(f"SAVINGS: ${savings:.2f} ({savings/most_expensive.price*100:.1f}%)")
            print(f"{'='*50}")
    
    def save_results(self, filename: str = "price_comparison.json") -> None:
        """Save results to JSON file"""
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'total_products': len(self.results),
                'products': [asdict(product) for product in self.results]
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"\nResults saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def load_demo_data(self) -> None:
        """Load demo data for testing purposes"""
        demo_products = [
            ProductInfo(
                name="Sample Laptop Computer",
                price=899.99,
                currency="USD",
                url="https://example-store1.com/laptop",
                site="Store1",
                availability="In Stock"
            ),
            ProductInfo(
                name="Sample Laptop Computer",
                price=849.99,
                currency="USD",
                url="https://example-store2.com/laptop",
                site="Store2",
                availability="In Stock"
            ),
            ProductInfo(
                name="Sample Laptop Computer",
                price=925.00,
                currency="USD",
                url="https://example-store3.com/laptop",
                site="Store3",
                availability="Limited Stock"
            )
        ]
        
        self.results.extend(demo_products)
        print("Demo data loaded successfully!")


def main():
    """Main function to run the price comparison tool"""
    parser = argparse.ArgumentParser(
        description="Price Comparison Tool - Compare prices across multiple websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --urls "https://amazon.com/product1" "https://ebay.com/product1"
  python main.py --demo
  python main.py --interactive
        """
    )
    
    parser.add_argument(
        '--urls', 
        nargs='+', 
        help='List of product URLs to compare'
    )
    parser.add_argument(
        '--demo', 
        action='store_true', 
        help='Run with demo data'
    )
    parser.add_argument(
        '--interactive', 
        action='store_true', 
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--output', 
        default='price_comparison.json',
        help='Output file for results (default: price_comparison.json)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    comparator = PriceComparator()
    
    print("🛒 Price Comparison Tool v1.0")
    print("="*40)
    
    try:
        if args.demo:
            print("Running with demo data...")
            comparator.load_demo_data()
        
        elif args.interactive:
            print("Interactive mode - Enter URLs one by one (empty line to finish):")
            while True:
                url = input("Enter product URL: ").strip()
                if not url:
                    break
                
                if not url.startswith(('http://', 'https://')):
                    print("Please enter a valid URL starting with http:// or https://")
                    continue
                
                comparator.add_url(url)
                if args.delay > 0:
                    time.sleep(args.delay)
        
        elif args.urls:
            for url in args.urls:
                comparator.add_url(url)
                if args.delay > 0:
                    time.sleep(args.delay)
        
        else:
            print("No URLs provided. Use --help for usage information.")
            print("Try: python main.py --demo")
            return
        
        # Display results
        comparator.compare_prices()
        
        # Save results
        if comparator.results:
            comparator.save_results(args.output)
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Simple unit tests (can be run with python -m pytest main.py)
def test_product_info_creation():
    """Test ProductInfo dataclass creation"""
    product = ProductInfo(
        name="Test Product",
        price=99.99,
        currency="USD",
        url="https://example.com",
        site="TestSite"
    )
    assert product.name == "Test Product"
    assert product.price == 99.99
    assert product.timestamp  # Should be automatically set


def test_price_extractor_generic():
    """Test generic price extraction"""
    extractor = PriceExtractor("Test")
    html = "<div>Price: $29.99</div>"
    price, currency = extractor.extract_price(html)
    assert price == 29.99
    assert currency == "USD"


def test_price_comparator_sorting():
    """Test price comparison sorting"""
    comparator = PriceComparator()
    comparator.results = [
        ProductInfo("Product A", 100.0, "USD", "url1", "Site1"),
        ProductInfo("Product B", 50.0, "USD", "url2", "Site2"),
        ProductInfo("Product C", 75.0, "USD", "url3", "Site3"),
    ]
    
    sorted_results = sorted(comparator.results, key=lambda x: x.price)
    assert sorted_results[0].price == 50.0
    assert sorted_results[-1].price == 100.0


if __name__ == "__main__":
    main()
