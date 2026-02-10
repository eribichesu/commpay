# Commpay - Commercial Document Builder

A Python-based document builder for generating PDF commercial documents, specifically credit notes and commission acknowledgements for real estate agencies.

## Features

- Generate PDF commercial documents from templates
- Support for credit notes and commission acknowledgements
- Template-based document generation
- Interactive console interface
- API integration (coming soon)

## Project Structure

```
commpay/
├── src/
│   └── commpay/
│       ├── __init__.py
│       ├── builder.py       # Document builder core logic
│       ├── templates.py     # Template management
│       └── utils.py         # Helper utilities
├── tests/
│   ├── __init__.py
│   └── test_builder.py
├── templates/               # Document templates
├── output/                  # Generated documents
├── requirements.txt
├── setup.py
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/eribichesu/commpay.git
cd commpay
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Console

```bash
python -m commpay.cli
```

### As a Library

```python
from commpay.builder import DocumentBuilder

builder = DocumentBuilder()
# Usage example coming soon
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines and uses:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

Format code:
```bash
black src/ tests/
```

Run linter:
```bash
flake8 src/ tests/
```

## Contributing

Please follow the development agreement guidelines. All pull requests must:
- Follow conventional commits
- Pass all tests and linting
- Include appropriate documentation
- Be reviewed before merging

## License

MIT License
