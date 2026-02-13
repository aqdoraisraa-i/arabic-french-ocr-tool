"""Simple validation script to check if all modules can be imported."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all modules can be imported."""
    try:
        print("Testing OCR module imports...")
        from ocr.preprocessor import ImagePreprocessor
        print("✓ ImagePreprocessor imported successfully")
        
        print("\nTesting utils module imports...")
        from utils.file_handler import FileHandler
        print("✓ FileHandler imported successfully")
        
        print("\nAll basic imports successful!")
        print("\nNote: OCR engine and GUI require additional dependencies:")
        print("  - pytesseract, PyQt5, Pillow, pdf2image, python-docx, opencv-python, numpy")
        print("  - Install with: pip install -r requirements.txt")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


if __name__ == '__main__':
    success = test_imports()
    sys.exit(0 if success else 1)
