# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"


class MeshModel:

    def __init__(self):
        self.ID = -1

        self.file = ''
        self.ModelTitle = ''
        self.MaterialTitle = ''

        self.countVertices = 0
        self.countTextureCoordinates = 0
        self.countNormals = 0
        self.countIndices = 0

        self.ModelMaterial  = None
        self.vertices = []
        self.texture_coordinates = []
        self.normals = []
        self.indices = []
