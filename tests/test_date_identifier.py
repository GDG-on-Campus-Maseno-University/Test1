"""
Tests for the Quantum Date Identifier module.
"""

import unittest
from datetime import datetime

from quantum_date_bot.date_identifier import QuantumDateIdentifier


class TestQuantumDateIdentifier(unittest.TestCase):
    """Test cases for QuantumDateIdentifier class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.identifier = QuantumDateIdentifier()
    
    def test_iso_format(self):
        """Test ISO format date identification (YYYY-MM-DD)."""
        results = self.identifier.identify_dates("Meeting on 2025-01-15")
        # May match multiple formats (ISO and Year-Month for prefix)
        self.assertGreaterEqual(len(results), 1)
        # Best match should be ISO with highest confidence
        best = results[0]
        self.assertEqual(best['format'], 'ISO')
        self.assertEqual(best['parsed'], datetime(2025, 1, 15))
        self.assertGreater(best['confidence'], 0.5)
    
    def test_us_format(self):
        """Test US format date identification (MM/DD/YYYY)."""
        results = self.identifier.identify_dates("Event on 01/15/2025")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['format'], 'US')
        self.assertEqual(results[0]['parsed'], datetime(2025, 1, 15))
    
    def test_written_format_full_month(self):
        """Test written format with full month name."""
        results = self.identifier.identify_dates("January 15, 2025 is the date")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['format'], 'Written')
        self.assertEqual(results[0]['parsed'], datetime(2025, 1, 15))
    
    def test_written_format_abbreviated(self):
        """Test written format with abbreviated month name."""
        results = self.identifier.identify_dates("Meeting on Jan 15, 2025")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['format'], 'Written')
        self.assertEqual(results[0]['parsed'], datetime(2025, 1, 15))
    
    def test_compact_format(self):
        """Test compact format (YYYYMMDD)."""
        results = self.identifier.identify_dates("Reference: 20250115")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['format'], 'Compact')
        self.assertEqual(results[0]['parsed'], datetime(2025, 1, 15))
    
    def test_multiple_dates(self):
        """Test identifying multiple dates in text."""
        text = "From 2025-01-15 to 2025-02-20"
        results = self.identifier.identify_dates(text)
        # Multiple matches possible per date due to overlapping patterns
        self.assertGreaterEqual(len(results), 2)
        dates = [r['parsed'] for r in results]
        self.assertIn(datetime(2025, 1, 15), dates)
        self.assertIn(datetime(2025, 2, 20), dates)
    
    def test_no_dates(self):
        """Test text with no dates."""
        results = self.identifier.identify_dates("No dates here!")
        self.assertEqual(len(results), 0)
    
    def test_get_best_date(self):
        """Test getting the best matching date."""
        result = self.identifier.get_best_date("Meeting 2025-01-15")
        self.assertIsNotNone(result)
        self.assertEqual(result['parsed'], datetime(2025, 1, 15))
    
    def test_get_best_date_none(self):
        """Test get_best_date returns None when no dates."""
        result = self.identifier.get_best_date("No dates here")
        self.assertIsNone(result)
    
    def test_format_date_iso(self):
        """Test formatting date to ISO format."""
        date = datetime(2025, 1, 15)
        formatted = self.identifier.format_date(date, 'ISO')
        self.assertEqual(formatted, '2025-01-15')
    
    def test_format_date_us(self):
        """Test formatting date to US format."""
        date = datetime(2025, 1, 15)
        formatted = self.identifier.format_date(date, 'US')
        self.assertEqual(formatted, '01/15/2025')
    
    def test_format_date_eu(self):
        """Test formatting date to EU format."""
        date = datetime(2025, 1, 15)
        formatted = self.identifier.format_date(date, 'EU')
        self.assertEqual(formatted, '15/01/2025')
    
    def test_format_date_written(self):
        """Test formatting date to written format."""
        date = datetime(2025, 1, 15)
        formatted = self.identifier.format_date(date, 'Written')
        self.assertEqual(formatted, 'January 15, 2025')
    
    def test_format_date_compact(self):
        """Test formatting date to compact format."""
        date = datetime(2025, 1, 15)
        formatted = self.identifier.format_date(date, 'Compact')
        self.assertEqual(formatted, '20250115')
    
    def test_confidence_scores(self):
        """Test that confidence scores are between 0 and 1."""
        results = self.identifier.identify_dates("2025-01-15, January 20, 2025")
        for result in results:
            self.assertGreaterEqual(result['confidence'], 0)
            self.assertLessEqual(result['confidence'], 1)
    
    def test_position_tracking(self):
        """Test that positions are correctly tracked."""
        text = "Date: 2025-01-15"
        results = self.identifier.identify_dates(text)
        self.assertGreaterEqual(len(results), 1)
        # Best match should have correct position for the ISO date
        best = results[0]
        start, end = best['position']
        self.assertEqual(text[start:end], '2025-01-15')
    
    def test_case_insensitive_months(self):
        """Test that month names are case insensitive."""
        results = self.identifier.identify_dates("JANUARY 15, 2025")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['parsed'], datetime(2025, 1, 15))
    
    def test_year_month_format(self):
        """Test year-month format (YYYY-MM)."""
        results = self.identifier.identify_dates("Report for 2025-01")
        self.assertTrue(any(r['format'] == 'Year-Month' for r in results))


class TestDateEdgeCases(unittest.TestCase):
    """Test edge cases for date identification."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.identifier = QuantumDateIdentifier()
    
    def test_invalid_date_values(self):
        """Test that invalid date values are handled."""
        # Month 13 is invalid
        results = self.identifier.identify_dates("2025-13-01")
        # Should not parse successfully or have low confidence
        valid_results = [r for r in results if r['parsed'] is not None]
        self.assertEqual(len(valid_results), 0)
    
    def test_leap_year_date(self):
        """Test leap year date (Feb 29)."""
        results = self.identifier.identify_dates("2024-02-29")
        self.assertGreaterEqual(len(results), 1)
        # Best match should be the full date
        best = results[0]
        self.assertEqual(best['parsed'], datetime(2024, 2, 29))
    
    def test_embedded_in_sentence(self):
        """Test date embedded in a sentence."""
        text = "The conference scheduled for December 25, 2025 will be amazing!"
        results = self.identifier.identify_dates(text)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['parsed'], datetime(2025, 12, 25))


if __name__ == '__main__':
    unittest.main()
