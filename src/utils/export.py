"""Export utilities for saving OCR results."""

import os
from typing import Optional
from docx import Document
from PyQt5.QtWidgets import QApplication


class ExportHandler:
    """
    Handler for exporting OCR results to various formats.
    
    Supports text files, Word documents, and clipboard.
    """
    
    @staticmethod
    def export_to_txt(text: str, file_path: str) -> bool:
        """
        Export text to .txt file.
        
        Args:
            text: Text to export
            file_path: Output file path
            
        Returns:
            True if successful
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Failed to export to TXT: {str(e)}")
            return False
    
    @staticmethod
    def export_to_docx(text: str, file_path: str) -> bool:
        """
        Export text to .docx file.
        
        Args:
            text: Text to export
            file_path: Output file path
            
        Returns:
            True if successful
        """
        try:
            doc = Document()
            
            # Add text with proper paragraph handling
            for line in text.split('\n'):
                doc.add_paragraph(line)
            
            doc.save(file_path)
            return True
        except Exception as e:
            print(f"Failed to export to DOCX: {str(e)}")
            return False
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        Copy text to system clipboard.
        
        Args:
            text: Text to copy
            
        Returns:
            True if successful
        """
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            return True
        except Exception as e:
            print(f"Failed to copy to clipboard: {str(e)}")
            return False
    
    @staticmethod
    def export(text: str, file_path: str, format_type: Optional[str] = None) -> bool:
        """
        Export text to file with automatic format detection.
        
        Args:
            text: Text to export
            file_path: Output file path
            format_type: Format type ('txt' or 'docx'), auto-detected if None
            
        Returns:
            True if successful
        """
        if format_type is None:
            _, ext = os.path.splitext(file_path.lower())
            format_type = ext.lstrip('.')
        
        if format_type == 'txt':
            return ExportHandler.export_to_txt(text, file_path)
        elif format_type in ('docx', 'doc'):
            return ExportHandler.export_to_docx(text, file_path)
        else:
            print(f"Unsupported export format: {format_type}")
            return False
