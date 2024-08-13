# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from maths.types.Vector3 import Vector3

class MaterialColor:
    def __init__(self, *args):
        self.colorPickerOpen = False
        self.animate = False
        self.strength = 1.0
        self.color = Vector3(.0)
        if len(args) == 4:
            self.colorPickerOpen = bool(args[0])
            self.animate = bool(args[1])
            self.strength = float(args[2])
            if (len(args[3]) == 3):
                self.color = Vector3(args[3][0], args[3][1], args[3][2])
