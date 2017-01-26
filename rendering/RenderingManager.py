"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

from settings import Settings

class RenderingManager:
    def __init__(self, parent=None):
        self.type = 1
        Settings.logInfo("Rendering Manager initialized...")

    def render(self):
        return 0
