"""Image preprocessing module for OCR optimization."""

import cv2
import numpy as np
from PIL import Image
from typing import Union


class ImagePreprocessor:
    """
    Image preprocessor for OCR optimization.
    
    Provides various image enhancement techniques to improve OCR accuracy.
    """
    
    @staticmethod
    def convert_to_grayscale(image: Union[Image.Image, np.ndarray]) -> np.ndarray:
        """
        Convert image to grayscale.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Grayscale image as numpy array
        """
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image
    
    @staticmethod
    def reduce_noise(image: np.ndarray) -> np.ndarray:
        """
        Apply noise reduction using median blur.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Noise-reduced image
        """
        return cv2.medianBlur(image, 3)
    
    @staticmethod
    def enhance_contrast(image: np.ndarray) -> np.ndarray:
        """
        Enhance image contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization).
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Contrast-enhanced image
        """
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(image)
    
    @staticmethod
    def binarize(image: np.ndarray) -> np.ndarray:
        """
        Apply adaptive thresholding for binarization.
        
        Args:
            image: Input grayscale image as numpy array
            
        Returns:
            Binary image
        """
        return cv2.adaptiveThreshold(
            image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    
    @staticmethod
    def deskew(image: np.ndarray) -> np.ndarray:
        """
        Correct image skew.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Deskewed image
        """
        coords = np.column_stack(np.where(image > 0))
        if len(coords) == 0:
            return image
            
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Only rotate if angle is significant
        if abs(angle) < 0.5:
            return image
            
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )
        
        return rotated
    
    @staticmethod
    def preprocess_image(
        image: Union[Image.Image, np.ndarray],
        grayscale: bool = True,
        denoise: bool = True,
        enhance: bool = True,
        binarize: bool = True,
        deskew: bool = True
    ) -> np.ndarray:
        """
        Apply full preprocessing pipeline to image.
        
        Args:
            image: Input image (PIL Image or numpy array)
            grayscale: Convert to grayscale
            denoise: Apply noise reduction
            enhance: Enhance contrast
            binarize: Apply binarization
            deskew: Correct skew
            
        Returns:
            Preprocessed image as numpy array
        """
        # Convert to numpy array if needed
        if isinstance(image, Image.Image):
            processed = np.array(image)
        else:
            processed = image.copy()
        
        # Grayscale conversion
        if grayscale:
            processed = ImagePreprocessor.convert_to_grayscale(processed)
        
        # Noise reduction
        if denoise:
            processed = ImagePreprocessor.reduce_noise(processed)
        
        # Contrast enhancement
        if enhance:
            processed = ImagePreprocessor.enhance_contrast(processed)
        
        # Deskewing
        if deskew:
            processed = ImagePreprocessor.deskew(processed)
        
        # Binarization
        if binarize:
            processed = ImagePreprocessor.binarize(processed)
        
        return processed
