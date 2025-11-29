"""
Quantum Date Identifier - Core date parsing and identification logic.

Uses a quantum-inspired approach with probabilistic scoring to identify
dates in various formats from text input.
"""

import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class QuantumDateIdentifier:
    """
    A quantum-inspired date identifier that can parse and identify dates
    in multiple formats with confidence scoring.
    
    The "quantum" aspect comes from:
    1. Superposition: A date string can match multiple formats simultaneously
    2. Measurement: When we parse, we "collapse" to the most likely format
    3. Probability: Each match has a confidence score (0-1)
    """
    
    # Date format patterns with their regex and strptime format
    DATE_PATTERNS = [
        # ISO format: 2025-01-15
        (r'\b(\d{4})-(\d{2})-(\d{2})\b', '%Y-%m-%d', 'ISO'),
        # US format: 01/15/2025 or 1/15/2025
        (r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', '%m/%d/%Y', 'US'),
        # European format: 15/01/2025 or 15.01.2025
        (r'\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b', '%d/%m/%Y', 'EU'),
        # Written format: January 15, 2025 or Jan 15, 2025
        (r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
         r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
         r'Dec(?:ember)?)\s+(\d{1,2}),?\s+(\d{4})\b', None, 'Written'),
        # Compact format: 20250115
        (r'\b(\d{4})(\d{2})(\d{2})\b', '%Y%m%d', 'Compact'),
        # Year-Month: 2025-01 or 2025/01
        (r'\b(\d{4})[-/](\d{2})\b', '%Y-%m', 'Year-Month'),
    ]
    
    MONTH_MAP = {
        'jan': 1, 'january': 1,
        'feb': 2, 'february': 2,
        'mar': 3, 'march': 3,
        'apr': 4, 'april': 4,
        'may': 5,
        'jun': 6, 'june': 6,
        'jul': 7, 'july': 7,
        'aug': 8, 'august': 8,
        'sep': 9, 'september': 9,
        'oct': 10, 'october': 10,
        'nov': 11, 'november': 11,
        'dec': 12, 'december': 12,
    }
    
    def __init__(self):
        """Initialize the Quantum Date Identifier."""
        self.compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), fmt, name)
            for pattern, fmt, name in self.DATE_PATTERNS
        ]
    
    def identify_dates(self, text: str) -> List[Dict]:
        """
        Identify all possible dates in the given text.
        
        Args:
            text: The input text to search for dates.
            
        Returns:
            A list of dictionaries containing:
            - 'original': The original matched string
            - 'parsed': The parsed datetime object (if valid)
            - 'format': The detected format name
            - 'confidence': Confidence score (0-1)
            - 'position': (start, end) position in text
        """
        results = []
        
        for pattern, strp_fmt, format_name in self.compiled_patterns:
            for match in pattern.finditer(text):
                original = match.group(0)
                position = (match.start(), match.end())
                
                parsed_date = self._parse_match(match, strp_fmt, format_name)
                confidence = self._calculate_confidence(parsed_date, format_name, original)
                
                if parsed_date or confidence > 0:
                    results.append({
                        'original': original,
                        'parsed': parsed_date,
                        'format': format_name,
                        'confidence': confidence,
                        'position': position
                    })
        
        # Sort by confidence (quantum collapse to most likely)
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Remove duplicates (same position with lower confidence)
        seen_positions = set()
        unique_results = []
        for result in results:
            pos_key = result['position']
            if pos_key not in seen_positions:
                seen_positions.add(pos_key)
                unique_results.append(result)
        
        return unique_results
    
    def _parse_match(self, match: re.Match, strp_fmt: Optional[str], 
                     format_name: str) -> Optional[datetime]:
        """Parse a regex match into a datetime object."""
        try:
            if format_name == 'Written':
                # Handle written format specially
                month_str = match.group(1).lower()
                day = int(match.group(2))
                year = int(match.group(3))
                month = self.MONTH_MAP.get(month_str)
                if month:
                    return datetime(year, month, day)
                return None
            elif format_name == 'Year-Month':
                # Year-Month format
                year = int(match.group(1))
                month = int(match.group(2))
                return datetime(year, month, 1)
            elif format_name == 'EU':
                # Try European format (day/month/year)
                day = int(match.group(1))
                month = int(match.group(2))
                year = int(match.group(3))
                # Validate ranges before creating datetime
                if not (1 <= month <= 12 and 1 <= day <= 31):
                    return None
                return datetime(year, month, day)
            elif strp_fmt:
                return datetime.strptime(match.group(0), strp_fmt)
        except (ValueError, TypeError):
            return None
        return None
    
    def _calculate_confidence(self, parsed_date: Optional[datetime], 
                              format_name: str, original: str) -> float:
        """
        Calculate confidence score for a date match.
        
        Uses quantum-inspired probabilistic scoring based on:
        - Whether the date could be parsed successfully
        - The specificity of the format
        - Whether the date is reasonable (not too far in past/future)
        """
        if not parsed_date:
            return 0.0
        
        confidence = 0.5  # Base confidence
        
        # Format specificity bonus
        format_scores = {
            'ISO': 0.3,      # ISO is unambiguous
            'Written': 0.25, # Written is clear
            'Compact': 0.2,  # Compact is specific
            'US': 0.1,       # US/EU can be ambiguous
            'EU': 0.1,
            'Year-Month': 0.15,
        }
        confidence += format_scores.get(format_name, 0)
        
        # Reasonable date check (within 100 years of now)
        now = datetime.now()
        years_diff = abs((parsed_date - now).days) / 365.25
        if years_diff <= 10:
            confidence += 0.15
        elif years_diff <= 50:
            confidence += 0.1
        elif years_diff <= 100:
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    def get_best_date(self, text: str) -> Optional[Dict]:
        """
        Get the single best date from the text (quantum collapse).
        
        Args:
            text: The input text to search for dates.
            
        Returns:
            The highest confidence date match, or None if no dates found.
        """
        results = self.identify_dates(text)
        return results[0] if results else None
    
    def format_date(self, date: datetime, output_format: str = 'ISO') -> str:
        """
        Format a datetime object to a specified format.
        
        Args:
            date: The datetime object to format.
            output_format: One of 'ISO', 'US', 'EU', 'Written', 'Compact'.
            
        Returns:
            The formatted date string.
        """
        formats = {
            'ISO': '%Y-%m-%d',
            'US': '%m/%d/%Y',
            'EU': '%d/%m/%Y',
            'Written': '%B %d, %Y',
            'Compact': '%Y%m%d',
        }
        return date.strftime(formats.get(output_format, '%Y-%m-%d'))
