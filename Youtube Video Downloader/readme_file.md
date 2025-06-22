# 🎥 YouTube Video Downloader

A simple, educational command-line tool for processing YouTube video URLs and extracting basic video information. This project demonstrates URL parsing, web scraping basics, and file handling in Python.

## ✨ Features

- **URL Validation**: Supports multiple YouTube URL formats (youtube.com, youtu.be, embed URLs)
- **Video Information Extraction**: Retrieves basic video metadata (title, ID)
- **Interactive Mode**: User-friendly CLI interface with continuous input
- **Batch Processing**: Command-line argument support for single URL processing
- **Safe File Handling**: Automatic filename sanitization and directory creation
- **Error Handling**: Graceful handling of network errors and invalid inputs
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No External Dependencies**: Uses only Python standard library

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Internet connection

### Installation
1. Download the `youtube_downloader.py` file
2. No additional installation required!

### Usage

#### Interactive Mode (Recommended)
```bash
python youtube_downloader.py
```

#### Command Line Mode
```bash
# Download single video
python youtube_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Show help
python youtube_downloader.py --help

# Show version
python youtube_downloader.py --version
```

#### Supported URL Formats
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `http://youtube.com/watch?v=VIDEO_ID` (with or without www)

## 📖 Example Usage

### Interactive Session
```
    ╔══════════════════════════════════════╗
    ║        YouTube Video Downloader      ║
    ║              v1.0.0                  ║
    ╚══════════════════════════════════════╝

🎵 Interactive YouTube Downloader
Enter YouTube URLs (or 'quit' to exit)
----------------------------------------

📎 Enter YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
🔍 Processing URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
📋 Video ID: dQw4w9WgXcQ
📺 Title: Rick Astley - Never Gonna Give You Up
📺 Starting download: Rick Astley - Never Gonna Give You Up
✅ Video info saved to: downloads/Rick Astley - Never Gonna Give You Up_dQw4w9WgXcQ.txt

✨ Download completed successfully!
```

### Command Line Usage
```bash
$ python youtube_downloader.py "https://youtu.be/dQw4w9WgXcQ"

    ╔══════════════════════════════════════╗
    ║        YouTube Video Downloader      ║
    ║              v1.0.0                  ║
    ╚══════════════════════════════════════╝

🔍 Processing URL: https://youtu.be/dQw4w9WgXcQ
📋 Video ID: dQw4w9WgXcQ
📺 Title: Rick Astley - Never Gonna Give You Up
✅ Video info saved to: downloads/Rick Astley - Never Gonna Give You Up_dQw4w9WgXcQ.txt

✨ Download completed successfully!
```

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Standard Libraries Used**:
  - `urllib` - HTTP requests and URL parsing
  - `re` - Regular expression pattern matching
  - `pathlib` - Modern file path handling
  - `json` - JSON data processing
  - `os` & `sys` - System operations
  - `typing` - Type hints for better code quality

## 📁 Project Structure

```
youtube-downloader/
├── youtube_downloader.py    # Main application file
├── README.md               # This file
├── downloads/              # Created automatically for output files
└── requirements.txt        # Optional (see Advanced Usage)
```

## ⚠️ Important Notes

This is an **educational project** that demonstrates:
- URL parsing and validation
- Basic web scraping techniques
- File I/O operations
- Command-line interface design
- Error handling best practices

**For actual video downloading**, you should use established tools like:
- `yt-dlp` (recommended): `pip install yt-dlp`
- `youtube-dl`: `pip install youtube-dl`

## 🔧 Advanced Usage

### For Real Video Downloads
If you want to actually download video files, create a `requirements.txt`:

```txt
yt-dlp>=2023.12.30
```

Then install and use:
```bash
pip install -r requirements.txt
yt-dlp [YouTube_URL]
```

### Customization Options
You can modify the script to:
- Change the output directory
- Add different output formats
- Implement playlist support
- Add progress bars
- Include audio-only downloads

## 🚀 Future Enhancement Ideas

### Easy Additions
- **Progress Bar**: Add download progress indication using `tqdm`
- **Playlist Support**: Handle YouTube playlist URLs
- **Quality Selection**: Let users choose video quality
- **Audio Extraction**: Download audio-only versions
- **Batch File Input**: Process URLs from a text file

### Advanced Features
- **GUI Version**: Create a Tkinter or PyQt interface
- **Web Interface**: Build a Flask/FastAPI web app
- **Configuration File**: Add settings via config file
- **Download History**: Track downloaded videos
- **Retry Logic**: Automatic retry for failed downloads
- **Thumbnail Download**: Save video thumbnails
- **Metadata Export**: Export video info to JSON/CSV

### Integration Ideas
- **Discord Bot**: YouTube downloader bot
- **Telegram Bot**: Download videos via chat
- **API Wrapper**: Create a REST API for the downloader
- **Docker Container**: Containerized version
- **GitHub Actions**: Automated testing and releases

## 🐛 Troubleshooting

### Common Issues

**"Invalid YouTube URL"**
- Ensure the URL is complete and properly formatted
- Check that the video is publicly accessible

**"Could not retrieve video information"**
- Video might be private or region-locked
- Check your internet connection
- Some videos may have enhanced protection

**"Permission denied" errors**
- Make sure you have write permissions in the output directory
- Try running with appropriate permissions

### Getting Help
1. Check the help message: `python youtube_downloader.py --help`
2. Ensure you're using Python 3.10+
3. Verify the YouTube URL is accessible in your browser

## 📜 License

This project is provided for educational purposes. Please respect YouTube's Terms of Service and copyright laws when using any video downloading tools.

## 🤝 Contributing

This is an educational project, but suggestions for improvements are welcome! Areas for contribution:
- Enhanced error handling
- Better URL pattern matching
- Cross-platform compatibility improvements
- Documentation enhancements

## 🙏 Acknowledgments

- YouTube for providing embeddable content
- Python community for excellent standard library documentation
- Open source projects like yt-dlp for inspiration

---

**Disclaimer**: This tool is for educational purposes only. Always respect content creators' rights and platform terms of service when downloading or processing online content.