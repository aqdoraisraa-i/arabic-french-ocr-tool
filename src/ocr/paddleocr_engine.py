
"""PaddleOCR engine for text extraction."""

from PIL import Image
from paddleocr import PaddleOCR
from typing import Optional


class PaddleOCREngine:
    """
    OCR engine using PaddleOCR.
    
    Supports Arabic, French, handwriting, and special characters better than Tesseract.
    """
    
    LANGUAGE_CODES = {
        'Arabic': 'ar',
        'French': 'fr',
        'Both': ['ar', 'fr']  # PaddleOCR can handle multiple languages
    }
    
    def __init__(self):
        """Initialize PaddleOCR engine."""
        import os
        # Set environment for Windows compatibility
        os.environ.setdefault('KMP_DUPLICATE_LIB_OK', 'TRUE')
        
        # Auto-detect GPU availability
        try:
            import paddle
            gpu_available = paddle.device.is_compiled_with_cuda()
        except:
            gpu_available = False
        
        # Initialize with default settings
        # First run downloads models (~200MB), subsequent runs use cache
        try:
            self.ocr = PaddleOCR(use_angle_cls=True, use_gpu=gpu_available, show_log=False)
        except Exception as e:
            # If that fails, try with minimal settings
            try:
                self.ocr = PaddleOCR(use_gpu=False, show_log=False)
            except Exception as e2:
                raise RuntimeError(f"Failed to initialize PaddleOCR: {str(e2)}")
    
    def extract_text(
        self,
        image: Image.Image,
        language: str = 'Both',
        preprocess: bool = True,
        **kwargs
    ) -> str:
        """
        Extract text from image using PaddleOCR.
        
        Args:
            image: PIL Image object
            language: Language for OCR ('Arabic', 'French', or 'Both')
            preprocess: Whether to preprocess (not used with PaddleOCR as it handles it internally)
            **kwargs: Additional options
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If language is not supported
        """
        if language not in self.LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}. Use 'Arabic', 'French', or 'Both'")
        
        try:
            # Convert PIL Image to numpy array for PaddleOCR
            import numpy as np
            image_array = np.array(image)
            
            # Perform OCR
            result = self.ocr.ocr(image_array)
            
            # Extract text from results
            # result is a list of lists, where each inner list contains line results
            # Each line result is a list of boxes and text info
            text_lines = []
            
            if result:
                for line in result:
                    if line:
                        for box_info in line:
                            # box_info is ((x1, y1), (x2, y2), (x3, y3), (x4, y4)), text, confidence
                            text = box_info[1]
                            confidence = box_info[2]
                            
                            # Filter very low confidence detections
                            if confidence > 0.1:
                                text_lines.append(text)
            
            combined_text = '\n'.join(text_lines)
            return combined_text.strip()
            
        except Exception as e:
            raise RuntimeError(f"PaddleOCR failed: {str(e)}")
