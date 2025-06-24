#!/usr/bin/env python3
"""
Personal Task Manager - A command-line task management application
Author: Claude Assistant
Version: 1.0.0
Python Version: 3.8+
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import argparse


class Task:
    """Represents a single task with its properties."""
    
    def __init__(self, title: str, description: str = "", priority: str = "medium", 
                 due_date: Optional[str] = None, task_id: Optional[int] = None):
        self.id = task_id if task_id is not None else int(datetime.now().timestamp() * 1000)
        self.title = title
        self.description = description
        self.priority = priority.lower()
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary."""
        task = cls(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            due_date=data.get('due_date'),
            task_id=data['id']
        )
        task.completed = data.get('completed', False)
        task.created_at = data.get('created_at', datetime.now().isoformat())
        task.completed_at = data.get('completed_at')
        return task
    
    def mark_complete(self):
        """Mark task as completed."""
        self.completed = True
        self.completed_at = datetime.now().isoformat()
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date or self.completed:
            return False
        try:
            due = datetime.fromisoformat(self.due_date)
            return datetime.now() > due
        except ValueError:
            return False
    
    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        priority_symbols = {"low": "↓", "medium": "→", "high": "↑"}
        priority_symbol = priority_symbols.get(self.priority, "→")
        
        result = f"{status} [{self.id}] {priority_symbol} {self.title}"
        
        if self.due_date:
            due_str = f" (Due: {self.due_date})"
            if self.is_overdue():
                due_str = f" (OVERDUE: {self.due_date})"
            result += due_str
        
        if self.description:
            result += f"\n    {self.description}"
        
        return result


class TaskManager:
    """Main task manager class that handles all operations."""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Warning: Could not load tasks from {self.data_file}: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2)
        except IOError as e:
            print(f"Error: Could not save tasks to {self.data_file}: {e}")
    
    def add_task(self, title: str, description: str = "", priority: str = "medium", 
                 due_date: Optional[str] = None) -> Task:
        """Add a new task."""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be 'low', 'medium', or 'high'")
        
        # Validate due date format if provided
        if due_date:
            try:
                datetime.fromisoformat(due_date)
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format")
        
        task = Task(title, description, priority, due_date)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def list_tasks(self, show_completed: bool = False, filter_priority: Optional[str] = None) -> List[Task]:
        """List tasks with optional filters."""
        filtered_tasks = self.tasks
        
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        
        if filter_priority:
            filtered_tasks = [task for task in filtered_tasks if task.priority == filter_priority.lower()]
        
        # Sort by priority (high -> medium -> low) then by due date
        priority_order = {"high": 0, "medium": 1, "low": 2}
        filtered_tasks.sort(key=lambda t: (
            priority_order.get(t.priority, 1),
            t.due_date or "9999-12-31",
            t.created_at
        ))
        
        return filtered_tasks
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    print(f"Task '{task.title}' is already completed!")
                    return False
                task.mark_complete()
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_stats(self) -> Dict:
        """Get task statistics."""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        overdue = sum(1 for task in self.tasks if task.is_overdue())
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue
        }


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Personal Task Manager - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add "Buy groceries" --priority high --due 2024-12-25
  python main.py list --all
  python main.py complete 123456789
  python main.py delete 123456789
  python main.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--description', '-d', default='', help='Task description')
    add_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], 
                           default='medium', help='Task priority')
    add_parser.add_argument('--due', help='Due date (YYYY-MM-DD format)')
    
    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--all', '-a', action='store_true', 
                           help='Show completed tasks too')
    list_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'],
                           help='Filter by priority')
    
    # Complete task command
    complete_parser = subparsers.add_parser('complete', help='Mark task as completed')
    complete_parser.add_argument('task_id', type=int, help='Task ID to complete')
    
    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='Task ID to delete')
    
    # Stats command
    subparsers.add_parser('stats', help='Show task statistics')
    
    return parser


def main():
    """Main application entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize task manager
    task_manager = TaskManager()
    
    try:
        if args.command == 'add':
            task = task_manager.add_task(
                title=args.title,
                description=args.description,
                priority=args.priority,
                due_date=args.due
            )
            print(f"✓ Task added successfully!")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            if task.description:
                print(f"  Description: {task.description}")
            print(f"  Priority: {task.priority}")
            if task.due_date:
                print(f"  Due: {task.due_date}")
        
        elif args.command == 'list':
            tasks = task_manager.list_tasks(
                show_completed=args.all,
                filter_priority=args.priority
            )
            
            if not tasks:
                print("No tasks found!")
                return
            
            print(f"\n{'='*50}")
            print(f"TASKS ({len(tasks)} found)")
            print(f"{'='*50}")
            
            for task in tasks:
                print(task)
                print("-" * 30)
        
        elif args.command == 'complete':
            if task_manager.complete_task(args.task_id):
                task = task_manager.get_task(args.task_id)
                print(f"✓ Task completed: {task.title}")
            else:
                print(f"✗ Task with ID {args.task_id} not found!")
        
        elif args.command == 'delete':
            task = task_manager.get_task(args.task_id)
            if task and task_manager.delete_task(args.task_id):
                print(f"✓ Task deleted: {task.title}")
            else:
                print(f"✗ Task with ID {args.task_id} not found!")
        
        elif args.command == 'stats':
            stats = task_manager.get_stats()
            print(f"\n{'='*30}")
            print(f"TASK STATISTICS")
            print(f"{'='*30}")
            print(f"Total tasks:     {stats['total']}")
            print(f"Completed:       {stats['completed']}")
            print(f"Pending:         {stats['pending']}")
            print(f"Overdue:         {stats['overdue']}")
            
            if stats['total'] > 0:
                completion_rate = (stats['completed'] / stats['total']) * 100
                print(f"Completion rate: {completion_rate:.1f}%")
        
        else:
            parser.print_help()
    
    except ValueError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


# Simple unit tests (can be run with: python -m doctest main.py)
def test_task_creation():
    """Test task creation and basic functionality."""
    task = Task("Test task", "Test description", "high", "2024-12-25")
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.priority == "high"
    assert task.due_date == "2024-12-25"
    assert not task.completed
    
    # Test completion
    task.mark_complete()
    assert task.completed
    assert task.completed_at is not None
    print("✓ Task tests passed")


def test_task_manager():
    """Test task manager functionality."""
    # Create a temporary task manager
    tm = TaskManager("test_tasks.json")
    
    # Add a task
    task = tm.add_task("Test task", "Test description", "high")
    assert len(tm.tasks) == 1
    
    # Complete the task
    tm.complete_task(task.id)
    assert tm.get_task(task.id).completed
    
    # Delete the task
    tm.delete_task(task.id)
    assert len(tm.tasks) == 0
    
    # Clean up
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")
    
    print("✓ TaskManager tests passed")


if __name__ == "__main__":
    # Run tests if --test flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_task_creation()
        test_task_manager()
        print("✓ All tests passed!")
    else:
        main()
