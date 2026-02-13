"""
Installer builder for Arabic-French OCR Tool
Creates a distributable package with all dependencies
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil


def create_installer_package():
    """Create a complete installer package."""
    
    print("\n" + "="*70)
    print(" Creating Distribution Package for Arabic-French OCR Tool")
    print("="*70 + "\n")
    
    base_dir = Path(__file__).parent
    dist_dir = base_dir / "installer_package"
    
    # Clean previous build
    if dist_dir.exists():
        print("Cleaning previous build...")
        shutil.rmtree(dist_dir)
    
    dist_dir.mkdir()
    
    print("Building executable...")
    
    # Build the full executable
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pytesseract',
        'PIL',
        'pdf2image', 
        'docx',
        'cv2',
        'torch',
        'torchvision',
        'easyocr',
        'paddleocr',
        'paddlepaddle',
        'numpy',
        'scipy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ArabicFrenchOCR',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    spec_file = base_dir / "ArabicFrenchOCR.spec"
    spec_file.write_text(spec_content)
    
    try:
        subprocess.run(['pyinstaller', 'ArabicFrenchOCR.spec', '--clean'], check=True)
        print("✓ Executable built successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False
    
    # Copy executable to installer package
    exe_source = base_dir / "dist" / "ArabicFrenchOCR.exe"
    exe_dest = dist_dir / "ArabicFrenchOCR.exe"
    
    if exe_source.exists():
        shutil.copy2(exe_source, exe_dest)
        print(f"✓ Copied executable to installer package\n")
    else:
        print("✗ Executable not found!")
        return False
    
    # Create README for users
    readme_content = """
Arabic-French OCR Tool - Installation Guide
============================================

Thank you for downloading the Arabic-French OCR Tool!

SYSTEM REQUIREMENTS
-------------------
- Windows 10/11 (64-bit)
- 8GB RAM (16GB recommended for advanced engines)
- 5GB free disk space
- Internet connection (first run only, to download AI models)

INSTALLATION STEPS
------------------

1. INSTALL REQUIRED DEPENDENCIES (IMPORTANT!)
   
   Run these installers in order:
   
   a) Microsoft Visual C++ Redistributable (REQUIRED)
      • Double-click: dependencies/vc_redist.x64.exe
      • Click Install
      • Restart computer if prompted
   
   b) Tesseract OCR (REQUIRED)
      • Double-click: dependencies/tesseract-ocr-setup.exe
      • During installation, make sure to select:
        ☑ Arabic language data
        ☑ French language data
      • Click Install

2. RUN THE APPLICATION
   • Double-click: ArabicFrenchOCR.exe
   • Wait for it to load (first run may take 30 seconds)

3. FIRST RUN - AI MODEL DOWNLOAD
   When you first use EasyOCR or PaddleOCR engines:
   • The app will download AI models (~300MB)
   • This happens ONCE, subsequent runs are instant
   • Please be patient and keep internet connected

USING THE APPLICATION
---------------------

For French Invoices:
- Engine: EasyOCR or PaddleOCR
- Language: French
- Preprocessing: Checked ✓

For Arabic Documents:
- Engine: PaddleOCR (best for Arabic)
- Language: Arabic  
- Preprocessing: Checked ✓

For Mixed Language Documents:
- Engine: EasyOCR or PaddleOCR
- Language: Both
- Preprocessing: Checked ✓

AVAILABLE ENGINES
-----------------

1. Tesseract (Fast)
   - Speed: Very Fast
   - Best for: Clean printed documents
   - Requirements: Tesseract installed

2. EasyOCR (Invoices) ⭐ Recommended for Invoices
   - Speed: Slower (GPU: Fast)
   - Best for: Invoices, tables, currency symbols
   - First use: Downloads models (~200MB)

3. PaddleOCR (Advanced) ⭐ Recommended for Handwriting
   - Speed: Slower (GPU: Fast)
   - Best for: Handwritten text, complex layouts, Arabic
   - First use: Downloads models (~200MB)

GPU SUPPORT (Optional, for faster processing)
----------------------------------------------

If you have an NVIDIA GPU:
1. Install NVIDIA CUDA Toolkit
   Download: https://developer.nvidia.com/cuda-downloads
2. Restart computer
3. The app will automatically use GPU for 10-50x speedup

Without GPU: App works fine on CPU, just slower for EasyOCR/PaddleOCR

TROUBLESHOOTING
---------------

Problem: "Missing DLL" or "WinError 1114" error
Solution: You didn't install Visual C++ Redistributable
         → Install: dependencies/vc_redist.x64.exe
         → Restart computer

Problem: Tesseract engine gives poor results
Solution: Tesseract not installed properly
         → Reinstall: dependencies/tesseract-ocr-setup.exe
         → Make sure to select Arabic and French language packs

Problem: EasyOCR/PaddleOCR very slow
Solution: This is normal on CPU. Options:
         → Use Tesseract for quick results
         → Use on a PC with NVIDIA GPU for speed
         → Be patient (CPU mode works, just slower)

Problem: "Connection error" on first run
Solution: Needs internet to download AI models first time
         → Connect to internet
         → Run again
         → After first download, works offline

SUPPORT
-------

For issues, check the troubleshooting section above.
Most problems are solved by installing the dependencies properly.

Enjoy using the Arabic-French OCR Tool!
"""
    
    readme_file = dist_dir / "README.txt"
    readme_file.write_text(readme_content)
    print("✓ Created README.txt\n")
    
    # Create dependencies folder info
    deps_dir = dist_dir / "dependencies"
    deps_dir.mkdir()
    
    deps_info = """
DEPENDENCIES FOLDER
===================

This folder should contain:

1. vc_redist.x64.exe
   Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
   Size: ~18MB
   Required: YES

2. tesseract-ocr-setup.exe  
   Download from: https://github.com/UB-Mannheim/tesseract/wiki
   Size: ~50-100MB
   Required: YES
   Note: Download version with Arabic and French language packs

HOW TO PREPARE FOR DISTRIBUTION:
---------------------------------

1. Download both files above
2. Place them in this "dependencies" folder
3. Zip the entire "installer_package" folder
4. Distribute the ZIP file to users
5. Users extract and follow README.txt instructions

DISTRIBUTION SIZE:
------------------

- ArabicFrenchOCR.exe: ~1.5-2.5GB (includes all AI engines)
- vc_redist.x64.exe: ~18MB
- tesseract-ocr-setup.exe: ~50-100MB
- Total package: ~2-3GB

This ensures users can install ALL engines and dependencies easily.
"""
    
    deps_readme = deps_dir / "DOWNLOAD_THESE_FILES.txt"
    deps_readme.write_text(deps_info)
    print("✓ Created dependencies folder\n")
    
    # Create quick start batch script
    batch_content = """@echo off
echo ===============================================
echo Arabic-French OCR Tool - Quick Start
echo ===============================================
echo.

REM Check if Visual C++ Redistributable is installed
if not exist "%SystemRoot%\\System32\\vcruntime140.dll" (
    echo [WARNING] Visual C++ Redistributable not detected!
    echo Please install: dependencies\\vc_redist.x64.exe
    echo.
    pause
)

echo Starting Arabic-French OCR Tool...
echo.
echo First run note:
echo - EasyOCR and PaddleOCR will download models on first use
echo - This requires internet connection
echo - Downloads are cached, subsequent runs are offline
echo.

start "" "ArabicFrenchOCR.exe"
"""
    
    batch_file = dist_dir / "Start_OCR_Tool.bat"
    batch_file.write_text(batch_content)
    print("✓ Created quick start script\n")
    
    print("="*70)
    print(" DISTRIBUTION PACKAGE CREATED SUCCESSFULLY!")
    print("="*70)
    print(f"\nLocation: {dist_dir}")
    print("\nNext steps:")
    print("1. Download dependencies into the 'dependencies' folder:")
    print("   - vc_redist.x64.exe")
    print("   - tesseract-ocr-setup.exe")
    print("2. Zip the entire 'installer_package' folder")
    print("3. Distribute to users")
    print("\nUsers will extract and follow README.txt")
    print("\n" + "="*70 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found!")
        print("Install: pip install pyinstaller")
        sys.exit(1)
    
    create_installer_package()
