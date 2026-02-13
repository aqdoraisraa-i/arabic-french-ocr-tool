"""EasyOCR engine for text extraction."""

from PIL import Image
import easyocr
from typing import Optional
import numpy as np


class EasyOCREngine:
    """
    OCR engine using EasyOCR.
    
    Better at handling invoices, special characters, and currency symbols.
    Supports Arabic, French, and multiple languages.
    """
    
    LANGUAGE_CODES = {
        'Arabic': 'ar',
        'French': 'fr',
        'Both': ['ar', 'fr', 'en']  # Include English for currency and numbers
    }
    
    def __init__(self):
        """Initialize EasyOCR engine."""
        import os
        # Set environment for Windows compatibility
        os.environ.setdefault('KMP_DUPLICATE_LIB_OK', 'TRUE')
        os.environ.setdefault('OMP_NUM_THREADS', '1')
        
        # Initialize readers for supported languages
        # First run downloads models (~200MB), subsequent runs use cache
        self.readers = {}
    
    def get_reader(self, languages):
        """Lazy load reader for specific languages."""
        lang_key = frozenset(languages) if isinstance(languages, list) else languages
        
        if lang_key not in self.readers:
            reader_langs = languages if isinstance(languages, list) else [languages]
            # Auto-detect GPU availability
            try:
                import torch
                gpu_available = torch.cuda.is_available()
            except:
                gpu_available = False
            
            self.readers[lang_key] = easyocr.Reader(
                reader_langs,
                gpu=gpu_available  # Automatically use GPU if available
            )
        
        return self.readers[lang_key]
    
    def extract_text(
        self,
        image: Image.Image,
        language: str = 'Both',
        preprocess: bool = True,
        **kwargs
    ) -> str:
        """
        Extract text from image using EasyOCR.
        
        Args:
            image: PIL Image object
            language: Language for OCR ('Arabic', 'French', or 'Both')
            preprocess: Whether to preprocess (not critical for EasyOCR)
            **kwargs: Additional options
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If language is not supported
        """
        if language not in self.LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}. Use 'Arabic', 'French', or 'Both'")
        
        try:
            # Convert PIL Image to numpy array for EasyOCR
            image_array = np.array(image)
            
            # Get the appropriate reader
            languages = self.LANGUAGE_CODES[language]
            reader = self.get_reader(languages)
            
            # Perform OCR
            # detail=1 returns detailed information (bounding boxes, confidence)
            result = reader.readtext(image_array, detail=1)
            
            # Extract text from results
            # Result is list of (bbox, text, confidence)
            text_lines = []
            previous_y = None
            
            if result:
                for detection in result:
                    text = detection[1]
                    confidence = detection[2]
                    
                    # Filter very low confidence detections
                    if confidence > 0.3:  # EasyOCR threshold
                        # Try to detect line breaks based on y-coordinate
                        bbox = detection[0]
                        current_y = bbox[0][1]  # y-coordinate of top-left
                        
                        # If y-coordinate changes significantly, add newline
                        if previous_y is not None and abs(current_y - previous_y) > 15:
                            if text_lines and not text_lines[-1].endswith('\n'):
                                text_lines.append('\n')
                        
                        text_lines.append(text)
                        previous_y = current_y
            
            combined_text = ''.join(text_lines)
            return combined_text.strip()
            
        except Exception as e:
            raise RuntimeError(f"EasyOCR failed: {str(e)}")
