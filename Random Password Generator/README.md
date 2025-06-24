# 🔐 Random Password Generator

A secure, customizable command-line password generator built in Python. This tool generates cryptographically secure passwords with various customization options and includes password strength analysis functionality.

## 📋 Project Description

This Random Password Generator uses Python's `secrets` module to create cryptographically secure passwords suitable for protecting sensitive accounts and data. The tool offers both interactive and command-line interfaces, making it versatile for different use cases. Whether you need a quick password or want to generate multiple passwords with specific criteria, this tool has you covered.

## ✨ Features

- **Cryptographically Secure**: Uses Python's `secrets` module for secure random generation
- **Highly Customizable**: Control password length, character types, and special requirements
- **Multiple Generation Modes**: Interactive mode and command-line interface
- **Password Strength Analysis**: Built-in password strength checker with detailed feedback
- **Bulk Generation**: Generate multiple passwords at once
- **Ambiguous Character Filtering**: Option to exclude confusing characters (0, O, 1, l, I)
- **Custom Character Support**: Add your own custom characters to the generation pool
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **No External Dependencies**: Uses only Python standard library

### Character Types Supported
- Lowercase letters (a-z)
- Uppercase letters (A-Z)
- Digits (0-9)
- Special characters (!@#$%^&*()_+-=[]{}|;:,.<>?)
- Custom characters (user-defined)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher

### Installation Steps

1. **Download the script**:
   ```bash
   # Option 1: Download directly
   curl -O https://example.com/main.py
   
   # Option 2: Clone if part of a repository
   git clone https://github.com/username/password-generator.git
   cd password-generator
   ```

2. **Make the script executable** (optional, for Unix-like systems):
   ```bash
   chmod +x main.py
   ```

3. **Verify installation**:
   ```bash
   python main.py --help
   ```

### Dependencies
This project uses only Python standard library modules:
- `random` - For shuffling operations
- `string` - For character constants
- `secrets` - For cryptographically secure random generation
- `argparse` - For command-line argument parsing
- `sys` - For system-specific parameters
- `typing` - For type hints

No additional packages need to be installed!

## 🚀 How to Run

### Interactive Mode (Recommended for beginners)
```bash
python main.py
# or
python main.py --interactive
```

### Command-Line Mode

#### Basic Usage
```bash
# Generate a 12-character password (default)
python main.py

# Generate a 16-character password
python main.py -l 16

# Generate 5 passwords of 20 characters each
python main.py -l 20 -c 5
```

#### Advanced Options
```bash
# No special characters
python main.py -l 12 --no-special

# Exclude ambiguous characters
python main.py --exclude-ambiguous

# No uppercase letters
python main.py --no-uppercase

# Add custom characters
python main.py --custom-chars "@#$"

# Analyze password strength
python main.py --analyze "MyPassword123!"
```

### Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-l, --length` | Password length | 12 |
| `--no-uppercase` | Exclude uppercase letters | False |
| `--no-lowercase` | Exclude lowercase letters | False |
| `--no-digits` | Exclude digits | False |
| `--no-special` | Exclude special characters | False |
| `--exclude-ambiguous` | Exclude 0,O,1,l,I | False |
| `-c, --count` | Number of passwords | 1 |
| `--custom-chars` | Additional characters | None |
| `--analyze` | Analyze password strength | None |
| `--interactive` | Interactive mode | False |

## 💡 Example Usage

### Example 1: Interactive Mode
```
$ python main.py

🔐 Interactive Password Generator
========================================

Password Options:
Password length (default 12): 16
Include uppercase letters? (Y/n): y
Include lowercase letters? (Y/n): y
Include digits? (Y/n): y
Include special characters? (Y/n): y
Exclude ambiguous characters (0,O,1,l,I)? (y/N): n
Number of passwords to generate (default 1): 1

🔑 Generated Password:
1: K3m$nP9#xR2vL8qW

📊 Password Analysis:
Length: 16 characters
Lowercase letters: ✓
Uppercase letters: ✓
Digits: ✓
Special characters: ✓
Unique characters: 16
Strength: Very Strong (9/9)
```

### Example 2: Command-Line Generation
```bash
$ python main.py -l 20 -c 3

🔑 Generated Passwords:
1: Bp4#xK9$mN2vQ8rT5wY7
2: H6j@sL3%nC8uF1kM4pR9
3: D7g&zA5*eX2bV6hJ9qN3
```

### Example 3: Password Analysis
```bash
$ python main.py --analyze "password123"

Password: password123
📊 Password Analysis:
Length: 11 characters
Lowercase letters: ✓
Uppercase letters: ✗
Digits: ✓
Special characters: ✗
Unique characters: 9
Strength: Weak (3/9)
```

### Example 4: Secure Password for Sensitive Accounts
```bash
$ python main.py -l 24 --exclude-ambiguous

🔑 Generated Password:
Rp8#xK3$mN7vQ2rT9wYc5zAb

📊 Password Analysis:
Length: 24 characters
Lowercase letters: ✓
Uppercase letters: ✓
Digits: ✓
Special characters: ✓
Unique characters: 24
Strength: Very Strong (9/9)
```

## 🔒 Security Features

- **Cryptographically Secure**: Uses `secrets.choice()` and `secrets.SystemRandom()` for all random operations
- **No Predictable Patterns**: Shuffles password characters after generation
- **Strong Default Settings**: Includes all character types by default
- **Ambiguous Character Filtering**: Optional removal of easily confused characters
- **Strength Analysis**: Built-in password strength evaluation

## 🧪 Testing

The script includes simple doctests that can be run using:

```bash
python -m doctest main.py -v
```

For more comprehensive testing, you can run the built-in test function:

```python
# In Python interactive shell
>>> from main import PasswordGenerator
>>> generator = PasswordGenerator()
>>> password = generator.generate_password(length=10)
>>> len(password) == 10
True
```

## 🚀 Future Improvements / Next Steps

### Planned Enhancements
- [ ] **Web Interface**: Convert to a Flask/Django web application
- [ ] **GUI Version**: Create a desktop GUI using tkinter or PyQt
- [ ] **Password Complexity Policies**: Add support for organizational password policies
- [ ] **Passphrase Generation**: Generate memorable passphrases using word lists
- [ ] **Password History**: Track generated passwords (with user consent)
- [ ] **Clipboard Integration**: Automatically copy passwords to clipboard
- [ ] **QR Code Generation**: Generate QR codes for easy mobile transfer
- [ ] **Bulk Export**: Export multiple passwords to CSV/JSON formats
- [ ] **Password Expiry Tracking**: Set and track password expiration dates

### Converting to Web Application
To convert this to a web application using Flask:

1. Install Flask: `pip install flask`
2. Create a simple HTML form for password options
3. Use the `PasswordGenerator` class as a backend service
4. Add AJAX for dynamic password generation
5. Implement client-side password strength visualization

### Converting to GUI Application
To create a desktop GUI version:

1. **Using tkinter** (built-in):
   ```python
   import tkinter as tk
   from tkinter import ttk
   # Use PasswordGenerator class with tkinter widgets
   ```

2. **Using PyQt5/PySide2**:
   ```bash
   pip install PyQt5
   # Create modern GUI with advanced widgets
   ```

### Mobile App Development
Consider using:
- **Kivy**: Cross-platform Python framework
- **BeeWare**: Python native mobile apps
- **React Native** with Python backend API

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update README.md for new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Python Software Foundation** for the excellent `secrets` module
- **Security community** for password security best practices
- **Open source contributors** who inspire better coding practices

## 📞 Support

If you encounter any issues or have questions:

1. Check the examples in this README
2. Run `python main.py --help` for quick reference
3. Review the source code comments for implementation details
4. Open an issue on GitHub (if applicable)

## 📈 Changelog

### Version 1.0.0
- Initial release
- Interactive and command-line modes
- Password strength analysis
- Multiple password generation
- Ambiguous character filtering
- Custom character support
- Comprehensive documentation

---

**Made with ❤️ and Python** | **Stay Secure! 🔐**
