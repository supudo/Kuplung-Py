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

        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vs_str)
        glCompileShader(vertex_shader)
        if glGetShaderiv(vertex_shader, GL_COMPILE_STATUS) != GL_TRUE:
            Settings.log_error("[Rendering Manager] Vertex shader compilation failed! " + str(glGetShaderInfoLog(vertex_shader)))
            glDeleteShader(vertex_shader)
        glAttachShader(self.shader_program, vertex_shader)

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fs_str)
        glCompileShader(fragment_shader)
        if glGetShaderiv(fragment_shader, GL_COMPILE_STATUS) != GL_TRUE:
            Settings.log_error("[Rendering Manager] Fragment shader compilation failed! " + str(glGetShaderInfoLog(fragment_shader)))
            glDeleteShader(fragment_shader)
        glAttachShader(self.shader_program, fragment_shader)

        glLinkProgram(self.shader_program)

        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.log_error("[Rendering Manager] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

        self.glVS_MVPMatrix = glGetUniformLocation(self.shader_program, "vs_MVPMatrix")
        if self.glVS_MVPMatrix == -1:
            Settings.log_error("[Rendering Manager] Cannot fetch shader uniform - vs_MVPMatrix")

        Settings.log_info("[Rendering Manager] Shader program initialized...")

    def render(self, openGL_context):
        glUseProgram(self.shader_program)

        # glUniformMatrix4fv(self.glVS_MVPMatrix, 1, GL_FALSE, mvp)

        for model in self.model_faces:
            model.render()

        glUseProgram(0)
