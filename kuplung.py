# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

import os
import time
from settings import Settings
from ui.ImGuiWindowSDL2 import ImGuiWindowSDL2

if __name__ == '__main__':
    Settings.log_info("[MAIN] Application starting...")
    Settings.ApplicationRootPath = os.path.dirname(os.path.abspath(__file__))
    Settings.ApplicationStartTime = time.time()
    app = ImGuiWindowSDL2()
    app.show_main_window()
    Settings.log_info("[MAIN] Running...")
