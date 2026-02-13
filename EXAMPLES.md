# Installation and Usage Examples

## Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/aqdoraisraa-i/arabic-french-ocr-tool.git
cd arabic-french-ocr-tool

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
python src/main.py
```

## Usage Examples

### Example 1: Extract Arabic Text from Image

1. Launch the application
2. Click "Select Files" and choose an Arabic document image
3. Select "Arabic" from the language dropdown
4. Click "Process OCR"
5. Click "Export as TXT" to save the result

### Example 2: Extract French Text from PDF

1. Launch the application
2. Drag and drop a French PDF document onto the window
3. Select "French" from the language dropdown
4. Ensure "Enable Preprocessing" is checked
5. Click "Process OCR"
6. Click "Export as DOCX" to save as Word document

### Example 3: Batch Processing Multiple Files

1. Launch the application
2. Click "Select Files" and choose multiple documents (hold Ctrl to select multiple)
3. Select "Both" to detect both Arabic and French
4. Click "Process OCR"
5. Wait for all files to be processed
6. Click "Copy to Clipboard" to copy all extracted text

## Code Examples

### Using the OCR Engine Programmatically

```python
from PIL import Image
from src.ocr.engine import OCREngine

# Initialize OCR engine
ocr = OCREngine()

# Load an image
image = Image.open('document.jpg')

# Extract text
text = ocr.extract_text(image, language='Arabic', preprocess=True)
print(text)
```

### Using the Preprocessor

```python
from PIL import Image
from src.ocr.preprocessor import ImagePreprocessor

# Load image
image = Image.open('document.jpg')

# Preprocess
preprocessor = ImagePreprocessor()
processed = preprocessor.preprocess_image(
    image,
    grayscale=True,
    denoise=True,
    enhance=True,
    binarize=True,
    deskew=True
)
```

### Handling Files

```python
from src.utils.file_handler import FileHandler

# Load a single image
images = FileHandler.load_file('document.jpg')

# Load a PDF (returns list of images, one per page)
images = FileHandler.load_file('document.pdf', dpi=300)

# Validate multiple files
valid, invalid = FileHandler.validate_files(['file1.jpg', 'file2.pdf', 'invalid.txt'])
```

### Exporting Results

```python
from src.utils.export import ExportHandler

text = "Extracted text content..."

# Export to text file
ExportHandler.export_to_txt(text, 'output.txt')

# Export to Word document
ExportHandler.export_to_docx(text, 'output.docx')

# Copy to clipboard
ExportHandler.copy_to_clipboard(text)
```

## Building the Executable

### Windows

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Run the build script
python build_exe.py

# The executable will be in the dist/ folder
# dist/ArabicFrenchOCR.exe
```

### Advanced Build Options

```bash
# Build with custom icon
pyinstaller --onefile --windowed \
    --name=ArabicFrenchOCR \
    --icon=assets/icon.ico \
    src/main.py

# Build with tessdata included
pyinstaller --onefile --windowed \
    --name=ArabicFrenchOCR \
    --add-data "tessdata;tessdata" \
    src/main.py
```

## Common Use Cases

### Use Case 1: Digitizing Handwritten Notes

Best settings:
- Enable preprocessing: ✓
- Language: Arabic or French (depending on content)
- DPI: 300 or higher
- Image quality: High contrast, good lighting

### Use Case 2: Extracting Text from Scanned Books

Best settings:
- Enable preprocessing: ✓
- Language: Both (if book contains both languages)
- DPI: 300
- File type: PDF (multi-page support)

### Use Case 3: Quick Text Extraction from Screenshots

Best settings:
- Enable preprocessing: May not be needed for digital screenshots
- Language: Based on content
- Export: Copy to clipboard for quick pasting

## Performance Tips

- **For large PDFs**: Process them in batches rather than all at once
- **For better accuracy**: Use 300 DPI or higher when scanning
- **For faster processing**: Disable preprocessing if images are already high quality
- **For mixed content**: Use "Both" language setting only when necessary

## Troubleshooting Common Issues

### Issue: OCR accuracy is low

Solutions:
1. Enable preprocessing
2. Increase image resolution
3. Ensure text is clear and well-lit
4. Try different language settings

### Issue: Application is slow

Solutions:
1. Process fewer files at once
2. Reduce PDF DPI (try 200 instead of 300)
3. Disable preprocessing if not needed
4. Close other applications to free memory

### Issue: Cannot process PDF

Solutions:
1. Install poppler-utils
2. Check PDF is not password-protected
3. Try converting PDF to images first
4. Check PDF file is not corrupted
