# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import glfw
from settings import Settings
from gl_utils import GLUtils
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype
import numpy
from maths.types.Matrix4x4 import Matrix4x4
from maths import MathOps


class AxisHelpers():
    def __init__(self):
        self.shader_program = None
        self.gl_mvp_matrix = -1
        self.gl_fs_color = -1
        self.mesh_model = None


    def init_properties(self):
        pass


    def set_model(self, mesh_model):
        self.mesh_model = mesh_model


    def init_shader_program(self):
        file_vs = open('resources/shaders/axis_helpers.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/axis_helpers.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shader_program = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.do_log("[AxisHelpers] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[AxisHelpers] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.gl_mvp_matrix = GLUtils.glGetUniform(self.shader_program, "u_MVPMatrix")
        self.gl_fs_color = GLUtils.glGetUniform(self.shader_program, "fs_color")

        return True


    def init_buffers(self):
        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        # vertices
        data_vertices = numpy.array(self.mesh_model.vertices, dtype=numpy.float32)
        vboVertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboVertices)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(0)

        # indices
        data_indices = numpy.array(self.mesh_model.indices, dtype=numpy.uint32)
        vboIndices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboIndices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_indices), data_indices, GL_STATIC_DRAW)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(2, [vboVertices, vboIndices])


    def render(self, matrixProjection, matrixCamera, position):
        if self.glVAO > 0:
            glUseProgram(self.shader_program)

            matrixModel = Matrix4x4(1.0)
            matrixModel = MathOps.matrix_translate(matrixModel, position)
            matrixModel = matrixProjection * matrixCamera * matrixModel

            glUniformMatrix4fv(self.gl_mvp_matrix, 1, GL_FALSE, MathOps.matrix_to_gl(matrixModel))
            glUniform3f(self.gl_fs_color,
                        self.mesh_model.ModelMaterial.color_diffuse[0],
                        self.mesh_model.ModelMaterial.color_diffuse[1],
                        self.mesh_model.ModelMaterial.color_diffuse[2])

            glBindVertexArray(self.glVAO)
            glDrawElements(GL_TRIANGLES, self.mesh_model.countIndices, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)

            glUseProgram(0)