#!/usr/bin/env python3
"""
Website Blocker - A command-line tool to block/unblock websites by modifying the hosts file.

This tool helps users block distracting websites by redirecting them to localhost
in the system's hosts file. It supports both temporary and permanent blocking.

Author: Claude AI
Version: 1.0.0
Python Version: 3.7+
"""

import os
import sys
import time
import argparse
import platform
import datetime
from pathlib import Path
from typing import List, Optional, Set
import re


class WebsiteBlocker:
    """Main class for website blocking functionality."""
    
    def __init__(self):
        """Initialize the website blocker with system-specific settings."""
        self.system = platform.system().lower()
        self.hosts_file = self._get_hosts_file_path()
        self.backup_file = self.hosts_file.parent / "hosts.backup"
        self.redirect_ip = "127.0.0.1"
        self.block_marker_start = "# === WEBSITE BLOCKER START ==="
        self.block_marker_end = "# === WEBSITE BLOCKER END ==="
    
    def _get_hosts_file_path(self) -> Path:
        """Get the system-specific hosts file path."""
        if self.system == "windows":
            return Path("C:/Windows/System32/drivers/etc/hosts")
        else:  # Linux, macOS, and other Unix-like systems
            return Path("/etc/hosts")
    
    def _check_admin_privileges(self) -> bool:
        """Check if the script is running with administrator/root privileges."""
        try:
            if self.system == "windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except Exception:
            return False
    
    def _validate_domain(self, domain: str) -> bool:
        """Validate if a domain name is properly formatted."""
        # Basic domain validation regex
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        return bool(re.match(pattern, domain)) and len(domain) <= 253
    
    def _normalize_domain(self, domain: str) -> str:
        """Normalize domain by removing protocol and trailing slashes."""
        # Remove common prefixes
        domain = domain.replace("http://", "").replace("https://", "")
        domain = domain.replace("www.", "")
        # Remove trailing slash and path components
        domain = domain.split('/')[0].strip().lower()
        return domain
    
    def _read_hosts_file(self) -> List[str]:
        """Read the contents of the hosts file."""
        try:
            with open(self.hosts_file, 'r', encoding='utf-8') as f:
                return f.readlines()
        except FileNotFoundError:
            print(f"Error: Hosts file not found at {self.hosts_file}")
            return []
        except PermissionError:
            print("Error: Permission denied. Please run as administrator/root.")
            return []
        except Exception as e:
            print(f"Error reading hosts file: {e}")
            return []
    
    def _write_hosts_file(self, lines: List[str]) -> bool:
        """Write content to the hosts file."""
        try:
            with open(self.hosts_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        except PermissionError:
            print("Error: Permission denied. Please run as administrator/root.")
            return False
        except Exception as e:
            print(f"Error writing to hosts file: {e}")
            return False
    
    def _create_backup(self) -> bool:
        """Create a backup of the current hosts file."""
        try:
            lines = self._read_hosts_file()
            if not lines:
                return False
            
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def _get_blocked_websites(self) -> Set[str]:
        """Get currently blocked websites from the hosts file."""
        lines = self._read_hosts_file()
        blocked_sites = set()
        in_block_section = False
        
        for line in lines:
            line = line.strip()
            if line == self.block_marker_start:
                in_block_section = True
                continue
            elif line == self.block_marker_end:
                in_block_section = False
                continue
            elif in_block_section and line.startswith(self.redirect_ip):
                # Extract domain from the line
                parts = line.split()
                if len(parts) >= 2:
                    domain = parts[1]
                    blocked_sites.add(domain)
        
        return blocked_sites
    
    def block_websites(self, domains: List[str]) -> bool:
        """Block the specified websites."""
        if not self._check_admin_privileges():
            print("Error: This operation requires administrator/root privileges.")
            print("Please run the script as administrator (Windows) or with sudo (Linux/macOS).")
            return False
        
        # Validate and normalize domains
        valid_domains = []
        for domain in domains:
            normalized = self._normalize_domain(domain)
            if self._validate_domain(normalized):
                valid_domains.append(normalized)
            else:
                print(f"Warning: Invalid domain '{domain}' skipped")
        
        if not valid_domains:
            print("No valid domains to block.")
            return False
        
        # Create backup before making changes
        if not self._create_backup():
            print("Warning: Could not create backup file.")
        
        lines = self._read_hosts_file()
        if not lines:
            return False
        
        # Remove existing block section if it exists
        filtered_lines = []
        in_block_section = False
        
        for line in lines:
            if line.strip() == self.block_marker_start:
                in_block_section = True
                continue
            elif line.strip() == self.block_marker_end:
                in_block_section = False
                continue
            elif not in_block_section:
                filtered_lines.append(line)
        
        # Add new block section
        filtered_lines.append(f"\n{self.block_marker_start}\n")
        filtered_lines.append(f"# Website Blocker - Added on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for domain in valid_domains:
            filtered_lines.append(f"{self.redirect_ip} {domain}\n")
            filtered_lines.append(f"{self.redirect_ip} www.{domain}\n")
        
        filtered_lines.append(f"{self.block_marker_end}\n")
        
        if self._write_hosts_file(filtered_lines):
            print(f"Successfully blocked {len(valid_domains)} website(s):")
            for domain in valid_domains:
                print(f"  - {domain}")
            return True
        
        return False
    
    def unblock_websites(self, domains: Optional[List[str]] = None) -> bool:
        """Unblock specified websites or all blocked websites."""
        if not self._check_admin_privileges():
            print("Error: This operation requires administrator/root privileges.")
            return False
        
        lines = self._read_hosts_file()
        if not lines:
            return False
        
        # Create backup before making changes
        if not self._create_backup():
            print("Warning: Could not create backup file.")
        
        if domains is None:
            # Remove entire block section
            filtered_lines = []
            in_block_section = False
            
            for line in lines:
                if line.strip() == self.block_marker_start:
                    in_block_section = True
                    continue
                elif line.strip() == self.block_marker_end:
                    in_block_section = False
                    continue
                elif not in_block_section:
                    filtered_lines.append(line)
            
            if self._write_hosts_file(filtered_lines):
                print("Successfully unblocked all websites.")
                return True
        else:
            # Remove specific domains
            domains_to_remove = [self._normalize_domain(d) for d in domains]
            filtered_lines = []
            in_block_section = False
            removed_count = 0
            
            for line in lines:
                if line.strip() == self.block_marker_start:
                    in_block_section = True
                    filtered_lines.append(line)
                    continue
                elif line.strip() == self.block_marker_end:
                    in_block_section = False
                    filtered_lines.append(line)
                    continue
                elif in_block_section and line.strip().startswith(self.redirect_ip):
                    # Check if this line contains a domain to remove
                    parts = line.split()
                    if len(parts) >= 2:
                        domain = parts[1].replace("www.", "")
                        if domain in domains_to_remove:
                            removed_count += 1
                            continue
                
                filtered_lines.append(line)
            
            if self._write_hosts_file(filtered_lines):
                print(f"Successfully unblocked {removed_count // 2} website(s).")
                return True
        
        return False
    
    def list_blocked_websites(self) -> None:
        """List all currently blocked websites."""
        blocked_sites = self._get_blocked_websites()
        
        if not blocked_sites:
            print("No websites are currently blocked.")
            return
        
        print(f"Currently blocked websites ({len(blocked_sites)}):")
        for site in sorted(blocked_sites):
            if not site.startswith("www."):
                print(f"  - {site}")
    
    def restore_backup(self) -> bool:
        """Restore the hosts file from backup."""
        if not self._check_admin_privileges():
            print("Error: This operation requires administrator/root privileges.")
            return False
        
        if not self.backup_file.exists():
            print("No backup file found.")
            return False
        
        try:
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if self._write_hosts_file(lines):
                print("Successfully restored hosts file from backup.")
                return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
        
        return False


def main():
    """Main function to handle command-line arguments and execute operations."""
    parser = argparse.ArgumentParser(
        description="Website Blocker - Block/unblock websites by modifying the hosts file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py block facebook.com twitter.com
  python main.py unblock facebook.com
  python main.py list
  python main.py unblock-all
  python main.py restore
        """
    )
    
    parser.add_argument(
        'action',
        choices=['block', 'unblock', 'unblock-all', 'list', 'restore'],
        help='Action to perform'
    )
    
    parser.add_argument(
        'domains',
        nargs='*',
        help='Domain names to block/unblock (required for block/unblock actions)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Website Blocker 1.0.0'
    )
    
    args = parser.parse_args()
    
    blocker = WebsiteBlocker()
    
    try:
        if args.action == 'block':
            if not args.domains:
                print("Error: Please specify at least one domain to block.")
                sys.exit(1)
            success = blocker.block_websites(args.domains)
            sys.exit(0 if success else 1)
        
        elif args.action == 'unblock':
            if not args.domains:
                print("Error: Please specify at least one domain to unblock.")
                sys.exit(1)
            success = blocker.unblock_websites(args.domains)
            sys.exit(0 if success else 1)
        
        elif args.action == 'unblock-all':
            success = blocker.unblock_websites()
            sys.exit(0 if success else 1)
        
        elif args.action == 'list':
            blocker.list_blocked_websites()
            sys.exit(0)
        
        elif args.action == 'restore':
            success = blocker.restore_backup()
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


# Simple unit tests (can be run with python -m pytest if pytest is installed)
def test_domain_validation():
    """Test domain validation functionality."""
    blocker = WebsiteBlocker()
    
    # Valid domains
    assert blocker._validate_domain("example.com")
    assert blocker._validate_domain("sub.example.com")
    assert blocker._validate_domain("test-site.org")
    
    # Invalid domains
    assert not blocker._validate_domain("")
    assert not blocker._validate_domain("invalid..domain")
    assert not blocker._validate_domain("-invalid.com")
    
    print("Domain validation tests passed!")


def test_domain_normalization():
    """Test domain normalization functionality."""
    blocker = WebsiteBlocker()
    
    assert blocker._normalize_domain("https://www.example.com/path") == "example.com"
    assert blocker._normalize_domain("http://facebook.com") == "facebook.com"
    assert blocker._normalize_domain("Twitter.COM") == "twitter.com"
    
    print("Domain normalization tests passed!")


if __name__ == "__main__":
    # Run tests if --test argument is provided
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_domain_validation()
        test_domain_normalization()
        print("All tests passed!")
    else:
        main()