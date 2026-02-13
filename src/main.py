"""Main entry point for Arabic-French OCR Tool."""

import sys
import os
from pathlib import Path

# Fix for Windows PyTorch DLL issues
if sys.platform == 'win32':
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    os.environ['OMP_NUM_THREADS'] = '1'
    # Set proper DLL loading
    try:
        import os
        os.add_dll_directory(os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'NVIDIA Corporation', 'NvToolsExt', 'bin', 'x64'))
    except:
        pass

# Add project root to Python path for imports to work
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    """Run the OCR application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
