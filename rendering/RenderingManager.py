# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

from OpenGL.GL import *
from settings import Settings
from gl_utils import GLUtils
from maths.types.Matrix4x4 import Matrix4x4
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from maths import MathOps


class RenderingManager:
    def __init__(self):
        self.faces = []
        self.model_faces = []
        self.shader_program = None
        self.gl_mvp_matrix = -1


    def initShaderProgram(self, openGL_context):
        file_vs = open('resources/shaders/model_face.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/model_face.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shader_program = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.log_error("[RenderingManager] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[RenderingManager] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.gl_mvp_matrix = GLUtils.glGetUniform(self.shader_program, "vs_MVPMatrix")

        return True


    def render(self, matrixProjection, matrixCamera, matrixGrid):
        glUseProgram(self.shader_program)

        for model in self.model_faces:

            matrixModel = Matrix4x4(1.0)
            # grid
            matrixModel *= matrixGrid
            # scale
            matrixModel = MathOps.matrix_scale( matrixModel, (model.scaleX['point'], model.scaleY['point'], model.scaleZ['point']))
            # translate
            matrixModel = MathOps.matrix_translate(matrixModel, (model.positionX['point'], model.positionY['point'], model.positionZ['point']))
            # rotate
            matrixModel = MathOps.matrix_translate(matrixModel, Vector4(.0))
            matrixModel = MathOps.matrix_rotate(matrixModel, model.rotateX['point'], Vector3(1, 0, 0))
            matrixModel = MathOps.matrix_rotate(matrixModel, model.rotateY['point'], Vector3(0, 1, 0))
            matrixModel = MathOps.matrix_rotate(matrixModel, model.rotateZ['point'], Vector3(0, 0, 1))
            matrixModel = MathOps.matrix_translate(matrixModel, Vector4(.0))
            # world
            model.matrixModel = matrixProjection * matrixCamera * matrixModel

            glUniformMatrix4fv(self.gl_mvp_matrix, 1, GL_FALSE, MathOps.matrix_to_gl(model.matrixModel))

            model.render()

        glUseProgram(0)
