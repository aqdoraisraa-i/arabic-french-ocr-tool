"""OCR engine module using Tesseract."""

import os
import pytesseract
from PIL import Image
import numpy as np
from typing import Optional, List, Tuple
from .preprocessor import ImagePreprocessor


class OCREngine:
    """
    OCR engine for text extraction from images.
    
    Supports Arabic and French languages using Tesseract OCR.
    """
    
    LANGUAGE_CODES = {
        'Arabic': 'ara',
        'French': 'fra',
        'Both': 'ara+fra'
    }
    
    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize OCR engine.
        
        Args:
            tesseract_cmd: Path to tesseract executable (optional)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        self.preprocessor = ImagePreprocessor()
    
    def extract_text(
        self,
        image: Image.Image,
        language: str = 'Both',
        preprocess: bool = True,
        **preprocess_kwargs
    ) -> str:
        """
        Extract text from image using OCR.
        
        Args:
            image: PIL Image object
            language: Language for OCR ('Arabic', 'French', or 'Both')
            preprocess: Whether to preprocess the image
            **preprocess_kwargs: Additional preprocessing options
            
        Returns:
            Extracted text as string
            
        Raises:
            ValueError: If language is not supported
        """
        if language not in self.LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}. Use 'Arabic', 'French', or 'Both'")
        
        # Preprocess image if enabled
        if preprocess:
            image_array = self.preprocessor.preprocess_image(image, **preprocess_kwargs)
            # Convert back to PIL Image
            processed_image = Image.fromarray(image_array)
        else:
            processed_image = image
        
        # Perform OCR
        lang_code = self.LANGUAGE_CODES[language]
        
        try:
            text = pytesseract.image_to_string(
                processed_image,
                lang=lang_code,
                config='--psm 3'  # Fully automatic page segmentation
            )
            return text.strip()
        except Exception as e:
            raise RuntimeError(f"OCR failed: {str(e)}")
    
    def extract_text_with_confidence(
        self,
        image: Image.Image,
        language: str = 'Both',
        preprocess: bool = True
    ) -> Tuple[str, float]:
        """
        Extract text with confidence score.
        
        Args:
            image: PIL Image object
            language: Language for OCR ('Arabic', 'French', or 'Both')
            preprocess: Whether to preprocess the image
            
        Returns:
            Tuple of (extracted text, average confidence score)
        """
        if language not in self.LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}")
        
        # Preprocess image if enabled
        if preprocess:
            image_array = self.preprocessor.preprocess_image(image)
            processed_image = Image.fromarray(image_array)
        else:
            processed_image = image
        
        # Get detailed OCR data
        lang_code = self.LANGUAGE_CODES[language]
        
        try:
            data = pytesseract.image_to_data(
                processed_image,
                lang=lang_code,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and calculate average confidence
            text_parts = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if conf != -1:  # -1 means no text detected
                    word = data['text'][i]
                    if word.strip():
                        text_parts.append(word)
                        confidences.append(float(conf))
            
            text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return text.strip(), avg_confidence
            
        except Exception as e:
            raise RuntimeError(f"OCR failed: {str(e)}")
    
    def get_available_languages(self) -> List[str]:
        """
        Get list of available Tesseract languages.
        
        Returns:
            List of available language codes
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception:
            return []
    
    def check_language_support(self, language: str) -> bool:
        """
        Check if a language is supported.
        
        Args:
            language: Language name ('Arabic', 'French', or 'Both')
            
        Returns:
            True if language is supported
        """
        available = self.get_available_languages()
        
        if language == 'Both':
            return 'ara' in available and 'fra' in available
        
        lang_code = self.LANGUAGE_CODES.get(language)
        return lang_code in available if lang_code else False
