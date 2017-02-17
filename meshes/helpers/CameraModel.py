# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype
import numpy
from settings import Settings
from gl_utils import GLUtils
from maths.types.Matrix4x4 import Matrix4x4
from maths import MathOps
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4


class CameraModel():
    def __init__(self):
        self.shader_program = None
        self.gl_mvp_matrix = -1
        self.gl_fs_color = -1
        self.gl_fs_innerLightDirection = -1
        self.mesh_model = None

        self.positionX = {'animate': False, 'point': -6.}
        self.positionY = {'animate': False, 'point': -2.}
        self.positionZ = {'animate': False, 'point': 3.}

        self.rotateX = {'animate': False, 'point': .0}
        self.rotateY = {'animate': False, 'point': .0}
        self.rotateZ = {'animate': False, 'point': 300.}

        self.rotateCenterX = {'animate': False, 'point': .0}
        self.rotateCenterY = {'animate': False, 'point': 35.}
        self.rotateCenterZ = {'animate': False, 'point': .0}

        self.innerLightDirectionX = {'animate': False, 'point': 1.}
        self.innerLightDirectionY = {'animate': False, 'point': .055}
        self.innerLightDirectionZ = {'animate': False, 'point': .206}

        self.colorR = {'animate': False, 'point': .61}
        self.colorG = {'animate': False, 'point': .61}
        self.colorB = {'animate': False, 'point': .61}

        self.showCameraObject = True
        self.showInWire = True

        self.matrixModel = Matrix4x4(1.)


    def init_properties(self):

        self.positionX = {'animate': False, 'point': -6.}
        self.positionY = {'animate': False, 'point': -2.}
        self.positionZ = {'animate': False, 'point': 3.}

        self.rotateX = {'animate': False, 'point': .0}
        self.rotateY = {'animate': False, 'point': .0}
        self.rotateZ = {'animate': False, 'point': 300.}

        self.rotateCenterX = {'animate': False, 'point': .0}
        self.rotateCenterY = {'animate': False, 'point': 35.}
        self.rotateCenterZ = {'animate': False, 'point': .0}

        self.innerLightDirectionX = {'animate': False, 'point': 1.}
        self.innerLightDirectionY = {'animate': False, 'point': .055}
        self.innerLightDirectionZ = {'animate': False, 'point': .206}

        self.colorR = {'animate': False, 'point': .61}
        self.colorG = {'animate': False, 'point': .61}
        self.colorB = {'animate': False, 'point': .61}

        self.showCameraObject = True
        self.showInWire = True

        self.matrixModel = Matrix4x4(1.)


    def set_model(self, mesh_model):
        self.mesh_model = mesh_model


    def init_shader_program(self):
        file_vs = open('resources/shaders/camera.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/camera.frag', 'r', encoding='utf-8')
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
        self.gl_fs_innerLightDirection = GLUtils.glGetUniform(self.shader_program, "fs_innerLightDirection")

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

        # normals
        data_normals = numpy.array(self.mesh_model.normals, dtype=numpy.float32)
        vboNormals = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboNormals)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_normals), data_normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(1)

        # indices
        data_indices = numpy.array(self.mesh_model.indices, dtype=numpy.uint32)
        vboIndices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboIndices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_indices), data_indices, GL_STATIC_DRAW)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(3, [vboVertices, vboNormals, vboIndices])


    def render(self, matrixProjection, matrixCamera, matrixGrid, fixedGridWorld):
        if self.glVAO > 0 and self.showCameraObject:
            glUseProgram(self.shader_program)

            self.matrixModel = Matrix4x4(1.0)

            if fixedGridWorld:
                self.matrixModel = matrixGrid

            # rotate
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateX['point'], Vector3(1, 0, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateY['point'], Vector3(0, 1, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateZ['point'], Vector3(0, 0, 1))
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))

            # translate
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, (self.positionX['point'], self.positionY['point'], self.positionZ['point']))

            # rotate center
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateCenterX['point'], Vector3(1, 0, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateCenterY['point'], Vector3(0, 1, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateCenterZ['point'], Vector3(0, 0, 1))

            self.matrixModel = matrixProjection * matrixCamera * self.matrixModel
            glUniformMatrix4fv(self.gl_mvp_matrix, 1, GL_FALSE, MathOps.matrix_to_gl(self.matrixModel))

            glUniform3f(self.gl_fs_color, self.colorR['point'], self.colorG['point'], self.colorB['point'])
            glUniform3f(self.gl_fs_innerLightDirection, self.innerLightDirectionX['point'], self.innerLightDirectionY['point'], self.innerLightDirectionZ['point'])

            glBindVertexArray(self.glVAO)
            glDrawElements(GL_TRIANGLES, self.mesh_model.countIndices, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)

            glUseProgram(0)