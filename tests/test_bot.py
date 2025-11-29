"""
Tests for the Quantum Date Bot CLI module.
"""

import unittest
import sys
from io import StringIO
from unittest.mock import patch

from quantum_date_bot.bot import main, create_parser


class TestBotCLI(unittest.TestCase):
    """Test cases for the CLI bot interface."""
    
    def test_basic_date_detection(self):
        """Test basic date detection via CLI."""
        with patch('sys.stdout', new=StringIO()) as output:
            result = main(['2025-01-15'])
            self.assertEqual(result, 0)
            self.assertIn('2025-01-15', output.getvalue())
    
    def test_all_flag(self):
        """Test --all flag to show all dates."""
        with patch('sys.stdout', new=StringIO()) as output:
            result = main(['--all', 'Meeting 2025-01-15 and 2025-02-20'])
            self.assertEqual(result, 0)
            output_text = output.getvalue()
            self.assertIn('2025-01-15', output_text)
            self.assertIn('2025-02-20', output_text)
    
    def test_json_output(self):
        """Test JSON output format."""
        with patch('sys.stdout', new=StringIO()) as output:
            result = main(['--json', '2025-01-15'])
            self.assertEqual(result, 0)
            import json
            output_data = json.loads(output.getvalue())
            self.assertIsInstance(output_data, list)
            self.assertEqual(len(output_data), 1)
    
    def test_format_option_us(self):
        """Test US format output option."""
        with patch('sys.stdout', new=StringIO()) as output:
            result = main(['--format', 'US', '2025-01-15'])
            self.assertEqual(result, 0)
            self.assertIn('01/15/2025', output.getvalue())
    
    def test_no_dates_found(self):
        """Test exit code when no dates found."""
        with patch('sys.stdout', new=StringIO()):
            result = main(['No dates here'])
            self.assertEqual(result, 1)
    
    def test_parser_creation(self):
        """Test argument parser creation."""
        parser = create_parser()
        self.assertIsNotNone(parser)
        # Test that help doesn't raise an error
        with self.assertRaises(SystemExit) as cm:
            parser.parse_args(['--help'])
        self.assertEqual(cm.exception.code, 0)


class TestBotOutputFormats(unittest.TestCase):
    """Test different output format options."""
    
    def test_eu_format(self):
        """Test EU format output."""
        with patch('sys.stdout', new=StringIO()) as output:
            result = main(['--format', 'EU', '2025-01-15'])
            self.assertEqual(result, 0)
            self.assertIn('15/01/2025', output.getvalue())
    
    def test_written_format(self):
        """Test Written format output."""
        with patch('sys.stdout', new=StringIO()) as output:
            result = main(['--format', 'Written', '2025-01-15'])
            self.assertEqual(result, 0)
            self.assertIn('January 15, 2025', output.getvalue())
    
    def test_compact_format(self):
        """Test Compact format output."""
        with patch('sys.stdout', new=StringIO()) as output:
            result = main(['--format', 'Compact', '2025-01-15'])
            self.assertEqual(result, 0)
            self.assertIn('20250115', output.getvalue())


if __name__ == '__main__':
    unittest.main()
