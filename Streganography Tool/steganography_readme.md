# 🕵️ Steganography Tool

A Python-based steganography tool that can hide and extract text messages within image files using the LSB (Least Significant Bit) technique. This tool allows you to secretly embed messages in images without visibly altering the image's appearance.

## 📋 Project Description

Steganography is the practice of concealing information within other non-secret data. This tool implements LSB steganography, which works by replacing the least significant bits of image pixels with the bits of the secret message. Since the LSB contributes minimally to the overall pixel value, the changes are virtually imperceptible to the human eye.

The tool supports:
- **Hiding text messages** in PNG, JPEG, and other common image formats
- **Extracting hidden messages** from steganographic images
- **Capacity calculation** to determine how much text an image can hold
- **Error handling** and input validation
- **Sample image generation** for testing purposes

## ✨ Features

- **LSB Steganography**: Uses the least significant bit technique for maximum stealth
- **Multiple Image Formats**: Supports PNG, JPEG, BMP, and other PIL-compatible formats
- **Automatic Capacity Check**: Prevents message overflow by checking image capacity
- **Message Delimiter**: Uses special delimiter to accurately detect message boundaries
- **Command-Line Interface**: Easy-to-use CLI with multiple commands
- **Error Handling**: Comprehensive error handling with descriptive messages
- **Sample Image Generator**: Creates test images with gradient patterns
- **Unit Tests**: Built-in test functions to verify functionality
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download
Download the project files:
- `main.py` (the main steganography tool)
- `README.md` (this file)
- `requirements.txt` (dependencies)

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Pillow numpy
```

### Step 3: Verify Installation
```bash
python main.py --help
```

## 🚀 How to Run

The tool provides three main commands: `hide`, `extract`, and `sample`.

### Basic Usage Pattern
```bash
python main.py <command> [options]
```

### Available Commands

#### 1. Create Sample Image (for testing)
```bash
python main.py sample
```

Custom sample image:
```bash
python main.py sample --filename my_sample.png --size 1024 768
```

#### 2. Hide a Message
```bash
python main.py hide --image <input_image> --message "<your_message>" --output <output_image>
```

#### 3. Extract a Message
```bash
python main.py extract --image <image_with_hidden_message>
```

## 📖 Example Usage

### Complete Workflow Example

```bash
# Step 1: Create a sample image for testing
python main.py sample --filename test_image.png

# Step 2: Hide a secret message
python main.py hide --image test_image.png --message "This is my secret message!" --output secret_image.png

# Step 3: Extract the hidden message
python main.py extract --image secret_image.png
```

### Expected Output

**When hiding a message:**
```
🔒 Hiding message in image...
✅ Message successfully hidden in image!
📁 Output saved to: secret_image.png
📊 Message length: 26 characters
📊 Image capacity: 600000 characters
```

**When extracting a message:**
```
🔍 Extracting message from image...
✅ Message successfully extracted!
📊 Message length: 26 characters

📝 Extracted Message:
'This is my secret message!'
```

### Real-World Example

```bash
# Hide a message in your vacation photo
python main.py hide --image vacation.jpg --message "Remember to check the secret location!" --output vacation_secret.png

# Someone else can extract it later
python main.py extract --image vacation_secret.png
```

## 🔧 Advanced Usage

### Check Image Capacity
The tool automatically checks if your message fits in the image. For a rough estimate:
- **Capacity = (Width × Height × 3) ÷ 8** characters
- Example: 800×600 image = 180,000 character capacity

### Supported Image Formats
- **Input**: PNG, JPEG, BMP, TIFF, GIF (converted to RGB)
- **Output**: Recommended PNG for lossless quality

### Message Length Limits
- **Maximum**: Depends on image size
- **Minimum**: At least 1 character
- **Special characters**: Full Unicode support

## 🧪 Running Tests

The project includes built-in unit tests. To run them:

1. Edit `main.py` and uncomment the test line:
```python
if __name__ == "__main__":
    run_tests()  # Uncomment this line
    # main()     # Comment this line
```

2. Run the tests:
```bash
python main.py
```

Expected test output:
```
🧪 Running unit tests...
✅ Test 1 passed: Text to binary conversion
📸 Sample image created: test_sample.png
✅ Test 2 passed: Image capacity calculation
🔒 Hiding message in image...
✅ Message successfully hidden in image!
🔍 Extracting message from image...
✅ Message successfully extracted!
✅ Test 3 passed: Hide and extract message
🎉 All tests passed!
```

## 📁 Project Structure

```
steganography-tool/
│
├── main.py              # Main steganography tool
├── README.md            # This documentation
├── requirements.txt     # Python dependencies
│
├── sample_images/       # Generated test images (created when running)
│   ├── sample.png
│   └── test_image.png
│
└── output/              # Hidden message images (created when running)
    └── secret_image.png
```

## ⚠️ Important Notes

### Security Considerations
- **Not encryption**: This tool hides messages but doesn't encrypt them
- **Lossy formats**: JPEG compression may damage hidden messages
- **Detection**: Sophisticated tools can detect LSB steganography
- **File size**: Output files may be slightly larger than input

### Best Practices
- Use PNG format for output to preserve message integrity
- Choose high-resolution images for better capacity
- Keep original images secret for maximum security
- Test with sample images before using important photos

### Limitations
- **Visible changes**: Very small images may show slight visual changes
- **Compression**: JPEG compression can corrupt hidden messages
- **Detection**: Not secure against dedicated steganography detection tools

## 🚀 Future Improvements

### Planned Enhancements
- **GUI Interface**: Drag-and-drop graphical user interface
- **Password Protection**: Encrypt messages before hiding
- **Multiple Channels**: Support for alpha channel in PNG images
- **Batch Processing**: Hide/extract from multiple images at once
- **Advanced Algorithms**: DCT-based steganography for JPEG images
- **Web Interface**: Browser-based tool using Flask/Django
- **Mobile App**: Android/iOS versions
- **File Hiding**: Support for hiding files, not just text

### Performance Optimizations
- **Memory efficiency**: Process large images in chunks
- **Speed improvements**: Use NumPy vectorization
- **Parallel processing**: Multi-threading for batch operations

### Additional Features
- **Message compression**: Compress text before hiding
- **Metadata preservation**: Keep original image metadata
- **Format conversion**: Automatic format optimization
- **Cloud integration**: Direct upload/download from cloud storage

## 🎯 Converting to Web/GUI Version

### Web Version (Flask)
```python
# Add to requirements.txt: flask
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hide', methods=['POST'])
def hide_message():
    # Handle file upload and message hiding
    pass

@app.route('/extract', methods=['POST'])
def extract_message():
    # Handle file upload and message extraction
    pass
```

### GUI Version (Tkinter)
```python
# Add to main.py
import tkinter as tk
from tkinter import filedialog, messagebox

def create_gui():
    root = tk.Tk()
    root.title("Steganography Tool")
    
    # Add buttons, file dialogs, and text areas
    # Connect to existing SteganographyTool methods
    
    root.mainloop()
```

### GUI Version (PyQt5/PySide)
```python
# Add to requirements.txt: PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout
# Create modern GUI with drag-and-drop support
```

## 🏆 Credits & Acknowledgments

- **PIL (Pillow)**: Image processing library
- **NumPy**: Numerical computing for efficient array operations
- **Python Community**: For excellent documentation and examples
- **LSB Steganography**: Based on classic computer science techniques

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Bug Reports**: Open an issue with detailed description
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Fork, modify, and submit pull requests
4. **Documentation**: Help improve README and code comments
5. **Testing**: Test on different platforms and image formats

## 📞 Support

If you encounter issues or have questions:

1. Check this README for common solutions
2. Run the built-in tests to verify installation
3. Try with sample images first
4. Ensure your Python version is 3.8+
5. Verify all dependencies are installed correctly

---

**Happy Steganography! 🕵️‍♂️**

*Remember: With great power comes great responsibility. Use this tool ethically and legally.*