"""File handling utilities for OCR application."""

import os
from typing import List, Optional
from PIL import Image
from pdf2image import convert_from_path
import tempfile


class FileHandler:
    """
    File handler for loading and validating input files.
    
    Supports images (JPG, PNG, BMP, TIFF) and PDF documents.
    """
    
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    SUPPORTED_FORMATS = SUPPORTED_IMAGE_FORMATS | {'.pdf'}
    
    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        """
        Check if file format is supported.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file format is supported
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext in FileHandler.SUPPORTED_FORMATS
    
    @staticmethod
    def is_image_file(file_path: str) -> bool:
        """
        Check if file is an image.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is an image
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext in FileHandler.SUPPORTED_IMAGE_FORMATS
    
    @staticmethod
    def is_pdf_file(file_path: str) -> bool:
        """
        Check if file is a PDF.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file is a PDF
        """
        _, ext = os.path.splitext(file_path.lower())
        return ext == '.pdf'
    
    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """
        Load image from file.
        
        Args:
            file_path: Path to image file
            
        Returns:
            PIL Image object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not FileHandler.is_image_file(file_path):
            raise ValueError(f"Unsupported image format: {file_path}")
        
        try:
            image = Image.open(file_path)
            # Convert to RGB if necessary
            if image.mode not in ('RGB', 'L'):
                image = image.convert('RGB')
            return image
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")
    
    @staticmethod
    def load_pdf(file_path: str, dpi: int = 300) -> List[Image.Image]:
        """
        Load PDF and convert to images.
        
        Args:
            file_path: Path to PDF file
            dpi: DPI for conversion (higher = better quality)
            
        Returns:
            List of PIL Image objects (one per page)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a PDF or conversion fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not FileHandler.is_pdf_file(file_path):
            raise ValueError(f"Not a PDF file: {file_path}")
        
        try:
            images = convert_from_path(file_path, dpi=dpi)
            return images
        except Exception as e:
            raise ValueError(f"Failed to load PDF: {str(e)}")
    
    @staticmethod
    def load_file(file_path: str, dpi: int = 300) -> List[Image.Image]:
        """
        Load file (image or PDF) and return as list of images.
        
        Args:
            file_path: Path to file
            dpi: DPI for PDF conversion
            
        Returns:
            List of PIL Image objects
        """
        if FileHandler.is_pdf_file(file_path):
            return FileHandler.load_pdf(file_path, dpi)
        elif FileHandler.is_image_file(file_path):
            return [FileHandler.load_image(file_path)]
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    
    @staticmethod
    def validate_files(file_paths: List[str]) -> tuple[List[str], List[str]]:
        """
        Validate list of file paths.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Tuple of (valid_files, invalid_files)
        """
        valid = []
        invalid = []
        
        for file_path in file_paths:
            if os.path.exists(file_path) and FileHandler.is_supported_file(file_path):
                valid.append(file_path)
            else:
                invalid.append(file_path)
        
        return valid, invalid
