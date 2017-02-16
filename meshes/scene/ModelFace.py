# -*- coding: utf-8 -*-

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
from PIL import Image
from settings import Settings
from maths.types.Matrix4x4 import Matrix4x4


class ModelFace:
    def __init__(self):
        self.positionX = {'animate': False, 'point': .0}
        self.positionY = {'animate': False, 'point': .0}
        self.positionZ = {'animate': False, 'point': .0}

        self.rotateX = {'animate': False, 'point': .0}
        self.rotateY = {'animate': False, 'point': .0}
        self.rotateZ = {'animate': False, 'point': .0}

        self.scaleX = {'animate': False, 'point': 1.}
        self.scaleY = {'animate': False, 'point': 1.}
        self.scaleZ = {'animate': False, 'point': 1.}

        self.displaceX = {'animate': False, 'point': 1.}
        self.displaceY = {'animate': False, 'point': 1.}
        self.displaceZ = {'animate': False, 'point': 1.}

        self.matrixModel = Matrix4x4(1.)

    def initBuffers(self, model):
        self.mesh_model = model

        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        vboTextureCoordinates = -1

        # vertices
        data_vertices = numpy.array(model.vertices, dtype=numpy.float32)
        vboVertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboVertices)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(0)

        # normals
        data_normals = numpy.array(model.normals, dtype=numpy.float32)
        vboNormals = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboNormals)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_normals), data_normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(1)

        # textures
        if model.countTextureCoordinates > 0:
            data_texCoords = numpy.array(model.texture_coordinates, dtype=numpy.float32)
            vboTextureCoordinates = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboTextureCoordinates)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_texCoords), data_texCoords, GL_STATIC_DRAW)
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
        data_indices = numpy.array(model.indices, dtype=numpy.uint32)
        vboIndices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboIndices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_indices), data_indices, GL_STATIC_DRAW)

        # print('Vertices:')
        # pstr = ''
        # for v in data_vertices:
        #     pstr += str(v[0]) + ', ' + str(v[1]) + ', ' + str(v[2]) + ', '
        # print(pstr)
        #
        # print('Indices:')
        # pstr = ''
        # for v in data_indices:
        #     pstr += str(v) + ', '
        # print(pstr)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(4, [vboVertices, vboNormals, vboTextureCoordinates, vboIndices])

    def loadTexture(self, texture, type):
        if texture is not None:
            if not texture.image_url == '':
                image_file = Settings.ApplicationAssetsPath + texture.image_url
                if os.path.exists(image_file):
                    texture_image = Image.open(image_file, 'r')
                    texture_image_data = numpy.array(list(texture_image.getdata()), numpy.uint8)
                    t_width = texture_image.width
                    t_height = texture_image.height
                    vbo_tex = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, vbo_tex)
                    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                    glGenerateMipmap(GL_TEXTURE_2D)
                    if texture_image.mode == "RGBA":
                        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, t_width, t_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_data)
                    elif texture_image.mode == "RGB":
                        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, t_width, t_height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_image_data)
                    return vbo_tex
                else:
                    Settings.do_log("[ModelFace] - Can't load " + type + " texture image! File doesn't exist!")
        return None

    def render(self):
        if Settings.Setting_Wireframe or Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        glBindVertexArray(self.glVAO)

        glDrawElements(GL_TRIANGLES, self.mesh_model.countIndices, GL_UNSIGNED_INT, None)

        glBindVertexArray(0)

        if Settings.Setting_Wireframe or Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
