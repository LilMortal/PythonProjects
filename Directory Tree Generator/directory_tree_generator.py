#!/usr/bin/env python3
"""
Directory Tree Generator
A Python utility to generate and display directory structures in a tree format.

Author: Assistant
Version: 1.0.0
Python Version: 3.8+
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Set, Optional


class DirectoryTreeGenerator:
    """
    A class to generate directory tree structures with customizable options.
    """
    
    def __init__(self, show_hidden: bool = False, max_depth: Optional[int] = None,
                 exclude_patterns: Optional[List[str]] = None):
        """
        Initialize the DirectoryTreeGenerator.
        
        Args:
            show_hidden (bool): Whether to show hidden files/directories
            max_depth (int, optional): Maximum depth to traverse
            exclude_patterns (list, optional): Patterns to exclude from the tree
        """
        self.show_hidden = show_hidden
        self.max_depth = max_depth
        self.exclude_patterns = exclude_patterns or []
        self.tree_chars = {
            'branch': '├── ',
            'last_branch': '└── ',
            'pipe': '│   ',
            'space': '    '
        }
    
    def should_exclude(self, path: Path) -> bool:
        """
        Check if a path should be excluded based on patterns.
        
        Args:
            path (Path): Path to check
            
        Returns:
            bool: True if path should be excluded
        """
        name = path.name
        
        # Skip hidden files/directories if not requested
        if not self.show_hidden and name.startswith('.'):
            return True
        
        # Check against exclude patterns
        for pattern in self.exclude_patterns:
            if pattern in name:
                return True
        
        return False
    
    def get_sorted_entries(self, directory: Path) -> List[Path]:
        """
        Get sorted entries from a directory.
        
        Args:
            directory (Path): Directory to scan
            
        Returns:
            List[Path]: Sorted list of directory entries
        """
        try:
            entries = []
            for entry in directory.iterdir():
                if not self.should_exclude(entry):
                    entries.append(entry)
            
            # Sort: directories first, then files, both alphabetically
            entries.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            return entries
        
        except PermissionError:
            return []
    
    def generate_tree(self, root_path: str, output_file: Optional[str] = None) -> str:
        """
        Generate the directory tree structure.
        
        Args:
            root_path (str): Root directory path
            output_file (str, optional): File to save the output
            
        Returns:
            str: Generated tree structure
        """
        try:
            root = Path(root_path).resolve()
            if not root.exists():
                raise FileNotFoundError(f"Directory '{root_path}' does not exist")
            
            if not root.is_dir():
                raise NotADirectoryError(f"'{root_path}' is not a directory")
            
            tree_lines = [str(root)]
            self._build_tree(root, "", True, tree_lines, 0)
            
            tree_output = '\n'.join(tree_lines)
            
            # Save to file if specified
            if output_file:
                self._save_to_file(tree_output, output_file)
            
            return tree_output
            
        except Exception as e:
            error_msg = f"Error generating tree: {str(e)}"
            print(error_msg, file=sys.stderr)
            return error_msg
    
    def _build_tree(self, directory: Path, prefix: str, is_last: bool, 
                   tree_lines: List[str], current_depth: int):
        """
        Recursively build the tree structure.
        
        Args:
            directory (Path): Current directory
            prefix (str): Current prefix for tree formatting
            is_last (bool): Whether this is the last item in its parent
            tree_lines (List[str]): List to store tree lines
            current_depth (int): Current depth in the tree
        """
        # Check depth limit
        if self.max_depth is not None and current_depth >= self.max_depth:
            return
        
        entries = self.get_sorted_entries(directory)
        
        for i, entry in enumerate(entries):
            is_last_entry = (i == len(entries) - 1)
            
            # Choose appropriate tree character
            if is_last_entry:
                tree_char = self.tree_chars['last_branch']
                next_prefix = prefix + self.tree_chars['space']
            else:
                tree_char = self.tree_chars['branch']
                next_prefix = prefix + self.tree_chars['pipe']
            
            # Add entry to tree
            entry_line = f"{prefix}{tree_char}{entry.name}"
            if entry.is_dir():
                entry_line += "/"
            tree_lines.append(entry_line)
            
            # Recurse into subdirectories
            if entry.is_dir():
                self._build_tree(entry, next_prefix, is_last_entry, 
                               tree_lines, current_depth + 1)
    
    def _save_to_file(self, content: str, filename: str):
        """
        Save tree output to a file.
        
        Args:
            content (str): Tree content to save
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Tree saved to: {filename}")
        except Exception as e:
            print(f"Error saving to file: {e}", file=sys.stderr)
    
    def get_stats(self, root_path: str) -> dict:
        """
        Get statistics about the directory structure.
        
        Args:
            root_path (str): Root directory path
            
        Returns:
            dict: Statistics including file and directory counts
        """
        stats = {'directories': 0, 'files': 0, 'total_size': 0}
        
        try:
            root = Path(root_path).resolve()
            for item in root.rglob('*'):
                if self.should_exclude(item):
                    continue
                
                if item.is_dir():
                    stats['directories'] += 1
                elif item.is_file():
                    stats['files'] += 1
                    try:
                        stats['total_size'] += item.stat().st_size
                    except (OSError, PermissionError):
                        pass
        
        except Exception as e:
            print(f"Error calculating stats: {e}", file=sys.stderr)
        
        return stats


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def main():
    """
    Main function to handle command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Generate a directory tree structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py /home/user/project
  python main.py . --show-hidden --max-depth 3
  python main.py /path/to/dir --output tree.txt --exclude __pycache__ .git
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to generate tree for (default: current directory)'
    )
    
    parser.add_argument(
        '--show-hidden',
        action='store_true',
        help='Show hidden files and directories'
    )
    
    parser.add_argument(
        '--max-depth',
        type=int,
        help='Maximum depth to traverse'
    )
    
    parser.add_argument(
        '--exclude',
        nargs='*',
        default=[],
        help='Patterns to exclude from the tree'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file to save the tree'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show directory statistics'
    )
    
    args = parser.parse_args()
    
    # Create tree generator with specified options
    generator = DirectoryTreeGenerator(
        show_hidden=args.show_hidden,
        max_depth=args.max_depth,
        exclude_patterns=args.exclude
    )
    
    # Generate and display tree
    tree_output = generator.generate_tree(args.directory, args.output)
    
    if not args.output:
        print(tree_output)
    
    # Show statistics if requested
    if args.stats:
        stats = generator.get_stats(args.directory)
        print(f"\nStatistics:")
        print(f"Directories: {stats['directories']}")
        print(f"Files: {stats['files']}")
        print(f"Total size: {format_size(stats['total_size'])}")


# Simple unit tests (run with: python main.py --test)
def run_tests():
    """
    Run basic unit tests for the DirectoryTreeGenerator.
    """
    import tempfile
    import shutil
    
    print("Running tests...")
    
    # Test 1: Basic functionality
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test structure
        (temp_path / "folder1").mkdir()
        (temp_path / "folder2").mkdir()
        (temp_path / "file1.txt").touch()
        (temp_path / "folder1" / "subfolder").mkdir()
        (temp_path / "folder1" / "file2.txt").touch()
        
        generator = DirectoryTreeGenerator()
        tree = generator.generate_tree(str(temp_path))
        
        assert "folder1/" in tree
        assert "folder2/" in tree
        assert "file1.txt" in tree
        assert "subfolder/" in tree
        print("✓ Basic functionality test passed")
    
    # Test 2: Hidden files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        (temp_path / ".hidden").touch()
        (temp_path / "visible.txt").touch()
        
        # Test without showing hidden
        generator = DirectoryTreeGenerator(show_hidden=False)
        tree = generator.generate_tree(str(temp_path))
        assert ".hidden" not in tree
        assert "visible.txt" in tree
        
        # Test with showing hidden
        generator = DirectoryTreeGenerator(show_hidden=True)
        tree = generator.generate_tree(str(temp_path))
        assert ".hidden" in tree
        print("✓ Hidden files test passed")
    
    # Test 3: Max depth
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        (temp_path / "level1").mkdir()
        (temp_path / "level1" / "level2").mkdir()
        (temp_path / "level1" / "level2" / "level3").mkdir()
        
        generator = DirectoryTreeGenerator(max_depth=2)
        tree = generator.generate_tree(str(temp_path))
        assert "level1/" in tree
        assert "level2/" in tree
        assert "level3/" not in tree
        print("✓ Max depth test passed")
    
    print("All tests passed! ✓")


if __name__ == "__main__":
    # Check for test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        main()
