#!/usr/bin/env python3
"""
Contact Book - A Complete CLI Application
A simple yet powerful contact management system with persistent storage.
Author: Assistant
Compatible with Python 3.10+
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional


class Contact:
    """Represents a single contact with validation and formatting."""
    
    def __init__(self, name: str, phone: str, email: str = "", address: str = "", notes: str = ""):
        self.name = self._validate_name(name)
        self.phone = self._validate_phone(phone)
        self.email = self._validate_email(email) if email else ""
        self.address = address.strip()
        self.notes = notes.strip()
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
    
    def _validate_name(self, name: str) -> str:
        """Validate and format contact name."""
        name = name.strip()
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return name.title()
    
    def _validate_phone(self, phone: str) -> str:
        """Validate and format phone number."""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10:
            raise ValueError("Phone number must contain at least 10 digits")
        
        # Format as (XXX) XXX-XXXX for US numbers
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        else:
            return digits  # International numbers kept as digits
    
    def _validate_email(self, email: str) -> str:
        """Validate email format."""
        email = email.strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        return email
    
    def update(self, **kwargs):
        """Update contact fields with validation."""
        for field, value in kwargs.items():
            if field == 'name' and value:
                self.name = self._validate_name(value)
            elif field == 'phone' and value:
                self.phone = self._validate_phone(value)
            elif field == 'email':
                self.email = self._validate_email(value) if value else ""
            elif field == 'address':
                self.address = value.strip()
            elif field == 'notes':
                self.notes = value.strip()
        
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert contact to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        """Create contact from dictionary."""
        contact = cls(data['name'], data['phone'], data.get('email', ''), 
                     data.get('address', ''), data.get('notes', ''))
        contact.created_at = data.get('created_at', contact.created_at)
        contact.updated_at = data.get('updated_at', contact.updated_at)
        return contact
    
    def __str__(self) -> str:
        """String representation of contact."""
        lines = [f"📞 {self.name}", f"   Phone: {self.phone}"]
        if self.email:
            lines.append(f"   Email: {self.email}")
        if self.address:
            lines.append(f"   Address: {self.address}")
        if self.notes:
            lines.append(f"   Notes: {self.notes}")
        return "\n".join(lines)


class ContactBook:
    """Main contact book class with file persistence and search functionality."""
    
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.contacts: Dict[str, Contact] = {}
        self.load_contacts()
    
    def load_contacts(self):
        """Load contacts from JSON file."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, contact_data in data.items():
                        self.contacts[name.lower()] = Contact.from_dict(contact_data)
                print(f"✅ Loaded {len(self.contacts)} contacts from {self.filename}")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"⚠️  Error loading contacts: {e}")
                print("Starting with empty contact book.")
        else:
            print("📱 Starting with a new contact book.")
    
    def save_contacts(self):
        """Save contacts to JSON file."""
        try:
            data = {contact.name: contact.to_dict() for contact in self.contacts.values()}
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Contacts saved to {self.filename}")
        except Exception as e:
            print(f"❌ Error saving contacts: {e}")
    
    def add_contact(self, name: str, phone: str, email: str = "", address: str = "", notes: str = "") -> bool:
        """Add a new contact."""
        try:
            contact = Contact(name, phone, email, address, notes)
            key = contact.name.lower()
            
            if key in self.contacts:
                print(f"⚠️  Contact '{contact.name}' already exists!")
                return False
            
            self.contacts[key] = contact
            self.save_contacts()
            print(f"✅ Contact '{contact.name}' added successfully!")
            return True
            
        except ValueError as e:
            print(f"❌ Error adding contact: {e}")
            return False
    
    def delete_contact(self, name: str) -> bool:
        """Delete a contact by name."""
        key = name.lower().strip()
        if key in self.contacts:
            contact_name = self.contacts[key].name
            del self.contacts[key]
            self.save_contacts()
            print(f"🗑️  Contact '{contact_name}' deleted successfully!")
            return True
        else:
            print(f"❌ Contact '{name}' not found!")
            return False
    
    def update_contact(self, name: str, **kwargs) -> bool:
        """Update an existing contact."""
        key = name.lower().strip()
        if key not in self.contacts:
            print(f"❌ Contact '{name}' not found!")
            return False
        
        try:
            old_name = self.contacts[key].name
            self.contacts[key].update(**kwargs)
            
            # If name changed, update the key
            if 'name' in kwargs and kwargs['name']:
                new_key = self.contacts[key].name.lower()
                if new_key != key:
                    self.contacts[new_key] = self.contacts[key]
                    del self.contacts[key]
            
            self.save_contacts()
            print(f"✅ Contact '{old_name}' updated successfully!")
            return True
            
        except ValueError as e:
            print(f"❌ Error updating contact: {e}")
            return False
    
    def search_contacts(self, query: str) -> List[Contact]:
        """Search contacts by name, phone, or email."""
        query = query.lower().strip()
        results = []
        
        for contact in self.contacts.values():
            if (query in contact.name.lower() or 
                query in contact.phone.lower() or 
                query in contact.email.lower() or
                query in contact.address.lower() or
                query in contact.notes.lower()):
                results.append(contact)
        
        return sorted(results, key=lambda c: c.name)
    
    def list_all_contacts(self) -> List[Contact]:
        """Get all contacts sorted by name."""
        return sorted(self.contacts.values(), key=lambda c: c.name)
    
    def get_contact(self, name: str) -> Optional[Contact]:
        """Get a specific contact by name."""
        return self.contacts.get(name.lower().strip())
    
    def get_stats(self) -> Dict:
        """Get contact book statistics."""
        total = len(self.contacts)
        with_email = sum(1 for c in self.contacts.values() if c.email)
        with_address = sum(1 for c in self.contacts.values() if c.address)
        with_notes = sum(1 for c in self.contacts.values() if c.notes)
        
        return {
            'total': total,
            'with_email': with_email,
            'with_address': with_address,
            'with_notes': with_notes
        }


class ContactBookCLI:
    """Command-line interface for the contact book."""
    
    def __init__(self):
        self.contact_book = ContactBook()
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("📱 CONTACT BOOK - Main Menu")
        print("="*50)
        print("1. 📝 Add New Contact")
        print("2. 👀 View All Contacts")
        print("3. 🔍 Search Contacts")
        print("4. ✏️  Edit Contact")
        print("5. 🗑️  Delete Contact")
        print("6. 📊 View Statistics")
        print("7. 💾 Export Contacts")
        print("8. ❌ Exit")
        print("="*50)
    
    def get_input(self, prompt: str, required: bool = True) -> str:
        """Get user input with validation."""
        while True:
            value = input(prompt).strip()
            if not required and not value:
                return ""
            if value:
                return value
            print("⚠️  This field is required. Please try again.")
    
    def add_contact_interactive(self):
        """Interactive contact addition."""
        print("\n📝 Adding New Contact")
        print("-" * 30)
        
        try:
            name = self.get_input("Name: ")
            phone = self.get_input("Phone: ")
            email = self.get_input("Email (optional): ", required=False)
            address = self.get_input("Address (optional): ", required=False)
            notes = self.get_input("Notes (optional): ", required=False)
            
            self.contact_book.add_contact(name, phone, email, address, notes)
            
        except KeyboardInterrupt:
            print("\n⚠️  Operation cancelled.")
    
    def view_all_contacts(self):
        """Display all contacts."""
        contacts = self.contact_book.list_all_contacts()
        
        if not contacts:
            print("\n📭 No contacts found. Add some contacts first!")
            return
        
        print(f"\n📋 All Contacts ({len(contacts)} total)")
        print("="*50)
        
        for i, contact in enumerate(contacts, 1):
            print(f"\n{i}. {contact}")
            print("-" * 30)
    
    def search_contacts_interactive(self):
        """Interactive contact search."""
        query = self.get_input("\n🔍 Enter search term (name, phone, email): ")
        results = self.contact_book.search_contacts(query)
        
        if not results:
            print(f"❌ No contacts found matching '{query}'")
            return
        
        print(f"\n🔍 Search Results for '{query}' ({len(results)} found)")
        print("="*50)
        
        for i, contact in enumerate(results, 1):
            print(f"\n{i}. {contact}")
            print("-" * 30)
    
    def edit_contact_interactive(self):
        """Interactive contact editing."""
        name = self.get_input("\n✏️  Enter name of contact to edit: ")
        contact = self.contact_book.get_contact(name)
        
        if not contact:
            print(f"❌ Contact '{name}' not found!")
            return
        
        print(f"\n📝 Editing Contact: {contact.name}")
        print("Leave blank to keep current value:")
        print("-" * 40)
        
        updates = {}
        
        new_name = input(f"Name [{contact.name}]: ").strip()
        if new_name:
            updates['name'] = new_name
        
        new_phone = input(f"Phone [{contact.phone}]: ").strip()
        if new_phone:
            updates['phone'] = new_phone
        
        new_email = input(f"Email [{contact.email}]: ").strip()
        updates['email'] = new_email
        
        new_address = input(f"Address [{contact.address}]: ").strip()
        updates['address'] = new_address
        
        new_notes = input(f"Notes [{contact.notes}]: ").strip()
        updates['notes'] = new_notes
        
        if updates:
            self.contact_book.update_contact(name, **updates)
        else:
            print("ℹ️  No changes made.")
    
    def delete_contact_interactive(self):
        """Interactive contact deletion."""
        name = self.get_input("\n🗑️  Enter name of contact to delete: ")
        contact = self.contact_book.get_contact(name)
        
        if not contact:
            print(f"❌ Contact '{name}' not found!")
            return
        
        print(f"\n⚠️  Are you sure you want to delete this contact?")
        print(f"{contact}")
        
        confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
        if confirm == 'yes':
            self.contact_book.delete_contact(name)
        else:
            print("❌ Deletion cancelled.")
    
    def show_statistics(self):
        """Display contact book statistics."""
        stats = self.contact_book.get_stats()
        
        print(f"\n📊 Contact Book Statistics")
        print("="*30)
        print(f"Total Contacts: {stats['total']}")
        print(f"With Email: {stats['with_email']}")
        print(f"With Address: {stats['with_address']}")
        print(f"With Notes: {stats['with_notes']}")
        
        if stats['total'] > 0:
            print(f"\nCompletion Rates:")
            print(f"Email: {stats['with_email']/stats['total']*100:.1f}%")
            print(f"Address: {stats['with_address']/stats['total']*100:.1f}%")
            print(f"Notes: {stats['with_notes']/stats['total']*100:.1f}%")
    
    def export_contacts(self):
        """Export contacts to a readable text file."""
        contacts = self.contact_book.list_all_contacts()
        
        if not contacts:
            print("\n📭 No contacts to export.")
            return
        
        filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("CONTACT BOOK EXPORT\n")
                f.write("="*50 + "\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Contacts: {len(contacts)}\n\n")
                
                for i, contact in enumerate(contacts, 1):
                    f.write(f"{i}. {contact.name}\n")
                    f.write(f"   Phone: {contact.phone}\n")
                    if contact.email:
                        f.write(f"   Email: {contact.email}\n")
                    if contact.address:
                        f.write(f"   Address: {contact.address}\n")
                    if contact.notes:
                        f.write(f"   Notes: {contact.notes}\n")
                    f.write(f"   Added: {contact.created_at[:10]}\n")
                    f.write("-" * 30 + "\n\n")
            
            print(f"✅ Contacts exported to '{filename}'")
            
        except Exception as e:
            print(f"❌ Error exporting contacts: {e}")
    
    def run(self):
        """Main application loop."""
        print("🚀 Welcome to Contact Book!")
        
        while True:
            try:
                self.display_menu()
                choice = input("\n👉 Enter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.add_contact_interactive()
                elif choice == '2':
                    self.view_all_contacts()
                elif choice == '3':
                    self.search_contacts_interactive()
                elif choice == '4':
                    self.edit_contact_interactive()
                elif choice == '5':
                    self.delete_contact_interactive()
                elif choice == '6':
                    self.show_statistics()
                elif choice == '7':
                    self.export_contacts()
                elif choice == '8':
                    print("\n👋 Thank you for using Contact Book!")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-8.")
                
                # Pause before showing menu again
                input("\n📱 Press Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                print("Please try again.")


def main():
    """Entry point of the application."""
    try:
        app = ContactBookCLI()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please check your Python installation and try again.")


if __name__ == "__main__":
    main()
