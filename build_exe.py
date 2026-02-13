"""Build script for creating standalone executable using PyInstaller."""

import os
import sys
import subprocess
import shutil


def build_exe():
    """Build standalone executable for the OCR application."""
    
    print("Building Arabic-French OCR Tool executable...")
    
    # Base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, 'src')
    assets_dir = os.path.join(base_dir, 'assets')
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',  # Single file executable
        '--windowed',  # No console window
        '--name=ArabicFrenchOCR',
        os.path.join(src_dir, 'main.py')
    ]
    
    # Add icon if it exists
    icon_path = os.path.join(assets_dir, 'icon.ico')
    if os.path.exists(icon_path):
        cmd.extend(['--icon', icon_path])
    
    # Add tessdata if it exists
    tessdata_path = os.path.join(base_dir, 'tessdata')
    if os.path.exists(tessdata_path):
        cmd.extend(['--add-data', f'{tessdata_path}{os.pathsep}tessdata'])
    
    # Additional hidden imports
    cmd.extend([
        '--hidden-import', 'pytesseract',
        '--hidden-import', 'PIL',
        '--hidden-import', 'cv2',
        '--hidden-import', 'pdf2image',
        '--hidden-import', 'docx',
        '--collect-all', 'pytesseract'
    ])
    
    # Run PyInstaller
    try:
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        print("\n" + "="*60)
        print("Build completed successfully!")
        print("="*60)
        print(f"\nExecutable location: {os.path.join(base_dir, 'dist', 'ArabicFrenchOCR.exe')}")
        print("\nNOTE: Make sure Tesseract OCR is installed on the target system")
        print("or bundle it with the executable.")
        print("\nLanguage data files (ara.traineddata, fra.traineddata) must be")
        print("available in the Tesseract tessdata directory on the target system.")
        
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    build_exe()
