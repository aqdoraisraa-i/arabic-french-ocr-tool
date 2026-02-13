# Building Executable Guide

## Overview

You can create **2 types** of executables for your OCR tool:

| Version | Size | Works On | Engines | Speed |
|---------|------|----------|---------|-------|
| **Lite** | ~100MB | Any Windows PC | Tesseract only | Fast enough |
| **Full** | ~2GB | GPU PCs or with dependencies | All 3 engines | Very fast on GPU |

## Prerequisites

1. **On your GPU laptop**, ensure everything works:
   ```bash
   python src\main.py
   # Test all 3 engines successfully
   ```

2. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

## Building the Executable

### Option 1: Build Both Versions (Recommended)

```bash
python build_exe_advanced.py
# Choose option 3 (Both versions)
```

This creates:
- `dist/ArabicFrenchOCR-Lite.exe` (~100MB)
- `dist/ArabicFrenchOCR-Full.exe` (~2GB)

### Option 2: Build Only What You Need

```bash
# Lite only (for distribution)
python build_exe_advanced.py
# Choose option 1

# Full only (for yourself)
python build_exe_advanced.py  
# Choose option 2
```

## Distribution Strategy

### For End Users (Recommended)

**Distribute the LITE version** with these instructions:

```
ArabicFrenchOCR Tool - Installation Instructions

1. Download ArabicFrenchOCR-Lite.exe
2. Install Tesseract OCR:
   - Download: https://github.com/UB-Mannheim/tesseract/wiki
   - Select Arabic and French language packs during installation
3. Double-click ArabicFrenchOCR-Lite.exe to run
4. Select files and choose language (Arabic/French/Both)

System Requirements:
- Windows 10/11
- Tesseract OCR installed
- No GPU required
```

### For Power Users / GPU Users

**Distribute the FULL version** with these instructions:

```
ArabicFrenchOCR Tool - Full Version

Prerequisites:
1. NVIDIA GPU (recommended for best performance)
2. Microsoft Visual C++ Redistributable
   Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
3. NVIDIA CUDA Toolkit (optional, for GPU acceleration)
   Download: https://developer.nvidia.com/cuda-downloads

Running:
- Double-click ArabicFrenchOCR-Full.exe
- Choose engine: Tesseract, EasyOCR, or PaddleOCR
- Automatically uses GPU if available

Note: First run downloads AI models (~300MB), subsequent runs are instant.
```

### For Personal Use Only

If you're the only user:
- Build the **Full version** on your GPU laptop
- Use it yourself with all 3 engines
- Don't distribute (too large and has dependencies)

## Testing the .exe

### Before distributing:

1. **Test on GPU laptop**:
   ```bash
   dist\ArabicFrenchOCR-Full.exe
   # Try all 3 engines
   ```

2. **Test on regular PC** (copy Lite version):
   ```bash
   # Copy ArabicFrenchOCR-Lite.exe to another PC
   # Install Tesseract there
   # Run and test
   ```

## File Sizes Explained

### Lite Version (~100MB)
- Tesseract bindings
- GUI (PyQt5)
- Image processing (OpenCV, Pillow)
- PDF support
- Document export (python-docx)

### Full Version (~2GB)
- Everything in Lite +
- PyTorch (~1.2GB)
- EasyOCR models
- PaddleOCR with dependencies
- GPU support libraries

## Common Issues

### "Missing DLL" error in Full version
**Solution**: User needs to install Visual C++ Redistributable
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Full version is too slow
**Cause**: Running on CPU instead of GPU
**Solution**: 
- Check GPU drivers installed
- Install CUDA toolkit
- Or use Lite version (Tesseract is fast enough for most cases)

### Lite version OCR quality not good enough
**Solution**: 
- Make sure Tesseract is installed with correct language packs
- Enable preprocessing in the app
- Or distribute Full version with dependency instructions

## Recommended Distribution

For most users, I recommend:

1. **Distribute Lite version** publicly
   - Small download
   - Easy setup
   - Works everywhere
   - Good enough for most invoices

2. **Keep Full version** for yourself or provide as "Pro version"
   - For users with GPUs
   - For batch processing
   - For handwritten text

3. **Provide both** and let users choose
   - Advanced users get Full version
   - Regular users get Lite version

## Building on Different Machines

### On GPU Laptop (Best)
- Build both versions
- Test thoroughly
- Full version will work perfectly

### On Current PC (CPU only)
- Can build Lite version only
- Can build Full version but can't test it properly
- Full version will have DLL issues on this PC
- But Full version WILL work on GPU PCs

## Summary

**Yes, you can create .exe on GPU laptop!**

The best approach:
1. Transfer project to GPU laptop
2. Test all engines work perfectly
3. Build BOTH versions using `build_exe_advanced.py`
4. Distribute Lite version to most users
5. Keep Full version for yourself or GPU users

This gives you maximum flexibility and works for everyone!
