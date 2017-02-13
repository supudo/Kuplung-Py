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
from maths.types.Matrix4x4 import Matrix4x4
from maths import MathOps


class AxisSystem():
    def __init__(self):
        self.shader_program = None
        self.gl_mvp_matrix = -1
        self.rotateX = {'animate': False, 'point': 0}
        self.rotateY = {'animate': False, 'point': 0}
        self.rotateZ = {'animate': False, 'point': 0}


    def init_properties(self):
        self.rotateX = {'animate': False, 'point': 0}
        self.rotateY = {'animate': False, 'point': 0}
        self.rotateZ = {'animate': False, 'point': 0}


    def init_shader_program(self):
        file_vs = open('resources/shaders/axis.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/axis.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shader_program = glCreateProgram()
        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.log_error("[AxisSystem] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.log_error("[AxisSystem] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.gl_mvp_matrix = GLUtils.glGetUniform(self.shader_program, "u_MVPMatrix")

        return True


    def init_buffers(self):
        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        vertices = [
            # X
            -100, 0, 0,
            100, 0, 0,
            # Y
            0, -100, 0,
            0, 100, 0,
            # Z
            0, 0, -100,
            0, 0, 100
        ]

        colors = [
            # X - red
            1.0, 0.0, 0.0, 1.0,
            1.0, 0.0, 0.0, 1.0,
            # Y - green
            0.0, 1.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0,
            # Z - blue
            0.0, 0.0, 1.0, 1.0,
            0.0, 0.0, 1.0, 1.0
        ]

        data_vertices = numpy.array(vertices, dtype=numpy.float32)
        vboVertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboVertices)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(0)

        data_colors = numpy.array(colors, dtype=numpy.float32)
        vboColors = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboColors)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_colors), data_colors, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 4, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)


    def render(self, matrixProjection, matrixCamera):
        if self.glVAO > 0:
            glUseProgram(self.shader_program)

            axisW = 120
            axisH = int((Settings.AppMainWindowHeight * axisW) / Settings.AppMainWindowWidth)
            axisX = 10
            axisY = 10

            glViewport(axisX, axisY, axisW, axisH)

            matrixModel = Matrix4x4(1.0)
            matrixModel = matrixModel * matrixProjection * matrixCamera

            glUniformMatrix4fv(self.gl_mvp_matrix, 1, GL_FALSE, MathOps.matrix_to_gl(matrixModel))

            glBindVertexArray(self.glVAO)
            glDrawArrays(GL_LINES, 0, 6)
            glBindVertexArray(0)

            glUseProgram(0)
            glViewport(0, 0, Settings.AppMainWindowWidth, Settings.AppMainWindowHeight)
