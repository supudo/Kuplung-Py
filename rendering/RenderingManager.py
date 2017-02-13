# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

__author__ = 'supudo'
__version__ = "1.0.0"

import time
from OpenGL.GL import *
import numpy
from math import *
from settings import Settings
from gl_utils import GLUtils


class RenderingManager:
    def __init__(self):
        self.faces = []
        self.model_faces = []
        self.shader_program = None


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
            Settings.log_error("[RenderingManager] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.glVS_MVPMatrix = glGetUniformLocation(self.shader_program, "vs_MVPMatrix")
        if self.glVS_MVPMatrix == -1:
            Settings.log_error("[RenderingManager] Cannot fetch shader uniform - vs_MVPMatrix")

        Settings.log_info("[RenderingManager] Shader program initialized...")

        return True


    def render(self, openGL_context):
        glUseProgram(self.shader_program)

        # glUniformMatrix4fv(self.glVS_MVPMatrix, 1, GL_FALSE, mvp)

        for model in self.model_faces:
            model.render()

        glUseProgram(0)
