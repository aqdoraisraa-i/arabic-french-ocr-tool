# Contributing to Arabic-French OCR Tool

Thank you for your interest in contributing to the Arabic-French OCR Tool! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: 
  - OS (Windows/Linux/macOS)
  - Python version
  - Tesseract version
  - Application version
- **Screenshots**: If applicable
- **Error Messages**: Full error messages or stack traces

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

- **Use Case**: Describe the problem you're trying to solve
- **Proposed Solution**: Your suggested approach
- **Alternatives**: Other solutions you've considered
- **Additional Context**: Any other relevant information

### Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/arabic-french-ocr-tool.git
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test Your Changes**
   - Ensure the application still runs
   - Test with various input files
   - Verify no existing functionality is broken

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR 4.0 or higher
- Git

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/your-username/arabic-french-ocr-tool.git
cd arabic-french-ocr-tool

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-qt black flake8
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_ocr.py

# Run with coverage
pytest --cov=src tests/
```

### Code Style

This project follows PEP 8 style guidelines.

```bash
# Check code style
flake8 src/

# Auto-format code
black src/
```

## Code Guidelines

### Python Code Style

- Follow PEP 8
- Use meaningful variable names
- Maximum line length: 100 characters
- Use type hints where applicable
- Write docstrings for all functions and classes

### Documentation

- Update README.md if adding new features
- Add docstrings to new functions/classes
- Update EXAMPLES.md with usage examples
- Keep comments up to date

### Commit Messages

Write clear commit messages:

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Examples:
```
Add Arabic handwriting support
Fix PDF processing on Windows
Update README with new examples
Refactor image preprocessing module
```

## Project Structure

```
arabic-french-ocr-tool/
├── src/               # Source code
│   ├── gui/          # GUI components
│   ├── ocr/          # OCR engine and preprocessing
│   └── utils/        # Utility functions
├── tests/            # Test files
├── assets/           # Assets (icons, etc.)
├── docs/             # Documentation
└── examples/         # Example files
```

## Adding New Features

### Adding a New Language

1. Ensure Tesseract supports the language
2. Add language code to `OCREngine.LANGUAGE_CODES`
3. Update GUI language dropdown
4. Update documentation
5. Test thoroughly

### Adding Export Format

1. Add export function to `utils/export.py`
2. Update `ExportHandler` class
3. Add GUI button in `main_window.py`
4. Update documentation
5. Test with various content

### Improving Preprocessing

1. Add new function to `preprocessor.py`
2. Update `preprocess_image` method
3. Add optional parameter for new technique
4. Document the new preprocessing step
5. Test impact on OCR accuracy

## Testing

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Test edge cases
- Include both positive and negative tests

Example test:

```python
def test_image_preprocessing():
    """Test image preprocessing functionality."""
    preprocessor = ImagePreprocessor()
    image = Image.open('test_image.jpg')
    
    processed = preprocessor.preprocess_image(image)
    
    assert processed is not None
    assert processed.shape[0] > 0
    assert processed.shape[1] > 0
```

### Test Coverage

- Aim for at least 70% code coverage
- Focus on critical functionality
- Test error handling
- Test edge cases

## Documentation

### Code Documentation

All functions and classes should have docstrings:

```python
def extract_text(image: Image.Image, language: str = 'Both') -> str:
    """
    Extract text from image using OCR.
    
    Args:
        image: PIL Image object
        language: Language for OCR ('Arabic', 'French', or 'Both')
        
    Returns:
        Extracted text as string
        
    Raises:
        ValueError: If language is not supported
    """
    pass
```

### User Documentation

- Update README.md for new features
- Add examples to EXAMPLES.md
- Update troubleshooting section
- Keep installation instructions current

## Release Process

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create git tag
4. Build executable
5. Create GitHub release
6. Update documentation

## Questions?

If you have questions about contributing:

- Check existing issues
- Read the documentation
- Create a new issue with your question

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
