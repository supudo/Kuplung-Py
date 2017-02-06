"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import os
import numpy
from PyQt5.QtGui import (
    QOpenGLBuffer,
    QOpenGLVertexArrayObject,
    QImage,
    QOpenGLTexture
)
from OpenGL import *
from settings import Settings


class ModelFace:
    def __init__(self):
        pass

    def initBuffers(self, openGL_context, model):
        self.mesh_model = model

        # glGenVertexArrays(1, self.glVAO)

        # self.glVAO = QOpenGLVertexArrayObject(openGL_context)
        # self.glVAO.bind()
        #
        # # vertices
        # self.vboVertices = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        # self.vboVertices.create()
        # self.vboVertices.setUsagePattern(QOpenGLBuffer.StaticDraw)
        # self.vboVertices.bind()
        # self.vboVertices.allocate(model.vertices[0] * len(model.vertices))
        # self.vboVertices.write(0, numpy.array(model.vertices, numpy.float32), len(model.vertices))
        #
        # # normals
        # self.vboNormals = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        # self.vboNormals.create()
        # self.vboNormals.setUsagePattern(QOpenGLBuffer.StaticDraw)
        # self.vboNormals.bind()
        # self.vboNormals.allocate(model.normals[0] * len(model.normals))
        # self.vboNormals.write(0, numpy.array(model.normals, numpy.float32), len(model.normals))
        #
        # # textures
        # if model.countTextureCoordinates > 0:
        #     self.vboTextureCoordinates = QOpenGLBuffer(QOpenGLBuffer.VertexBuffer)
        #     self.vboTextureCoordinates.create()
        #     self.vboTextureCoordinates.setUsagePattern(QOpenGLBuffer.StaticDraw)
        #     self.vboTextureCoordinates.bind()
        #     self.vboTextureCoordinates.allocate(model.texture_coordinates[0] * len(model.texture_coordinates))
        #     self.vboTextureCoordinates.write(0, numpy.array(model.texture_coordinates, numpy.float32), len(model.texture_coordinates))
        #
        # self.tex_ambient = self.loadTexture(model.ModelMaterial.texture_ambient, 'ambient')
        # self.tex_diffuse = self.loadTexture(model.ModelMaterial.texture_diffuse, 'diffuse')
        # self.tex_normal = self.loadTexture(model.ModelMaterial.texture_normal, 'normal')
        # self.tex_displacement = self.loadTexture(model.ModelMaterial.texture_displacement, 'displacement')
        # self.tex_specular = self.loadTexture(model.ModelMaterial.texture_specular, 'specular')
        # self.tex_specular_exp = self.loadTexture(model.ModelMaterial.texture_specular_exp, 'specular_exp')
        # self.tex_dissolve = self.loadTexture(model.ModelMaterial.texture_dissolve, 'dissolve')
        #
        # # indices
        # self.vboIndices = QOpenGLBuffer(QOpenGLBuffer.IndexBuffer)
        # self.vboIndices.create()
        # self.vboIndices.setUsagePattern(QOpenGLBuffer.StaticDraw)
        # self.vboIndices.bind()
        # self.vboIndices.allocate(model.indices[0] * len(model.indices))
        # self.vboIndices.write(0, numpy.array(model.indices, numpy.float32), len(model.indices))
        #
        # self.glVAO.release()

        Settings.log_info("[Model Face] Buffers initialized ...")

    def loadTexture(self, texture, type):
        if not texture.image_url == '':
            image_file = Settings.ApplicationAssetsPath + texture.image_url
            if os.path.exists(image_file):
                q_image = QImage(image_file).mirrored()
                return QOpenGLTexture(q_image)
            else:
                Settings.log_error("[ModelFace] - Can't load " + type + " texture image! File doesn't exist!")
                return None
        else:
            return None

    def render(self, openGL_context):
        # self.glVAO.bind()
        # openGL_context.glDrawArrays(openGL_context.GL_TRIANGLE_STRIP, 0, 4)
        # openGL_context.glDrawElements(openGL_context.GL_TRIANGLES, self.mesh_model.countIndices, openGL_context.GL_UNSIGNED_INT, 0);
        # self.glVAO.release()
        pass

