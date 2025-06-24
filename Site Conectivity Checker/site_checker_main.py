#!/usr/bin/env python3
"""
Site Connectivity Checker
A comprehensive tool to check website connectivity and health status.

Author: Claude AI Assistant
Version: 1.0.0
Python: 3.8+
"""

import urllib.request
import urllib.parse
import urllib.error
import socket
import ssl
import time
import json
import argparse
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re


class SiteConnectivityChecker:
    """Main class for checking site connectivity and health."""
    
    def __init__(self, timeout: int = 10, user_agent: str = None):
        """
        Initialize the connectivity checker.
        
        Args:
            timeout (int): Request timeout in seconds
            user_agent (str): Custom user agent string
        """
        self.timeout = timeout
        self.user_agent = user_agent or "SiteConnectivityChecker/1.0"
        self.results = []
    
    def validate_url(self, url: str) -> str:
        """
        Validate and normalize URL format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            str: Normalized URL
            
        Raises:
            ValueError: If URL is invalid
        """
        if not url:
            raise ValueError("URL cannot be empty")
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Basic URL validation
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc:
            raise ValueError(f"Invalid URL format: {url}")
        
        return url
    
    def check_dns_resolution(self, hostname: str) -> Dict[str, any]:
        """
        Check if hostname resolves to IP address.
        
        Args:
            hostname (str): Hostname to resolve
            
        Returns:
            Dict: DNS resolution results
        """
        try:
            start_time = time.time()
            ip_address = socket.gethostbyname(hostname)
            resolution_time = round((time.time() - start_time) * 1000, 2)
            
            return {
                'success': True,
                'ip_address': ip_address,
                'resolution_time_ms': resolution_time,
                'error': None
            }
        except socket.gaierror as e:
            return {
                'success': False,
                'ip_address': None,
                'resolution_time_ms': None,
                'error': str(e)
            }
    
    def check_port_connectivity(self, hostname: str, port: int) -> Dict[str, any]:
        """
        Check if specific port is accessible on hostname.
        
        Args:
            hostname (str): Target hostname
            port (int): Port number to check
            
        Returns:
            Dict: Port connectivity results
        """
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((hostname, port))
            connection_time = round((time.time() - start_time) * 1000, 2)
            sock.close()
            
            return {
                'success': result == 0,
                'port': port,
                'connection_time_ms': connection_time,
                'error': None if result == 0 else f"Connection failed (code: {result})"
            }
        except Exception as e:
            return {
                'success': False,
                'port': port,
                'connection_time_ms': None,
                'error': str(e)
            }
    
    def check_ssl_certificate(self, hostname: str, port: int = 443) -> Dict[str, any]:
        """
        Check SSL certificate information for HTTPS sites.
        
        Args:
            hostname (str): Target hostname
            port (int): SSL port (default: 443)
            
        Returns:
            Dict: SSL certificate information
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse certificate dates
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    return {
                        'success': True,
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'version': cert['version'],
                        'not_before': cert['notBefore'],
                        'not_after': cert['notAfter'],
                        'days_until_expiry': days_until_expiry,
                        'is_expired': days_until_expiry < 0,
                        'error': None
                    }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_http_response(self, url: str) -> Dict[str, any]:
        """
        Check HTTP response from URL.
        
        Args:
            url (str): URL to check
            
        Returns:
            Dict: HTTP response information
        """
        try:
            # Create request with custom headers
            request = urllib.request.Request(url)
            request.add_header('User-Agent', self.user_agent)
            request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            
            start_time = time.time()
            
            # Make the request
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response_time = round((time.time() - start_time) * 1000, 2)
                content_length = response.headers.get('Content-Length', 'Unknown')
                
                return {
                    'success': True,
                    'status_code': response.getcode(),
                    'response_time_ms': response_time,
                    'content_length': content_length,
                    'content_type': response.headers.get('Content-Type', 'Unknown'),
                    'server': response.headers.get('Server', 'Unknown'),
                    'final_url': response.geturl(),
                    'headers': dict(response.headers),
                    'error': None
                }
                
        except urllib.error.HTTPError as e:
            response_time = round((time.time() - start_time) * 1000, 2)
            return {
                'success': False,
                'status_code': e.code,
                'response_time_ms': response_time,
                'error': f"HTTP Error {e.code}: {e.reason}"
            }
        except urllib.error.URLError as e:
            return {
                'success': False,
                'status_code': None,
                'response_time_ms': None,
                'error': f"URL Error: {e.reason}"
            }
        except Exception as e:
            return {
                'success': False,
                'status_code': None,
                'response_time_ms': None,
                'error': str(e)
            }
    
    def comprehensive_check(self, url: str) -> Dict[str, any]:
        """
        Perform comprehensive connectivity check for a URL.
        
        Args:
            url (str): URL to check
            
        Returns:
            Dict: Complete check results
        """
        try:
            # Validate and normalize URL
            normalized_url = self.validate_url(url)
            parsed_url = urllib.parse.urlparse(normalized_url)
            hostname = parsed_url.netloc
            is_https = parsed_url.scheme == 'https'
            
            print(f"Checking: {normalized_url}")
            
            # Initialize result structure
            result = {
                'url': normalized_url,
                'hostname': hostname,
                'timestamp': datetime.now().isoformat(),
                'checks': {}
            }
            
            # 1. DNS Resolution Check
            print("  → Checking DNS resolution...")
            result['checks']['dns'] = self.check_dns_resolution(hostname)
            
            if result['checks']['dns']['success']:
                ip = result['checks']['dns']['ip_address']
                print(f"    ✓ Resolved to: {ip}")
                
                # 2. Port Connectivity Check
                port = 443 if is_https else 80
                print(f"  → Checking port {port} connectivity...")
                result['checks']['port'] = self.check_port_connectivity(hostname, port)
                
                if result['checks']['port']['success']:
                    print(f"    ✓ Port {port} is accessible")
                    
                    # 3. SSL Certificate Check (for HTTPS)
                    if is_https:
                        print("  → Checking SSL certificate...")
                        result['checks']['ssl'] = self.check_ssl_certificate(hostname)
                        
                        if result['checks']['ssl']['success']:
                            days_left = result['checks']['ssl']['days_until_expiry']
                            if days_left > 0:
                                print(f"    ✓ SSL certificate valid ({days_left} days remaining)")
                            else:
                                print(f"    ⚠ SSL certificate expired ({abs(days_left)} days ago)")
                        else:
                            print(f"    ✗ SSL check failed: {result['checks']['ssl']['error']}")
                    
                    # 4. HTTP Response Check
                    print("  → Checking HTTP response...")
                    result['checks']['http'] = self.check_http_response(normalized_url)
                    
                    if result['checks']['http']['success']:
                        status = result['checks']['http']['status_code']
                        time_ms = result['checks']['http']['response_time_ms']
                        print(f"    ✓ HTTP {status} ({time_ms}ms)")
                    else:
                        print(f"    ✗ HTTP check failed: {result['checks']['http']['error']}")
                        
                else:
                    print(f"    ✗ Port {port} is not accessible: {result['checks']['port']['error']}")
            else:
                print(f"    ✗ DNS resolution failed: {result['checks']['dns']['error']}")
            
            # Determine overall status
            result['overall_success'] = (
                result['checks']['dns']['success'] and
                result['checks'].get('port', {}).get('success', False) and
                result['checks'].get('http', {}).get('success', False)
            )
            
            return result
            
        except Exception as e:
            return {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'overall_success': False,
                'error': str(e),
                'checks': {}
            }
    
    def check_multiple_sites(self, urls: List[str]) -> List[Dict[str, any]]:
        """
        Check connectivity for multiple sites.
        
        Args:
            urls (List[str]): List of URLs to check
            
        Returns:
            List[Dict]: Results for all sites
        """
        results = []
        
        print(f"Checking connectivity for {len(urls)} site(s)...\n")
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] ", end="")
            result = self.comprehensive_check(url)
            results.append(result)
            
            # Print summary
            status = "✓ ONLINE" if result['overall_success'] else "✗ OFFLINE"
            print(f"  → {status}\n")
        
        self.results = results
        return results
    
    def generate_report(self, format_type: str = 'text') -> str:
        """
        Generate a formatted report of check results.
        
        Args:
            format_type (str): Report format ('text' or 'json')
            
        Returns:
            str: Formatted report
        """
        if not self.results:
            return "No results available. Run checks first."
        
        if format_type.lower() == 'json':
            return json.dumps(self.results, indent=2, default=str)
        
        # Text format report
        report = []
        report.append("=" * 60)
        report.append("SITE CONNECTIVITY REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Sites checked: {len(self.results)}")
        report.append("")
        
        for i, result in enumerate(self.results, 1):
            report.append(f"{i}. {result['url']}")
            report.append("-" * len(f"{i}. {result['url']}"))
            
            if result['overall_success']:
                report.append("Status: ✓ ONLINE")
            else:
                report.append("Status: ✗ OFFLINE")
            
            # DNS Info
            if 'dns' in result['checks']:
                dns = result['checks']['dns']
                if dns['success']:
                    report.append(f"IP Address: {dns['ip_address']}")
                    report.append(f"DNS Resolution: {dns['resolution_time_ms']}ms")
                else:
                    report.append(f"DNS Error: {dns['error']}")
            
            # HTTP Info
            if 'http' in result['checks']:
                http = result['checks']['http']
                if http['success']:
                    report.append(f"HTTP Status: {http['status_code']}")
                    report.append(f"Response Time: {http['response_time_ms']}ms")
                    report.append(f"Server: {http.get('server', 'Unknown')}")
                else:
                    report.append(f"HTTP Error: {http['error']}")
            
            # SSL Info
            if 'ssl' in result['checks']:
                ssl_info = result['checks']['ssl']
                if ssl_info['success']:
                    days = ssl_info['days_until_expiry']
                    status = "Valid" if days > 0 else "EXPIRED"
                    report.append(f"SSL Certificate: {status} ({days} days)")
                else:
                    report.append(f"SSL Error: {ssl_info['error']}")
            
            report.append("")
        
        return "\n".join(report)


def main():
    """Main function to handle command-line interface."""
    parser = argparse.ArgumentParser(
        description="Site Connectivity Checker - Check website accessibility and health",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py google.com
  python main.py https://github.com facebook.com twitter.com
  python main.py -t 15 -o report.json --format json example.com
  python main.py --batch sites.txt
        """
    )
    
    parser.add_argument(
        'urls',
        nargs='*',
        help='URLs to check (can be multiple)'
    )
    
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file to save results'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--batch',
        help='File containing URLs to check (one per line)'
    )
    
    parser.add_argument(
        '--user-agent',
        help='Custom User-Agent string'
    )
    
    args = parser.parse_args()
    
    # Collect URLs to check
    urls_to_check = []
    
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                batch_urls = [line.strip() for line in f if line.strip()]
                urls_to_check.extend(batch_urls)
                print(f"Loaded {len(batch_urls)} URLs from {args.batch}")
        except FileNotFoundError:
            print(f"Error: Batch file '{args.batch}' not found.")
            sys.exit(1)
    
    if args.urls:
        urls_to_check.extend(args.urls)
    
    if not urls_to_check:
        print("Error: No URLs provided. Use --help for usage information.")
        sys.exit(1)
    
    # Initialize checker
    checker = SiteConnectivityChecker(
        timeout=args.timeout,
        user_agent=args.user_agent
    )
    
    try:
        # Run checks
        results = checker.check_multiple_sites(urls_to_check)
        
        # Generate report
        report = checker.generate_report(args.format)
        
        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Results saved to: {args.output}")
        else:
            print(report)
        
        # Exit with appropriate code
        failed_checks = sum(1 for r in results if not r['overall_success'])
        if failed_checks > 0:
            print(f"\n{failed_checks} site(s) failed connectivity check.")
            sys.exit(1)
        else:
            print(f"\nAll {len(results)} site(s) are accessible.")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


# Simple unit tests (run with: python main.py --test)
def run_tests():
    """Run basic unit tests."""
    print("Running unit tests...")
    
    checker = SiteConnectivityChecker(timeout=5)
    
    # Test URL validation
    try:
        assert checker.validate_url("google.com") == "https://google.com"
        assert checker.validate_url("http://example.com") == "http://example.com"
        print("✓ URL validation tests passed")
    except AssertionError:
        print("✗ URL validation tests failed")
    
    # Test DNS resolution for known good domain
    dns_result = checker.check_dns_resolution("google.com")
    if dns_result['success']:
        print("✓ DNS resolution test passed")
    else:
        print("✗ DNS resolution test failed")
    
    print("Unit tests completed.")


if __name__ == "__main__":
    # Check for test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        main()
