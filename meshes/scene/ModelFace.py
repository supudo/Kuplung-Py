"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import os
import numpy
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype

from settings import Settings


class ModelFace:
    def __init__(self):
        pass

    def initBuffers(self, openGL_context, model):
        self.mesh_model = model

        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        # vertices
        vertices = numpy.array(model.vertices, dtype=numpy.float32)
        self.vboVertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboVertices)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertices), vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(0)

        # normals
        normals = numpy.array(model.normals, dtype=numpy.float32)
        self.vboNormals = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vboNormals)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(normals), normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(1)

        # textures
        if model.countTextureCoordinates > 0:
            texCoords = numpy.array(model.texture_coordinates, dtype=numpy.float32)
            self.vboTextureCoordinates = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vboTextureCoordinates)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(texCoords), texCoords, GL_STATIC_DRAW)
            glVertexAttribPointer(2, 2, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(2)

        self.vbo_tex_ambient = self.loadTexture(model.ModelMaterial.texture_ambient, 'ambient')
        self.vbo_tex_diffuse = self.loadTexture(model.ModelMaterial.texture_diffuse, 'diffuse')
        self.vbo_tex_normal = self.loadTexture(model.ModelMaterial.texture_normal, 'normal')
        self.vbo_tex_displacement = self.loadTexture(model.ModelMaterial.texture_displacement, 'displacement')
        self.vbo_tex_specular = self.loadTexture(model.ModelMaterial.texture_specular, 'specular')
        self.vbo_tex_specular_exp = self.loadTexture(model.ModelMaterial.texture_specular_exp, 'specular_exp')
        self.vbo_tex_dissolve = self.loadTexture(model.ModelMaterial.texture_dissolve, 'dissolve')

        # indices
        indices = numpy.array(model.indices, dtype=numpy.uint)
        self.vboIndices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vboIndices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        Settings.log_info("[Model Face] Buffers initialized ...")

    def loadTexture(self, texture, type):
        if not texture.image_url == '':
            image_file = Settings.ApplicationAssetsPath + texture.image_url
            if os.path.exists(image_file):
                texture_image = open(image_file)
                t_width = texture_image.size[0]
                t_height = texture_image.size[1]
                vbo_tex = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, vbo_tex)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glGenerateMipmap(GL_TEXTURE_2D)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, t_width,
                             t_height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                             texture_image)
                return vbo_tex
            else:
                Settings.log_error("[ModelFace] - Can't load " + type + " texture image! File doesn't exist!")
                return None
        else:
             return None

    def render(self):
        if Settings.Setting_Wireframe or Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glBindVertexArray(self.glVAO)

        glDrawElements(GL_TRIANGLES, self.mesh_model.countIndices, GL_UNSIGNED_INT, self.mesh_model.indices)

        glBindVertexArray(0)

        if Settings.Setting_Wireframe or Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
