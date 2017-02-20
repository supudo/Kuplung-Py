# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

import os
from settings import Settings
from ui.ImGuiWindowGLFW3 import ImGuiWindowGLFW3
from ui.ImGuiWindowSDL2 import ImGuiWindowSDL2

if __name__ == '__main__':
    Settings.log_info("[MAIN] Application starting...")
    Settings.ApplicationRootPath = os.path.dirname(os.path.abspath(__file__))

    if Settings.ApplicationGLFW3:
        app = ImGuiWindowGLFW3()
    else:
        app = ImGuiWindowSDL2()

    app.show_main_window()

    Settings.log_info("[MAIN] Running...")
