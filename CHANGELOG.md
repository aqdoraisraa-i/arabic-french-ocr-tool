# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024

### Added
- Initial release of Arabic-French OCR Tool
- Support for Arabic and French text recognition
- Image preprocessing capabilities (grayscale, noise reduction, contrast enhancement, skew correction, binarization)
- Multi-format support (JPG, PNG, BMP, TIFF, PDF)
- PyQt5-based GUI with drag-and-drop functionality
- Batch processing support for multiple files
- Export options (TXT, DOCX, clipboard)
- Progress indicators for long-running operations
- Comprehensive documentation (README, EXAMPLES, CONTRIBUTING)
- PyInstaller build script for .exe creation
- Language selection (Arabic, French, Both)
- Preprocessing toggle for better performance on high-quality images

### Features
- **OCR Engine**: Powered by Tesseract OCR
- **Image Processing**: OpenCV-based preprocessing pipeline
- **GUI**: Modern, intuitive interface with PyQt5
- **File Handling**: Support for both images and multi-page PDFs
- **Export**: Multiple export formats including Word documents
- **Batch Processing**: Process multiple files in sequence
- **Cross-platform**: Works on Windows, Linux, and macOS

### Documentation
- Installation guide for all platforms
- Usage examples and best practices
- Troubleshooting section
- API documentation with code examples
- Contributing guidelines
- Build instructions for creating executable

### Known Limitations
- Handwritten text recognition may have lower accuracy than printed text
- Requires Tesseract OCR to be installed separately
- PDF processing requires poppler-utils on some platforms
- Large PDFs may take significant time to process

## [Unreleased]

### Planned Features
- Support for additional languages
- Real-time OCR preview
- Cloud OCR API integration option
- Advanced image editing tools in GUI
- OCR confidence visualization
- Batch export options
- Settings persistence
- Recent files history
- Auto-detection of language
- Multi-column text support
- Table extraction capabilities

---

For the complete version history, see the [GitHub releases](https://github.com/aqdoraisraa-i/arabic-french-ocr-tool/releases) page.
