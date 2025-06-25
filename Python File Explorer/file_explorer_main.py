#!/usr/bin/env python3
"""
Python File Explorer - A command-line file manager
Author: Assistant
Python Version: 3.8+
"""

import os
import sys
import shutil
import stat
import datetime
import fnmatch
from pathlib import Path
from typing import List, Optional, Tuple


class FileExplorer:
    """A simple command-line file explorer with basic file operations."""
    
    def __init__(self):
        self.current_path = Path.cwd()
        self.history = [self.current_path]
        self.history_index = 0
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_size(self, size_bytes: int) -> str:
        """Convert bytes to human-readable format."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def get_file_info(self, path: Path) -> Tuple[str, str, str, str]:
        """Get file information: type, size, modified date, permissions."""
        try:
            stat_info = path.stat()
            
            # File type
            if path.is_dir():
                file_type = "DIR"
            elif path.is_file():
                file_type = "FILE"
            elif path.is_symlink():
                file_type = "LINK"
            else:
                file_type = "OTHER"
            
            # Size
            size = self.format_size(stat_info.st_size) if path.is_file() else "-"
            
            # Modified date
            mod_time = datetime.datetime.fromtimestamp(stat_info.st_mtime)
            mod_date = mod_time.strftime("%Y-%m-%d %H:%M")
            
            # Permissions
            mode = stat_info.st_mode
            permissions = stat.filemode(mode)
            
            return file_type, size, mod_date, permissions
            
        except (OSError, PermissionError):
            return "ERROR", "-", "-", "-"
    
    def list_directory(self, show_hidden: bool = False) -> List[Path]:
        """List contents of current directory."""
        try:
            items = []
            for item in self.current_path.iterdir():
                if not show_hidden and item.name.startswith('.'):
                    continue
                items.append(item)
            
            # Sort: directories first, then files, alphabetically
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            return items
            
        except PermissionError:
            print(f"Permission denied: Cannot access {self.current_path}")
            return []
        except Exception as e:
            print(f"Error listing directory: {e}")
            return []
    
    def display_directory(self, show_hidden: bool = False):
        """Display current directory contents in a formatted table."""
        items = self.list_directory(show_hidden)
        
        print(f"\n📁 Current Directory: {self.current_path}")
        print("=" * 80)
        
        if not items:
            print("Directory is empty or inaccessible.")
            return
        
        # Header
        print(f"{'Type':<6} {'Name':<30} {'Size':<10} {'Modified':<17} {'Permissions'}")
        print("-" * 80)
        
        # Parent directory link
        if self.current_path.parent != self.current_path:
            print(f"{'DIR':<6} {'.. (parent)':<30} {'-':<10} {'-':<17} {'-'}")
        
        # Directory contents
        for item in items:
            file_type, size, mod_date, permissions = self.get_file_info(item)
            name = item.name
            
            # Truncate long names
            if len(name) > 28:
                name = name[:25] + "..."
            
            # Add visual indicators
            if file_type == "DIR":
                name = f"📁 {name}"
            elif file_type == "LINK":
                name = f"🔗 {name}"
            else:
                name = f"📄 {name}"
            
            print(f"{file_type:<6} {name:<30} {size:<10} {mod_date:<17} {permissions}")
    
    def change_directory(self, path_str: str) -> bool:
        """Change current directory."""
        try:
            if path_str == "..":
                new_path = self.current_path.parent
            elif path_str == ".":
                return True
            elif path_str.startswith("/") or (os.name == 'nt' and ":" in path_str):
                new_path = Path(path_str).resolve()
            else:
                new_path = (self.current_path / path_str).resolve()
            
            if new_path.exists() and new_path.is_dir():
                self.current_path = new_path
                # Add to history
                if self.history_index < len(self.history) - 1:
                    self.history = self.history[:self.history_index + 1]
                self.history.append(self.current_path)
                self.history_index = len(self.history) - 1
                return True
            else:
                print(f"Directory not found: {path_str}")
                return False
                
        except Exception as e:
            print(f"Error changing directory: {e}")
            return False
    
    def create_file(self, filename: str) -> bool:
        """Create a new empty file."""
        try:
            file_path = self.current_path / filename
            if file_path.exists():
                response = input(f"File '{filename}' already exists. Overwrite? (y/N): ")
                if response.lower() != 'y':
                    return False
            
            file_path.touch()
            print(f"File '{filename}' created successfully.")
            return True
            
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    def create_directory(self, dirname: str) -> bool:
        """Create a new directory."""
        try:
            dir_path = self.current_path / dirname
            if dir_path.exists():
                print(f"Directory '{dirname}' already exists.")
                return False
            
            dir_path.mkdir()
            print(f"Directory '{dirname}' created successfully.")
            return True
            
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    def delete_item(self, name: str) -> bool:
        """Delete a file or directory."""
        try:
            item_path = self.current_path / name
            if not item_path.exists():
                print(f"Item '{name}' not found.")
                return False
            
            # Confirm deletion
            item_type = "directory" if item_path.is_dir() else "file"
            response = input(f"Delete {item_type} '{name}'? This cannot be undone! (y/N): ")
            if response.lower() != 'y':
                return False
            
            if item_path.is_dir():
                shutil.rmtree(item_path)
            else:
                item_path.unlink()
            
            print(f"{item_type.capitalize()} '{name}' deleted successfully.")
            return True
            
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False
    
    def copy_item(self, source: str, destination: str) -> bool:
        """Copy a file or directory."""
        try:
            src_path = self.current_path / source
            
            if not src_path.exists():
                print(f"Source '{source}' not found.")
                return False
            
            # Handle destination path
            if "/" in destination or "\\" in destination:
                dst_path = Path(destination)
            else:
                dst_path = self.current_path / destination
            
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
            
            print(f"'{source}' copied to '{destination}' successfully.")
            return True
            
        except Exception as e:
            print(f"Error copying item: {e}")
            return False
    
    def move_item(self, source: str, destination: str) -> bool:
        """Move/rename a file or directory."""
        try:
            src_path = self.current_path / source
            
            if not src_path.exists():
                print(f"Source '{source}' not found.")
                return False
            
            # Handle destination path
            if "/" in destination or "\\" in destination:
                dst_path = Path(destination)
            else:
                dst_path = self.current_path / destination
            
            shutil.move(str(src_path), str(dst_path))
            print(f"'{source}' moved to '{destination}' successfully.")
            return True
            
        except Exception as e:
            print(f"Error moving item: {e}")
            return False
    
    def search_files(self, pattern: str, recursive: bool = False) -> List[Path]:
        """Search for files matching a pattern."""
        try:
            matches = []
            search_path = self.current_path
            
            if recursive:
                # Recursive search
                for item in search_path.rglob(pattern):
                    matches.append(item)
            else:
                # Search in current directory only
                for item in search_path.glob(pattern):
                    matches.append(item)
            
            return matches
            
        except Exception as e:
            print(f"Error searching files: {e}")
            return []
    
    def navigate_history(self, direction: str) -> bool:
        """Navigate through directory history."""
        if direction == "back" and self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            return True
        elif direction == "forward" and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            return True
        else:
            print(f"Cannot navigate {direction}.")
            return False
    
    def show_help(self):
        """Display help information."""
        help_text = """
📚 PYTHON FILE EXPLORER - HELP
================================

NAVIGATION:
  ls, list              - List directory contents
  ls -a                 - List all files (including hidden)
  cd <directory>        - Change directory
  cd ..                 - Go to parent directory
  pwd                   - Print current directory
  back                  - Go back in history
  forward               - Go forward in history

FILE OPERATIONS:
  touch <filename>      - Create empty file
  mkdir <dirname>       - Create directory
  rm <name>             - Delete file or directory
  cp <source> <dest>    - Copy file or directory
  mv <source> <dest>    - Move/rename file or directory

SEARCH:
  find <pattern>        - Search files in current directory
  find -r <pattern>     - Search files recursively

OTHER:
  clear                 - Clear screen
  help                  - Show this help
  exit, quit            - Exit the program

EXAMPLES:
  cd Documents
  touch newfile.txt
  mkdir projects
  find *.py
  cp file1.txt backup.txt
        """
        print(help_text)
    
    def run(self):
        """Main program loop."""
        print("🗂️  Python File Explorer")
        print("Type 'help' for commands or 'exit' to quit.")
        
        while True:
            try:
                # Display prompt
                prompt = f"\n[{self.current_path.name}]> "
                command = input(prompt).strip()
                
                if not command:
                    continue
                
                # Parse command
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                # Execute commands
                if cmd in ['exit', 'quit']:
                    print("Goodbye! 👋")
                    break
                
                elif cmd == 'clear':
                    self.clear_screen()
                
                elif cmd == 'help':
                    self.show_help()
                
                elif cmd in ['ls', 'list']:
                    show_hidden = '-a' in args
                    self.display_directory(show_hidden)
                
                elif cmd == 'pwd':
                    print(f"Current directory: {self.current_path}")
                
                elif cmd == 'cd':
                    if args:
                        self.change_directory(args[0])
                    else:
                        # Go to home directory
                        self.change_directory(str(Path.home()))
                
                elif cmd == 'back':
                    self.navigate_history('back')
                
                elif cmd == 'forward':
                    self.navigate_history('forward')
                
                elif cmd == 'touch':
                    if args:
                        self.create_file(args[0])
                    else:
                        print("Usage: touch <filename>")
                
                elif cmd == 'mkdir':
                    if args:
                        self.create_directory(args[0])
                    else:
                        print("Usage: mkdir <directory_name>")
                
                elif cmd == 'rm':
                    if args:
                        self.delete_item(args[0])
                    else:
                        print("Usage: rm <file_or_directory>")
                
                elif cmd == 'cp':
                    if len(args) >= 2:
                        self.copy_item(args[0], args[1])
                    else:
                        print("Usage: cp <source> <destination>")
                
                elif cmd == 'mv':
                    if len(args) >= 2:
                        self.move_item(args[0], args[1])
                    else:
                        print("Usage: mv <source> <destination>")
                
                elif cmd == 'find':
                    if args:
                        recursive = args[0] == '-r'
                        pattern = args[1] if recursive and len(args) > 1 else args[0]
                        
                        if recursive and len(args) < 2:
                            print("Usage: find -r <pattern>")
                            continue
                        
                        matches = self.search_files(pattern, recursive)
                        if matches:
                            print(f"\nFound {len(matches)} matches:")
                            for match in matches:
                                rel_path = match.relative_to(self.current_path) if recursive else match.name
                                file_type = "📁" if match.is_dir() else "📄"
                                print(f"  {file_type} {rel_path}")
                        else:
                            print(f"No files found matching '{pattern}'")
                    else:
                        print("Usage: find <pattern> or find -r <pattern>")
                
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit the program.")
            except EOFError:
                print("\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


def run_tests():
    """Simple unit tests for FileExplorer class."""
    print("🧪 Running basic tests...")
    
    explorer = FileExplorer()
    
    # Test 1: Format size
    assert explorer.format_size(0) == "0 B"
    assert explorer.format_size(1024) == "1.0 KB"
    assert explorer.format_size(1048576) == "1.0 MB"
    print("✅ Size formatting test passed")
    
    # Test 2: Current directory should be accessible
    assert explorer.current_path.exists()
    print("✅ Current directory test passed")
    
    # Test 3: List directory should return a list
    items = explorer.list_directory()
    assert isinstance(items, list)
    print("✅ Directory listing test passed")
    
    print("🎉 All tests passed!")


if __name__ == "__main__":
    # Uncomment the line below to run tests
    # run_tests()
    
    # Run the main application
    try:
        explorer = FileExplorer()
        explorer.run()
    except Exception as e:
        print(f"Failed to start File Explorer: {e}")
        sys.exit(1)