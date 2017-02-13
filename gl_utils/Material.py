# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"


class MaterialTextureImage:

    def __init__(self):
        self.image_url = ''

class Material:

    def __init__(self):
        self.material_title = ''
        self.color_ambient = []
        self.color_diffuse = []
        self.color_specular = []
        self.color_emission = []
        self.specular_exp = 0
        self.transparency1 = 0
        self.transparency2 = 0
        self.optical_density = 0
        self.illumination_mode = 0
        self.texture_ambient = MaterialTextureImage()
        self.texture_diffuse = MaterialTextureImage()
        self.texture_normal = MaterialTextureImage()
        self.texture_displacement = MaterialTextureImage()
        self.texture_specular = MaterialTextureImage()
        self.texture_specular_exp = MaterialTextureImage()
        self.texture_dissolve = MaterialTextureImage()

