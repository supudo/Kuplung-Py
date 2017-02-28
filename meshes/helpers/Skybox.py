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
import os
from PIL import Image
from settings import Settings
from gl_utils import GLUtils
from maths.types.Matrix4x4 import Matrix4x4
from maths import MathOps
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4


class Skybox():
    def __init__(self):
        self.shader_program = -1
        self.glVAO = -1
        self.glVS_MatrixView = -1
        self.glVS_MatrixProjection = -1
        self.vboTexture = -1
        self.gridSize = 0
        self.Setting_Skybox_Item = 0
        self.skyboxItems = [
            ['-- No box --', '', '', '', '', '', ''],
            [
                'Lake Mountain',
                'lake_mountain_right.jpg',
                'lake_mountain_left.jpg',
                'lake_mountain_top.jpg',
                'lake_mountain_bottom.jpg',
                'lake_mountain_back.jpg',
                'lake_mountain_front.jpg'
            ],
            [
                'Fire Planet',
                'fire_planet_right.jpg',
                'fire_planet_left.jpg',
                'fire_planet_top.jpg',
                'fire_planet_bottom.jpg',
                'fire_planet_back.jpg',
                'fire_planet_front.jpg'
            ],
            [
                'Stormy Days',
                'stormydays_right.jpg',
                'stormydays_left.jpg',
                'stormydays_top.jpg',
                'stormydays_bottom.jpg',
                'stormydays_back.jpg',
                'stormydays_front.jpg'
            ]
        ]

    def init_properties(self, gris_size):
        self.gridSize = gris_size
        self.Setting_Skybox_Item = 0

    def init_buffers(self):
        file_vs = open('resources/shaders/skybox.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/skybox.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shader_program = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.do_log("[Skybox] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[Skybox] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.glVS_MatrixView = GLUtils.glGetUniform(self.shader_program, "vs_MatrixView")
        self.glVS_MatrixProjection = GLUtils.glGetUniform(self.shader_program, "vs_MatrixProjection")

        if self.Setting_Skybox_Item > 0:
            self.glVAO = glGenVertexArrays(1)
            glBindVertexArray(self.glVAO)

            skyboxVertices = [
                -1.0, 1.0, -1.0,
                -1.0, -1.0, -1.0,
                1.0, -1.0, -1.0,
                1.0, -1.0, -1.0,
                1.0, 1.0, -1.0,
                -1.0, 1.0, -1.0,

                -1.0, -1.0, 1.0,
                -1.0, -1.0, -1.0,
                -1.0, 1.0, -1.0,
                -1.0, 1.0, -1.0,
                -1.0, 1.0, 1.0,
                -1.0, -1.0, 1.0,

                1.0, -1.0, -1.0,
                1.0, -1.0, 1.0,
                1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,
                1.0, 1.0, -1.0,
                1.0, -1.0, -1.0,

                -1.0, -1.0, 1.0,
                -1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,
                1.0, -1.0, 1.0,
                -1.0, -1.0, 1.0,

                -1.0, 1.0, -1.0,
                1.0, 1.0, -1.0,
                1.0, 1.0, 1.0,
                1.0, 1.0, 1.0,
                -1.0, 1.0, 1.0,
                -1.0, 1.0, -1.0,

                -1.0, -1.0, -1.0,
                -1.0, -1.0, 1.0,
                1.0, -1.0, -1.0,
                1.0, -1.0, -1.0,
                -1.0, -1.0, 1.0,
                1.0, -1.0, 1.0
            ]

            for i in range(len(skyboxVertices)):
                skyboxVertices[i] *= self.gridSize * 10.0

            # vertices
            data_vertices = numpy.array(skyboxVertices, dtype=numpy.float32)
            vboVertices = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboVertices)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            # textures
            self.vboTexture = glGenTextures(1)
            glActiveTexture(GL_TEXTURE0)

            skyboxTextureCubemap = [
                GL_TEXTURE_CUBE_MAP_POSITIVE_X, # Right
                GL_TEXTURE_CUBE_MAP_NEGATIVE_X, # Left
                GL_TEXTURE_CUBE_MAP_POSITIVE_Y, # Top
                GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, # Bottom
                GL_TEXTURE_CUBE_MAP_POSITIVE_Z, # Back
                GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, # Front
            ]

            glBindTexture(GL_TEXTURE_CUBE_MAP, self.vboTexture)
            for i in range(1, len(self.skyboxItems[self.Setting_Skybox_Item])):
                skybox_image = 'resources/skybox/' + self.skyboxItems[self.Setting_Skybox_Item][i]
                if os.path.exists(skybox_image):
                    texture_image = Image.open(skybox_image, 'r')
                    texture_image_data = numpy.array(list(texture_image.getdata()), numpy.uint8)
                    t_width = texture_image.width
                    t_height = texture_image.height
                    glTexImage2D(skyboxTextureCubemap[i - 1], 0, GL_RGB, t_width, t_height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_image_data)
                    texture_image.close()
                else:
                    Settings.do_log("[Skybox] - Can't load texture image! File doesn't exist! (" + skybox_image + ")")

            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
            glBindTexture(GL_TEXTURE_CUBE_MAP, 0)

            glBindVertexArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
            glDeleteBuffers(1, [vboVertices])
        return True

    def render(self, matrixCamera, planeClose, planeFar, fov):
        if self.glVAO > 0:
            glBindVertexArray(self.glVAO)
            glUseProgram(self.shader_program)

            currentDepthFuncMode = -1
            glGetIntegerv(GL_DEPTH_FUNC, currentDepthFuncMode)
            glDepthFunc(GL_LEQUAL)

            glUniformMatrix4fv(self.glVS_MatrixView, 1, GL_FALSE, MathOps.matrix_to_gl(matrixCamera))

            matrixProjection = MathOps.perspective(fov, Settings.AppWindowWidth / Settings.AppWindowHeight, planeClose, planeFar)
            glUniformMatrix4fv(self.glVS_MatrixProjection, 1, GL_FALSE, MathOps.matrix_to_gl(matrixProjection))

            glBindTexture(GL_TEXTURE_CUBE_MAP, self.vboTexture)
            glDrawArrays(GL_TRIANGLES, 0, 36)

            if currentDepthFuncMode > -1:
                glDepthFunc(currentDepthFuncMode)

            glUseProgram(0)
            glBindVertexArray(0)