# main.py
# This is the main entry point for the application.

import sys
from PyQt6.QtWidgets import QApplication

# Import the MainWindow class from our other file.
from main_window import MainWindow

if __name__ == "__main__":
    # Create the application instance.
    app = QApplication(sys.argv)
    
    # Create and show our main window.
    window = MainWindow()
    window.show()
    
    # Start the application's event loop.
    sys.exit(app.exec())
