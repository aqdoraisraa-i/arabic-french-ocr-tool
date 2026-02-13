# Quick Start Guide

Get started with the Arabic-French OCR Tool in 5 minutes!

## Prerequisites

Before you begin, make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ Tesseract OCR installed
- ✅ 5 minutes of your time

## Step 1: Install Tesseract OCR (5 minutes)

### Windows
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. **IMPORTANT**: During installation, select:
   - ✅ Arabic language data
   - ✅ French language data
4. Add Tesseract to PATH (usually automatic)

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-ara tesseract-ocr-fra
```

### macOS
```bash
brew install tesseract tesseract-lang
```

## Step 2: Install the Application (2 minutes)

### Option A: Using Pre-built Executable (Windows Only)
1. Download `ArabicFrenchOCR.exe` from the Releases page
2. Double-click to run
3. Done! ✨

### Option B: From Source
```bash
# Clone the repository
git clone https://github.com/aqdoraisraa-i/arabic-french-ocr-tool.git
cd arabic-french-ocr-tool

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run the Application (30 seconds)

### If using executable:
```bash
# Just double-click ArabicFrenchOCR.exe
```

### If running from source:
```bash
python src/main.py
```

## Step 4: Extract Your First Text (1 minute)

1. **Launch the application** - You should see a window with "Arabic-French OCR Tool" at the top

2. **Add a file** - Either:
   - Click "Select Files" button
   - OR drag and drop a file onto the window

3. **Choose language**:
   - Select "Arabic" for Arabic text
   - Select "French" for French text
   - Select "Both" for mixed content

4. **Click "Process OCR"** - Wait a few seconds

5. **View results** - The extracted text appears in the output area

6. **Export** (optional):
   - Click "Copy to Clipboard" to paste elsewhere
   - Click "Export as TXT" for a text file
   - Click "Export as DOCX" for a Word document

## That's it! 🎉

You're now ready to extract text from Arabic and French documents!

## Quick Tips

### For Best Results:
- ✅ Use clear, well-lit images
- ✅ Keep "Enable Preprocessing" checked (it's on by default)
- ✅ Use 300 DPI or higher for scanned documents
- ✅ Make sure images are straight (not rotated)

### Supported Files:
- 📷 Images: JPG, PNG, BMP, TIFF
- 📄 Documents: PDF (single and multi-page)

### Processing Multiple Files:
1. Select multiple files (hold Ctrl while clicking)
2. Click "Process OCR"
3. Results for all files will be combined

## Need Help?

### Common Issues:

**"Tesseract not found" error?**
- Make sure Tesseract is installed
- Check it's in your system PATH
- Try restarting the application

**"Missing language data" warning?**
- Reinstall Tesseract with Arabic/French language packs
- Or download language files manually from: https://github.com/tesseract-ocr/tessdata

**Poor text accuracy?**
- Enable preprocessing (checkbox should be checked)
- Use higher quality images
- Make sure image is straight
- Verify correct language is selected

**Can't process PDF files?**
- Windows: Download poppler from https://github.com/oschwartz10612/poppler-windows/releases
- Linux: `sudo apt install poppler-utils`
- macOS: `brew install poppler`

### Still stuck?
- Check the full [README.md](README.md)
- Look at [EXAMPLES.md](EXAMPLES.md) for more detailed usage
- Check [Troubleshooting](README.md#troubleshooting) section
- Open an issue on GitHub

## Next Steps

Want to do more? Check out:
- [EXAMPLES.md](EXAMPLES.md) - More usage examples and code samples
- [README.md](README.md) - Full documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Help improve the project

---

**Happy OCR-ing! 🚀**
