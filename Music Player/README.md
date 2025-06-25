# 🎵 Simple Music Player

A command-line music player written in Python with playlist management, playback controls, and cross-platform audio support. This lightweight music player focuses on simplicity and ease of use while providing essential music playback features.

## 📖 Description

Simple Music Player is a terminal-based music application that allows you to organize and play your music collection without the need for complex GUI applications. It supports common audio formats and provides intuitive commands for playlist management and playback control. The player automatically saves your playlist and preferences, so you can pick up where you left off.

## ✨ Features

- **Multi-format Support**: Plays MP3, WAV, M4A, FLAC, OGG, and AAC files
- **Playlist Management**: Add single files or entire directories to your playlist
- **Playback Controls**: Play, stop, next, previous, and jump to specific songs
- **Auto-advance**: Automatically plays the next song when current song finishes
- **Repeat & Shuffle**: Toggle repeat mode for current song and shuffle mode
- **Persistence**: Automatically saves and loads your playlist between sessions
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Clean Interface**: Simple command-line interface with clear feedback
- **Play Statistics**: Tracks how many times each song has been played

## 🔧 System Requirements

- **Python Version**: Python 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Audio Dependencies**: 
  - macOS: Built-in `afplay` (no additional installation needed)
  - Linux: `mpg123`, `mplayer`, or `aplay` (install via package manager)
  - Windows: Built-in PowerShell audio support

## 📦 Installation

### Step 1: Download the Files

Save the `main.py` file to your desired directory.

### Step 2: Install Audio Dependencies (Linux only)

On Linux systems, install an audio player:

```bash
# Ubuntu/Debian
sudo apt-get install mpg123

# CentOS/RHEL/Fedora
sudo yum install mpg123
# or
sudo dnf install mpg123

# Arch Linux
sudo pacman -S mpg123
```

### Step 3: Make the Script Executable (Optional)

```bash
chmod +x main.py
```

## 🚀 How to Run

Navigate to the directory containing `main.py` and run:

```bash
python main.py
```

Or if you made it executable:

```bash
./main.py
```

## 💻 Usage Examples

### Basic Usage

```
🎵 Welcome to Simple Music Player!
Type 'help' for commands or 'quit' to exit

♪ > help
🎵 Music Player Commands:

File Management:
  add <file/directory>  - Add music file(s) to playlist
  remove <number>       - Remove song by number from playlist
  clear                 - Clear entire playlist

Playback Controls:
  play                  - Play current song
  stop                  - Stop playback
  next                  - Next song
  prev                  - Previous song

Playlist Management:
  list                  - Show playlist
  goto <number>         - Jump to song number
  shuffle               - Toggle shuffle mode
  repeat                - Toggle repeat mode

Other:
  save                  - Save current playlist
  help                  - Show this help
  quit/exit             - Exit player
```

### Adding Music

```bash
# Add a single file
♪ > add /path/to/song.mp3
Added: My Favorite Song

# Add entire directory
♪ > add /path/to/music/folder
Added 25 songs from /path/to/music/folder

# View your playlist
♪ > list
📋 Playlist: Default
--------------------------------------------------
►  1. My Favorite Song by Unknown Artist (3:45)
   2. Another Song by Cool Artist (4:12)
   3. Great Track by Awesome Band (3:28)
--------------------------------------------------
Total: 3 songs
```

### Playback Control

```bash
# Play current song
♪ > play
♪ Playing: My Favorite Song by Unknown Artist (3:45)

# Skip to next song
♪ > next
♪ Playing: Another Song by Cool Artist (4:12)

# Jump to specific song
♪ > goto 3
Moved to: Great Track by Awesome Band (3:28)

# Toggle repeat mode
♪ > repeat
Repeat mode: ON
```

### Sample Session

```
$ python main.py
🎵 Welcome to Simple Music Player!
Type 'help' for commands or 'quit' to exit

♪ > add ~/Music
Added 42 songs from /home/user/Music

♪ > list
📋 Playlist: Default
--------------------------------------------------
►  1. Bohemian Rhapsody by Queen (5:55)
   2. Stairway to Heaven by Led Zeppelin (8:02)
   3. Hotel California by Eagles (6:30)
--------------------------------------------------
Total: 42 songs

♪ > play
♪ Playing: Bohemian Rhapsody by Queen (5:55)

♪ > shuffle
Shuffle mode: ON

♪ > next
♪ Playing: Hotel California by Eagles (6:30)

♪ > quit
Configuration saved.
👋 Thanks for using Simple Music Player!
```

## 🧪 Testing

The code includes basic unit tests. Run them with:

```bash
python main.py test
```

For more comprehensive testing (requires pytest):

```bash
pip install pytest
python -m pytest main.py::test_* -v
```

## 🔧 Configuration

The player automatically saves your configuration to `~/.music_player_config.json`, including:
- Your current playlist
- Current song position
- Repeat and shuffle mode settings
- Play count statistics

## 🎨 Converting to GUI or Web Version

### GUI Version with tkinter

To create a GUI version, you could:

1. **Replace the command loop** with tkinter widgets:
   ```python
   import tkinter as tk
   from tkinter import filedialog, messagebox
   
   class MusicPlayerGUI:
       def __init__(self):
           self.root = tk.Tk()
           self.player = MusicPlayer()
           self.create_widgets()
   ```

2. **Add visual controls**:
   - Play/Pause/Stop buttons
   - Progress bar for current song
   - Volume slider
   - Playlist display with scrollbar

### Web Version with Flask

For a web interface:

1. **Create Flask routes** for each player action:
   ```python
   from flask import Flask, render_template, request, jsonify
   
   app = Flask(__name__)
   player = MusicPlayer()
   
   @app.route('/play', methods=['POST'])
   def play_song():
       player.play_current()
       return jsonify({'status': 'playing'})
   ```

2. **Add HTML templates** with JavaScript for real-time updates
3. **Use WebSocket** for live playback status updates

## 🚀 Future Improvements

### Audio Features
- **Volume Control**: Add volume adjustment functionality
- **Equalizer**: Basic bass/treble controls
- **Crossfade**: Smooth transitions between songs
- **Audio Visualizer**: Simple frequency spectrum display

### Playlist Features
- **Multiple Playlists**: Create and manage multiple named playlists
- **Smart Playlists**: Auto-generate playlists based on criteria
- **Playlist Import/Export**: Support for M3U and PLS formats
- **Search Functionality**: Find songs by title, artist, or album

### User Interface
- **Progress Bar**: Show current playback position
- **Lyrics Display**: Show synchronized lyrics if available
- **Album Art**: Display cover art for current song
- **Keyboard Shortcuts**: Global hotkeys for common actions

### Advanced Features
- **Music Library Scanner**: Automatically detect and organize music
- **Metadata Editing**: Edit song tags and information
- **Last.fm Integration**: Scrobble played tracks
- **Internet Radio**: Stream online radio stations
- **Podcast Support**: Play and manage podcast episodes

### Technical Improvements
- **Better Audio Backend**: Use pygame or pyglet for better audio control
- **Gapless Playback**: Seamless transitions between songs
- **Audio Format Conversion**: Convert between different audio formats
- **Plugin System**: Allow custom extensions and themes

## 🤝 Contributing

This is a single-file educational project, but you can extend it by:

1. **Fork the code** and add new features
2. **Create additional modules** for specific functionality
3. **Add new audio backends** for better platform support
4. **Improve error handling** for edge cases
5. **Add more comprehensive tests**

## 📄 License

This project is provided as-is for educational purposes. Feel free to modify and distribute according to your needs.

## 🙏 Acknowledgments

- **Python Standard Library**: For providing robust cross-platform functionality
- **Platform Audio Tools**: afplay (macOS), mpg123 (Linux), PowerShell (Windows)
- **Music Community**: For inspiring simple, functional music player design

---

**Note**: This music player is designed for personal use with legally owned music files. Ensure you have the rights to play any audio files you add to your playlist.
