#!/usr/bin/env python3
"""
Instagram Photo Downloader
A simple tool to download Instagram photos from public profiles and posts.

Author: Your Name
Version: 1.0.0
Python Version: 3.8+
"""

import os
import re
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse
import sys


class InstagramDownloader:
    """
    A class to handle Instagram photo downloads from public profiles.
    
    This downloader works by parsing publicly available Instagram data
    without requiring authentication or API access.
    """
    
    def __init__(self, download_dir: str = "downloads"):
        """
        Initialize the Instagram downloader.
        
        Args:
            download_dir (str): Directory to save downloaded photos
        """
        self.download_dir = download_dir
        self.session_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.create_download_directory()
    
    def create_download_directory(self) -> None:
        """Create the download directory if it doesn't exist."""
        try:
            os.makedirs(self.download_dir, exist_ok=True)
            print(f"✓ Download directory ready: {self.download_dir}")
        except OSError as e:
            print(f"✗ Error creating download directory: {e}")
            sys.exit(1)
    
    def validate_instagram_url(self, url: str) -> Tuple[bool, str]:
        """
        Validate if the provided URL is a valid Instagram URL.
        
        Args:
            url (str): The URL to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, url_type)
        """
        instagram_patterns = {
            'profile': r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)/?$',
            'post': r'https?://(?:www\.)?instagram\.com/p/([a-zA-Z0-9_-]+)/?',
            'reel': r'https?://(?:www\.)?instagram\.com/reel/([a-zA-Z0-9_-]+)/?'
        }
        
        for url_type, pattern in instagram_patterns.items():
            if re.match(pattern, url):
                return True, url_type
        
        return False, "invalid"
    
    def extract_username_from_url(self, url: str) -> Optional[str]:
        """
        Extract username from Instagram profile URL.
        
        Args:
            url (str): Instagram profile URL
            
        Returns:
            Optional[str]: Username if found, None otherwise
        """
        pattern = r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)/?'
        match = re.match(pattern, url)
        return match.group(1) if match else None
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for safe file system storage.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Sanitized filename
        """
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip()
        return filename[:255]  # Limit filename length
    
    def download_image(self, image_url: str, filename: str) -> bool:
        """
        Download an image from the given URL.
        
        Args:
            image_url (str): URL of the image to download
            filename (str): Local filename to save the image
            
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            # Create request with headers
            request = urllib.request.Request(image_url, headers=self.session_headers)
            
            # Download the image
            with urllib.request.urlopen(request, timeout=30) as response:
                if response.status == 200:
                    filepath = os.path.join(self.download_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.read())
                    print(f"✓ Downloaded: {filename}")
                    return True
                else:
                    print(f"✗ Failed to download {filename}: HTTP {response.status}")
                    return False
                    
        except urllib.error.URLError as e:
            print(f"✗ Network error downloading {filename}: {e}")
            return False
        except Exception as e:
            print(f"✗ Error downloading {filename}: {e}")
            return False
    
    def extract_post_data(self, post_url: str) -> Optional[Dict]:
        """
        Extract post data from Instagram post URL.
        
        Args:
            post_url (str): Instagram post URL
            
        Returns:
            Optional[Dict]: Post data if extraction successful
        """
        try:
            # Add embed suffix to get JSON data
            if not post_url.endswith('/'):
                post_url += '/'
            embed_url = post_url + 'embed/captioned/'
            
            request = urllib.request.Request(embed_url, headers=self.session_headers)
            
            with urllib.request.urlopen(request, timeout=30) as response:
                html_content = response.read().decode('utf-8')
                
                # Look for JSON data in the HTML
                json_pattern = r'window\.__additionalDataLoaded\([^,]+,({.+?})\);'
                match = re.search(json_pattern, html_content)
                
                if match:
                    json_data = json.loads(match.group(1))
                    return json_data
                else:
                    # Alternative: look for image URLs directly in HTML
                    img_pattern = r'"display_url":"([^"]+)"'
                    img_matches = re.findall(img_pattern, html_content)
                    if img_matches:
                        return {'images': [url.replace('\\u0026', '&') for url in img_matches]}
                    
        except Exception as e:
            print(f"✗ Error extracting post data: {e}")
        
        return None
    
    def download_from_post_url(self, post_url: str) -> int:
        """
        Download photos from a single Instagram post.
        
        Args:
            post_url (str): Instagram post URL
            
        Returns:
            int: Number of photos downloaded
        """
        print(f"📸 Processing post: {post_url}")
        
        # Extract post ID from URL
        post_id_match = re.search(r'/p/([a-zA-Z0-9_-]+)', post_url)
        if not post_id_match:
            print("✗ Could not extract post ID from URL")
            return 0
        
        post_id = post_id_match.group(1)
        
        # Try to extract post data
        post_data = self.extract_post_data(post_url)
        
        if not post_data:
            print("✗ Could not extract post data")
            return 0
        
        download_count = 0
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Handle different data structures
        images = []
        
        if 'images' in post_data:
            images = post_data['images']
        elif 'graphql' in post_data and 'shortcode_media' in post_data['graphql']:
            media = post_data['graphql']['shortcode_media']
            if 'display_url' in media:
                images = [media['display_url']]
            elif 'edge_sidecar_to_children' in media:
                for edge in media['edge_sidecar_to_children']['edges']:
                    if 'display_url' in edge['node']:
                        images.append(edge['node']['display_url'])
        
        # Download images
        for i, img_url in enumerate(images):
            if img_url:
                filename = f"{post_id}_{timestamp}_{i+1:02d}.jpg"
                filename = self.sanitize_filename(filename)
                
                if self.download_image(img_url, filename):
                    download_count += 1
        
        print(f"✓ Downloaded {download_count} photos from post")
        return download_count
    
    def simulate_profile_download(self, profile_url: str, limit: int = 12) -> int:
        """
        Simulate downloading from a profile (demo version).
        In a real implementation, this would require more complex scraping.
        
        Args:
            profile_url (str): Instagram profile URL
            limit (int): Maximum number of photos to download
            
        Returns:
            int: Number of photos downloaded (simulated)
        """
        username = self.extract_username_from_url(profile_url)
        if not username:
            print("✗ Could not extract username from profile URL")
            return 0
        
        print(f"👤 Processing profile: @{username}")
        print("ℹ️  Profile downloading is limited in this demo version.")
        print("ℹ️  For full profile downloads, consider using specialized tools or APIs.")
        print("ℹ️  This demo will create sample placeholder files.")
        
        # Create sample placeholder files to demonstrate functionality
        download_count = 0
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i in range(min(3, limit)):  # Create 3 sample files
            filename = f"{username}_sample_{timestamp}_{i+1:02d}.txt"
            filename = self.sanitize_filename(filename)
            filepath = os.path.join(self.download_dir, filename)
            
            try:
                with open(filepath, 'w') as f:
                    f.write(f"Sample placeholder for {username}'s photo #{i+1}\n")
                    f.write(f"Created: {datetime.now()}\n")
                    f.write("This is a demo file. Real implementation would download actual photos.\n")
                
                print(f"✓ Created sample: {filename}")
                download_count += 1
                
            except Exception as e:
                print(f"✗ Error creating sample file: {e}")
        
        return download_count


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Instagram Photo Downloader - Download photos from public Instagram posts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://www.instagram.com/p/ABC123/
  python main.py https://www.instagram.com/username/ --type profile --limit 10
  python main.py https://www.instagram.com/p/ABC123/ --output my_downloads
        """
    )
    
    parser.add_argument(
        'url',
        help='Instagram URL (post or profile)'
    )
    
    parser.add_argument(
        '--type',
        choices=['auto', 'post', 'profile'],
        default='auto',
        help='Type of URL (default: auto-detect)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='downloads',
        help='Output directory for downloaded photos (default: downloads)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=12,
        help='Maximum number of photos to download from profile (default: 12)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Instagram Photo Downloader 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Initialize downloader
    print("🚀 Instagram Photo Downloader v1.0.0")
    print("=" * 50)
    
    downloader = InstagramDownloader(download_dir=args.output)
    
    # Validate URL
    is_valid, url_type = downloader.validate_instagram_url(args.url)
    
    if not is_valid:
        print("✗ Invalid Instagram URL provided")
        print("ℹ️  Please provide a valid Instagram post or profile URL")
        print("   Examples:")
        print("   - https://www.instagram.com/p/ABC123/")
        print("   - https://www.instagram.com/username/")
        sys.exit(1)
    
    # Override auto-detection if type is specified
    if args.type != 'auto':
        url_type = args.type
    
    print(f"🔍 Detected URL type: {url_type}")
    
    # Download based on URL type
    total_downloads = 0
    
    try:
        if url_type == 'post' or url_type == 'reel':
            total_downloads = downloader.download_from_post_url(args.url)
        elif url_type == 'profile':
            total_downloads = downloader.simulate_profile_download(args.url, args.limit)
        else:
            print(f"✗ Unsupported URL type: {url_type}")
            sys.exit(1)
        
        print("=" * 50)
        print(f"✅ Download complete! Total files: {total_downloads}")
        print(f"📁 Files saved to: {args.output}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Download interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


# Simple unit tests (can be run by uncommenting and running this section)
def run_tests():
    """
    Simple unit tests for the InstagramDownloader class.
    Uncomment the code below and run to test functionality.
    """
    print("🧪 Running unit tests...")
    
    downloader = InstagramDownloader("test_downloads")
    
    # Test URL validation
    test_urls = [
        ("https://www.instagram.com/p/ABC123/", True, "post"),
        ("https://instagram.com/username/", True, "profile"),
        ("https://www.instagram.com/reel/XYZ789/", True, "reel"),
        ("https://twitter.com/username", False, "invalid"),
        ("not_a_url", False, "invalid")
    ]
    
    print("Testing URL validation...")
    for url, expected_valid, expected_type in test_urls:
        is_valid, url_type = downloader.validate_instagram_url(url)
        status = "✓" if (is_valid == expected_valid and url_type == expected_type) else "✗"
        print(f"{status} {url} -> valid: {is_valid}, type: {url_type}")
    
    # Test filename sanitization
    test_filenames = [
        ("normal_file.jpg", "normal_file.jpg"),
        ("file with spaces.jpg", "file with spaces.jpg"),
        ("file<>:\"/\\|?*.jpg", "file_________.jpg"),
    ]
    
    print("\nTesting filename sanitization...")
    for original, expected in test_filenames:
        sanitized = downloader.sanitize_filename(original)
        status = "✓" if sanitized == expected else "✗"
        print(f"{status} '{original}' -> '{sanitized}'")
    
    # Test username extraction
    test_usernames = [
        ("https://www.instagram.com/testuser/", "testuser"),
        ("https://instagram.com/user.name_123/", "user.name_123"),
        ("https://www.instagram.com/p/ABC123/", None),
    ]
    
    print("\nTesting username extraction...")
    for url, expected in test_usernames:
        username = downloader.extract_username_from_url(url)
        status = "✓" if username == expected else "✗"
        print(f"{status} {url} -> {username}")
    
    print("🧪 Unit tests completed!")


if __name__ == "__main__":
    # Uncomment the line below to run unit tests instead of main program
    # run_tests()
    
    main()
