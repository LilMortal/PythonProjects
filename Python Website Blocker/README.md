# Website Blocker

A command-line Python tool that helps you stay focused by blocking access to distracting websites. The tool works by modifying your system's hosts file to redirect blocked websites to localhost, effectively preventing access to them from any browser or application.

## 🎯 Purpose

Website Blocker is designed to help users maintain productivity by temporarily or permanently blocking access to distracting websites like social media, entertainment sites, or any other web destinations that might interfere with work or study time. Unlike browser extensions, this tool works system-wide across all applications and browsers.

## ✨ Features

- **Cross-platform compatibility**: Works on Windows, macOS, and Linux
- **Simple command-line interface**: Easy to use with intuitive commands
- **Batch operations**: Block or unblock multiple websites at once
- **Automatic backup**: Creates backup of your hosts file before making changes
- **Domain validation**: Validates domain names before processing
- **Flexible blocking**: Blocks both www and non-www versions of websites
- **List management**: View all currently blocked websites
- **Safe restoration**: Restore original hosts file from backup
- **Administrator privilege detection**: Automatically checks for required permissions

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Administrator/root privileges (required for modifying hosts file)

### Setup Instructions

1. **Download the script**:
   ```bash
   # Save the main.py file to your desired directory
   curl -O https://raw.githubusercontent.com/your-repo/website-blocker/main/main.py
   ```
   
   Or simply copy the `main.py` code into a new file on your system.

2. **Make the script executable** (Linux/macOS):
   ```bash
   chmod +x main.py
   ```

3. **No additional dependencies required** - the script uses only Python standard libraries!

## 🚀 Usage

The tool must be run with administrator privileges to modify the hosts file.

### Basic Commands

#### Block websites:
```bash
# Windows (run as Administrator)
python main.py block facebook.com twitter.com instagram.com

# Linux/macOS (run with sudo)
sudo python main.py block facebook.com twitter.com instagram.com
```

#### Unblock specific websites:
```bash
# Windows
python main.py unblock facebook.com

# Linux/macOS
sudo python main.py unblock facebook.com
```

#### Unblock all websites:
```bash
# Windows
python main.py unblock-all

# Linux/macOS
sudo python main.py unblock-all
```

#### List blocked websites:
```bash
python main.py list
```

#### Restore from backup:
```bash
# Windows
python main.py restore

# Linux/macOS
sudo python main.py restore
```

#### View help:
```bash
python main.py --help
```

#### Run tests:
```bash
python main.py --test
```

### Example Usage Session

```bash
# Block social media sites
$ sudo python main.py block facebook.com twitter.com youtube.com
Successfully blocked 3 website(s):
  - facebook.com
  - twitter.com  
  - youtube.com

# Check what's currently blocked
$ python main.py list
Currently blocked websites (3):
  - facebook.com
  - twitter.com
  - youtube.com

# Unblock one specific site
$ sudo python main.py unblock youtube.com
Successfully unblocked 1 website(s).

# Unblock everything
$ sudo python main.py unblock-all
Successfully unblocked all websites.
```

## 🔧 How It Works

The Website Blocker modifies your system's hosts file by:

1. **Creating a backup** of your current hosts file for safety
2. **Adding entries** that redirect blocked domains to `127.0.0.1` (localhost)
3. **Using markers** to identify its entries for easy removal later
4. **Validating domains** to ensure proper formatting
5. **Handling both www and non-www versions** of each domain

The hosts file locations:
- **Windows**: `C:\Windows\System32\drivers\etc\hosts`
- **Linux/macOS**: `/etc/hosts`

## 📋 Requirements

- Python 3.7+
- Administrator privileges on Windows OR root privileges on Linux/macOS
- Write access to the system hosts file

## ⚠️ Important Notes

- **Administrator privileges required**: The script needs elevated permissions to modify the hosts file
- **System-wide blocking**: This blocks websites across all browsers and applications
- **Backup safety**: Always creates a backup before making changes
- **Persistent blocking**: Websites remain blocked until explicitly unblocked
- **DNS cache**: You may need to flush your DNS cache after blocking/unblocking for immediate effect

### Flush DNS Cache (if needed):
```bash
# Windows
ipconfig /flushdns

# macOS
sudo dscacheutil -flushcache

# Linux
sudo systemctl restart systemd-resolved
```

## 🧪 Testing

The script includes basic unit tests that can be run with:

```bash
python main.py --test
```

For more comprehensive testing with pytest:
```bash
pip install pytest
python -m pytest main.py::test_domain_validation -v
```

## 🎨 Future Improvements

Here are some potential enhancements for future versions:

### Planned Features
- **Scheduled blocking**: Set specific times when websites should be blocked
- **Time-based restrictions**: Block websites for a specific duration
- **Category-based blocking**: Predefined lists for social media, news, entertainment
- **Password protection**: Require password to unblock websites
- **Whitelist mode**: Block all websites except specified ones
- **Configuration file**: Save blocking preferences in a config file
- **Logging**: Track blocking/unblocking activities with timestamps

### GUI and Web Versions
- **Desktop GUI**: Create a user-friendly desktop application using tkinter or PyQt
- **Web interface**: Build a local web server for browser-based management
- **System tray integration**: Add system tray icon for quick access
- **Browser extension**: Complement the hosts-based blocking with browser-specific features

### Advanced Features
- **Regex support**: Use regular expressions for more flexible domain matching
- **Import/export**: Save and share blocking lists
- **Statistics**: Track time saved by blocking distracting websites
- **Integration**: Connect with productivity apps and time trackers

## 🤝 Contributing

This project is open for improvements! Some areas where contributions would be valuable:

- Cross-platform testing on different operating systems
- Additional validation for edge cases
- Performance optimizations for large hosts files
- User interface improvements
- Documentation enhancements

## 📄 License

This project is released under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- Built with Python standard libraries for maximum compatibility
- Inspired by the need for simple, effective website blocking solutions
- Thanks to the productivity and focus communities for feature suggestions

## 🆘 Troubleshooting

### Common Issues

**Permission Denied Error**:
- Make sure you're running the script as Administrator (Windows) or with sudo (Linux/macOS)

**Websites Still Accessible**:
- Try flushing your DNS cache (see commands above)
- Check if the domains were added correctly with `python main.py list`
- Some browsers may use their own DNS settings

**Backup File Missing**:
- The backup is created automatically in the same directory as the hosts file
- If missing, you can manually restore your hosts file or use system restore

**Script Won't Run**:
- Verify Python 3.7+ is installed: `python --version`
- Check file permissions and ensure the script is executable

For additional help, please check the error messages provided by the script, as they usually contain specific guidance for resolving issues.
