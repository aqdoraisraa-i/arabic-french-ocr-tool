# GPU Setup Guide for High-Performance OCR

## Requirements for GPU-Enabled PC

### Hardware
- NVIDIA GPU (GTX 1050 or better recommended)
- 8GB+ RAM
- 10GB+ free disk space

### Software Prerequisites

1. **NVIDIA CUDA Toolkit** (for GPU acceleration)
   - Download: https://developer.nvidia.com/cuda-downloads
   - Install CUDA 11.8 or 12.x

2. **Microsoft Visual C++ Redistributable**
   - Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
   - Install and restart

## Installation Steps

### 1. Clone/Copy Project
```bash
# Copy the entire project folder to your GPU PC
```

### 2. Create Virtual Environment
```bash
cd arabic-french-ocr-tool
python -m venv venv
venv\Scripts\activate
```

### 3. Install GPU-Enabled PyTorch
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.x
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### 4. Install Other Dependencies
```bash
pip install -r requirements.txt
```

### 5. Verify GPU Detection
```bash
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

Should output:
```
CUDA Available: True
GPU: NVIDIA GeForce GTX/RTX XXXX
```

### 6. Run the Application
```bash
python src\main.py
```

## Performance Comparison

| Engine | CPU (This PC) | GPU PC |
|--------|---------------|---------|
| Tesseract | ⚡ Fast | ⚡ Fast |
| EasyOCR | ❌ DLL Error | 🚀 10-50x Faster |
| PaddleOCR | ❌ DLL Error | 🚀 10-50x Faster |

## Recommended Settings for Invoices

### French Invoices
- **Engine**: EasyOCR or PaddleOCR
- **Language**: French
- **Preprocessing**: ✓ Enabled

### Arabic Invoices
- **Engine**: PaddleOCR (best for Arabic)
- **Language**: Arabic
- **Preprocessing**: ✓ Enabled

### Mixed Language Invoices
- **Engine**: EasyOCR or PaddleOCR
- **Language**: Both
- **Preprocessing**: ✓ Enabled

### Handwritten Text
- **Engine**: PaddleOCR (Advanced)
- **Language**: French or Arabic
- **Preprocessing**: ✓ Enabled

## Troubleshooting

### CUDA Out of Memory
- Close other GPU applications
- Process fewer images at once
- Use CPU fallback (engines auto-detect)

### Models Download Slowly
- First run downloads 200-300MB per engine
- Subsequent runs use cached models
- Be patient on first use

## Notes
- The application automatically detects GPU and uses it if available
- If GPU detection fails, it falls back to CPU mode
- GPU dramatically improves speed but quality is the same
