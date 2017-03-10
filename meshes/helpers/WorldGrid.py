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


class WorldGrid():
    def __init__(self):
        self.shader_program = None
        self.gl_mvp_matrix = -1
        self.gl_a_alpha = -1
        self.gl_a_actAsMirror = -1

        self.positionX = ObjectCoordinate(animate=False, point=0.0)
        self.positionY = ObjectCoordinate(animate=False, point=0.0)
        self.positionZ = ObjectCoordinate(animate=False, point=0.0)

        self.rotateX = ObjectCoordinate(animate=False, point=0.0)
        self.rotateY = ObjectCoordinate(animate=False, point=0.0)
        self.rotateZ = ObjectCoordinate(animate=False, point=0.0)

        self.scaleX = ObjectCoordinate(animate=False, point=1.0)
        self.scaleY = ObjectCoordinate(animate=False, point=1.0)
        self.scaleZ = ObjectCoordinate(animate=False, point=1.0)

        self.act_as_mirror = False
        self.showGrid = True
        self.transparency = 0.5

        self.matrixModel = Matrix4x4(1.)

        self.mirror_translateX = 0.0
        self.mirror_translateY = 5.0
        self.mirror_translateZ = -5.0
        self.mirror_rotateX = 90.0
        self.mirror_rotateY = 0.0
        self.mirror_rotateZ = 0.0

    def init_properties(self):
        self.positionX = ObjectCoordinate(animate=False, point=0.0)
        self.positionY = ObjectCoordinate(animate=False, point=0.0)
        self.positionZ = ObjectCoordinate(animate=False, point=0.0)

        self.rotateX = ObjectCoordinate(animate=False, point=0.0)
        self.rotateY = ObjectCoordinate(animate=False, point=0.0)
        self.rotateZ = ObjectCoordinate(animate=False, point=0.0)

        self.scaleX = ObjectCoordinate(animate=False, point=1.0)
        self.scaleY = ObjectCoordinate(animate=False, point=1.0)
        self.scaleZ = ObjectCoordinate(animate=False, point=1.0)

        self.act_as_mirror = False
        self.showGrid = True
        self.transparency = 0.5

        self.matrixModel = Matrix4x4(1.)

    def init_shader_program(self):
        file_vs = open('resources/shaders/grid.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/grid.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shader_program = glCreateProgram()
        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.do_log("[WorldGrid] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[WorldGrid] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.gl_mvp_matrix = GLUtils.glGetUniform(self.shader_program, "u_MVPMatrix")
        self.gl_a_alpha = GLUtils.glGetUniform(self.shader_program, "a_alpha")
        self.gl_a_actAsMirror = GLUtils.glGetUniform(self.shader_program, "a_actAsMirror")

        return True

    def init_buffers(self, grid_size, unit_size):
        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        vboVertices = -1
        vboColors = -1
        vboIndices = -1

        if not self.act_as_mirror:
            self.grid_size = grid_size
            self.grid_size_vertex = self.grid_size

            if self.grid_size_vertex % 2 == 0:
                self.grid_size_vertex += 1

            grid_minus = floor(self.grid_size_vertex / 2)
            vertices = []
            colors = []
            indices = []
            h = False
            for i in range(self.grid_size_vertex * 2):
                for j in range(self.grid_size_vertex):
                    h = True
                    if i > self.grid_size_vertex - 1:
                        h = False
                    if h:
                        p = Vector3(.0)
                        p.x = (j - grid_minus) * unit_size
                        p.y = .0
                        p.z = (i - grid_minus) * unit_size
                        vertices.append(p)
                        if p.z < 0 or p.z > 0:
                            colors.append(0.7)
                            colors.append(0.7)
                            colors.append(0.7)
                        else:
                            colors.append(1.)
                            colors.append(.0)
                            colors.append(.0)
                    else:
                        p = Vector3(.0)
                        p.x = (i - self.grid_size_vertex - grid_minus) * unit_size
                        p.y = .0
                        p.z = (j - grid_minus) * unit_size
                        vertices.append(p)
                        if p.x < 0 or p.x > 0:
                            colors.append(0.7)
                            colors.append(0.7)
                            colors.append(0.7)
                        else:
                            colors.append(.0)
                            colors.append(.0)
                            colors.append(1.)
            self.z_index = len(vertices)

            p_z_Minus_Down = Vector3()
            p_z_Minus_Down.x = .0
            p_z_Minus_Down.y = -1 * grid_minus
            p_z_Minus_Down.z = .0
            vertices.append(p_z_Minus_Down)
            colors.append(.0)
            colors.append(1.)
            colors.append(.0)

            p_z_Plus_Up = Vector3()
            p_z_Plus_Up.x = .0
            p_z_Plus_Up.y = grid_minus
            p_z_Plus_Up.z = .0
            vertices.append(p_z_Plus_Up)
            colors.append(.0)
            colors.append(1.)
            colors.append(.0)

            # vertices
            data_vertices = numpy.array(vertices, dtype=numpy.float32)
            vboVertices = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboVertices)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            # colors
            data_colors = numpy.array(colors, dtype=numpy.float32)
            vboColors = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboColors)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_colors), data_colors, GL_STATIC_DRAW)
            glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(1)

            # indices
            indices = numpy.array(indices, dtype=numpy.uint32)
            vboIndices = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboIndices)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(indices), indices, GL_STATIC_DRAW)

        else:
            pass

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(3, [vboVertices, vboColors, vboIndices])

    def render(self, matrixProjection, matrixCamera, showZAxis):
        if self.glVAO > 0 and self.showGrid:
            glUseProgram(self.shader_program)

            self.matrixModel = Matrix4x4(1.0)
            self.matrixModel = MathOps.matrix_scale(self.matrixModel, Vector3(self.scaleX.point, self.scaleY.point, self.scaleZ.point))

            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateX.point, Vector3(1, 0, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateY.point, Vector3(0, 1, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateZ.point, Vector3(0, 0, 1))
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))

            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(self.positionX.point, self.positionY.point, self.positionZ.point, .0))

            mvpModel =  matrixProjection * matrixCamera * self.matrixModel
            glUniformMatrix4fv(self.gl_mvp_matrix, 1, GL_FALSE, MathOps.matrix_to_gl(mvpModel))

            glBindVertexArray(self.glVAO)

            if not self.act_as_mirror:
                glUniform1f(self.gl_a_alpha, 1.0)
                glUniform1f(self.gl_a_actAsMirror, 0)
                for i in range(self.grid_size_vertex * 2):
                    glDrawArrays(GL_LINE_STRIP, self.grid_size_vertex * i, self.grid_size_vertex)
                for i in range(self.grid_size_vertex):
                    glDrawArrays(GL_LINE_STRIP, 0, self.grid_size_vertex)
                if showZAxis:
                    glDrawArrays(GL_LINES, self.z_index, 2)

            glBindVertexArray(0)

            glUseProgram(0)
