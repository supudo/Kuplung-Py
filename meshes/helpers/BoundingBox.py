# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from settings import Settings
from gl_utils import GLUtils
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype
import numpy
from math import floor
from maths.types.Matrix4x4 import Matrix4x4
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from maths import MathOps
from gl_utils.GLUtils import ObjectCoordinate


class BoundingBox():
    def __init__(self):
        self.shaderProgram = None
        self.glVAO = -1
        self.glUniformMVPMatrix = -1
        self.glUniformColor = -1
        self.meshModel = None
        self.dataVertices = []
        self.dataIndices = []
        self.min_x = self.max_x = 0.0
        self.min_y = self.max_y = 0.0
        self.min_z = self.max_z = 0.0
        self.size = Vector3(1.0)
        self.center = Vector3(0.0)
        self.matrixTransform = Matrix4x4(1.0)

    def init_shader_program(self):
        file_vs = open('resources/shaders/bounding_box.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/bounding_box.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shaderProgram = glCreateProgram()
        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shaderProgram, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shaderProgram, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.do_log("[BoundingBox] Shader compilation failed!")
            return False

        glLinkProgram(self.shaderProgram)
        if glGetProgramiv(self.shaderProgram, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[BoundingBox] Shader linking failed! " + str(glGetProgramInfoLog(self.shaderProgram)))
            return False

        self.glUniformMVPMatrix = GLUtils.glGetUniform(self.shaderProgram, "u_MVPMatrix")
        self.glUniformColor = GLUtils.glGetUniform(self.shaderProgram, "fs_color")

        return True

    def init_buffers(self, mesh_model):
        self.meshModel = mesh_model
        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        # Cube 1 x1x1, centered on origin

        # vertices
        self.dataVertices = [
            -0.5, -0.5, -0.5, 1.0,
             0.5, -0.5, -0.5, 1.0,
             0.5,  0.5, -0.5, 1.0,
            -0.5,  0.5, -0.5, 1.0,
            -0.5, -0.5,  0.5, 1.0,
             0.5, -0.5,  0.5, 1.0,
             0.5,  0.5,  0.5, 1.0,
            -0.5,  0.5,  0.5, 1.0
        ]
        data_vertices = numpy.array(self.dataVertices, dtype=numpy.float32)
        vboVertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboVertices)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 4, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(0)

        # indices
        self.dataIndices = [
            0, 1, 2, 3,
            4, 5, 6, 7,
            0, 4, 1, 5, 2, 6, 3, 7
        ]
        indices = numpy.array(self.dataIndices, dtype=numpy.uint32)
        vboIndices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboIndices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

        self.min_x = self.max_x = 0.0
        self.min_y = self.max_y = 0.0
        self.min_z = self.max_z = 0.0

        if len(self.meshModel.vertices) > 0:
            self.min_x = self.max_x = self.meshModel.vertices[0].x
            self.min_y = self.max_y = self.meshModel.vertices[0].y
            self.min_z = self.max_z = self.meshModel.vertices[0].z

        for i in range(len(self.meshModel.vertices)):
            if self.meshModel.vertices[i].x < self.min_x:
                self.min_x = self.meshModel.vertices[i].x
            if self.meshModel.vertices[i].x > self.max_x:
                self.max_x = self.meshModel.vertices[i].x
            if self.meshModel.vertices[i].y < self.min_y:
                self.min_y = self.meshModel.vertices[i].y
            if self.meshModel.vertices[i].y > self.max_y:
                self.max_y = self.meshModel.vertices[i].y
            if self.meshModel.vertices[i].z < self.min_z:
                self.min_z = self.meshModel.vertices[i].z
            if self.meshModel.vertices[i].z > self.max_z:
                self.max_z = self.meshModel.vertices[i].z

        padding = Settings.Setting_BoundingBoxPadding
        self.min_x += padding if self.min_x > 0 else -padding
        self.max_x += padding if self.max_x > 0 else -padding
        self.min_y += padding if self.min_y > 0 else -padding
        self.max_y += padding if self.max_y > 0 else -padding
        self.min_z += padding if self.min_z > 0 else -padding
        self.max_z += padding if self.max_z > 0 else -padding

        self.size = Vector3(self.max_x - self.min_x, self.max_y - self.min_y, self.max_z - self.min_z)
        self.center = Vector3((self.min_x + self.max_x) / 2, (self.min_y + self.max_y) / 2, (self.min_z + self.max_z) / 2) * .5
        self.matrixTransform = MathOps.matrix_scale(Matrix4x4(1.0), self.size) * MathOps.matrix_translate(Matrix4x4(1.0), self.center)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(2, [vboVertices, vboIndices])

        Settings.Setting_BoundingBoxRefresh = False

    def render(self, matrixMVP, outlineColor):
        if Settings.Setting_BoundingBoxRefresh:
            self.init_buffers(self.meshModel)
        if self.glVAO > 0:
            glUseProgram(self.shaderProgram)

            mtxModel = matrixMVP * self.matrixTransform
            glUniformMatrix4fv(self.glUniformMVPMatrix, 1, GL_FALSE, MathOps.matrix_to_gl(mtxModel))
            glUniform3f(self.glUniformColor, outlineColor.r, outlineColor.g, outlineColor.b)

            glBindVertexArray(self.glVAO)

            firstIndex = 0
            indexDataSize = 4
            glDrawElements(GL_LINE_LOOP, 4, GL_UNSIGNED_INT, (firstIndex * indexDataSize))
            glDrawElements(GL_LINE_LOOP, 4, GL_UNSIGNED_INT, (4 * indexDataSize))
            glDrawElements(GL_LINES, 8, GL_UNSIGNED_INT, (8 * indexDataSize))

            glBindVertexArray(0)
            glUseProgram(0)
