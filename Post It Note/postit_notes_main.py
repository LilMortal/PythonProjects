#!/usr/bin/env python3
"""
Post-it Notes Manager
A command-line application for managing digital sticky notes.

Author: Claude AI Assistant
Version: 1.0.0
Python: 3.8+
"""

import json
import os
import datetime
from typing import List, Dict, Optional
import argparse
import sys


class PostItNote:
    """Represents a single Post-it note."""
    
    def __init__(self, title: str, content: str, note_id: Optional[int] = None, 
                 created_at: Optional[str] = None, color: str = "yellow"):
        self.id = note_id
        self.title = title.strip()
        self.content = content.strip()
        self.color = color
        self.created_at = created_at or datetime.datetime.now().isoformat()
        self.updated_at = datetime.datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert note to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'color': self.color,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PostItNote':
        """Create note from dictionary."""
        note = cls(data['title'], data['content'], data.get('id'), 
                  data.get('created_at'), data.get('color', 'yellow'))
        note.updated_at = data.get('updated_at', note.updated_at)
        return note
    
    def __str__(self) -> str:
        """String representation of the note."""
        border = "=" * 50
        return f"\n{border}\n📝 Note #{self.id} - {self.title}\n{border}\n{self.content}\n📅 Created: {self.created_at[:19]}\n🎨 Color: {self.color}\n{border}"


class PostItNotesManager:
    """Main class for managing Post-it notes."""
    
    def __init__(self, data_file: str = "notes_data.json"):
        self.data_file = data_file
        self.notes: List[PostItNote] = []
        self.next_id = 1
        self.load_notes()
    
    def load_notes(self) -> None:
        """Load notes from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.notes = [PostItNote.from_dict(note_data) for note_data in data.get('notes', [])]
                    self.next_id = data.get('next_id', 1)
                    
                    # Ensure all notes have IDs
                    for note in self.notes:
                        if note.id is None:
                            note.id = self.next_id
                            self.next_id += 1
            else:
                print(f"📂 No existing data file found. Starting fresh!")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️  Error loading notes: {e}")
            print("Starting with empty notes collection.")
            self.notes = []
    
    def save_notes(self) -> None:
        """Save notes to JSON file."""
        try:
            data = {
                'notes': [note.to_dict() for note in self.notes],
                'next_id': self.next_id
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving notes: {e}")
    
    def create_note(self, title: str, content: str, color: str = "yellow") -> PostItNote:
        """Create a new note."""
        if not title.strip():
            raise ValueError("Note title cannot be empty")
        if not content.strip():
            raise ValueError("Note content cannot be empty")
        
        valid_colors = ["yellow", "blue", "green", "pink", "orange", "purple"]
        if color not in valid_colors:
            print(f"⚠️  Invalid color '{color}'. Using 'yellow' instead.")
            color = "yellow"
        
        note = PostItNote(title, content, self.next_id, color=color)
        self.notes.append(note)
        self.next_id += 1
        self.save_notes()
        print(f"✅ Note created successfully! (ID: {note.id})")
        return note
    
    def list_notes(self, color_filter: Optional[str] = None) -> None:
        """List all notes or filter by color."""
        if not self.notes:
            print("📭 No notes found. Create your first note!")
            return
        
        filtered_notes = self.notes
        if color_filter:
            filtered_notes = [note for note in self.notes if note.color == color_filter]
            if not filtered_notes:
                print(f"📭 No notes found with color '{color_filter}'")
                return
        
        print(f"\n📚 Your Notes ({len(filtered_notes)} total):")
        print("=" * 60)
        
        for note in filtered_notes:
            print(f"#{note.id:2d} | 🎨 {note.color:8s} | {note.title[:30]:30s} | {note.created_at[:19]}")
        
        print("=" * 60)
        print("💡 Use 'view <id>' to see full content or 'help' for more options")
    
    def view_note(self, note_id: int) -> Optional[PostItNote]:
        """View a specific note by ID."""
        note = self.find_note_by_id(note_id)
        if note:
            print(note)
            return note
        else:
            print(f"❌ Note with ID {note_id} not found")
            return None
    
    def update_note(self, note_id: int, title: Optional[str] = None, 
                   content: Optional[str] = None, color: Optional[str] = None) -> bool:
        """Update an existing note."""
        note = self.find_note_by_id(note_id)
        if not note:
            print(f"❌ Note with ID {note_id} not found")
            return False
        
        if title:
            note.title = title.strip()
        if content:
            note.content = content.strip()
        if color:
            valid_colors = ["yellow", "blue", "green", "pink", "orange", "purple"]
            if color in valid_colors:
                note.color = color
            else:
                print(f"⚠️  Invalid color '{color}'. Color not updated.")
        
        note.updated_at = datetime.datetime.now().isoformat()
        self.save_notes()
        print(f"✅ Note #{note_id} updated successfully!")
        return True
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note by ID."""
        note = self.find_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print(f"🗑️  Note #{note_id} deleted successfully!")
            return True
        else:
            print(f"❌ Note with ID {note_id} not found")
            return False
    
    def search_notes(self, query: str) -> List[PostItNote]:
        """Search notes by title or content."""
        query = query.lower()
        results = []
        for note in self.notes:
            if query in note.title.lower() or query in note.content.lower():
                results.append(note)
        
        if results:
            print(f"\n🔍 Search results for '{query}' ({len(results)} found):")
            print("=" * 60)
            for note in results:
                print(f"#{note.id:2d} | {note.title[:40]:40s} | {note.color}")
            print("=" * 60)
        else:
            print(f"🔍 No notes found matching '{query}'")
        
        return results
    
    def find_note_by_id(self, note_id: int) -> Optional[PostItNote]:
        """Find a note by its ID."""
        for note in self.notes:
            if note.id == note_id:
                return note
        return None
    
    def get_stats(self) -> None:
        """Display statistics about notes."""
        if not self.notes:
            print("📊 No notes to analyze")
            return
        
        total_notes = len(self.notes)
        color_counts = {}
        
        for note in self.notes:
            color_counts[note.color] = color_counts.get(note.color, 0) + 1
        
        print(f"\n📊 Notes Statistics")
        print("=" * 30)
        print(f"Total Notes: {total_notes}")
        print(f"Data File: {self.data_file}")
        print("\nNotes by Color:")
        for color, count in sorted(color_counts.items()):
            print(f"  🎨 {color.capitalize()}: {count}")
        print("=" * 30)


def print_help():
    """Display help information."""
    help_text = """
🗒️  Post-it Notes Manager - Help

COMMANDS:
  create                    Create a new note (interactive)
  list [color]             List all notes or filter by color
  view <id>                View a specific note
  search <query>           Search notes by title/content
  update <id>              Update a note (interactive)
  delete <id>              Delete a note
  stats                    Show notes statistics
  help                     Show this help message
  exit                     Exit the application

COLORS:
  yellow, blue, green, pink, orange, purple

EXAMPLES:
  python main.py create
  python main.py list blue
  python main.py view 1
  python main.py search "meeting"
  python main.py delete 5

You can also run without arguments for interactive mode.
    """
    print(help_text)


def interactive_create_note(manager: PostItNotesManager) -> None:
    """Interactive note creation."""
    try:
        print("\n📝 Creating a new note...")
        title = input("Enter note title: ").strip()
        if not title:
            print("❌ Title cannot be empty!")
            return
        
        print("Enter note content (press Enter twice to finish):")
        content_lines = []
        while True:
            line = input()
            if line == "" and content_lines and content_lines[-1] == "":
                break
            content_lines.append(line)
        
        content = "\n".join(content_lines).strip()
        if not content:
            print("❌ Content cannot be empty!")
            return
        
        print("Available colors: yellow, blue, green, pink, orange, purple")
        color = input("Enter color (default: yellow): ").strip().lower() or "yellow"
        
        manager.create_note(title, content, color)
        
    except KeyboardInterrupt:
        print("\n❌ Note creation cancelled.")
    except Exception as e:
        print(f"❌ Error creating note: {e}")


def interactive_update_note(manager: PostItNotesManager, note_id: int) -> None:
    """Interactive note update."""
    try:
        note = manager.find_note_by_id(note_id)
        if not note:
            print(f"❌ Note {note_id} not found!")
            return
        
        print(f"\n✏️  Updating note #{note_id}")
        print(f"Current title: {note.title}")
        new_title = input("New title (press Enter to keep current): ").strip()
        
        print(f"Current content: {note.content[:50]}...")
        update_content = input("Update content? (y/n): ").strip().lower()
        new_content = None
        
        if update_content == 'y':
            print("Enter new content (press Enter twice to finish):")
            content_lines = []
            while True:
                line = input()
                if line == "" and content_lines and content_lines[-1] == "":
                    break
                content_lines.append(line)
            new_content = "\n".join(content_lines).strip()
        
        print(f"Current color: {note.color}")
        new_color = input("New color (press Enter to keep current): ").strip().lower()
        
        manager.update_note(
            note_id, 
            new_title if new_title else None,
            new_content if new_content else None,
            new_color if new_color else None
        )
        
    except KeyboardInterrupt:
        print("\n❌ Update cancelled.")
    except Exception as e:
        print(f"❌ Error updating note: {e}")


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Post-it Notes Manager - A command-line sticky notes app",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')
    parser.add_argument('--data-file', default='notes_data.json', 
                       help='Path to data file (default: notes_data.json)')
    
    # If no arguments provided, show help and enter interactive mode
    if len(sys.argv) == 1:
        print("🗒️  Welcome to Post-it Notes Manager!")
        print("Type 'help' for available commands or 'exit' to quit.")
        
        manager = PostItNotesManager()
        
        while True:
            try:
                user_input = input("\n📝 > ").strip().split()
                if not user_input:
                    continue
                
                command = user_input[0].lower()
                args = user_input[1:]
                
                if command == 'exit':
                    print("👋 Goodbye!")
                    break
                elif command == 'help':
                    print_help()
                elif command == 'create':
                    interactive_create_note(manager)
                elif command == 'list':
                    color_filter = args[0] if args else None
                    manager.list_notes(color_filter)
                elif command == 'view':
                    if args:
                        try:
                            note_id = int(args[0])
                            manager.view_note(note_id)
                        except ValueError:
                            print("❌ Please provide a valid note ID")
                    else:
                        print("❌ Please provide a note ID")
                elif command == 'search':
                    if args:
                        query = ' '.join(args)
                        manager.search_notes(query)
                    else:
                        print("❌ Please provide a search query")
                elif command == 'update':
                    if args:
                        try:
                            note_id = int(args[0])
                            interactive_update_note(manager, note_id)
                        except ValueError:
                            print("❌ Please provide a valid note ID")
                    else:
                        print("❌ Please provide a note ID")
                elif command == 'delete':
                    if args:
                        try:
                            note_id = int(args[0])
                            confirm = input(f"Are you sure you want to delete note #{note_id}? (y/n): ")
                            if confirm.lower() == 'y':
                                manager.delete_note(note_id)
                        except ValueError:
                            print("❌ Please provide a valid note ID")
                    else:
                        print("❌ Please provide a note ID")
                elif command == 'stats':
                    manager.get_stats()
                else:
                    print(f"❌ Unknown command: {command}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return
    
    # Command-line mode
    args = parser.parse_args()
    manager = PostItNotesManager(args.data_file)
    
    if not args.command:
        print_help()
        return
    
    command = args.command.lower()
    
    try:
        if command == 'create':
            interactive_create_note(manager)
        elif command == 'list':
            color_filter = args.args[0] if args.args else None
            manager.list_notes(color_filter)
        elif command == 'view':
            if args.args:
                note_id = int(args.args[0])
                manager.view_note(note_id)
            else:
                print("❌ Please provide a note ID")
        elif command == 'search':
            if args.args:
                query = ' '.join(args.args)
                manager.search_notes(query)
            else:
                print("❌ Please provide a search query")
        elif command == 'update':
            if args.args:
                note_id = int(args.args[0])
                interactive_update_note(manager, note_id)
            else:
                print("❌ Please provide a note ID")
        elif command == 'delete':
            if args.args:
                note_id = int(args.args[0])
                manager.delete_note(note_id)
            else:
                print("❌ Please provide a note ID")
        elif command == 'stats':
            manager.get_stats()
        elif command == 'help':
            print_help()
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
            
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


# Simple unit tests (run with: python main.py test)
def run_tests():
    """Run basic unit tests."""
    print("🧪 Running unit tests...")
    
    # Test note creation
    note = PostItNote("Test Title", "Test Content")
    assert note.title == "Test Title"
    assert note.content == "Test Content"
    assert note.color == "yellow"
    print("✅ Note creation test passed")
    
    # Test manager
    import tempfile
    import os
    
    temp_file = tempfile.mktemp(suffix='.json')
    try:
        manager = PostItNotesManager(temp_file)
        
        # Test create
        note = manager.create_note("Test", "Content", "blue")
        assert note.id == 1
        assert len(manager.notes) == 1
        print("✅ Manager create test passed")
        
        # Test find
        found = manager.find_note_by_id(1)
        assert found is not None
        assert found.title == "Test"
        print("✅ Manager find test passed")
        
        # Test update
        success = manager.update_note(1, title="Updated Title")
        assert success
        assert manager.find_note_by_id(1).title == "Updated Title"
        print("✅ Manager update test passed")
        
        # Test delete
        success = manager.delete_note(1)
        assert success
        assert len(manager.notes) == 0
        print("✅ Manager delete test passed")
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print("🎉 All tests passed!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
    else:
        main()