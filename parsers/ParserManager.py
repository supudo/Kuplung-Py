# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

from parsers.OBJ.ParserObj import ParserObj
from settings import Settings

class ParserManager:

    def __init__(self, parent=None):
        self.ParserMethod = 0
        self.parserObj = ParserObj()
        Settings.logInfo("Parser Manager initialized...")
