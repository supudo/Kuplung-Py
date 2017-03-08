# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

import datetime
import numpy
import os
import imgui
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype
from PIL import Image
from settings import Settings
from gl_utils import GLUtils


__author__ = 'supudo'
__version__ = "1.0.0"

class Shadertoy():

    def __init__(self):
        self.shader_program = None
        self.tFBO = -1
        self.tRBO = -1

        self.iChannel0_Image = ''
        self.iChannel1_Image = ''
        self.iChannel2_Image = ''
        self.iChannel3_Image = ''
        self.iChannel0_CubeImage = ''
        self.iChannel1_CubeImage = ''
        self.iChannel2_CubeImage = ''
        self.iChannel3_CubeImage = ''
        self.textureWidth = 0
        self.textureHeight = 0

        self.iResolution = 0
        self.iGlobalTime = 0
        self.iTimeDelta = 0
        self.iFrame = 0
        self.iFrameRate = 0
        self.iChannelTime = [0, 0, 0, 0]
        self.iChannelResolution = [0, 0, 0, 0]
        self.iChannelResolution0 = [0, 0]
        self.iChannelResolution1 = [0, 0]
        self.iChannelResolution2 = [0, 0]
        self.iChannelResolution3 = [0, 0]
        self.iMouse = 0
        self.iDate = 0
        self.iChannel0 = -1
        self.iChannel1 = -1
        self.iChannel2 = -1
        self.iChannel3 = -1

    def initShaderProgram(self, main_func):
        file_vs = open('resources/shaders/shadertoy.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())

        shaderFragment = """#version 410 core

out vec4 outFragmentColor;
uniform vec3 iResolution;
uniform float iGlobalTime;
uniform float iTimeDelta;
uniform int iFrame;
uniform int iFrameRate;
uniform float iChannelTime[4];
uniform vec3 iChannelResolution[4];
uniform vec4 iMouse;
uniform vec4 iDate;
uniform float iSampleRate;
                         """

        if self.iChannel0_Image != '':
            shaderFragment += "uniform sampler2D iChannel0;"
        elif self.iChannel0_CubeImage != '':
            shaderFragment += "uniform samplerCube iChannel0;"

        if self.iChannel1_Image != '':
            shaderFragment += "uniform sampler2D iChannel1;"
        elif self.iChannel1_CubeImage != '':
            shaderFragment += "uniform samplerCube iChannel1;"

        if self.iChannel2_Image != '':
            shaderFragment += "uniform sampler2D iChannel2;"
        elif self.iChannel2_CubeImage != '':
            shaderFragment += "uniform samplerCube iChannel2;"

        if self.iChannel3_Image != '':
            shaderFragment += "uniform sampler2D iChannel3;"
        elif self.iChannel3_CubeImage != '':
            shaderFragment += "uniform samplerCube iChannel3;"

        shaderFragment += """
#define texture2D texture
#define textureCube texture

        """

        shaderFragment += main_func

        shaderFragment += """

void main() {
    vec4 color = vec4(1.0, 0.0, 0.0, 1.0);
    mainImage(color, gl_FragCoord.xy);
    outFragmentColor = color;
}
        """

        self.shader_program = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, shaderFragment)

        if not shader_compilation:
            Settings.do_log("[Shadertoy] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[Shadertoy] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.vs_InFBO = GLUtils.glGetUniform(self.shader_program, "vs_inFBO")
        self.vs_ScreenResolution = GLUtils.glGetUniform(self.shader_program,  "vs_screenResolution")
        self.iResolution = GLUtils.glGetUniform(self.shader_program, "iResolution")
        self.iGlobalTime = GLUtils.glGetUniform(self.shader_program, "iGlobalTime")
        self.iTimeDelta = GLUtils.glGetUniform(self.shader_program, "iTimeDelta")
        self.iFrameRate = GLUtils.glGetUniform(self.shader_program, "iFrameRate")
        self.iFrame = GLUtils.glGetUniform(self.shader_program, "iFrame")
        self.iChannelTime[0] = GLUtils.glGetUniform(self.shader_program, "iChannelTime[0]")
        self.iChannelTime[1] = GLUtils.glGetUniform(self.shader_program, "iChannelTime[1]")
        self.iChannelTime[2] = GLUtils.glGetUniform(self.shader_program, "iChannelTime[2]")
        self.iChannelTime[3] = GLUtils.glGetUniform(self.shader_program, "iChannelTime[3]")
        self.iChannelResolution[0] = GLUtils.glGetUniform(self.shader_program, "iChannelResolution[0]")
        self.iChannelResolution[1] = GLUtils.glGetUniform(self.shader_program, "iChannelResolution[1]")
        self.iChannelResolution[2] = GLUtils.glGetUniform(self.shader_program, "iChannelResolution[2]")
        self.iChannelResolution[3] = GLUtils.glGetUniform(self.shader_program, "iChannelResolution[3]")
        self.iMouse = GLUtils.glGetUniform(self.shader_program, "iMouse")
        self.iDate = GLUtils.glGetUniform(self.shader_program, "iDate")
        self.gl_iChannel0 = GLUtils.glGetUniform(self.shader_program, "iChannel0")
        self.gl_iChannel1 = GLUtils.glGetUniform(self.shader_program, "iChannel1")
        self.gl_iChannel2 = GLUtils.glGetUniform(self.shader_program, "iChannel2")
        self.gl_iChannel3 = GLUtils.glGetUniform(self.shader_program, "iChannel3")

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

        self.iChannel0_Image = 'noise16.png'
        self.initTextures()

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(1, [vboVertices])

    def initTextures(self):
        tc = 0
        if self.iChannel0_Image != '':
            self.iChannel0 = self.addTexture(self.iChannel0_Image, self.iChannel0, tc)
            tc += 1
        if self.iChannel1_Image != '':
            self.iChannel1 = self.addTexture(self.iChannel1_Image, self.iChannel1, tc)
            tc += 1
        if self.iChannel2_Image != '':
            self.iChannel2 = self.addTexture(self.iChannel2_Image, self.iChannel2, tc)
            tc += 1
        if self.iChannel3_Image != '':
            self.iChannel3 = self.addTexture(self.iChannel3_Image, self.iChannel3, tc)

    def addTexture(self, textureImage, vboTexture, textureID):
        if textureImage != '':
            image_file = 'resources/shadertoy/' + textureImage
            if os.path.exists(image_file):
                texture_image = Image.open(image_file, 'r')
                texture_image_data = numpy.array(list(texture_image.getdata()), numpy.uint8)
                t_width = texture_image.width
                t_height = texture_image.height
                vboTexture = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, vboTexture)
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
                if textureID == 0:
                    self.iChannelResolution0[0] = float(t_width)
                    self.iChannelResolution0[1] = float(t_height)
                elif textureID == 1:
                    self.iChannelResolution1[0] = float(t_width)
                    self.iChannelResolution1[1] = float(t_height)
                elif textureID == 2:
                    self.iChannelResolution2[0] = float(t_width)
                    self.iChannelResolution2[1] = float(t_height)
                elif textureID == 3:
                    self.iChannelResolution3[0] = float(t_width)
                    self.iChannelResolution3[1] = float(t_height)
            else:
                Settings.do_log("[Shadertoy] - Can't load texture image! File doesn't exist!")
        return vboTexture

    def renderToTexture(self, mouse_x, mouse_y, seconds, vbo):
        self.bindFBO()
        self.render(mouse_x, mouse_y, seconds)
        vbo = self.unbindFBO(vbo)
        return vbo

    def render(self, mouse_x, mouse_y, seconds):
        if self.glVAO > 0:
            imgui_io = imgui.get_io()

            glUseProgram(self.shader_program)

            # glEnable(GL_TEXTURE_2D)
            # glActiveTexture(GL_TEXTURE2)
            glUniform1i(self.vs_InFBO, 1)

            try:
                tc = 0
                if self.iChannel0_Image != '' and self.iChannel0 is not None:
                    glActiveTexture(GL_TEXTURE0 + tc)
                    glBindTexture(GL_TEXTURE_2D, self.iChannel0)
                    glUniform1i(self.iChannel0, tc)
                    glUniform3f(self.iChannelResolution[0], self.iChannelResolution0[0], self.iChannelResolution0[1], 0.0)
                    tc += 1
                if self.iChannel1_Image != '' and self.iChannel1 is not None:
                    glActiveTexture(GL_TEXTURE0 + tc)
                    glBindTexture(GL_TEXTURE_2D, self.iChannel1)
                    glUniform1i(self.iChannel1, tc)
                    glUniform3f(self.iChannelResolution[0], self.iChannelResolution1[0], self.iChannelResolution2[1], 0.0)
                    tc += 1
                if self.iChannel2_Image != '' and self.iChannel2 is not None:
                    glActiveTexture(GL_TEXTURE0 + tc)
                    glBindTexture(GL_TEXTURE_2D, self.iChannel2)
                    glUniform1i(self.iChannel2, tc)
                    glUniform3f(self.iChannelResolution[0], self.iChannelResolution2[0], self.iChannelResolution3[1], 0.0)
                    tc += 1
                if self.iChannel3_Image != '' and self.iChannel3 is not None:
                    glActiveTexture(GL_TEXTURE0 + tc)
                    glBindTexture(GL_TEXTURE_2D, self.iChannel3)
                    glUniform1i(self.iChannel3, tc)
                    glUniform3f(self.iChannelResolution[0], self.iChannelResolution3[0], self.iChannelResolution3[1], 0.0)
                    tc += 1
            except (GLError):
                Settings.do_log("[Shadertoy-ERROR] - Error while binding the textures!")

            glUniform2f(self.vs_ScreenResolution, self.textureWidth, self.textureHeight)
            glUniform3f(self.iResolution, self.textureWidth, self.textureHeight, 0)
            glUniform1f(self.iGlobalTime, seconds)
            glUniform4f(self.iMouse, float(mouse_x), float(mouse_y), 0.0, 0.0)

            glUniform1f(self.iChannelTime[0], seconds)
            glUniform1f(self.iChannelTime[1], seconds)
            glUniform1f(self.iChannelTime[2], seconds)
            glUniform1f(self.iChannelTime[3], seconds)
            glUniform1f(self.iTimeDelta, imgui_io.delta_time)

            now = datetime.datetime.now()
            glUniform4f(self.iDate, now.year, now.month, now.day, now.second)

            glUniform1f(self.iFrameRate, imgui_io.framerate)
            glUniform1f(self.iFrame, 0.0)

            glBindVertexArray(self.glVAO)
            glDrawArrays(GL_TRIANGLES, 0, 6)
            glBindVertexArray(0)

            glUseProgram(0)

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
           Settings.do_log("[Shadertoy] - Error creating FBO! - " + str(glCheckFramebufferStatus(GL_FRAMEBUFFER)))

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
