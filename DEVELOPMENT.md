# Development Guide for Arabic-French OCR Tool

This document provides guidance for developers who want to understand, modify, or extend the Arabic-French OCR Tool.

## Architecture Overview

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    GUI Layer (PyQt5)                     │
│                  src/gui/main_window.py                  │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Business Logic Layer                   │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │  OCR Engine    │  │ File Handler │  │   Export    │ │
│  │ (engine.py)    │  │(file_handler)│  │ (export.py) │ │
│  └────────────────┘  └──────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Processing Layer                       │
│  ┌──────────────────────┐  ┌──────────────────────────┐ │
│  │  Image Preprocessor  │  │   Tesseract OCR Engine   │ │
│  │  (preprocessor.py)   │  │     (pytesseract)        │ │
│  └──────────────────────┘  └──────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Module Breakdown

### 1. OCR Module (`src/ocr/`)

#### `engine.py` - OCR Engine
- **Purpose**: Manages text extraction using Tesseract OCR
- **Key Classes**: `OCREngine`
- **Main Functions**:
  - `extract_text()`: Basic text extraction
  - `extract_text_with_confidence()`: Text extraction with confidence scores
  - `check_language_support()`: Verify language availability

**Usage Example**:
```python
from src.ocr.engine import OCREngine
from PIL import Image

ocr = OCREngine()
image = Image.open('document.jpg')
text = ocr.extract_text(image, language='Arabic')
```

#### `preprocessor.py` - Image Preprocessing
- **Purpose**: Enhance image quality before OCR
- **Key Classes**: `ImagePreprocessor`
- **Processing Steps**:
  1. Grayscale conversion
  2. Noise reduction (median blur)
  3. Contrast enhancement (CLAHE)
  4. Skew correction
  5. Binarization (adaptive thresholding)

**Usage Example**:
```python
from src.ocr.preprocessor import ImagePreprocessor
from PIL import Image

preprocessor = ImagePreprocessor()
image = Image.open('noisy_document.jpg')
enhanced = preprocessor.preprocess_image(image)
```

### 2. Utilities Module (`src/utils/`)

#### `file_handler.py` - File Operations
- **Purpose**: Handle file loading and validation
- **Key Classes**: `FileHandler`
- **Supported Formats**: JPG, PNG, BMP, TIFF, PDF
- **Main Functions**:
  - `load_file()`: Load image or PDF
  - `validate_files()`: Validate file list
  - `is_supported_file()`: Check format support

#### `export.py` - Export Operations
- **Purpose**: Export extracted text to various formats
- **Key Classes**: `ExportHandler`
- **Export Formats**: TXT, DOCX, Clipboard
- **Main Functions**:
  - `export_to_txt()`: Save as text file
  - `export_to_docx()`: Save as Word document
  - `copy_to_clipboard()`: Copy to system clipboard

### 3. GUI Module (`src/gui/`)

#### `main_window.py` - Main Application Window
- **Purpose**: User interface and interaction
- **Key Classes**: 
  - `MainWindow`: Main application window
  - `OCRWorker`: Background thread for OCR processing
- **Features**:
  - Drag-and-drop file upload
  - Multi-file selection
  - Progress tracking
  - Language selection
  - Export options

## Threading Model

The application uses PyQt5's QThread for background processing to keep the UI responsive:

```
Main Thread (GUI)
    │
    ├─ User interactions (buttons, dropdowns, etc.)
    │
    └─► OCRWorker Thread
        │
        ├─ File loading
        ├─ Image preprocessing
        ├─ OCR processing
        └─► Signals back to main thread
            ├─ progress (update progress bar)
            ├─ result (display text)
            └─ finished (re-enable buttons)
```

**Important**: All OCR processing happens in the worker thread to prevent UI freezing.

## Data Flow

1. **File Selection**:
   ```
   User → File Dialog/Drag-Drop → FileHandler.validate_files()
   → Update file list → Enable "Process OCR" button
   ```

2. **OCR Processing**:
   ```
   User clicks "Process OCR"
   → Create OCRWorker thread
   → For each file:
       → FileHandler.load_file() → Image(s)
       → ImagePreprocessor.preprocess_image() → Enhanced image
       → OCREngine.extract_text() → Text
       → Emit result signal
   → Update GUI with results
   ```

3. **Export**:
   ```
   User clicks Export button
   → ExportHandler.export() → Save file
   → Show success message
   ```

## Error Handling

The application implements comprehensive error handling:

```python
# File loading errors
try:
    images = FileHandler.load_file(file_path)
except FileNotFoundError:
    # Handle missing file
except ValueError:
    # Handle unsupported format
```

```python
# OCR errors
try:
    text = ocr_engine.extract_text(image, language)
except RuntimeError:
    # Handle OCR failure
except ValueError:
    # Handle invalid language
```

## Extending the Application

### Adding a New Language

1. **Update Language Codes**:
   ```python
   # In src/ocr/engine.py
   LANGUAGE_CODES = {
       'Arabic': 'ara',
       'French': 'fra',
       'Spanish': 'spa',  # New language
       'Both': 'ara+fra'
   }
   ```

2. **Update GUI**:
   ```python
   # In src/gui/main_window.py
   self.language_combo.addItems(['Both', 'Arabic', 'French', 'Spanish'])
   ```

3. **Update Documentation**:
   - Add to README.md
   - Update EXAMPLES.md
   - Note in CHANGELOG.md

### Adding a New Export Format

1. **Create Export Function**:
   ```python
   # In src/utils/export.py
   @staticmethod
   def export_to_pdf(text: str, file_path: str) -> bool:
       """Export text to PDF."""
       # Implementation
   ```

2. **Update Export Handler**:
   ```python
   # Add to export() method
   elif format_type == 'pdf':
       return ExportHandler.export_to_pdf(text, file_path)
   ```

3. **Add GUI Button**:
   ```python
   # In src/gui/main_window.py
   self.export_pdf_btn = QPushButton("Export as PDF")
   self.export_pdf_btn.clicked.connect(lambda: self.export_text('pdf'))
   ```

### Adding New Preprocessing Technique

1. **Add Processing Function**:
   ```python
   # In src/ocr/preprocessor.py
   @staticmethod
   def sharpen(image: np.ndarray) -> np.ndarray:
       """Sharpen image."""
       kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
       return cv2.filter2D(image, -1, kernel)
   ```

2. **Update Pipeline**:
   ```python
   # Add to preprocess_image() method
   if sharpen:
       processed = ImagePreprocessor.sharpen(processed)
   ```

3. **Add GUI Control** (optional):
   ```python
   # Add checkbox for user control
   self.sharpen_checkbox = QCheckBox("Enable Sharpening")
   ```

## Performance Optimization

### Tips for Better Performance

1. **Image Size**: Resize large images before processing
   ```python
   if image.width > 3000:
       ratio = 3000 / image.width
       new_size = (3000, int(image.height * ratio))
       image = image.resize(new_size)
   ```

2. **Batch Processing**: Process files in smaller batches
   ```python
   # Process in batches of 10
   for batch in chunks(files, 10):
       process_batch(batch)
   ```

3. **Caching**: Cache preprocessed images for retry
   ```python
   cache = {}
   if file_path in cache:
       image = cache[file_path]
   ```

4. **Parallel Processing**: Use multiprocessing for batch operations
   ```python
   from multiprocessing import Pool
   
   with Pool(4) as p:
       results = p.map(process_file, files)
   ```

## Testing

### Unit Tests

Create tests in `tests/` directory:

```python
# tests/test_preprocessor.py
import pytest
from src.ocr.preprocessor import ImagePreprocessor
from PIL import Image
import numpy as np

def test_grayscale_conversion():
    preprocessor = ImagePreprocessor()
    # Create test image
    image = Image.new('RGB', (100, 100), color='red')
    
    # Convert to grayscale
    gray = preprocessor.convert_to_grayscale(image)
    
    # Verify shape
    assert len(gray.shape) == 2
    assert gray.shape == (100, 100)
```

### Integration Tests

```python
# tests/test_integration.py
def test_full_ocr_pipeline():
    # Load test image
    image = Image.open('tests/data/test_arabic.jpg')
    
    # Process
    ocr = OCREngine()
    text = ocr.extract_text(image, language='Arabic')
    
    # Verify result
    assert len(text) > 0
    assert 'expected text' in text
```

## Debugging

### Enable Debug Logging

```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Common Issues

1. **Tesseract Not Found**:
   - Check PATH
   - Set explicit path: `pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

2. **Missing Language Data**:
   - Download from: https://github.com/tesseract-ocr/tessdata
   - Place in Tesseract's tessdata directory

3. **PDF Loading Fails**:
   - Install poppler: `pip install pdf2image`
   - Add poppler to PATH

## Best Practices

1. **Error Messages**: Always provide user-friendly error messages
2. **Input Validation**: Validate all user inputs
3. **Resource Cleanup**: Close file handles and clean up temp files
4. **Thread Safety**: Use signals for thread communication
5. **Documentation**: Keep docstrings updated
6. **Type Hints**: Use type hints for better IDE support
7. **Logging**: Log errors and important events
8. **Testing**: Write tests for new features

## Deployment

### Creating Executable

```bash
# Simple build
python build_exe.py

# Advanced build with custom options
pyinstaller --onefile --windowed \
    --name=ArabicFrenchOCR \
    --icon=assets/icon.ico \
    --add-data "tessdata;tessdata" \
    --hidden-import=pytesseract \
    src/main.py
```

### Distribution

1. **Include Dependencies**:
   - Tesseract installer
   - Poppler (for PDF support)
   - Language data files

2. **Create Installer**:
   - Use NSIS or Inno Setup
   - Include setup wizard
   - Register file associations

3. **Documentation**:
   - User guide
   - Installation instructions
   - Troubleshooting guide

## Resources

- [Tesseract Documentation](https://github.com/tesseract-ocr/tesseract)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)

## Support

For development questions:
- Check this guide
- Review existing code
- Check GitHub issues
- Create new issue if needed
