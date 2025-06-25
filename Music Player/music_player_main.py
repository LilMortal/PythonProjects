#!/usr/bin/env python3
"""
Simple Music Player
A command-line music player with playlist management and basic controls.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import List, Dict, Optional
import subprocess
import platform

# For audio playback, we'll use platform-specific commands
# This keeps the project dependency-free for basic functionality


class Song:
    """Represents a single song with metadata."""
    
    def __init__(self, filepath: str, title: str = None, artist: str = None, duration: float = None):
        self.filepath = Path(filepath)
        self.title = title or self.filepath.stem
        self.artist = artist or "Unknown Artist"
        self.duration = duration or 0.0
        self.play_count = 0
    
    def to_dict(self) -> Dict:
        """Convert song to dictionary for JSON serialization."""
        return {
            'filepath': str(self.filepath),
            'title': self.title,
            'artist': self.artist,
            'duration': self.duration,
            'play_count': self.play_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Song':
        """Create song from dictionary."""
        song = cls(data['filepath'], data['title'], data['artist'], data['duration'])
        song.play_count = data.get('play_count', 0)
        return song
    
    def __str__(self) -> str:
        duration_str = f"{int(self.duration//60)}:{int(self.duration%60):02d}" if self.duration > 0 else "Unknown"
        return f"{self.title} by {self.artist} ({duration_str})"


class Playlist:
    """Manages a collection of songs."""
    
    def __init__(self, name: str = "Default"):
        self.name = name
        self.songs: List[Song] = []
        self.current_index = 0
        self.shuffle_mode = False
        self.repeat_mode = False
    
    def add_song(self, song: Song) -> None:
        """Add a song to the playlist."""
        self.songs.append(song)
        print(f"Added: {song.title}")
    
    def remove_song(self, index: int) -> bool:
        """Remove a song by index."""
        if 0 <= index < len(self.songs):
            removed = self.songs.pop(index)
            print(f"Removed: {removed.title}")
            if self.current_index >= len(self.songs) and self.songs:
                self.current_index = len(self.songs) - 1
            return True
        return False
    
    def get_current_song(self) -> Optional[Song]:
        """Get the currently selected song."""
        if self.songs and 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
        return None
    
    def next_song(self) -> Optional[Song]:
        """Move to next song."""
        if not self.songs:
            return None
        
        if self.repeat_mode:
            # Stay on current song
            return self.get_current_song()
        
        self.current_index = (self.current_index + 1) % len(self.songs)
        return self.get_current_song()
    
    def previous_song(self) -> Optional[Song]:
        """Move to previous song."""
        if not self.songs:
            return None
        
        self.current_index = (self.current_index - 1) % len(self.songs)
        return self.get_current_song()
    
    def to_dict(self) -> Dict:
        """Convert playlist to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'songs': [song.to_dict() for song in self.songs],
            'current_index': self.current_index,
            'shuffle_mode': self.shuffle_mode,
            'repeat_mode': self.repeat_mode
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Playlist':
        """Create playlist from dictionary."""
        playlist = cls(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        playlist.current_index = data.get('current_index', 0)
        playlist.shuffle_mode = data.get('shuffle_mode', False)
        playlist.repeat_mode = data.get('repeat_mode', False)
        return playlist


class AudioPlayer:
    """Handles audio playback using system commands."""
    
    def __init__(self):
        self.current_process = None
        self.is_playing = False
        self.is_paused = False
        self.system = platform.system().lower()
    
    def play(self, filepath: str) -> bool:
        """Start playing an audio file."""
        try:
            self.stop()  # Stop any current playback
            
            # Platform-specific audio playback
            if self.system == "darwin":  # macOS
                cmd = ["afplay", filepath]
            elif self.system == "linux":
                # Try common Linux audio players
                for player in ["mpg123", "mplayer", "aplay"]:
                    if subprocess.run(["which", player], capture_output=True).returncode == 0:
                        cmd = [player, filepath]
                        break
                else:
                    print("No audio player found. Install mpg123, mplayer, or similar.")
                    return False
            elif self.system == "windows":
                # Windows Media Player command line
                cmd = ["powershell", "-c", f"(New-Object Media.SoundPlayer '{filepath}').PlaySync()"]
            else:
                print(f"Unsupported platform: {self.system}")
                return False
            
            # Start playback in background thread
            self.current_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            self.is_playing = True
            self.is_paused = False
            return True
            
        except Exception as e:
            print(f"Error playing file: {e}")
            return False
    
    def stop(self) -> None:
        """Stop current playback."""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.current_process.kill()
            except Exception:
                pass
            finally:
                self.current_process = None
        
        self.is_playing = False
        self.is_paused = False
    
    def is_playing_song(self) -> bool:
        """Check if a song is currently playing."""
        if self.current_process:
            return self.current_process.poll() is None
        return False


class MusicPlayer:
    """Main music player class that coordinates everything."""
    
    def __init__(self):
        self.playlist = Playlist()
        self.audio_player = AudioPlayer()
        self.config_file = Path.home() / ".music_player_config.json"
        self.supported_formats = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac'}
        
        # Load saved configuration
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.playlist = Playlist.from_dict(data.get('playlist', {}))
                print(f"Loaded playlist: {len(self.playlist.songs)} songs")
        except Exception as e:
            print(f"Could not load config: {e}")
    
    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            config = {
                'playlist': self.playlist.to_dict()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print("Configuration saved.")
        except Exception as e:
            print(f"Could not save config: {e}")
    
    def add_music_from_directory(self, directory: str) -> None:
        """Add all supported music files from a directory."""
        directory_path = Path(directory)
        if not directory_path.exists():
            print(f"Directory not found: {directory}")
            return
        
        added_count = 0
        for file_path in directory_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                song = Song(str(file_path))
                self.playlist.add_song(song)
                added_count += 1
        
        print(f"Added {added_count} songs from {directory}")
    
    def add_single_file(self, filepath: str) -> None:
        """Add a single music file."""
        file_path = Path(filepath)
        if not file_path.exists():
            print(f"File not found: {filepath}")
            return
        
        if file_path.suffix.lower() not in self.supported_formats:
            print(f"Unsupported format: {file_path.suffix}")
            return
        
        song = Song(str(file_path))
        self.playlist.add_song(song)
    
    def play_current(self) -> None:
        """Play the current song."""
        current_song = self.playlist.get_current_song()
        if not current_song:
            print("No songs in playlist!")
            return
        
        if not current_song.filepath.exists():
            print(f"File not found: {current_song.filepath}")
            return
        
        print(f"♪ Playing: {current_song}")
        current_song.play_count += 1
        
        if self.audio_player.play(str(current_song.filepath)):
            # Monitor playback in separate thread
            threading.Thread(target=self._monitor_playback, daemon=True).start()
    
    def _monitor_playback(self) -> None:
        """Monitor playback and auto-advance to next song."""
        while self.audio_player.is_playing_song():
            time.sleep(1)
        
        # Song finished, advance to next if not manually stopped
        if self.audio_player.is_playing:
            self.next_song()
    
    def next_song(self) -> None:
        """Skip to next song."""
        next_song = self.playlist.next_song()
        if next_song:
            self.play_current()
        else:
            print("End of playlist")
    
    def previous_song(self) -> None:
        """Go to previous song."""
        prev_song = self.playlist.previous_song()
        if prev_song:
            self.play_current()
    
    def stop(self) -> None:
        """Stop playback."""
        self.audio_player.stop()
        print("⏹ Stopped")
    
    def show_playlist(self) -> None:
        """Display the current playlist."""
        if not self.playlist.songs:
            print("Playlist is empty")
            return
        
        print(f"\n📋 Playlist: {self.playlist.name}")
        print("-" * 50)
        for i, song in enumerate(self.playlist.songs):
            marker = "► " if i == self.playlist.current_index else "  "
            print(f"{marker}{i+1:2d}. {song}")
        print("-" * 50)
        print(f"Total: {len(self.playlist.songs)} songs")
        
        modes = []
        if self.playlist.shuffle_mode:
            modes.append("Shuffle")
        if self.playlist.repeat_mode:
            modes.append("Repeat")
        if modes:
            print(f"Modes: {', '.join(modes)}")
    
    def show_help(self) -> None:
        """Display help information."""
        help_text = """
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
        """
        print(help_text)
    
    def run(self) -> None:
        """Main interactive loop."""
        print("🎵 Welcome to Simple Music Player!")
        print("Type 'help' for commands or 'quit' to exit")
        
        if self.playlist.songs:
            print(f"Loaded {len(self.playlist.songs)} songs")
        
        try:
            while True:
                try:
                    command = input("\n♪ > ").strip().lower()
                    
                    if not command:
                        continue
                    
                    parts = command.split()
                    cmd = parts[0]
                    
                    if cmd in ['quit', 'exit', 'q']:
                        break
                    elif cmd == 'help':
                        self.show_help()
                    elif cmd == 'play':
                        self.play_current()
                    elif cmd == 'stop':
                        self.stop()
                    elif cmd == 'next':
                        self.next_song()
                    elif cmd == 'prev':
                        self.previous_song()
                    elif cmd == 'list':
                        self.show_playlist()
                    elif cmd == 'add':
                        if len(parts) > 1:
                            path = ' '.join(parts[1:])
                            if os.path.isdir(path):
                                self.add_music_from_directory(path)
                            else:
                                self.add_single_file(path)
                        else:
                            print("Usage: add <file_or_directory>")
                    elif cmd == 'remove':
                        if len(parts) > 1:
                            try:
                                index = int(parts[1]) - 1
                                self.playlist.remove_song(index)
                            except ValueError:
                                print("Please provide a valid song number")
                        else:
                            print("Usage: remove <song_number>")
                    elif cmd == 'goto':
                        if len(parts) > 1:
                            try:
                                index = int(parts[1]) - 1
                                if 0 <= index < len(self.playlist.songs):
                                    self.playlist.current_index = index
                                    print(f"Moved to: {self.playlist.get_current_song()}")
                                else:
                                    print("Invalid song number")
                            except ValueError:
                                print("Please provide a valid song number")
                        else:
                            print("Usage: goto <song_number>")
                    elif cmd == 'clear':
                        self.playlist.songs.clear()
                        self.playlist.current_index = 0
                        print("Playlist cleared")
                    elif cmd == 'shuffle':
                        self.playlist.shuffle_mode = not self.playlist.shuffle_mode
                        status = "ON" if self.playlist.shuffle_mode else "OFF"
                        print(f"Shuffle mode: {status}")
                    elif cmd == 'repeat':
                        self.playlist.repeat_mode = not self.playlist.repeat_mode
                        status = "ON" if self.playlist.repeat_mode else "OFF"
                        print(f"Repeat mode: {status}")
                    elif cmd == 'save':
                        self.save_config()
                    else:
                        print(f"Unknown command: {cmd}. Type 'help' for available commands.")
                
                except KeyboardInterrupt:
                    print("\nUse 'quit' to exit")
                except Exception as e:
                    print(f"Error: {e}")
        
        finally:
            # Cleanup
            self.stop()
            self.save_config()
            print("👋 Thanks for using Simple Music Player!")


def main():
    """Entry point of the application."""
    player = MusicPlayer()
    player.run()


if __name__ == "__main__":
    main()


# Simple Unit Tests (run with: python -m pytest main.py::test_* -v)
def test_song_creation():
    """Test song creation and serialization."""
    song = Song("test.mp3", "Test Song", "Test Artist", 180.0)
    assert song.title == "Test Song"
    assert song.artist == "Test Artist"
    assert song.duration == 180.0
    
    # Test serialization
    data = song.to_dict()
    restored_song = Song.from_dict(data)
    assert restored_song.title == song.title
    assert restored_song.artist == song.artist


def test_playlist_operations():
    """Test playlist functionality."""
    playlist = Playlist("Test Playlist")
    
    # Test adding songs
    song1 = Song("song1.mp3", "Song 1")
    song2 = Song("song2.mp3", "Song 2")
    
    playlist.add_song(song1)
    playlist.add_song(song2)
    
    assert len(playlist.songs) == 2
    assert playlist.get_current_song() == song1
    
    # Test navigation
    next_song = playlist.next_song()
    assert next_song == song2
    
    prev_song = playlist.previous_song()
    assert prev_song == song1


def test_supported_formats():
    """Test supported audio formats."""
    player = MusicPlayer()
    supported = player.supported_formats
    
    assert '.mp3' in supported
    assert '.wav' in supported
    assert '.flac' in supported
    assert '.txt' not in supported


# Run tests if called with test argument
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    print("Running basic tests...")
    test_song_creation()
    test_playlist_operations()
    test_supported_formats()
    print("✅ All tests passed!")
