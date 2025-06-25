#!/usr/bin/env python3
"""
Regex Query Tool - A comprehensive regular expression testing and analysis tool
Author: Claude AI Assistant
Version: 1.0.0
Python: 3.8+
"""

import re
import sys
import json
import argparse
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time


class OutputFormat(Enum):
    """Output format options for regex results"""
    SIMPLE = "simple"
    DETAILED = "detailed"
    JSON = "json"
    TABLE = "table"


@dataclass
class RegexMatch:
    """Data class to store regex match information"""
    match_text: str
    start_pos: int
    end_pos: int
    groups: List[str]
    named_groups: Dict[str, str]


@dataclass
class RegexResult:
    """Data class to store complete regex operation result"""
    pattern: str
    text: str
    matches: List[RegexMatch]
    flags: List[str]
    execution_time: float
    total_matches: int
    is_valid_pattern: bool
    error_message: Optional[str] = None


class RegexQueryTool:
    """
    A comprehensive regex testing tool with multiple features and output formats
    """
    
    def __init__(self):
        self.flag_mapping = {
            'i': re.IGNORECASE,
            'm': re.MULTILINE,
            's': re.DOTALL,
            'x': re.VERBOSE,
            'a': re.ASCII,
            'l': re.LOCALE
        }
        self.predefined_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w.*))?)?',
            'ipv4': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'date_us': r'\b(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/(\d{4}|\d{2})\b',
            'time_24h': r'\b([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?\b',
            'hex_color': r'#(?:[0-9a-fA-F]{3}){1,2}\b',
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'zip_code': r'\b\d{5}(-\d{4})?\b'
        }
    
    def parse_flags(self, flag_string: str) -> Tuple[int, List[str]]:
        """
        Parse flag string and return compiled flags and flag list
        
        Args:
            flag_string: String containing flag characters (e.g., 'im')
            
        Returns:
            Tuple of compiled flags and list of flag names
        """
        flags = 0
        flag_names = []
        
        for char in flag_string.lower():
            if char in self.flag_mapping:
                flags |= self.flag_mapping[char]
                flag_names.append(char.upper())
        
        return flags, flag_names
    
    def validate_pattern(self, pattern: str) -> Tuple[bool, Optional[str]]:
        """
        Validate if the regex pattern is valid
        
        Args:
            pattern: Regular expression pattern string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            re.compile(pattern)
            return True, None
        except re.error as e:
            return False, str(e)
    
    def find_matches(self, pattern: str, text: str, flags: str = '') -> RegexResult:
        """
        Find all matches for the given pattern in text
        
        Args:
            pattern: Regular expression pattern
            text: Text to search in
            flags: Flag string (e.g., 'im')
            
        Returns:
            RegexResult object containing all match information
        """
        start_time = time.perf_counter()
        
        # Validate pattern first
        is_valid, error_msg = self.validate_pattern(pattern)
        if not is_valid:
            return RegexResult(
                pattern=pattern,
                text=text,
                matches=[],
                flags=[],
                execution_time=0,
                total_matches=0,
                is_valid_pattern=False,
                error_message=error_msg
            )
        
        # Parse flags
        compiled_flags, flag_names = self.parse_flags(flags)
        
        try:
            # Compile pattern with flags
            regex = re.compile(pattern, compiled_flags)
            
            # Find all matches
            matches = []
            for match in regex.finditer(text):
                regex_match = RegexMatch(
                    match_text=match.group(0),
                    start_pos=match.start(),
                    end_pos=match.end(),
                    groups=list(match.groups()),
                    named_groups=match.groupdict()
                )
                matches.append(regex_match)
            
            execution_time = time.perf_counter() - start_time
            
            return RegexResult(
                pattern=pattern,
                text=text,
                matches=matches,
                flags=flag_names,
                execution_time=execution_time,
                total_matches=len(matches),
                is_valid_pattern=True
            )
            
        except Exception as e:
            return RegexResult(
                pattern=pattern,
                text=text,
                matches=[],
                flags=flag_names,
                execution_time=0,
                total_matches=0,
                is_valid_pattern=False,
                error_message=str(e)
            )
    
    def format_output(self, result: RegexResult, output_format: OutputFormat) -> str:
        """
        Format the regex result according to specified format
        
        Args:
            result: RegexResult object
            output_format: Desired output format
            
        Returns:
            Formatted string output
        """
        if not result.is_valid_pattern:
            return f"❌ Invalid regex pattern: {result.error_message}"
        
        if output_format == OutputFormat.JSON:
            return self._format_json(result)
        elif output_format == OutputFormat.TABLE:
            return self._format_table(result)
        elif output_format == OutputFormat.DETAILED:
            return self._format_detailed(result)
        else:  # SIMPLE
            return self._format_simple(result)
    
    def _format_simple(self, result: RegexResult) -> str:
        """Format output in simple format"""
        if not result.matches:
            return f"No matches found for pattern: {result.pattern}"
        
        output = [f"Found {result.total_matches} match(es):"]
        for i, match in enumerate(result.matches, 1):
            output.append(f"{i}. '{match.match_text}' at position {match.start_pos}-{match.end_pos}")
        
        return "\n".join(output)
    
    def _format_detailed(self, result: RegexResult) -> str:
        """Format output in detailed format"""
        output = [
            "=" * 50,
            f"REGEX ANALYSIS RESULTS",
            "=" * 50,
            f"Pattern: {result.pattern}",
            f"Flags: {', '.join(result.flags) if result.flags else 'None'}",
            f"Execution time: {result.execution_time:.4f} seconds",
            f"Total matches: {result.total_matches}",
            "-" * 50
        ]
        
        if not result.matches:
            output.append("No matches found.")
            return "\n".join(output)
        
        for i, match in enumerate(result.matches, 1):
            output.extend([
                f"Match #{i}:",
                f"  Text: '{match.match_text}'",
                f"  Position: {match.start_pos}-{match.end_pos}",
                f"  Length: {len(match.match_text)} characters"
            ])
            
            if match.groups:
                output.append(f"  Groups: {match.groups}")
            
            if match.named_groups:
                output.append(f"  Named groups: {match.named_groups}")
            
            output.append("")
        
        return "\n".join(output)
    
    def _format_table(self, result: RegexResult) -> str:
        """Format output in table format"""
        if not result.matches:
            return f"No matches found for pattern: {result.pattern}"
        
        # Header
        output = [
            f"Pattern: {result.pattern} | Matches: {result.total_matches}",
            "-" * 80,
            f"{'#':<3} {'Match':<25} {'Start':<6} {'End':<6} {'Groups':<20}",
            "-" * 80
        ]
        
        # Rows
        for i, match in enumerate(result.matches, 1):
            match_text = match.match_text[:22] + "..." if len(match.match_text) > 25 else match.match_text
            groups_str = str(match.groups)[:17] + "..." if len(str(match.groups)) > 20 else str(match.groups)
            
            output.append(f"{i:<3} {match_text:<25} {match.start_pos:<6} {match.end_pos:<6} {groups_str:<20}")
        
        return "\n".join(output)
    
    def _format_json(self, result: RegexResult) -> str:
        """Format output in JSON format"""
        json_data = {
            "pattern": result.pattern,
            "flags": result.flags,
            "execution_time": result.execution_time,
            "total_matches": result.total_matches,
            "matches": []
        }
        
        for match in result.matches:
            json_data["matches"].append({
                "text": match.match_text,
                "start": match.start_pos,
                "end": match.end_pos,
                "groups": match.groups,
                "named_groups": match.named_groups
            })
        
        return json.dumps(json_data, indent=2)
    
    def get_predefined_pattern(self, name: str) -> Optional[str]:
        """Get a predefined regex pattern by name"""
        return self.predefined_patterns.get(name.lower())
    
    def list_predefined_patterns(self) -> str:
        """List all available predefined patterns"""
        output = ["Available predefined patterns:"]
        for name, pattern in self.predefined_patterns.items():
            output.append(f"  {name}: {pattern}")
        return "\n".join(output)
    
    def substitute_text(self, pattern: str, replacement: str, text: str, flags: str = '', count: int = 0) -> Dict[str, Any]:
        """
        Perform regex substitution
        
        Args:
            pattern: Regular expression pattern
            replacement: Replacement string
            text: Text to perform substitution on
            flags: Flag string
            count: Maximum number of substitutions (0 = all)
            
        Returns:
            Dictionary with substitution results
        """
        is_valid, error_msg = self.validate_pattern(pattern)
        if not is_valid:
            return {"error": error_msg, "result": None, "count": 0}
        
        compiled_flags, flag_names = self.parse_flags(flags)
        
        try:
            regex = re.compile(pattern, compiled_flags)
            result, num_subs = regex.subn(replacement, text, count=count)
            
            return {
                "error": None,
                "result": result,
                "count": num_subs,
                "flags": flag_names
            }
        except Exception as e:
            return {"error": str(e), "result": None, "count": 0}


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser"""
    parser = argparse.ArgumentParser(
        description="Regex Query Tool - Test and analyze regular expressions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -p "\\d+" -t "I have 123 apples and 456 oranges"
  python main.py -p "email" -t "Contact us at test@example.com" --predefined
  python main.py -p "\\w+" -t "Hello World" -f "i" --format detailed
  python main.py --list-patterns
  python main.py -p "\\d+" -r "X" -t "Replace 123 with X" --substitute
        """
    )
    
    parser.add_argument('-p', '--pattern', help='Regular expression pattern')
    parser.add_argument('-t', '--text', help='Text to search in')
    parser.add_argument('-f', '--flags', default='', help='Regex flags (i,m,s,x,a,l)')
    parser.add_argument('--format', choices=['simple', 'detailed', 'json', 'table'], 
                       default='simple', help='Output format')
    parser.add_argument('--predefined', action='store_true', 
                       help='Use predefined pattern by name')
    parser.add_argument('--list-patterns', action='store_true', 
                       help='List all predefined patterns')
    parser.add_argument('-r', '--replace', help='Replacement string for substitution')
    parser.add_argument('--substitute', action='store_true', 
                       help='Perform substitution instead of matching')
    parser.add_argument('--count', type=int, default=0, 
                       help='Max substitutions (0=all)')
    parser.add_argument('--interactive', action='store_true', 
                       help='Start interactive mode')
    
    return parser


def interactive_mode(tool: RegexQueryTool):
    """Run the tool in interactive mode"""
    print("\n🔍 Regex Query Tool - Interactive Mode")
    print("Type 'help' for commands, 'quit' to exit\n")
    
    while True:
        try:
            command = input("regex> ").strip()
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif command.lower() == 'help':
                print("""
Available commands:
  match <pattern> <text> [flags]     - Find matches
  sub <pattern> <replacement> <text> - Substitute text
  validate <pattern>                 - Validate pattern
  predefined                         - List predefined patterns
  use <pattern_name> <text>          - Use predefined pattern
  help                              - Show this help
  quit/exit/q                       - Exit interactive mode
                """)
            elif command.lower() == 'predefined':
                print(tool.list_predefined_patterns())
            elif command.startswith('match '):
                parts = command.split(' ', 3)
                if len(parts) >= 3:
                    pattern, text = parts[1], parts[2]
                    flags = parts[3] if len(parts) > 3 else ''
                    result = tool.find_matches(pattern, text, flags)
                    print(tool.format_output(result, OutputFormat.DETAILED))
                else:
                    print("Usage: match <pattern> <text> [flags]")
            elif command.startswith('sub '):
                parts = command.split(' ', 4)
                if len(parts) >= 4:
                    pattern, replacement, text = parts[1], parts[2], parts[3]
                    result = tool.substitute_text(pattern, replacement, text)
                    if result['error']:
                        print(f"❌ Error: {result['error']}")
                    else:
                        print(f"✅ Made {result['count']} substitution(s)")
                        print(f"Result: {result['result']}")
                else:
                    print("Usage: sub <pattern> <replacement> <text>")
            elif command.startswith('validate '):
                pattern = command[9:]
                is_valid, error = tool.validate_pattern(pattern)
                if is_valid:
                    print("✅ Valid regex pattern")
                else:
                    print(f"❌ Invalid pattern: {error}")
            elif command.startswith('use '):
                parts = command.split(' ', 2)
                if len(parts) >= 3:
                    pattern_name, text = parts[1], parts[2]
                    pattern = tool.get_predefined_pattern(pattern_name)
                    if pattern:
                        result = tool.find_matches(pattern, text)
                        print(tool.format_output(result, OutputFormat.DETAILED))
                    else:
                        print(f"❌ Unknown predefined pattern: {pattern_name}")
                else:
                    print("Usage: use <pattern_name> <text>")
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


def main():
    """Main function to run the regex query tool"""
    parser = create_parser()
    args = parser.parse_args()
    
    tool = RegexQueryTool()
    
    # Handle special commands
    if args.list_patterns:
        print(tool.list_predefined_patterns())
        return
    
    if args.interactive:
        interactive_mode(tool)
        return
    
    # Validate required arguments for normal operation
    if not args.pattern or not args.text:
        print("❌ Error: Both --pattern and --text are required (unless using --list-patterns or --interactive)")
        parser.print_help()
        return
    
    # Get pattern (predefined or direct)
    if args.predefined:
        pattern = tool.get_predefined_pattern(args.pattern)
        if not pattern:
            print(f"❌ Error: Unknown predefined pattern '{args.pattern}'")
            print("\nUse --list-patterns to see available patterns")
            return
    else:
        pattern = args.pattern
    
    # Handle substitution vs matching
    if args.substitute:
        if not args.replace:
            print("❌ Error: --replace is required when using --substitute")
            return
        
        result = tool.substitute_text(pattern, args.replace, args.text, args.flags, args.count)
        if result['error']:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Made {result['count']} substitution(s)")
            print(f"Flags used: {', '.join(result['flags']) if result['flags'] else 'None'}")
            print(f"Result:\n{result['result']}")
    else:
        # Perform matching
        result = tool.find_matches(pattern, args.text, args.flags)
        output_format = OutputFormat(args.format)
        print(tool.format_output(result, output_format))


# Simple unit tests (can be run by adding --test flag handling)
def run_tests():
    """Run basic unit tests"""
    tool = RegexQueryTool()
    
    print("Running basic tests...")
    
    # Test 1: Basic matching
    result = tool.find_matches(r'\d+', "I have 123 apples and 456 oranges")
    assert result.total_matches == 2
    assert result.matches[0].match_text == "123"
    assert result.matches[1].match_text == "456"
    print("✅ Test 1 passed: Basic matching")
    
    # Test 2: Invalid pattern
    result = tool.find_matches(r'[', "test")
    assert not result.is_valid_pattern
    print("✅ Test 2 passed: Invalid pattern handling")
    
    # Test 3: Predefined pattern
    pattern = tool.get_predefined_pattern('email')
    result = tool.find_matches(pattern, "Contact test@example.com for help")
    assert result.total_matches == 1
    print("✅ Test 3 passed: Predefined patterns")
    
    # Test 4: Substitution
    sub_result = tool.substitute_text(r'\d+', 'X', "Replace 123 and 456", count=1)
    assert sub_result['count'] == 1
    assert "Replace X and 456" == sub_result['result']
    print("✅ Test 4 passed: Substitution")
    
    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    # Uncomment the next two lines to run tests
    # run_tests()
    # sys.exit(0)
    
    main()
