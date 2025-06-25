# Image Resize Application 🖼️

A powerful and user-friendly command-line image resizing tool built with Python. This application allows you to resize single images or batch process entire directories while maintaining image quality and offering flexible aspect ratio options.

## 📋 Project Description

This image resize application provides a comprehensive solution for image resizing needs. Whether you're preparing images for web use, creating thumbnails, or standardizing image dimensions across a collection, this tool handles it efficiently. It supports multiple image formats, maintains image quality, and offers both single-file and batch processing capabilities.

## ✨ Features

- **Multiple Format Support**: Works with JPEG, PNG, BMP, TIFF, WebP, and GIF images
- **Aspect Ratio Control**: Choose to maintain original proportions or force exact dimensions
- **Batch Processing**: Resize entire directories of images at once
- **Quality Control**: Adjustable JPEG quality settings (1-100)
- **Smart Format Handling**: Automatically handles RGBA to RGB conversion for JPEG output
- **Image Information**: View detailed image properties before processing
- **Progress Tracking**: Real-time feedback on processing status
- **Error Handling**: Comprehensive error checking and user-friendly messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download
Download the project files:
- `main.py` - Main application file
- `requirements.txt` - Dependencies list
- `README.md` - This documentation

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Pillow
```

### Step 3: Verify Installation
```bash
python main.py --help
```

## 🚀 How to Run

### Basic Syntax
```bash
python main.py -i INPUT -o OUTPUT -w WIDTH -h HEIGHT [OPTIONS]
```

### Command-Line Options
- `-i, --input`: Input image file or directory (required)
- `-o, --output`: Output image file or directory
- `-w, --width`: Target width in pixels
- `-h, --height`: Target height in pixels
- `--no-aspect`: Disable aspect ratio maintenance
- `-q, --quality`: JPEG quality (1-100, default: 95)
- `--info`: Show image information only

## 📖 Example Usage

### 1. Resize Single Image (Maintain Aspect Ratio)
```bash
python main.py -i photo.jpg -o resized_photo.jpg -w 800 -h 600
```
**Output**: `✓ Resized 'photo.jpg' to 800x450 -> 'resized_photo.jpg'`

### 2. Resize to Exact Dimensions
```bash
python main.py -i photo.jpg -o exact_photo.jpg -w 800 -h 600 --no-aspect
```
**Output**: `✓ Resized 'photo.jpg' to 800x600 -> 'exact_photo.jpg'`

### 3. Batch Resize Directory
```bash
python main.py -i ./photos -o ./resized_photos -w 1920 -h 1080
```
**Output**: 
```
Found 15 image(s) to process...
✓ Resized './photos/img1.jpg' to 1920x1080 -> './resized_photos/img1.jpg'
✓ Resized './photos/img2.png' to 1920x1440 -> './resized_photos/img2.png'
...
Processing complete:
✓ Successfully processed: 15
✗ Failed: 0
```

### 4. Get Image Information
```bash
python main.py -i photo.jpg --info
```
**Output**:
```
Image: photo.jpg
Dimensions: 3024 x 4032 pixels
Format: JPEG
File size: 2847.3 KB
```

### 5. High-Quality Resize
```bash
python main.py -i photo.jpg -o hq_photo.jpg -w 1200 -h 800 -q 98
```

## 🧪 Running Tests

The application includes built-in unit tests. To run them:

1. Uncomment the test line in `main.py`:
```python
# Change this line:
# run_tests()
# To this:
run_tests()
```

2. Run the tests:
```bash
python main.py
```

## 📁 File Structure

```
image-resize-app/
│
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
│
├── examples/           # Example images (optional)
│   ├── input/
│   └── output/
│
└── tests/             # Additional test files (optional)
```

## 🔧 Converting to Web/GUI Version

### Web Version with Flask
```python
from flask import Flask, request, send_file
from main import ImageResizer

app = Flask(__name__)
resizer = ImageResizer()

@app.route('/resize', methods=['POST'])
def resize_endpoint():
    # Handle file upload and resize
    # Return resized image
    pass
```

### GUI Version with Tkinter
```python
import tkinter as tk
from tkinter import filedialog, messagebox
from main import ImageResizer

class ImageResizerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.resizer = ImageResizer()
        # Create GUI elements
```

## 🎯 Future Improvements

### Planned Features
- **Format Conversion**: Convert between different image formats
- **Watermarking**: Add text or image watermarks
- **Filters**: Apply basic filters (blur, sharpen, brightness)
- **Batch Renaming**: Rename files during processing
- **Progress Bar**: Visual progress indicator for batch operations
- **Configuration Files**: Save and load processing presets
- **Multi-threading**: Parallel processing for faster batch operations

### Advanced Features
- **AI Upscaling**: Integration with AI-based image enhancement
- **Metadata Preservation**: Maintain EXIF data during resize
- **Cloud Integration**: Direct upload/download from cloud storage
- **API Endpoints**: RESTful API for web integration
- **Docker Support**: Containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 Requirements File

Create a `requirements.txt` file with:
```
Pillow>=9.0.0
```

## 🐛 Troubleshooting

### Common Issues

**ImportError: No module named 'PIL'**
```bash
pip install Pillow
```

**Permission Denied Error**
- Ensure you have write permissions to the output directory
- Try running with administrator/sudo privileges if needed

**Unsupported Format Error**
- Check that your input file is one of: JPEG, PNG, BMP, TIFF, WebP, GIF
- Verify the file is not corrupted

**Memory Error with Large Images**
- Try processing smaller batches
- Reduce target dimensions
- Increase system memory

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- Built with [Pillow (PIL)](https://pillow.readthedocs.io/) - Python Imaging Library
- Developed by Claude (Anthropic)
- Inspired by the need for simple, efficient image processing tools

---

**Made with ❤️ for the Python community**
