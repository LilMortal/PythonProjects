# Directory Tree Generator

A powerful and flexible Python utility that generates visual directory tree structures, perfect for documentation, project overviews, and file system analysis.

## 📋 Project Description

The Directory Tree Generator is a command-line tool that creates ASCII tree representations of directory structures. It provides a clean, hierarchical view of files and folders, similar to the Unix `tree` command but with additional customization options and cross-platform compatibility.

Whether you're documenting a project structure, analyzing file organization, or just need a quick visual overview of a directory, this tool provides an elegant solution with various filtering and output options.

## ✨ Features

- **Clean Tree Visualization**: Generates ASCII tree structures with proper Unicode characters
- **Hidden File Control**: Option to show or hide hidden files and directories
- **Depth Limiting**: Set maximum traversal depth to focus on specific levels
- **Pattern Exclusion**: Exclude files/directories based on name patterns
- **File Output**: Save tree structures to text files
- **Directory Statistics**: Get counts of files, directories, and total size
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Error Handling**: Graceful handling of permission errors and invalid paths
- **Sorting**: Directories listed before files, both sorted alphabetically
- **Customizable**: Easy to extend and modify for specific needs

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- No third-party dependencies required (uses only standard library)

### Installation Steps

1. **Download the script**:
   ```bash
   # Save the main.py file to your desired location
   curl -o main.py [script-url]  # or download manually
   ```

2. **Make it executable** (Linux/macOS):
   ```bash
   chmod +x main.py
   ```

3. **Verify installation**:
   ```bash
   python main.py --help
   ```

### Optional: Add to PATH

To use the tool from anywhere, you can:

**Linux/macOS**:
```bash
# Copy to a directory in your PATH
sudo cp main.py /usr/local/bin/tree-gen
sudo chmod +x /usr/local/bin/tree-gen
```

**Windows**:
```cmd
# Copy to a directory in your PATH or create a batch file
copy main.py C:\Windows\System32\tree-gen.py
```

## 🚀 How to Run

### Basic Usage
```bash
python main.py [directory_path] [options]
```

### Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `directory` | Target directory (default: current) | `python main.py /home/user/project` |
| `--show-hidden` | Include hidden files/directories | `python main.py . --show-hidden` |
| `--max-depth N` | Limit traversal depth | `python main.py . --max-depth 3` |
| `--exclude PATTERNS` | Exclude patterns | `python main.py . --exclude __pycache__ .git` |
| `--output FILE` | Save to file | `python main.py . --output tree.txt` |
| `--stats` | Show directory statistics | `python main.py . --stats` |
| `--help` | Show help message | `python main.py --help` |

## 📖 Example Usage

### Basic Directory Tree
```bash
python main.py /home/user/myproject
```

**Output**:
```
/home/user/myproject
├── README.md
├── src/
│   ├── main.py
│   ├── utils.py
│   └── config/
│       └── settings.json
├── tests/
│   ├── test_main.py
│   └── test_utils.py
└── requirements.txt
```

### Show Hidden Files with Depth Limit
```bash
python main.py . --show-hidden --max-depth 2
```

### Exclude Common Build Directories
```bash
python main.py /path/to/project --exclude __pycache__ .git node_modules .vscode
```

### Generate Tree with Statistics
```bash
python main.py . --stats --output project_structure.txt
```

**Output**:
```
Tree saved to: project_structure.txt

Statistics:
Directories: 15
Files: 42
Total size: 2.3 MB
```

### Advanced Example
```bash
python main.py ~/Documents/Projects --show-hidden --max-depth 4 --exclude .DS_Store Thumbs.db --output full_tree.txt --stats
```

## 🧪 Testing

The project includes built-in unit tests. Run them with:

```bash
python main.py --test
```

This will test:
- Basic tree generation functionality
- Hidden file filtering
- Maximum depth limiting
- File system edge cases

## 🔧 Customization & Extension

### Modifying Tree Characters

You can customize the tree appearance by modifying the `tree_chars` dictionary in the `DirectoryTreeGenerator` class:

```python
self.tree_chars = {
    'branch': '├── ',       # Branch character
    'last_branch': '└── ',  # Last branch character
    'pipe': '│   ',         # Vertical pipe
    'space': '    '         # Spacing
}
```

### Adding New Exclusion Patterns

Extend the exclusion logic in the `should_exclude` method:

```python
def should_exclude(self, path: Path) -> bool:
    # Add custom exclusion logic here
    if path.suffix in ['.pyc', '.pyo']:
        return True
    return False
```

## 🌐 Converting to Web/GUI Version

### Web Version (Flask)
To create a web interface:

1. Install Flask: `pip install flask`
2. Create a simple web form for directory input
3. Use the `DirectoryTreeGenerator` class to process requests
4. Return HTML-formatted trees with `<pre>` tags

### GUI Version (Tkinter)
For a desktop GUI:

1. Use Python's built-in `tkinter` library
2. Create a file browser dialog for directory selection
3. Display results in a scrollable text widget
4. Add buttons for various options (show hidden, max depth, etc.)

### Example Web Integration
```python
from flask import Flask, render_template, request
from main import DirectoryTreeGenerator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        directory = request.form['directory']
        generator = DirectoryTreeGenerator()
        tree = generator.generate_tree(directory)
        return render_template('result.html', tree=tree)
    return render_template('form.html')
```

## 🔮 Future Improvements

### Planned Features
- **JSON/XML Output**: Export trees in structured data formats
- **File Size Display**: Show file sizes in the tree
- **Last Modified Dates**: Include modification timestamps
- **Color Output**: Syntax highlighting for different file types
- **Search Functionality**: Find specific files/directories in large trees
- **Interactive Mode**: Browse directories interactively
- **Performance Optimization**: Handle very large directory structures efficiently

### Enhancement Ideas
- **Git Integration**: Show git status for files (modified, staged, etc.)
- **File Type Icons**: ASCII icons for different file types
- **Compression Detection**: Identify and mark compressed files
- **Symbolic Link Handling**: Better display of symlinks and their targets
- **Plugin System**: Allow custom extensions for specialized use cases
- **Configuration File**: Support for `.treetoolrc` configuration files

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements. Areas where contributions are welcome:

- Performance optimizations
- Additional output formats
- Better error handling
- Cross-platform compatibility improvements
- Documentation enhancements

## 📄 License

This project is released under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- Inspired by the Unix `tree` command
- Built with Python's powerful `pathlib` module
- Thanks to the Python community for excellent documentation and examples

---

**Happy tree generating!** 🌳

For issues, suggestions, or contributions, please create an issue in the project repository.