"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

import os, sys
from settings import Settings
from PyQt5.QtWidgets import QApplication
from ui.MainWindow import KuplungMainWindow

if __name__ == '__main__':
    Settings.log_info("Application starting...")
    Settings.ApplicationRootPath = os.path.dirname(os.path.abspath(__file__))

    app = QApplication(sys.argv)
    mainWindow = KuplungMainWindow()

    Settings.log_info("Running...")

    sys.exit(app.exec_())
