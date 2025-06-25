# Plagiarism Checker

A comprehensive Python-based plagiarism detection tool that uses multiple similarity algorithms to identify potential plagiarism between text documents. This tool provides detailed similarity analysis using various metrics including cosine similarity, Jaccard similarity, n-gram analysis, and sequence matching.

## Features

- **Multiple Similarity Algorithms**: Implements 6 different similarity metrics for comprehensive analysis
  - Sequence similarity (using difflib)
  - Cosine similarity (based on word frequency vectors)
  - Jaccard similarity (word-based, bigram, and trigram)
  - Longest Common Subsequence (LCS) ratio
  - Weighted average of all metrics

- **Flexible Input Options**: 
  - Compare two specific files
  - Batch process all files in a directory
  - Support for different file extensions

- **Smart Text Processing**:
  - Text normalization and cleaning
  - Stopword removal
  - N-gram generation (bigrams and trigrams)
  - Unicode support

- **Detailed Reporting**:
  - Comprehensive similarity scores
  - Clear plagiarism determination
  - Interpretation of results (Low/Moderate/High/Very High similarity)
  - JSON and human-readable output formats

- **Configurable Thresholds**: Adjustable similarity threshold for plagiarism detection

## Requirements

- **Python Version**: Python 3.8 or higher
- **Dependencies**: Uses only Python standard library (no external packages required)

## Installation

1. **Clone or Download**: Download the `main.py` file to your local machine

2. **Make Executable** (optional, for Unix/Linux/MacOS):
   ```bash
   chmod +x main.py
   ```

3. **Verify Installation**:
   ```bash
   python main.py --help
   ```

## Usage

### Basic Usage

#### Compare Two Files
```bash
python main.py document1.txt document2.txt
```

#### Compare All Files in a Directory
```bash
python main.py --directory ./documents
```

#### Specify File Extension
```bash
python main.py --directory ./essays --extension .docx
```

### Advanced Usage

#### Custom Similarity Threshold
```bash
python main.py --threshold 0.5 file1.txt file2.txt
```

#### JSON Output
```bash
python main.py --json file1.txt file2.txt
```

#### Save Results to File
```bash
python main.py --output results.txt file1.txt file2.txt
```

#### Combined Options
```bash
python main.py --directory ./papers --extension .txt --threshold 0.4 --output analysis.json --json
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `files` | - | Two files to compare | - |
| `--directory` | `-d` | Directory containing files to compare | - |
| `--extension` | `-e` | File extension to check in directory mode | `.txt` |
| `--threshold` | `-t` | Similarity threshold for plagiarism detection | `0.3` |
| `--output` | `-o` | Output file for results | - |
| `--json` | - | Output results in JSON format | False |

## Example Output

```
============================================================
PLAGIARISM CHECK RESULTS
============================================================

Result 1:
File 1: essay1.txt
File 2: essay2.txt
Plagiarism Detected: YES

Similarity Scores:
  Sequence Similarity: 0.742
  Cosine Similarity: 0.681
  Jaccard Word Similarity: 0.523
  Jaccard Trigram Similarity: 0.445
  Jaccard Bigram Similarity: 0.567
  Lcs Ratio: 0.634
  Weighted Average: 0.598

Interpretation: High Similarity - Possible Plagiarism
----------------------------------------
```

## How It Works

### Similarity Algorithms

1. **Sequence Similarity**: Uses Python's `difflib.SequenceMatcher` to find the longest common subsequence ratio between texts.

2. **Cosine Similarity**: Converts texts to word frequency vectors and calculates the cosine angle between them.

3. **Jaccard Similarity**: Measures the intersection over union of:
   - Individual words
   - Bigrams (2-word sequences)
   - Trigrams (3-word sequences)

4. **LCS Ratio**: Calculates the ratio of the longest common subsequence to the length of the longer text.

### Text Processing Pipeline

1. **Normalization**: Convert to lowercase, remove extra whitespace
2. **Cleaning**: Remove special characters while preserving basic punctuation
3. **Tokenization**: Split text into words
4. **Stopword Removal**: Remove common words (optional)
5. **N-gram Generation**: Create bigrams and trigrams for analysis

### Scoring and Interpretation

The tool combines all similarity metrics using weighted averages:
- Sequence Similarity: 20%
- Cosine Similarity: 25%
- Jaccard Word Similarity: 15%
- Jaccard Trigram Similarity: 25%
- Jaccard Bigram Similarity: 10%
- LCS Ratio: 5%

**Interpretation Scale**:
- 0.8+ : Very High Similarity - Likely Plagiarism
- 0.6-0.8: High Similarity - Possible Plagiarism
- 0.3-0.6: Moderate Similarity - Review Recommended
- 0.0-0.3: Low Similarity - Unlikely Plagiarism

## Testing

The tool includes built-in unit tests. To run them, uncomment the test line in the `main.py` file:

```python
# Uncomment this line at the bottom of main.py
run_tests()
```

Then run:
```bash
python main.py
```

## File Format Support

Currently supports plain text files. The tool works best with:
- `.txt` files
- `.md` files
- Any UTF-8 encoded text files

For other formats (Word documents, PDFs), you'll need to convert them to plain text first.

## Limitations

- **Text-only**: Currently only supports plain text files
- **Language**: Optimized for English text (stopwords are English)
- **Local Analysis**: Does not check against online sources
- **No Semantic Analysis**: Focuses on textual similarity rather than meaning

## Future Improvements

### Planned Enhancements
- **GUI Interface**: Web-based interface using Flask or Streamlit
- **More File Formats**: Direct support for PDF, Word documents
- **Semantic Analysis**: Integration with NLP libraries for meaning-based comparison
- **Online Checking**: Integration with plagiarism databases
- **Visualization**: Graphical representation of similarity scores
- **Batch Processing**: Enhanced batch processing with progress bars
- **Configuration Files**: Support for configuration files
- **Database Storage**: Store results in SQLite database
- **Export Options**: Export to Excel, CSV formats

### Converting to Web Application

To convert this to a web application:

1. **Flask Framework**:
   ```python
   from flask import Flask, request, render_template, jsonify
   
   app = Flask(__name__)
   checker = PlagiarismChecker()
   
   @app.route('/', methods=['GET', 'POST'])
   def index():
       if request.method == 'POST':
           # Handle file uploads and process
           pass
       return render_template('index.html')
   ```

2. **Streamlit Framework** (Easier option):
   ```python
   import streamlit as st
   
   st.title("Plagiarism Checker")
   uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
   
   if len(uploaded_files) == 2:
       # Process files and display results
       pass
   ```

### Converting to GUI Application

Using tkinter for a desktop GUI:

```python
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class PlagiarismGUI:
    def __init__(self, root):
        self.root = root
        self.checker = PlagiarismChecker()
        self.setup_ui()
    
    def setup_ui(self):
        # Create GUI elements
        pass
```

## Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting new features
- Improving algorithms
- Adding support for new file formats
- Enhancing the user interface

## License

This project is provided as-is for educational and research purposes. Please ensure you comply with your institution's academic integrity policies when using this tool.

## Acknowledgments

- Built using Python's standard library
- Inspired by various plagiarism detection algorithms
- Text similarity algorithms based on established NLP techniques

## Contact

For questions, suggestions, or bug reports, please create an issue in the project repository.

---

**Note**: This tool is designed to assist in plagiarism detection but should not be the sole method for determining academic misconduct. Always use human judgment and consider context when interpreting results.