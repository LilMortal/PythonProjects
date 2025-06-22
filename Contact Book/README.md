# 📱 Contact Book - Complete CLI Application

A powerful, user-friendly command-line contact management system built in Python. Store, search, and manage your contacts with persistent JSON storage and advanced features.

## 🌟 Features

### Core Functionality
- **Add Contacts**: Store name, phone, email, address, and notes
- **View All Contacts**: Display all contacts in a clean, organized format
- **Search Contacts**: Find contacts by name, phone, email, address, or notes
- **Edit Contacts**: Update any contact information with validation
- **Delete Contacts**: Remove contacts with confirmation prompts
- **Persistent Storage**: Automatic saving to JSON file (`contacts.json`)

### Advanced Features
- **Phone Number Formatting**: Automatically formats US phone numbers as (XXX) XXX-XXXX
- **Email Validation**: Ensures proper email format with regex validation
- **Name Formatting**: Automatically capitalizes names properly
- **Search Flexibility**: Search across all contact fields simultaneously
- **Statistics Dashboard**: View contact book statistics and completion rates
- **Export Functionality**: Export contacts to readable text files
- **Error Handling**: Graceful handling of invalid inputs and edge cases
- **Unicode Support**: Full international character support

### Data Validation
- **Name**: Minimum 2 characters, auto-capitalized
- **Phone**: Minimum 10 digits, auto-formatted for US numbers
- **Email**: Proper email format validation (optional field)
- **Timestamps**: Automatic creation and update tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- No external dependencies required!

### Installation & Usage

1. **Download the application**:
   ```bash
   # Save the contact_book.py file to your desired directory
   wget [your-file-source]/contact_book.py
   # OR simply copy the code into a new file named contact_book.py
   ```

2. **Make it executable** (optional, Linux/Mac):
   ```bash
   chmod +x contact_book.py
   ```

3. **Run the application**:
   ```bash
   python contact_book.py
   # OR if made executable:
   ./contact_book.py
   ```

## 📖 Usage Examples

### Adding a Contact
```
📝 Adding New Contact
------------------------------
Name: John Doe
Phone: 5551234567
Email (optional): john.doe@email.com
Address (optional): 123 Main St, City, State
Notes (optional): College friend
✅ Contact 'John Doe' added successfully!
```

### Searching Contacts
```
🔍 Enter search term (name, phone, email): john
🔍 Search Results for 'john' (1 found)
==================================================

1. 📞 John Doe
   Phone: (555) 123-4567
   Email: john.doe@email.com
   Address: 123 Main St, City, State
   Notes: College friend
```

### Contact Statistics
```
📊 Contact Book Statistics
==============================
Total Contacts: 25
With Email: 20
With Address: 15
With Notes: 10

Completion Rates:
Email: 80.0%
Address: 60.0%
Notes: 40.0%
```

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Storage**: JSON file format
- **Libraries Used**:
  - `json` - Data persistence
  - `os` - File system operations
  - `re` - Regular expressions for validation
  - `datetime` - Timestamp management
  - `typing` - Type hints for better code quality

## 📁 File Structure

```
contact-book/
├── contact_book.py          # Main application (single file)
├── contacts.json            # Data storage (auto-created)
├── contacts_export_*.txt    # Export files (auto-generated)
└── README.md               # This file
```

## 🎛️ Menu Options

1. **📝 Add New Contact** - Create a new contact entry
2. **👀 View All Contacts** - Display all stored contacts
3. **🔍 Search Contacts** - Find contacts by any field
4. **✏️ Edit Contact** - Modify existing contact information
5. **🗑️ Delete Contact** - Remove a contact (with confirmation)
6. **📊 View Statistics** - Show contact book analytics
7. **💾 Export Contacts** - Generate readable text file
8. **❌ Exit** - Close the application

## 🔧 Configuration

The application uses sensible defaults but can be customized:

- **Data File**: Contacts are saved to `contacts.json` in the same directory
- **Phone Format**: US numbers formatted as (XXX) XXX-XXXX
- **Export Format**: Text files with timestamp: `contacts_export_YYYYMMDD_HHMMSS.txt`

## 🚀 Future Enhancement Ideas

### User Interface Improvements
- **GUI Version**: Implement with Tkinter or PyQt for desktop application
- **Web Interface**: Create Flask/Django web application version
- **Mobile App**: React Native or Flutter mobile version

### Feature Expansions
- **Groups/Categories**: Organize contacts into groups (family, work, friends)
- **Photo Support**: Add profile pictures for contacts
- **Social Media**: Store social media handles and links
- **Birthday Reminders**: Track and notify about birthdays
- **Call/Email Integration**: Direct integration with email clients and phone apps

### Advanced Features
- **Import/Export**: Support CSV, VCF (vCard), and Excel formats
- **Backup & Sync**: Cloud storage integration (Google Drive, Dropbox)
- **Advanced Search**: Filters, tags, and custom queries
- **Contact History**: Track contact interaction history
- **Duplicate Detection**: Find and merge duplicate contacts

### Technical Improvements
- **Database Backend**: SQLite or PostgreSQL for better performance
- **API Integration**: RESTful API for external integrations
- **Encryption**: Encrypt sensitive contact data
- **Multi-user Support**: User accounts and permissions
- **Contact Sharing**: Share contacts between users

## 🛡️ Error Handling

The application includes comprehensive error handling for:
- Invalid phone numbers and email addresses
- File permission issues
- JSON corruption or invalid format
- User input validation
- Graceful handling of interrupted operations (Ctrl+C)

## 🌍 International Support

- **Phone Numbers**: Supports international formats (stores as digits for non-US)
- **Unicode**: Full UTF-8 support for international names and addresses
- **Character Encoding**: Proper handling of special characters in all fields

## 💡 Tips for Best Usage

1. **Consistent Formatting**: The app auto-formats data, but consistent input helps
2. **Regular Backups**: Export contacts periodically for additional backup
3. **Search Tips**: Use partial terms for broader search results
4. **Data Entry**: Fill in optional fields for better contact organization

## 🤝 Contributing

This is a single-file educational project. Feel free to:
- Extend functionality for your needs
- Add new features and improvements
- Create GUI or web versions
- Integrate with external services

## 📄 License

This project is provided as-is for educational and personal use. Feel free to modify and distribute according to your needs.

## 🙏 Acknowledgments

- Built with Python's standard library only
- Inspired by traditional contact book applications
- Designed for educational purposes and practical use
- CLI interface designed for cross-platform compatibility

---

**Made with ❤️ for Python learners and productivity enthusiasts**

*For support or questions, refer to the inline code comments and Python documentation.*
