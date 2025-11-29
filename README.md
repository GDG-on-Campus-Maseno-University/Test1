# Quantum Date Identifier Bot 🔮

A quantum-inspired date identification library and command-line tool that uses probabilistic scoring to identify and parse dates in various formats.

## Features

- 📅 **Multi-format Support**: Recognizes dates in ISO, US, European, written, and compact formats
- 🎯 **Confidence Scoring**: Each identified date comes with a quantum-inspired confidence score
- 🔄 **Format Conversion**: Convert dates between different formats
- 💻 **CLI Tool**: Easy-to-use command-line interface
- 🐍 **Python API**: Clean, well-documented Python interface

## Installation

```bash
# Clone the repository
git clone https://github.com/GDG-on-Campus-Maseno-University/Test1.git
cd Test1

# Install the package
pip install -e .
```

## Quick Start

### Command Line

```bash
# Identify dates in text
quantum-date-bot "Meeting scheduled for 2025-01-15"

# Show all dates found
quantum-date-bot --all "From January 1, 2025 to February 28, 2025"

# Output in different format
quantum-date-bot --format US "2025-01-15"

# Get JSON output
quantum-date-bot --json "2025-01-15"

# Interactive mode
quantum-date-bot --interactive
```

### Python API

```python
from quantum_date_bot import QuantumDateIdentifier

# Create identifier
identifier = QuantumDateIdentifier()

# Identify dates in text
results = identifier.identify_dates("Meeting on 2025-01-15 at 3pm")
for result in results:
    print(f"Found: {result['original']}")
    print(f"Parsed: {result['parsed']}")
    print(f"Format: {result['format']}")
    print(f"Confidence: {result['confidence']:.0%}")

# Get the best matching date
best = identifier.get_best_date("January 15, 2025 is the deadline")
if best:
    print(f"Best match: {best['parsed']}")

# Format dates
from datetime import datetime
date = datetime(2025, 1, 15)
print(identifier.format_date(date, 'Written'))  # January 15, 2025
print(identifier.format_date(date, 'US'))       # 01/15/2025
print(identifier.format_date(date, 'ISO'))      # 2025-01-15
```

## Supported Date Formats

| Format | Example | Description |
|--------|---------|-------------|
| ISO | 2025-01-15 | International standard |
| US | 01/15/2025 | Month/Day/Year |
| EU | 15/01/2025 | Day/Month/Year |
| Written | January 15, 2025 | Full month name |
| Written (abbr) | Jan 15, 2025 | Abbreviated month |
| Compact | 20250115 | No separators |
| Year-Month | 2025-01 | Year and month only |

## The Quantum Approach 🔮

The "quantum" aspect of this bot is inspired by quantum computing concepts:

1. **Superposition**: A date string can potentially match multiple formats simultaneously until we "measure" it
2. **Measurement/Collapse**: When we parse a date, we collapse the possibilities to the most likely interpretation
3. **Probability Amplitudes**: Each match has a confidence score representing its probability of being correct

The confidence score is calculated based on:
- Format specificity (ISO is unambiguous, US/EU can be ambiguous)
- Date validity (parsed successfully)
- Temporal reasonableness (dates closer to now score higher)

## Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=quantum_date_bot --cov-report=term-missing
```

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
