#!/usr/bin/env python3
"""
Quantum Date Bot - Command line interface for date identification.
"""

import argparse
import sys
from typing import Optional

from .date_identifier import QuantumDateIdentifier


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='quantum-date-bot',
        description='🔮 Quantum Date Identifier Bot - Identify dates with quantum-inspired confidence scoring',
        epilog='Example: quantum-date-bot "Meeting on 2025-01-15 at 3pm"'
    )
    
    parser.add_argument(
        'text',
        nargs='?',
        help='Text to search for dates'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['ISO', 'US', 'EU', 'Written', 'Compact'],
        default='ISO',
        help='Output format for dates (default: ISO)'
    )
    
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Show all identified dates (not just the best match)'
    )
    
    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    return parser


def format_result(result: dict, identifier: QuantumDateIdentifier, 
                  output_format: str) -> str:
    """Format a single result for display."""
    if result['parsed']:
        formatted_date = identifier.format_date(result['parsed'], output_format)
        confidence_bar = '█' * int(result['confidence'] * 10)
        confidence_bar += '░' * (10 - int(result['confidence'] * 10))
        return (f"  📅 {result['original']}\n"
                f"     → {formatted_date} ({result['format']})\n"
                f"     Confidence: [{confidence_bar}] {result['confidence']:.0%}")
    return f"  ⚠️  {result['original']} (Could not parse)"


def run_interactive(identifier: QuantumDateIdentifier, output_format: str):
    """Run the bot in interactive mode."""
    print("\n🔮 Quantum Date Identifier Bot - Interactive Mode")
    print("=" * 50)
    print("Enter text to identify dates. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            text = input("🔍 Enter text: ").strip()
            if text.lower() in ('quit', 'exit', 'q'):
                print("\n👋 Goodbye!")
                break
            if not text:
                continue
                
            results = identifier.identify_dates(text)
            if results:
                print(f"\n✨ Found {len(results)} date(s):\n")
                for result in results:
                    print(format_result(result, identifier, output_format))
                    print()
            else:
                print("\n❌ No dates found in the text.\n")
        except EOFError:
            print("\n👋 Goodbye!")
            break
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break


def main(args: Optional[list] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    identifier = QuantumDateIdentifier()
    
    # Interactive mode
    if parsed_args.interactive:
        run_interactive(identifier, parsed_args.format)
        return 0
    
    # Check if text was provided
    if not parsed_args.text:
        # Try reading from stdin
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
        else:
            parser.print_help()
            return 1
    else:
        text = parsed_args.text
    
    # Process text
    if parsed_args.all:
        results = identifier.identify_dates(text)
    else:
        result = identifier.get_best_date(text)
        results = [result] if result else []
    
    if not results:
        print("❌ No dates found in the text.")
        return 1
    
    # Output results
    if parsed_args.json:
        import json
        output = []
        for r in results:
            item = {
                'original': r['original'],
                'formatted': identifier.format_date(r['parsed'], parsed_args.format) if r['parsed'] else None,
                'format': r['format'],
                'confidence': r['confidence'],
                'position': r['position']
            }
            output.append(item)
        print(json.dumps(output, indent=2))
    else:
        print(f"\n🔮 Quantum Date Identifier Results")
        print("=" * 40)
        print(f"\nInput: \"{text}\"\n")
        for result in results:
            print(format_result(result, identifier, parsed_args.format))
            print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
