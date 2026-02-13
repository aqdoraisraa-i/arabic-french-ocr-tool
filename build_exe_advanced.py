"""Advanced build script for creating OCR executables with GPU support."""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_tesseract_only():
    """Build lightweight version with Tesseract only (works everywhere)."""
    
    print("\n" + "="*60)
    print("Building TESSERACT-ONLY version (Lightweight, Universal)")
    print("="*60 + "\n")
    
    base_dir = Path(__file__).parent
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=ArabicFrenchOCR-Lite',
        str(base_dir / 'src' / 'main.py'),
        '--hidden-import', 'pytesseract',
        '--hidden-import', 'PIL',
        '--hidden-import', 'pdf2image',
        '--hidden-import', 'docx',
        '--hidden-import', 'cv2',
        '--exclude-module', 'torch',
        '--exclude-module', 'easyocr',
        '--exclude-module', 'paddleocr',
        '--exclude-module', 'paddlepaddle',
    ]
    
    # Add icon if exists
    icon_path = base_dir / 'assets' / 'icon.ico'
    if icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Tesseract-only .exe created successfully!")
        print(f"  Location: dist/ArabicFrenchOCR-Lite.exe")
        print(f"  Size: ~50-100MB")
        print(f"  Works on: Any Windows PC")
        print(f"  Engines: Tesseract only")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        return False
    
    return True


def build_full_version():
    """Build full version with all OCR engines (GPU laptop only)."""
    
    print("\n" + "="*60)
    print("Building FULL version (All Engines, GPU Support)")
    print("="*60 + "\n")
    
    base_dir = Path(__file__).parent
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=ArabicFrenchOCR-Full',
        str(base_dir / 'src' / 'main.py'),
        '--hidden-import', 'pytesseract',
        '--hidden-import', 'PIL',
        '--hidden-import', 'pdf2image',
        '--hidden-import', 'docx',
        '--hidden-import', 'cv2',
        '--hidden-import', 'torch',
        '--hidden-import', 'easyocr',
        '--hidden-import', 'paddleocr',
        '--collect-all', 'torch',
        '--collect-all', 'easyocr',
        '--collect-all', 'paddleocr',
        '--collect-all', 'paddlepaddle',
    ]
    
    # Add icon if exists
    icon_path = base_dir / 'assets' / 'icon.ico'
    if icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Full .exe created successfully!")
        print(f"  Location: dist/ArabicFrenchOCR-Full.exe")
        print(f"  Size: ~1.5-2.5GB")
        print(f"  Works on: GPU PCs (NVIDIA) + any Windows PC")
        print(f"  Engines: Tesseract, EasyOCR, PaddleOCR")
        print(f"  Note: Auto-detects GPU and uses it if available")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        return False
    
    return True


def main():
    """Main build function."""
    
    print("\n╔════════════════════════════════════════════════════════╗")
    print("║   Arabic-French OCR Tool - Executable Builder         ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    print("Choose build option:")
    print("  1. Tesseract-only (Lite) - ~100MB, works everywhere")
    print("  2. Full version - ~2GB, all engines, GPU support")
    print("  3. Both versions")
    print()
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == '1':
        build_tesseract_only()
    elif choice == '2':
        build_full_version()
    elif choice == '3':
        build_tesseract_only()
        print("\n" + "-"*60 + "\n")
        build_full_version()
    else:
        print("Invalid choice!")
        return
    
    print("\n" + "="*60)
    print("BUILD COMPLETE!")
    print("="*60)
    print("\nExecutables are in the 'dist' folder.")
    print("\nDistribution Notes:")
    print("  • Lite version: Distribute to anyone, works on all PCs")
    print("  • Full version: For GPU PCs or users who installed dependencies")
    print("  • Both: Let users choose based on their hardware")


if __name__ == '__main__':
    # Check if pyinstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found!")
        print("Install it with: pip install pyinstaller")
        sys.exit(1)
    
    main()
