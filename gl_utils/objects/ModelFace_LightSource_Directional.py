# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"


class ModelFace_LightSource_Directional:

    def __init__(self):
        self.gl_InUse = -1
        self.gl_Direction = -1
        self.gl_Ambient = -1
        self.gl_Diffuse = -1
        self.gl_Specular = -1
        self.gl_StrengthAmbient = -1
        self.gl_StrengthDiffuse = -1
        self.gl_StrengthSpecular = -1
