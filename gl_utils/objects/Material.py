# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

from enum import Enum


__author__ = 'supudo'
__version__ = "1.0.0"

from maths.types.Vector4 import Vector4


class MaterialTextureType(Enum):
    MaterialTextureType_Undefined = 0
    MaterialTextureType_Ambient = 1
    MaterialTextureType_Diffuse = 2
    MaterialTextureType_Dissolve = 3
    MaterialTextureType_Bump = 4
    MaterialTextureType_Specular = 5
    MaterialTextureType_SpecularExp = 6
    MaterialTextureType_Displacement = 7

class MaterialTextureImage:

    def __init__(self):
        self.Image = ''
        self.Filename = ''
        self.UseTexture = False
        self.TextureType = MaterialTextureType.MaterialTextureType_Undefined
        self.Height = 0
        self.Width = 0
        self.Commands = []

class Material:

    def __init__(self):
        self.material_title = ''

        self.color_ambient = Vector4(.0)
        self.color_diffuse = Vector4(.0)
        self.color_specular = Vector4(.0)
        self.color_emission = Vector4(.0)

        self.specular_exp = 0
        self.transparency = 0
        self.optical_density = 0
        self.illumination_mode = 0

        self.texture_ambient = MaterialTextureImage()
        self.texture_diffuse = MaterialTextureImage()
        self.texture_normal = MaterialTextureImage()
        self.texture_displacement = MaterialTextureImage()
        self.texture_specular = MaterialTextureImage()
        self.texture_specular_exp = MaterialTextureImage()
        self.texture_dissolve = MaterialTextureImage()

