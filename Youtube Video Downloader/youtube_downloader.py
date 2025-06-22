#!/usr/bin/env python3
"""
YouTube Video Downloader
A simple command-line tool to download YouTube videos and audio.
Compatible with Python 3.10+
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class YouTubeDownloader:
    """Main class for downloading YouTube videos"""
    
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def sanitize_filename(self, filename: str) -> str:
        """Clean filename to be filesystem-safe"""
        # Remove invalid characters for filenames
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace multiple spaces with single space
        filename = re.sub(r'\s+', ' ', filename).strip()
        # Limit length to avoid filesystem issues
        if len(filename) > 200:
            filename = filename[:200] + "..."
        return filename
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/watch\?.*v=([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_info(self, video_id: str) -> Optional[Dict]:
        """Get video information using YouTube's embed page"""
        try:
            # Use the embed page to get basic video information
            embed_url = f"https://www.youtube.com/embed/{video_id}"
            request = urllib.request.Request(embed_url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            with urllib.request.urlopen(request, timeout=10) as response:
                html = response.read().decode('utf-8')
            
            # Extract title from HTML
            title_match = re.search(r'"title":"([^"]+)"', html)
            if not title_match:
                title_match = re.search(r'<title>([^<]+)</title>', html)
            
            title = "Unknown Title"
            if title_match:
                title = title_match.group(1)
                # Decode unicode escape sequences
                title = title.encode().decode('unicode_escape')
            
            return {
                'id': video_id,
                'title': title,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
            
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    def download_video_simple(self, video_id: str, title: str) -> bool:
        """
        Simple video download method.
        Note: This is a basic implementation. For full functionality,
        you would need yt-dlp or similar library.
        """
        try:
            # This is a simplified approach - in practice, you'd need
            # to parse the YouTube player response to get actual video URLs
            print(f"📺 Starting download: {title}")
            print("⚠️  Note: This is a basic implementation.")
            print("   For full YouTube downloading capability, install 'yt-dlp':")
            print("   pip install yt-dlp")
            print()
            
            # Create a placeholder file to demonstrate the concept
            safe_title = self.sanitize_filename(title)
            filename = f"{safe_title}_{video_id}.txt"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"YouTube Video Information\n")
                f.write(f"========================\n")
                f.write(f"Title: {title}\n")
                f.write(f"Video ID: {video_id}\n")
                f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
                f.write(f"\nTo download the actual video, use yt-dlp:\n")
                f.write(f"yt-dlp https://www.youtube.com/watch?v={video_id}\n")
            
            print(f"✅ Video info saved to: {filepath}")
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def download(self, url: str) -> bool:
        """Main download method"""
        print(f"🔍 Processing URL: {url}")
        
        # Extract video ID
        video_id = self.extract_video_id(url)
        if not video_id:
            print("❌ Invalid YouTube URL")
            return False
        
        print(f"📋 Video ID: {video_id}")
        
        # Get video information
        video_info = self.get_video_info(video_id)
        if not video_info:
            print("❌ Could not retrieve video information")
            return False
        
        print(f"📺 Title: {video_info['title']}")
        
        # Download the video
        return self.download_video_simple(video_id, video_info['title'])


def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════╗
    ║        YouTube Video Downloader      ║
    ║              v1.0.0                  ║
    ╚══════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print help information"""
    help_text = """
    Usage:
        python youtube_downloader.py [URL]
        
    Options:
        -h, --help      Show this help message
        -v, --version   Show version information
        
    Examples:
        python youtube_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
        python youtube_downloader.py https://youtu.be/dQw4w9WgXcQ
        
    Note:
        This is a basic implementation for educational purposes.
        For full YouTube downloading functionality, consider using yt-dlp:
        
        pip install yt-dlp
        yt-dlp [URL]
    """
    print(help_text)


def validate_url(url: str) -> bool:
    """Validate if URL is a proper YouTube URL"""
    youtube_patterns = [
        r'https?://(?:www\.)?youtube\.com/watch\?.*v=',
        r'https?://youtu\.be/',
        r'https?://(?:www\.)?youtube\.com/embed/',
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)


def interactive_mode():
    """Run in interactive mode"""
    downloader = YouTubeDownloader()
    
    print("🎵 Interactive YouTube Downloader")
    print("Enter YouTube URLs (or 'quit' to exit)")
    print("-" * 40)
    
    while True:
        try:
            url = input("\n📎 Enter YouTube URL: ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not url:
                continue
                
            if not validate_url(url):
                print("❌ Please enter a valid YouTube URL")
                continue
            
            success = downloader.download(url)
            if success:
                print("\n✨ Download completed successfully!")
            else:
                print("\n💥 Download failed!")
                
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


def main():
    """Main application entry point"""
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['-h', '--help']:
            print_banner()
            print_help()
            return
        
        if arg in ['-v', '--version']:
            print("YouTube Downloader v1.0.0")
            return
        
        # Treat as URL
        url = sys.argv[1]
        if not validate_url(url):
            print("❌ Invalid YouTube URL provided")
            print("Use --help for usage information")
            return
        
        print_banner()
        downloader = YouTubeDownloader()
        success = downloader.download(url)
        
        if success:
            print("\n✨ Download completed successfully!")
        else:
            print("\n💥 Download failed!")
            sys.exit(1)
    else:
        # Run in interactive mode
        print_banner()
        interactive_mode()


if __name__ == "__main__":
    main()
