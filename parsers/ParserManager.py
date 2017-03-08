# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

from parsers.OBJ.ParserObj1 import ParserObj1
from parsers.OBJ.ParserObj2 import ParserObj2
from parsers.OBJ.AssimpObj import AssimpObj
from settings import Settings

class ParserManager:

    def __init__(self, parent=None):
        self.ParserMethod = 0
        self.parserObj = None
        Settings.do_log("[ParserManager] Parser Manager initialized.")


    def init_parser(self):
        if Settings.ModelFileParser == Settings.ModelFileParserTypes.ModelFileParser_Own1:
            self.parserObj = ParserObj1()
        elif Settings.ModelFileParser == Settings.ModelFileParserTypes.ModelFileParser_Own2:
            self.parserObj = ParserObj2()
        elif Settings.ModelFileParser == Settings.ModelFileParserTypes.ModelFileParser_Assimp:
            self.parserObj = AssimpObj()


    def parse_file(self, f_folder, f_filename):
        if self.parserObj == None:
            self.init_parser()
        return self.parserObj.parse_file(f_folder, f_filename)
