# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

import numpy
import imgui
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype
from PIL import Image
from settings import Settings
from gl_utils import GLUtils


__author__ = 'supudo'
__version__ = "1.0.0"

class StructuredVolumetricSampling():

    def __init__(self):
        self.shader_program = None

        self.glAttributeVertexPosition = -1
        self.glVS_screenResolution = -1
        self.glFS_deltaRunningTime = -1
        self.glFS_noiseTextureSampler = -1
        self.glFS_screenResolution = -1
        self.glFS_mouseCoordinates = -1
        self.vboTextureNoise = -1

    def initShaderProgram(self):
        file_vs = open('resources/shaders/structured_vol_sampling.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/structured_vol_sampling.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shader_program = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.do_log("[SVS] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[SVS] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.glAttributeVertexPosition = GLUtils.glGetAttribute(self.shader_program, "a_vertexPosition")
        self.glVS_screenResolution = GLUtils.glGetUniform(self.shader_program, "vs_screenResolution")
        self.glFS_deltaRunningTime = GLUtils.glGetUniform(self.shader_program, "fs_deltaRunningTime")
        self.glFS_noiseTextureSampler = GLUtils.glGetUniform(self.shader_program, "fs_noiseTextureSampler")
        self.glFS_screenResolution = GLUtils.glGetUniform(self.shader_program, "fs_screenResolution")
        self.glFS_mouseCoordinates = GLUtils.glGetUniform(self.shader_program, "fs_mouseCoordinates")

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glDisable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        return True

    def initBuffers(self):
        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        # vertices
        vertices = [
            -1.0, -1.0, 0.0,
             1.0, -1.0, 0.0,
             1.0,  1.0, 0.0,
             1.0,  1.0, 0.0,
            -1.0,  1.0, 0.0,
            -1.0, -1.0, 0.0
        ]
        data_vertices = numpy.array(vertices, dtype=numpy.float32)
        vboVertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboVertices)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(0)

        self.initNoiseTextures()

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(1, [vboVertices])

    def initNoiseTextures(self):
        image_file = 'resources/shadertoy/noise16.png'
        texture_image = Image.open(image_file, 'r')
        texture_image_data = numpy.array(list(texture_image.getdata()), numpy.uint8)
        t_width = texture_image.width
        t_height = texture_image.height
        self.vboTextureNoise = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.vboTextureNoise)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)
        if texture_image.mode == "RGBA":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, t_width, t_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_data)
        elif texture_image.mode == "RGB":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, t_width, t_height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_image_data)
        texture_image.close()

    def render(self, mouse_x, mouse_y, seconds):
        if self.glVAO > 0:
            glUseProgram(self.shader_program)

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.vboTextureNoise)
            glUniform1i(self.glFS_noiseTextureSampler, 0)

            glUniform2f(self.glVS_screenResolution, Settings.AppWindowWidth, Settings.AppWindowHeight)
            glUniform1f(self.glFS_deltaRunningTime, seconds)
            glUniform3f(self.glFS_screenResolution, Settings.AppWindowWidth, Settings.AppWindowHeight, 0.0)
            glUniform4f(self.glFS_mouseCoordinates, float(mouse_x), float(mouse_y), 0.0, 0.0)

            glBindVertexArray(self.glVAO)
            glDrawArrays(GL_TRIANGLES, 0, 6)
            glBindVertexArray(0)

            glUseProgram(0)

    def renderToTexture(self, mouse_x, mouse_y, seconds, vbo):
        self.bindFBO()
        self.render(mouse_x, mouse_y, seconds)
        vbo = self.unbindFBO(vbo)
        return vbo

    def initFBO(self, windowWidth, windowHeight, vboTexture):
        self.textureWidth = windowWidth
        self.textureHeight = windowHeight

        vboTexture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, vboTexture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, windowWidth, windowHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glBindTexture(GL_TEXTURE_2D, 0)

        self.tRBO = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.tRBO)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, int(windowWidth), int(windowHeight))
        glBindRenderbuffer(GL_RENDERBUFFER, 0)

        self.tFBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.tFBO)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, vboTexture, 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.tRBO)

        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
           Settings.do_log("[SVS] - Error creating FBO! - " + str(glCheckFramebufferStatus(GL_FRAMEBUFFER)))

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        return vboTexture

    def bindFBO(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.tFBO)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def unbindFBO(self, vbo):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, vbo)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        return vbo
