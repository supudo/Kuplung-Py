# -*- coding: utf-8 -*-

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
from ui.ImGuiWindow import ImGuiWindow

if __name__ == '__main__':
    Settings.log_info("[MAIN] Application starting...")
    Settings.ApplicationRootPath = os.path.dirname(os.path.abspath(__file__))

    # app = QApplication(sys.argv)
    # mainWindow = KuplungMainWindow()
    # sys.exit(app.exec_())

    app = ImGuiWindow()
    app.show_main_window()

    Settings.log_info("[MAIN] Running...")
