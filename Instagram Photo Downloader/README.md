# Instagram Photo Downloader 📸

A simple, lightweight Python tool for downloading photos from public Instagram posts and profiles. This tool works without requiring Instagram API access or user authentication, making it easy to use for downloading publicly available content.

## 🎯 Purpose

This Instagram Photo Downloader allows you to:
- Download photos from individual Instagram posts
- Save photos from public profiles (demo version)
- Organize downloads in custom directories
- Handle multiple photos from carousel posts
- Maintain original image quality

**Note**: This tool respects Instagram's terms of service and only works with publicly available content. It's designed for educational purposes and personal use.

## ✨ Features

- **Single Post Downloads**: Download all photos from a specific Instagram post
- **Profile Support**: Basic profile photo downloading (demo implementation)
- **Multiple Image Support**: Handle carousel posts with multiple photos
- **Smart URL Detection**: Automatically detect post vs profile URLs
- **Custom Output Directory**: Specify where to save downloaded photos
- **Error Handling**: Robust error handling with informative messages
- **Progress Tracking**: Real-time download progress and status updates
- **Filename Sanitization**: Safe filename generation for all operating systems
- **Command-Line Interface**: Easy-to-use CLI with helpful options
- **Unit Tests**: Built-in testing functionality for reliability

## 🛠️ Requirements

- **Python Version**: Python 3.8 or higher
- **Dependencies**: Uses only Python standard libraries (no external packages required!)
- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Internet Connection**: Required for downloading content

## 📦 Installation

### Option 1: Direct Download
1. Download the `main.py` file
2. Save it to your desired directory
3. You're ready to go! No additional dependencies needed.

### Option 2: Clone/Copy
```bash
# Create a new directory for the project
mkdir instagram-downloader
cd instagram-downloader

# Copy the main.py file to this directory
# (paste the code from main.py into a new file)
```

### Verify Installation
```bash
python main.py --version
```

## 🚀 How to Run

### Basic Usage
```bash
# Download from a single post
python main.py https://www.instagram.com/p/POST_ID/

# Download from a profile (demo version)
python main.py https://www.instagram.com/username/
```

### Advanced Usage
```bash
# Specify custom output directory
python main.py https://www.instagram.com/p/POST_ID/ --output my_photos

# Limit number of profile photos
python main.py https://www.instagram.com/username/ --limit 20

# Force URL type detection
python main.py https://www.instagram.com/p/POST_ID/ --type post
```

### Command-Line Options
```bash
python main.py --help
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--type` | | URL type (auto, post, profile) | auto |
| `--output` | `-o` | Output directory | downloads |
| `--limit` | `-l` | Max photos from profile | 12 |
| `--version` | | Show version information | |

## 📋 Example Usage

### Example 1: Download from Post
```bash
$ python main.py https://www.instagram.com/p/ABC123DEF456/

🚀 Instagram Photo Downloader v1.0.0
==================================================
✓ Download directory ready: downloads
🔍 Detected URL type: post
📸 Processing post: https://www.instagram.com/p/ABC123DEF456/
✓ Downloaded: ABC123DEF456_20241225_143022_01.jpg
✓ Downloaded: ABC123DEF456_20241225_143022_02.jpg
✓ Downloaded 2 photos from post
==================================================
✅ Download complete! Total files: 2
📁 Files saved to: downloads
```

### Example 2: Download from Profile (Demo)
```bash
$ python main.py https://www.instagram.com/nature_photography/ --limit 5

🚀 Instagram Photo Downloader v1.0.0
==================================================
✓ Download directory ready: downloads
🔍 Detected URL type: profile
👤 Processing profile: @nature_photography
ℹ️  Profile downloading is limited in this demo version.
ℹ️  For full profile downloads, consider using specialized tools or APIs.
ℹ️  This demo will create sample placeholder files.
✓ Created sample: nature_photography_sample_20241225_143155_01.txt
✓ Created sample: nature_photography_sample_20241225_143155_02.txt
✓ Created sample: nature_photography_sample_20241225_143155_03.txt
==================================================
✅ Download complete! Total files: 3
📁 Files saved to: downloads
```

### Example 3: Custom Output Directory
```bash
$ python main.py https://www.instagram.com/p/XYZ789/ -o vacation_photos

🚀 Instagram Photo Downloader v1.0.0
==================================================
✓ Download directory ready: vacation_photos
🔍 Detected URL type: post
📸 Processing post: https://www.instagram.com/p/XYZ789/
✓ Downloaded: XYZ789_20241225_143300_01.jpg
==================================================
✅ Download complete! Total files: 1
📁 Files saved to: vacation_photos
```

## 🧪 Testing

The application includes built-in unit tests. To run them:

1. Open `main.py` in a text editor
2. Find the line at the bottom: `# run_tests()`
3. Uncomment it by removing the `#`: `run_tests()`
4. Comment out the `main()` line: `# main()`
5. Run the file:

```bash
python main.py
```

This will run tests for:
- URL validation
- Filename sanitization
- Username extraction
- Basic functionality

## 🔧 Troubleshooting

### Common Issues and Solutions

**Issue**: "Invalid Instagram URL provided"
```
Solution: Ensure you're using a complete Instagram URL:
✓ https://www.instagram.com/p/POST_ID/
✓ https://www.instagram.com/username/
✗ instagram.com/p/POST_ID (missing https://)
```

**Issue**: "Could not extract post data"
```
Solution: 
- Ensure the post is public (not private)
- Check your internet connection
- The post might have been deleted or made private
- Try again after a few minutes
```

**Issue**: "Network error downloading"
```
Solution:
- Check your internet connection
- The Instagram servers might be temporarily unavailable
- Try downloading again later
- Some posts might have restricted access
```

**Issue**: Permission denied when creating directory
```
Solution:
- Choose a different output directory you have write access to
- Run with appropriate permissions
- Use: python main.py URL -o ~/Downloads/instagram
```

## ⚖️ Legal and Ethical Considerations

- **Public Content Only**: This tool only works with publicly available Instagram content
- **Respect Copyright**: Only download content you have permission to use
- **Terms of Service**: Ensure your usage complies with Instagram's Terms of Service
- **Rate Limiting**: The tool includes natural rate limiting to be respectful of Instagram's servers
- **Personal Use**: Intended for personal, educational, and research purposes

## 🔮 Future Improvements

### Planned Features
- **Video Support**: Download videos and reels
- **Batch Processing**: Process multiple URLs from a file
- **Metadata Extraction**: Save post captions, dates, and hashtags
- **GUI Version**: Desktop application with graphical interface
- **Web Interface**: Browser-based version using Flask/Django
- **Database Integration**: Store download history and metadata
- **Resume Downloads**: Continue interrupted downloads
- **Image Processing**: Automatic resizing and format conversion

### Advanced Features (Possible)
- **Stories Download**: Download Instagram Stories (with limitations)
- **IGTV Support**: Download longer-form video content
- **Bulk Profile Analysis**: Download and analyze multiple profiles
- **Duplicate Detection**: Avoid downloading the same content twice
- **Cloud Integration**: Upload downloads directly to cloud storage

### Converting to Web/GUI Version

**Web Version (Flask)**:
```python
# Add to your project
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.json['url']
    downloader = InstagramDownloader()
    # Process download and return status
    return jsonify({'status': 'success'})
```

**GUI Version (Tkinter)**:
```python
# Add to your project
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class InstagramDownloaderGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Instagram Photo Downloader")
        # Add GUI components
```

## 🤝 Contributing

This is a single-file educational project, but improvements are welcome!

### How to Contribute
1. Fork or copy the project
2. Make your improvements
3. Test thoroughly
4. Share your enhancements

### Areas for Contribution
- Better error handling
- More robust HTML parsing
- Additional Instagram features
- Performance optimizations
- UI improvements

## 📝 Credits and Acknowledgments

- **Python Standard Library**: For providing all necessary tools without external dependencies
- **Instagram**: For providing publicly accessible content
- **Community**: For feedback and testing

## 📄 License

This project is provided for educational purposes. Please ensure your usage complies with:
- Instagram's Terms of Service
- Copyright laws in your jurisdiction
- Applicable data protection regulations

## 📞 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Test with the built-in unit tests
4. Ensure you're using Python 3.8+

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Python Compatibility**: 3.8+  
**Platform**: Cross-platform (Windows, macOS, Linux)

---

### Quick Start Summary
```bash
# 1. Save main.py to your computer
# 2. Open terminal/command prompt
# 3. Navigate to the directory containing main.py
# 4. Run your first download:
python main.py https://www.instagram.com/p/YOUR_POST_ID/
```

Happy downloading! 📸✨
