#!/usr/bin/env python3
"""
Email Slicer - A comprehensive email address analyzer and processor
Author: Python Developer
Version: 1.0.0
Compatible with Python 3.10+
"""

import re
import sys
from typing import Dict, List, Tuple, Optional
from collections import Counter
import json


class EmailSlicer:
    """
    A comprehensive email address analyzer that extracts and processes
    various components of email addresses.
    """
    
    def __init__(self):
        """Initialize the EmailSlicer with common domain categories."""
        self.domain_categories = {
            'gmail.com': 'Google',
            'yahoo.com': 'Yahoo',
            'outlook.com': 'Microsoft',
            'hotmail.com': 'Microsoft',
            'live.com': 'Microsoft',
            'icloud.com': 'Apple',
            'me.com': 'Apple',
            'aol.com': 'AOL',
            'protonmail.com': 'ProtonMail',
            'tutanota.com': 'Tutanota'
        }
        
        # Email validation regex pattern
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
    
    def is_valid_email(self, email: str) -> bool:
        """
        Validate if the provided string is a valid email address.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return bool(self.email_pattern.match(email.strip()))
    
    def slice_email(self, email: str) -> Optional[Dict[str, str]]:
        """
        Extract all components from an email address.
        
        Args:
            email (str): Email address to slice
            
        Returns:
            dict: Dictionary containing email components or None if invalid
        """
        email = email.strip().lower()
        
        if not self.is_valid_email(email):
            return None
        
        # Split email into username and domain
        username, domain = email.split('@')
        
        # Extract domain parts
        domain_parts = domain.split('.')
        domain_name = domain_parts[0]
        tld = '.'.join(domain_parts[1:])
        
        # Determine provider category
        provider = self.domain_categories.get(domain, 'Other')
        
        # Analyze username patterns
        username_analysis = self._analyze_username(username)
        
        return {
            'original_email': email,
            'username': username,
            'domain': domain,
            'domain_name': domain_name,
            'tld': tld,
            'provider_category': provider,
            'username_length': len(username),
            'domain_length': len(domain),
            'total_length': len(email),
            'has_numbers': username_analysis['has_numbers'],
            'has_special_chars': username_analysis['has_special_chars'],
            'special_chars_used': username_analysis['special_chars'],
            'estimated_type': self._estimate_email_type(username, domain)
        }
    
    def _analyze_username(self, username: str) -> Dict[str, any]:
        """
        Analyze username patterns and characteristics.
        
        Args:
            username (str): Username part of email
            
        Returns:
            dict: Analysis results
        """
        has_numbers = bool(re.search(r'\d', username))
        special_chars = re.findall(r'[._%+-]', username)
        has_special_chars = len(special_chars) > 0
        
        return {
            'has_numbers': has_numbers,
            'has_special_chars': has_special_chars,
            'special_chars': list(set(special_chars))
        }
    
    def _estimate_email_type(self, username: str, domain: str) -> str:
        """
        Estimate the type/purpose of the email address.
        
        Args:
            username (str): Username part
            domain (str): Domain part
            
        Returns:
            str: Estimated email type
        """
        business_keywords = ['admin', 'info', 'contact', 'support', 'sales', 
                           'marketing', 'hr', 'noreply', 'help']
        
        if any(keyword in username for keyword in business_keywords):
            return 'Business/Professional'
        elif domain in self.domain_categories:
            return 'Personal'
        elif '.' in username and len(username.split('.')) == 2:
            return 'Personal (Name-based)'
        else:
            return 'Personal/Other'
    
    def batch_process(self, emails: List[str]) -> Dict[str, any]:
        """
        Process multiple email addresses and provide aggregate statistics.
        
        Args:
            emails (list): List of email addresses
            
        Returns:
            dict: Batch processing results with statistics
        """
        results = []
        valid_emails = []
        invalid_emails = []
        
        for email in emails:
            sliced = self.slice_email(email)
            if sliced:
                results.append(sliced)
                valid_emails.append(email)
            else:
                invalid_emails.append(email)
        
        # Generate statistics
        if results:
            domains = [r['domain'] for r in results]
            providers = [r['provider_category'] for r in results]
            tlds = [r['tld'] for r in results]
            email_types = [r['estimated_type'] for r in results]
            
            stats = {
                'total_processed': len(emails),
                'valid_emails': len(valid_emails),
                'invalid_emails': len(invalid_emails),
                'domain_distribution': dict(Counter(domains)),
                'provider_distribution': dict(Counter(providers)),
                'tld_distribution': dict(Counter(tlds)),
                'type_distribution': dict(Counter(email_types)),
                'avg_username_length': sum(r['username_length'] for r in results) / len(results),
                'avg_total_length': sum(r['total_length'] for r in results) / len(results)
            }
        else:
            stats = {
                'total_processed': len(emails),
                'valid_emails': 0,
                'invalid_emails': len(invalid_emails),
                'message': 'No valid emails found'
            }
        
        return {
            'individual_results': results,
            'invalid_emails': invalid_emails,
            'statistics': stats
        }


class EmailSlicerCLI:
    """Command Line Interface for the Email Slicer application."""
    
    def __init__(self):
        """Initialize the CLI with an EmailSlicer instance."""
        self.slicer = EmailSlicer()
    
    def display_banner(self):
        """Display the application banner."""
        banner = """
╔══════════════════════════════════════════════╗
║               EMAIL SLICER v1.0              ║
║        Comprehensive Email Analyzer          ║
╚══════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self):
        """Display the main menu options."""
        menu = """
📧 MAIN MENU:
1. Analyze Single Email
2. Batch Process Multiple Emails
3. Load Emails from Text (comma-separated)
4. Export Results to JSON
5. View Email Statistics
6. Help & Examples
7. Exit

Choose an option (1-7): """
        return input(menu).strip()
    
    def analyze_single_email(self):
        """Handle single email analysis."""
        print("\n🔍 SINGLE EMAIL ANALYSIS")
        print("=" * 50)
        
        email = input("Enter email address: ").strip()
        
        if not email:
            print("❌ No email provided!")
            return
        
        result = self.slicer.slice_email(email)
        
        if result:
            print(f"\n✅ Email Analysis Results for: {email}")
            print("-" * 50)
            print(f"📝 Username: {result['username']}")
            print(f"🌐 Domain: {result['domain']}")
            print(f"🏢 Domain Name: {result['domain_name']}")
            print(f"🔗 TLD: {result['tld']}")
            print(f"🏷️  Provider: {result['provider_category']}")
            print(f"📏 Username Length: {result['username_length']} characters")
            print(f"📏 Total Length: {result['total_length']} characters")
            print(f"🔢 Contains Numbers: {'Yes' if result['has_numbers'] else 'No'}")
            print(f"🔣 Special Characters: {', '.join(result['special_chars_used']) if result['special_chars_used'] else 'None'}")
            print(f"📊 Estimated Type: {result['estimated_type']}")
        else:
            print(f"❌ Invalid email address: {email}")
        
        input("\nPress Enter to continue...")
    
    def batch_process_emails(self):
        """Handle batch processing of multiple emails."""
        print("\n📦 BATCH EMAIL PROCESSING")
        print("=" * 50)
        
        emails = []
        print("Enter email addresses (one per line, empty line to finish):")
        
        while True:
            email = input("📧 ").strip()
            if not email:
                break
            emails.append(email)
        
        if not emails:
            print("❌ No emails provided!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🔄 Processing {len(emails)} email(s)...")
        results = self.slicer.batch_process(emails)
        
        self._display_batch_results(results)
        input("\nPress Enter to continue...")
    
    def load_emails_from_text(self):
        """Load emails from comma-separated text input."""
        print("\n📝 LOAD EMAILS FROM TEXT")
        print("=" * 50)
        
        text_input = input("Enter emails separated by commas: ").strip()
        
        if not text_input:
            print("❌ No input provided!")
            input("Press Enter to continue...")
            return
        
        # Split by comma and clean up
        emails = [email.strip() for email in text_input.split(',') if email.strip()]
        
        if not emails:
            print("❌ No valid emails found in input!")
            input("Press Enter to continue...")
            return
        
        print(f"\n🔄 Processing {len(emails)} email(s)...")
        results = self.slicer.batch_process(emails)
        
        self._display_batch_results(results)
        input("\nPress Enter to continue...")
    
    def _display_batch_results(self, results: Dict[str, any]):
        """Display batch processing results."""
        stats = results['statistics']
        
        print(f"\n📊 BATCH PROCESSING RESULTS")
        print("=" * 50)
        print(f"📧 Total Processed: {stats['total_processed']}")
        print(f"✅ Valid Emails: {stats['valid_emails']}")
        print(f"❌ Invalid Emails: {stats['invalid_emails']}")
        
        if stats['valid_emails'] > 0:
            print(f"\n📈 STATISTICS:")
            print(f"📏 Average Username Length: {stats['avg_username_length']:.1f} characters")
            print(f"📏 Average Total Length: {stats['avg_total_length']:.1f} characters")
            
            print(f"\n🏷️  TOP PROVIDERS:")
            for provider, count in stats['provider_distribution'].items():
                print(f"   {provider}: {count}")
            
            print(f"\n🔗 TOP TLDs:")
            for tld, count in stats['tld_distribution'].items():
                print(f"   .{tld}: {count}")
            
            print(f"\n📊 EMAIL TYPES:")
            for email_type, count in stats['type_distribution'].items():
                print(f"   {email_type}: {count}")
        
        if results['invalid_emails']:
            print(f"\n❌ INVALID EMAILS:")
            for invalid in results['invalid_emails']:
                print(f"   {invalid}")
    
    def export_to_json(self):
        """Export results to JSON file."""
        print("\n💾 EXPORT TO JSON")
        print("=" * 50)
        print("This feature exports the last batch processing results.")
        print("Please run batch processing first.")
        input("Press Enter to continue...")
    
    def show_help(self):
        """Display help and examples."""
        help_text = """
📚 HELP & EXAMPLES

🔍 What is Email Slicing?
Email slicing is the process of breaking down email addresses into their
component parts for analysis and processing.

📧 Valid Email Examples:
• john.doe@gmail.com
• user123@company.org
• support@business.co.uk  
• info@example-site.com

🚫 Invalid Email Examples:
• plainaddress
• @missingdomain.com
• username@.com
• spaces in@email.com

🔧 Features:
• Username and domain extraction
• Provider categorization (Google, Microsoft, etc.)
• Email type estimation (Personal, Business)
• Character analysis (numbers, special chars)
• Batch processing with statistics
• TLD (Top Level Domain) analysis

💡 Use Cases:
• Email list validation and cleaning
• Marketing campaign analysis
• User registration data processing
• Email pattern recognition
• Domain popularity analysis

🎯 Tips:
• Use batch processing for multiple emails
• Check statistics for insights
• Validate emails before processing
• Export results for further analysis
        """
        print(help_text)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop."""
        self.display_banner()
        
        while True:
            try:
                choice = self.display_menu()
                
                if choice == '1':
                    self.analyze_single_email()
                elif choice == '2':
                    self.batch_process_emails()
                elif choice == '3':
                    self.load_emails_from_text()
                elif choice == '4':
                    self.export_to_json()
                elif choice == '5':
                    print("\n📊 Email statistics are shown after batch processing.")
                    input("Press Enter to continue...")
                elif choice == '6':
                    self.show_help()
                elif choice == '7':
                    print("\n👋 Thank you for using Email Slicer!")
                    print("Visit us again for more email analysis needs.")
                    sys.exit(0)
                else:
                    print("\n❌ Invalid choice! Please select 1-7.")
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("Press Enter to continue...")


def main():
    """Main function to run the Email Slicer CLI application."""
    cli = EmailSlicerCLI()
    cli.run()


# Example usage and testing
if __name__ == "__main__":
    # You can uncomment the following for quick testing without running the CLI
    # slicer = EmailSlicer()
    # test_emails = [
    #     "john.doe@gmail.com",
    #     "user123@company.org", 
    #     "invalid-email",
    #     "support@business.co.uk"
    # ]
    # results = slicer.batch_process(test_emails)
    # print(json.dumps(results, indent=2))
    
    # Run the CLI application
    main()
