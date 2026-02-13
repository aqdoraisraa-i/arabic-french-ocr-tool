"""Main window for Arabic-French OCR Tool GUI."""

import os
import sys
from typing import List, Optional
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QComboBox, QFileDialog, QMessageBox,
    QProgressBar, QListWidget, QSplitter, QGroupBox, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMimeData
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QFont
from PIL import Image

from ..ocr.engine import OCREngine
from ..utils.file_handler import FileHandler
from ..utils.export import ExportHandler


class OCRWorker(QThread):
    """Worker thread for OCR processing to keep UI responsive."""
    
    progress = pyqtSignal(int, int)  # current, total
    result = pyqtSignal(str, str)  # text, filename
    error = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, files: List[str], language: str, preprocess: bool):
        super().__init__()
        self.files = files
        self.language = language
        self.preprocess = preprocess
        self.ocr_engine = OCREngine()
    
    def run(self):
        """Run OCR processing on files."""
        try:
            for idx, file_path in enumerate(self.files):
                try:
                    # Load images from file
                    images = FileHandler.load_file(file_path)
                    
                    all_text = []
                    for page_num, image in enumerate(images):
                        # Extract text
                        text = self.ocr_engine.extract_text(
                            image, 
                            self.language,
                            preprocess=self.preprocess
                        )
                        
                        if len(images) > 1:
                            all_text.append(f"--- Page {page_num + 1} ---\n{text}")
                        else:
                            all_text.append(text)
                    
                    combined_text = '\n\n'.join(all_text)
                    self.result.emit(combined_text, os.path.basename(file_path))
                    
                except Exception as e:
                    self.error.emit(f"Error processing {os.path.basename(file_path)}: {str(e)}")
                
                self.progress.emit(idx + 1, len(self.files))
            
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(f"OCR processing failed: {str(e)}")
            self.finished.emit()


class MainWindow(QMainWindow):
    """Main window for OCR application."""
    
    def __init__(self):
        super().__init__()
        self.current_files = []
        self.extracted_text = ""
        self.ocr_worker = None
        
        self.init_ui()
        self.check_tesseract()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Arabic-French OCR Tool")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel("Arabic-French OCR Tool")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Controls section
        controls_layout = QHBoxLayout()
        
        # Language selection
        lang_label = QLabel("Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(['Both', 'Arabic', 'French'])
        controls_layout.addWidget(lang_label)
        controls_layout.addWidget(self.language_combo)
        
        # Preprocessing checkbox
        self.preprocess_checkbox = QCheckBox("Enable Preprocessing")
        self.preprocess_checkbox.setChecked(True)
        controls_layout.addWidget(self.preprocess_checkbox)
        
        controls_layout.addStretch()
        
        # Buttons
        self.select_btn = QPushButton("Select Files")
        self.select_btn.clicked.connect(self.select_files)
        controls_layout.addWidget(self.select_btn)
        
        self.process_btn = QPushButton("Process OCR")
        self.process_btn.clicked.connect(self.process_ocr)
        self.process_btn.setEnabled(False)
        controls_layout.addWidget(self.process_btn)
        
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        controls_layout.addWidget(self.clear_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Splitter for file list and output
        splitter = QSplitter(Qt.Horizontal)
        
        # File list section
        file_group = QGroupBox("Selected Files")
        file_layout = QVBoxLayout()
        
        self.file_list = QListWidget()
        self.file_list.setAcceptDrops(True)
        self.file_list.setDragEnabled(True)
        file_layout.addWidget(self.file_list)
        
        file_btn_layout = QHBoxLayout()
        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self.remove_selected_files)
        file_btn_layout.addWidget(self.remove_btn)
        file_layout.addLayout(file_btn_layout)
        
        file_group.setLayout(file_layout)
        splitter.addWidget(file_group)
        
        # Output section
        output_group = QGroupBox("Extracted Text")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Arial", 10))
        output_layout.addWidget(self.output_text)
        
        # Export buttons
        export_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton("Copy to Clipboard")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        export_layout.addWidget(self.copy_btn)
        
        self.export_txt_btn = QPushButton("Export as TXT")
        self.export_txt_btn.clicked.connect(lambda: self.export_text('txt'))
        export_layout.addWidget(self.export_txt_btn)
        
        self.export_docx_btn = QPushButton("Export as DOCX")
        self.export_docx_btn.clicked.connect(lambda: self.export_text('docx'))
        export_layout.addWidget(self.export_docx_btn)
        
        output_layout.addLayout(export_layout)
        output_group.setLayout(output_layout)
        splitter.addWidget(output_group)
        
        splitter.setSizes([300, 900])
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Enable drag and drop
        self.setAcceptDrops(True)
    
    def check_tesseract(self):
        """Check if Tesseract is available and show warning if not."""
        try:
            ocr_engine = OCREngine()
            available_langs = ocr_engine.get_available_languages()
            
            if not available_langs:
                self.show_warning(
                    "Tesseract OCR not found",
                    "Tesseract OCR is not installed or not in PATH. Please install Tesseract OCR."
                )
            elif 'ara' not in available_langs or 'fra' not in available_langs:
                missing = []
                if 'ara' not in available_langs:
                    missing.append('Arabic')
                if 'fra' not in available_langs:
                    missing.append('French')
                
                self.show_warning(
                    "Missing language data",
                    f"Missing language data for: {', '.join(missing)}. Please install the required Tesseract language data files."
                )
        except Exception as e:
            self.show_warning("OCR Engine Error", f"Error initializing OCR engine: {str(e)}")
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop event."""
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.add_files(files)
    
    def select_files(self):
        """Open file dialog to select files."""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files",
            "",
            "All Supported (*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.pdf);;Images (*.jpg *.jpeg *.png *.bmp *.tiff *.tif);;PDF (*.pdf)"
        )
        
        if files:
            self.add_files(files)
    
    def add_files(self, files: List[str]):
        """Add files to the list."""
        valid_files, invalid_files = FileHandler.validate_files(files)
        
        for file_path in valid_files:
            if file_path not in self.current_files:
                self.current_files.append(file_path)
                self.file_list.addItem(os.path.basename(file_path))
        
        if invalid_files:
            self.show_warning(
                "Invalid Files",
                f"The following files are not supported:\n" + "\n".join([os.path.basename(f) for f in invalid_files])
            )
        
        self.process_btn.setEnabled(len(self.current_files) > 0)
        self.statusBar().showMessage(f"{len(self.current_files)} file(s) selected")
    
    def remove_selected_files(self):
        """Remove selected files from the list."""
        selected_items = self.file_list.selectedItems()
        
        for item in selected_items:
            idx = self.file_list.row(item)
            self.file_list.takeItem(idx)
            if idx < len(self.current_files):
                self.current_files.pop(idx)
        
        self.process_btn.setEnabled(len(self.current_files) > 0)
        self.statusBar().showMessage(f"{len(self.current_files)} file(s) selected")
    
    def process_ocr(self):
        """Process OCR on selected files."""
        if not self.current_files:
            return
        
        language = self.language_combo.currentText()
        preprocess = self.preprocess_checkbox.isChecked()
        
        # Disable buttons during processing
        self.process_btn.setEnabled(False)
        self.select_btn.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(self.current_files))
        self.progress_bar.setValue(0)
        
        # Clear previous output
        self.output_text.clear()
        self.extracted_text = ""
        
        # Create and start worker thread
        self.ocr_worker = OCRWorker(self.current_files, language, preprocess)
        self.ocr_worker.progress.connect(self.update_progress)
        self.ocr_worker.result.connect(self.append_result)
        self.ocr_worker.error.connect(self.show_error)
        self.ocr_worker.finished.connect(self.ocr_finished)
        self.ocr_worker.start()
        
        self.statusBar().showMessage("Processing OCR...")
    
    def update_progress(self, current: int, total: int):
        """Update progress bar."""
        self.progress_bar.setValue(current)
        self.statusBar().showMessage(f"Processing {current}/{total} files...")
    
    def append_result(self, text: str, filename: str):
        """Append OCR result to output."""
        if self.extracted_text:
            self.extracted_text += f"\n\n{'='*50}\n{filename}\n{'='*50}\n\n"
        else:
            self.extracted_text = f"{'='*50}\n{filename}\n{'='*50}\n\n"
        
        self.extracted_text += text
        self.output_text.setPlainText(self.extracted_text)
    
    def ocr_finished(self):
        """Handle OCR completion."""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        self.select_btn.setEnabled(True)
        self.statusBar().showMessage("OCR processing completed")
        
        if self.extracted_text:
            QMessageBox.information(self, "Success", "OCR processing completed successfully!")
    
    def copy_to_clipboard(self):
        """Copy extracted text to clipboard."""
        if not self.extracted_text:
            self.show_warning("No Text", "No text to copy. Please process files first.")
            return
        
        if ExportHandler.copy_to_clipboard(self.extracted_text):
            self.statusBar().showMessage("Text copied to clipboard")
            QMessageBox.information(self, "Success", "Text copied to clipboard!")
    
    def export_text(self, format_type: str):
        """Export extracted text to file."""
        if not self.extracted_text:
            self.show_warning("No Text", "No text to export. Please process files first.")
            return
        
        if format_type == 'txt':
            file_filter = "Text Files (*.txt)"
            default_ext = ".txt"
        else:
            file_filter = "Word Documents (*.docx)"
            default_ext = ".docx"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            f"ocr_output{default_ext}",
            file_filter
        )
        
        if file_path:
            success = ExportHandler.export(self.extracted_text, file_path, format_type)
            
            if success:
                self.statusBar().showMessage(f"Exported to {os.path.basename(file_path)}")
                QMessageBox.information(self, "Success", f"Text exported successfully to {os.path.basename(file_path)}!")
            else:
                self.show_warning("Export Failed", f"Failed to export text to {format_type.upper()} file.")
    
    def clear_all(self):
        """Clear all files and output."""
        self.current_files.clear()
        self.file_list.clear()
        self.output_text.clear()
        self.extracted_text = ""
        self.process_btn.setEnabled(False)
        self.statusBar().showMessage("Cleared")
    
    def show_warning(self, title: str, message: str):
        """Show warning message."""
        QMessageBox.warning(self, title, message)
    
    def show_error(self, message: str):
        """Show error message."""
        QMessageBox.critical(self, "Error", message)
