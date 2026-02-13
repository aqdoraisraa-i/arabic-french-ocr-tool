# Arabic-French OCR Tool

A complete desktop application for extracting text from images and PDF documents in Arabic and French languages using Optical Character Recognition (OCR).

## Features

- **Multi-language Support**: Extract text in Arabic, French, or both languages simultaneously
- **Multiple Input Formats**: Support for images (JPG, PNG, BMP, TIFF) and PDF documents
- **Advanced Preprocessing**: Automatic image enhancement for better OCR accuracy
  - Grayscale conversion
  - Noise reduction
  - Contrast enhancement
  - Skew correction
  - Adaptive binarization
- **User-Friendly GUI**: Intuitive interface built with PyQt5
  - Drag-and-drop file upload
  - File browser for selection
  - Real-time progress tracking
  - Batch processing support
- **Export Options**:
  - Export as plain text (.txt)
  - Export as Word document (.docx)
  - Copy to clipboard
- **Standalone Executable**: Can be packaged as a single .exe file for easy distribution

## Screenshots

![Main Interface](docs/screenshot.png) *(Screenshot will be generated)*

## Requirements

### System Requirements
- Windows 10/11 (primary), Linux, or macOS
- Python 3.8 or higher (for development)
- Tesseract OCR 4.0 or higher

### Python Dependencies
See `requirements.txt` for all dependencies:
- pytesseract
- PyQt5
- Pillow
- pdf2image
- python-docx
- opencv-python
- numpy

## Installation

### Option 1: Using Pre-built Executable (Windows)

1. Download the latest release from the Releases page
2. Install Tesseract OCR:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - During installation, make sure to select Arabic and French language data
   - Add Tesseract to your system PATH
3. Run `ArabicFrenchOCR.exe`

### Option 2: Running from Source

#### Step 1: Install Tesseract OCR

**Windows:**
```bash
# Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki

# Add to PATH (typically):
C:\Program Files\Tesseract-OCR
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-ara tesseract-ocr-fra
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

#### Step 2: Install Python Dependencies

```bash
# Clone the repository
git clone https://github.com/aqdoraisraa-i/arabic-french-ocr-tool.git
cd arabic-french-ocr-tool

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# For PDF support on Windows, also install poppler:
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
# Extract and add to PATH
```

#### Step 3: Run the Application

```bash
# From the project root directory
python src/main.py
```

## Building the Executable

To create a standalone .exe file:

```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Run the build script
python build_exe.py
```

The executable will be created in the `dist` folder.

### Manual PyInstaller Command

Alternatively, you can use PyInstaller directly:

```bash
pyinstaller --onefile --windowed --name=ArabicFrenchOCR \
    --icon=assets/icon.ico \
    --hidden-import=pytesseract \
    --hidden-import=PIL \
    --hidden-import=cv2 \
    --hidden-import=pdf2image \
    --hidden-import=docx \
    src/main.py
```

## Usage Guide

### Basic Usage

1. **Launch the Application**
   - Run the executable or `python src/main.py`

2. **Select Files**
   - Click "Select Files" button, or
   - Drag and drop files directly onto the window

3. **Choose Language**
   - Select "Arabic", "French", or "Both" from the dropdown

4. **Enable/Disable Preprocessing**
   - Check "Enable Preprocessing" for better accuracy (recommended)
   - Uncheck if images are already high quality

5. **Process OCR**
   - Click "Process OCR" button
   - Wait for processing to complete

6. **Export Results**
   - Copy to clipboard
   - Export as .txt file
   - Export as .docx (Word) file

### Batch Processing

The application supports processing multiple files at once:
1. Select multiple files using the file browser (Ctrl+Click or Shift+Click)
2. Or drag and drop multiple files
3. Click "Process OCR" to process all files sequentially
4. Results for all files will be combined in the output area

### Tips for Best Results

- **Image Quality**: Higher resolution images (300 DPI or higher) produce better results
- **Text Clarity**: Clear, well-lit images with good contrast work best
- **Preprocessing**: Enable preprocessing for scanned documents or poor quality images
- **Language Selection**: Choose the correct language for best accuracy
  - Use "Both" only if the document contains both Arabic and French text

## Project Structure

```
arabic-french-ocr-tool/
├── src/
│   ├── main.py                 # Application entry point
│   ├── gui/
│   │   ├── __init__.py
│   │   └── main_window.py      # Main GUI window
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── engine.py           # OCR processing logic
│   │   └── preprocessor.py     # Image preprocessing
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py     # File I/O operations
│       └── export.py           # Export functionality
├── assets/
│   └── icon.ico                # Application icon
├── requirements.txt            # Python dependencies
├── build_exe.py                # PyInstaller build script
├── README.md                   # This file
├── LICENSE                     # License information
└── .gitignore                  # Git ignore rules
```

## Troubleshooting

### "Tesseract not found" Error

**Solution:**
- Make sure Tesseract is installed
- Add Tesseract to your system PATH
- On Windows, typical path is `C:\Program Files\Tesseract-OCR`
- Restart the application after adding to PATH

### "Missing language data" Warning

**Solution:**
- Install Arabic language data: `ara.traineddata`
- Install French language data: `fra.traineddata`
- These should be in the Tesseract `tessdata` directory
- On Windows: `C:\Program Files\Tesseract-OCR\tessdata`
- On Linux: `/usr/share/tesseract-ocr/4.00/tessdata`

### PDF Processing Error

**Solution:**
- Install poppler-utils
- Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases
- Linux: `sudo apt install poppler-utils`
- macOS: `brew install poppler`

### Poor OCR Accuracy

**Solutions:**
- Enable preprocessing
- Use higher resolution images (300 DPI recommended)
- Ensure good lighting and contrast in source images
- Try different language settings
- For handwritten text, results may vary - printed text works best

### Application Won't Start

**Solutions:**
- Check Python version (3.8+ required)
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check for error messages in console
- Try running with `python src/main.py` to see detailed errors

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-qt

# Run tests
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Format code using:

```bash
pip install black
black src/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [PyTesseract](https://github.com/madmaze/pytesseract) - Python wrapper for Tesseract
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [Pillow](https://python-pillow.org/) - Image processing library
- [OpenCV](https://opencv.org/) - Computer vision library

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the Troubleshooting section
- Review existing issues for similar problems

## Roadmap

Future enhancements planned:
- [ ] Support for more languages
- [ ] Real-time OCR preview
- [ ] Cloud OCR API integration option
- [ ] Advanced image editing tools
- [ ] OCR confidence visualization
- [ ] Batch export options
- [ ] Settings persistence
- [ ] Recent files history

---

**Version:** 1.0.0  
**Last Updated:** 2024