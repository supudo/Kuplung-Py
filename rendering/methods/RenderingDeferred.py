# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

from math import cos, radians, sqrt
import numpy
import random
import time

from OpenGL.GL import *
from gl_utils import GLUtils
from gl_utils.objects.ModelFace_LightSource_Directional import (
    ModelFace_LightSource_Directional
)
from gl_utils.objects.ModelFace_LightSource_Point import (
    ModelFace_LightSource_Point
)
from gl_utils.objects.ModelFace_LightSource_Spot import (
    ModelFace_LightSource_Spot
)
from maths import MathOps
from maths.types.Matrix4x4 import Matrix4x4
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from settings import Settings

__author__ = 'supudo'
__version__ = "1.0.0"


class RenderingDeferred:
    def __init__(self):
        self.model_faces = []
        self.shaderProgram_GeometryPass = None
        self.shaderProgram_LightingPass = None
        self.shaderProgram_LightBox = None
        self.gl_GeometryPass_Texture_Diffuse = -1
        self.gl_GeometryPass_Texture_Specular = -1

        self.GLSL_LightSourceNumber_Directional = 8
        self.GLSL_LightSourceNumber_Point = 4
        self.GLSL_LightSourceNumber_Spot = 4
        self.mfLights_Directional = []
        self.mfLights_Point = []
        self.mfLights_Spot = []

        self.gBuffer = -1
        self.gPosition = -1
        self.gNormal = -1
        self.gAlbedoSpec = -1

        self.NR_LIGHTS = 32
        self.lightPositions = []
        self.lightColors = []

        self.quadVAO = 0
        self.cubeVAO = 0

        self.gl_GeometryPass_Texture_Diffuse = -1
        self.gl_GeometryPass_Texture_Specular = -1

        self.objectPositions = []
        self.lightPositions = []

        self.matrixProject = Matrix4x4(1.0)
        self.matrixCamera = Matrix4x4(1.0)

    def init_renderer(self, mo):
        success = True
        success &= self.initGeometryPass()
        success &= self.initLighingPass()
        success &= self.initLightObjects()
        success &= self.initProps(mo)
        success &= self.initGBuffer()
        success &= self.initLights()
        return success

    def initGeometryPass(self):
        file_vs = open('resources/shaders/deferred_g_buffer.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/deferred_g_buffer.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shaderProgram_GeometryPass = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileShader(self.shaderProgram_GeometryPass, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileShader(self.shaderProgram_GeometryPass, GL_FRAGMENT_SHADER, fs_str)

        file_vs.close()
        file_fs.close()

        if not shader_compilation:
            Settings.log_error("[RenderingDeferred - Geometry Pass] Shader compilation failed!")
            return False

        glLinkProgram(self.shaderProgram_GeometryPass)
        if glGetProgramiv(self.shaderProgram_GeometryPass, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[RenderingDeferred - Geometry Pass] Shader linking failed! " + str(self.shaderProgram_GeometryPass))
            GLUtils.printProgramLog(self.shaderProgram_GeometryPass)
            return False

        self.gl_GeometryPass_Texture_Diffuse = GLUtils.glGetUniform(self.shaderProgram_GeometryPass, "texture_diffuse")
        self.gl_GeometryPass_Texture_Specular = GLUtils.glGetUniform(self.shaderProgram_GeometryPass, "texture_specular")

        return True

    def initLighingPass(self):
        file_vs = open('resources/shaders/deferred_shading.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/deferred_shading.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shaderProgram_LightingPass = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileShader(self.shaderProgram_LightingPass, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileShader(self.shaderProgram_LightingPass, GL_FRAGMENT_SHADER, fs_str)

        file_vs.close()
        file_fs.close()

        if not shader_compilation:
            Settings.log_error("[RenderingDeferred - Lighting Pass] Shader compilation failed!")
            return False

        glLinkProgram(self.shaderProgram_LightingPass)
        if glGetProgramiv(self.shaderProgram_LightingPass, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[RenderingDeferred - Lighting Pass] Shader linking failed! " + str(self.shaderProgram_LightingPass))
            GLUtils.printProgramLog(self.shaderProgram_LightingPass)
            return False

        return True

    def initLightObjects(self):
        file_vs = open('resources/shaders/deferred_light_box.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/deferred_light_box.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shaderProgram_LightBox = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileShader(self.shaderProgram_LightBox, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileShader(self.shaderProgram_LightBox, GL_FRAGMENT_SHADER, fs_str)

        file_vs.close()
        file_fs.close()

        if not shader_compilation:
            Settings.log_error("[RenderingDeferred - Light Box] Shader compilation failed!")
            return False

        glLinkProgram(self.shaderProgram_LightBox)
        if glGetProgramiv(self.shaderProgram_LightBox, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[RenderingDeferred - Light Box] Shader linking failed! " + str(self.shaderProgram_LightBox))
            GLUtils.printProgramLog(self.shaderProgram_LightBox)
            return False

        return True

    def initProps(self, mo):
        result = True

        glUseProgram(self.shaderProgram_LightingPass)
        glUniform1i(glGetUniformLocation(self.shaderProgram_LightingPass, "sampler_position"), 0)
        glUniform1i(glGetUniformLocation(self.shaderProgram_LightingPass, "sampler_normal"), 1)
        glUniform1i(glGetUniformLocation(self.shaderProgram_LightingPass, "sampler_albedospec"), 2)

        # TODO: parametrize this in the GUI
        threshold = 3.0
        self.objectPositions.clear()
        if mo.Setting_DeferredTestMode:
            self.objectPositions.append(Vector3(0.0, -threshold, 0.0))
            self.objectPositions.append(Vector3(-threshold, -threshold, -threshold))
            self.objectPositions.append(Vector3(0.0, -threshold, -threshold))
            self.objectPositions.append(Vector3(threshold, -threshold, -threshold))
            self.objectPositions.append(Vector3(-threshold, -threshold, 0.0))
            self.objectPositions.append(Vector3(threshold, -threshold, 0.0))
            self.objectPositions.append(Vector3(-threshold, -threshold, threshold))
            self.objectPositions.append(Vector3(0.0, -threshold, threshold))
            self.objectPositions.append(Vector3(threshold, -threshold, threshold))
        else:
            self.objectPositions.append(Vector3(0.0, 0.0, 0.0))

        # Colors
        self.lightPositions.clear()
        self.lightColors.clear()
        random.seed(time.time())
        for i in range(self.NR_LIGHTS):
            # Calculate slightly random offsets
            xPos = ((random.randint(0, 100) / 100.0) * 6.0) - threshold
            yPos = (random.randint(0, 100) / 100.0) * 6.0
            zPos = ((random.randint(0, 100) / 100.0) * 6.0) - threshold
            self.lightPositions.append(Vector3(float("%.3f" % xPos), float("%.3f" % yPos), float("%.3f" % zPos)))

            # Also calculate random color
            rColor = random.uniform(0.5, 1.0) # Between 0.5 and 1.0
            gColor = random.uniform(0.5, 1.0) # Between 0.5 and 1.0
            bColor = random.uniform(0.5, 1.0) # Between 0.5 and 1.0
            self.lightColors.append(Vector3(float("%.3f" % rColor), float("%.3f" % gColor), float("%.3f" % bColor)))

        return result

    def initGBuffer(self):
        result = True
        # Set up G - Buffer
        # 3 textures:
        # 1. Positions(RGB)
        # 2. Color(RGB) + Specular(A)
        # 3. Normals(RGB)
        self.gBuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.gBuffer)

        # - Position color buffer
        self.gPosition = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.gPosition)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB16F, Settings.AppWindowWidth * 2, Settings.AppWindowHeight, 0, GL_RGB, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.gPosition, 0)

        # - Normal color buffer
        self.gNormal = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.gNormal)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB16F, Settings.AppWindowWidth, Settings.AppWindowHeight, 0, GL_RGB, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT1, GL_TEXTURE_2D, self.gNormal, 0)

        # - Color + Specular color buffer
        self.gAlbedoSpec = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.gAlbedoSpec)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, Settings.AppWindowWidth, Settings.AppWindowHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT2, GL_TEXTURE_2D, self.gAlbedoSpec, 0)

        # - Tell OpenGL which color attachments we'll use (of this framebuffer) for rendering
        glDrawBuffers(3, [GL_COLOR_ATTACHMENT0, GL_COLOR_ATTACHMENT1, GL_COLOR_ATTACHMENT2])

        # - Create and attach depth buffer(renderbuffer)
        rboDepth = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rboDepth)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, Settings.AppWindowWidth, Settings.AppWindowHeight)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, rboDepth)
        # - Finally check if framebuffer is complete
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            result = False
            Settings.do_log("[RenderingDeferred - GBuffer init] Framebuffer not complete!")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDeleteBuffers(1, [rboDepth])

        return result

    def initLights(self):
        # light - directional
        for i in range(self.GLSL_LightSourceNumber_Directional):
            f = ModelFace_LightSource_Directional()
            f.gl_InUse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].inUse"))
            f.gl_Direction = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].direction"))

            f.gl_Ambient = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].ambient"))
            f.gl_Diffuse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].diffuse"))
            f.gl_Specular = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].specular"))

            f.gl_StrengthAmbient = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].strengthAmbient"))
            f.gl_StrengthDiffuse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].strengthDiffuse"))
            f.gl_StrengthSpecular = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("directionalLights[" + str(i) + "].strengthSpecular"))
            self.mfLights_Directional.append(f)

        # light - point
        for i in range(self.GLSL_LightSourceNumber_Point):
            f = ModelFace_LightSource_Point()
            f.gl_InUse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].inUse"))
            f.gl_Position = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].position"))

            f.gl_Constant = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].constant"))
            f.gl_Linear = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].linear"))
            f.gl_Quadratic = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].quadratic"))

            f.gl_Ambient = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].ambient"))
            f.gl_Diffuse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].diffuse"))
            f.gl_Specular = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].specular"))

            f.gl_StrengthAmbient = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].strengthAmbient"))
            f.gl_StrengthDiffuse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].strengthDiffuse"))
            f.gl_StrengthSpecular = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("pointLights[" + str(i) + "].strengthSpecular"))
            self.mfLights_Point.append(f)

        # light - spot
        for i in range(self.GLSL_LightSourceNumber_Spot):
            f = ModelFace_LightSource_Spot()
            f.gl_InUse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].inUse"))
            f.gl_Position = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].position"))
            f.gl_Direction = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].direction"))

            f.gl_CutOff = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].cutOff"))
            f.gl_OuterCutOff = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].outerCutOff"))

            f.gl_Constant = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].constant"))
            f.gl_Linear = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].linear"))
            f.gl_Quadratic = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].quadratic"))

            f.gl_Ambient = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].ambient"))
            f.gl_Diffuse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].diffuse"))
            f.gl_Specular = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].specular"))

            f.gl_StrengthAmbient = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].strengthAmbient"))
            f.gl_StrengthDiffuse = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].strengthDiffuse"))
            f.gl_StrengthSpecular = GLUtils.glGetUniform(self.shaderProgram_LightingPass, ("spotLights[" + str(i) + "].strengthSpecular"))
            self.mfLights_Spot.append(f)

        return True

    def render(self, mo, selectedModel):
        if mo.Setting_DeferredRandomizeLightPositions:
            self.init_renderer(mo)
            mo.Setting_DeferredRandomizeLightPositions = False
        self.renderGBuffer(mo, selectedModel)
        self.renderLightingPass(mo)
        if mo.Setting_DeferredTestLights:
            self.renderLightObjects(mo)
        else:
            glBindFramebuffer(GL_READ_FRAMEBUFFER, self.gBuffer)
            glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
            glBlitFramebuffer(0, 0,
                              Settings.AppWindowWidth, Settings.AppWindowHeight,
                              0, 0,
                              Settings.AppWindowWidth, Settings.AppWindowHeight,
                              GL_DEPTH_BUFFER_BIT, GL_NEAREST)
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
        return mo

    def renderGBuffer(self, mo, selectedModel):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # 1.Geometry Pass: render scene's geometry/color data into gbuffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.gBuffer)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.matrixProject = mo.matrixProjection
        self.matrixCamera = mo.camera.matrixCamera
        glUseProgram(self.shaderProgram_GeometryPass)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram_GeometryPass, "projection"), 1, GL_FALSE, MathOps.matrix_to_gl(self.matrixProject))
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram_GeometryPass, "view"), 1, GL_FALSE, MathOps.matrix_to_gl(self.matrixCamera))
        objPositions = 1
        if mo.Setting_DeferredTestMode:
            objPositions = len(self.objectPositions)
        for i in range(objPositions):
            matrixModel = Matrix4x4(1.0)
            matrixModel = MathOps.matrix_translate(matrixModel, self.objectPositions[i])
            if len(self.objectPositions) > 1:
                matrixModel = MathOps.matrix_scale(matrixModel, Vector3(0.25))
            matrixModel = MathOps.matrix_translate(matrixModel, Vector4(0))
            matrixModel = MathOps.matrix_rotate(matrixModel, -90.0, Vector3(1, 0, 0))
            # matrixModel = MathOps.matrix_rotate(matrixModel, 180.0, Vector3(1, 0, 1))
            matrixModel = MathOps.matrix_translate(matrixModel, Vector4(0))
            # matrixModel *= mo.grid.matrixModel

            modelCounter = 0
            for mfd in self.model_faces:
                # scale
                matrixModel = MathOps.matrix_scale( matrixModel, (mfd.scaleX.point, mfd.scaleY.point, mfd.scaleZ.point))
                # rotate
                matrixModel = MathOps.matrix_translate(matrixModel, Vector4(.0))
                matrixModel = MathOps.matrix_rotate(matrixModel, mfd.rotateX.point, Vector3(1, 0, 0))
                matrixModel = MathOps.matrix_rotate(matrixModel, mfd.rotateY.point, Vector3(0, 1, 0))
                matrixModel = MathOps.matrix_rotate(matrixModel, mfd.rotateZ.point, Vector3(0, 0, 1))
                matrixModel = MathOps.matrix_translate(matrixModel, Vector4(.0))
                # translate
                matrixModel = MathOps.matrix_translate(matrixModel, (mfd.positionX.point, mfd.positionY.point, mfd.positionZ.point))

                glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram_GeometryPass, "model"), 1, GL_FALSE, MathOps.matrix_to_gl(matrixModel))

                if mfd.vbo_tex_diffuse is not None and mfd.mesh_model.ModelMaterial.texture_diffuse.UseTexture:
                    glUniform1i(self.gl_GeometryPass_Texture_Diffuse, 0)
                    glActiveTexture(GL_TEXTURE0)
                    glBindTexture(GL_TEXTURE_2D, mfd.vbo_tex_diffuse)

                if mfd.vbo_tex_specular is not None and mfd.mesh_model.ModelMaterial.texture_specular.UseTexture:
                    glUniform1i(self.gl_GeometryPass_Texture_Specular, 1)
                    glActiveTexture(GL_TEXTURE1)
                    glBindTexture(GL_TEXTURE_2D, mfd.vbo_tex_specular)

                mfd.matrixProjection = self.matrixProject
                mfd.matrixCamera = self.matrixCamera
                mfd.matrixModel = matrixModel
                mfd.Setting_ModelViewSkin = mo.viewModelSkin
                mfd.lightSources = mo.lightSources
                mfd.so_outlineColor = mo.Setting_OutlineColor
                mfd.so_outlineThickness = mo.Setting_OutlineThickness
                mfd.so_selectedYn = selectedModel == modelCounter
                mfd.render(False)

                modelCounter += 1

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def renderLightingPass(self, mo):
        # 2. Lighting Pass: calculate lighting by iterating over a screen filled quad pixel - by - pixel using the gbuffer 's content.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shaderProgram_LightingPass)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.gPosition)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.gNormal)
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.gAlbedoSpec)

        lightsCount_Directional = 0
        lightsCount_Point = 0
        lightsCount_Spot = 0
        for i in range(len(mo.lightSources)):
            light = mo.lightSources[i]
            if light.type == Settings.LightSourceTypes.LightSourceType_Directional and lightsCount_Directional < self.GLSL_LightSourceNumber_Directional:
                f = self.mfLights_Directional[lightsCount_Directional]
                glUniform1i(f.gl_InUse, 1)

                # light
                glUniform3f(f.gl_Direction, light.positionX.point, light.positionY.point, light.positionZ.point)

                # color
                glUniform3f(f.gl_Ambient, light.ambient.color.r, light.ambient.color.g, light.ambient.color.b)
                glUniform3f(f.gl_Diffuse, light.diffuse.color.r, light.diffuse.color.g, light.diffuse.color.b)
                glUniform3f(f.gl_Specular, light.specular.color.r, light.specular.color.g, light.specular.color.b)

                # light factors
                glUniform1f(f.gl_StrengthAmbient, light.ambient.strength)
                glUniform1f(f.gl_StrengthDiffuse, light.diffuse.strength)
                glUniform1f(f.gl_StrengthSpecular, light.specular.strength)

                lightsCount_Directional += 1
            elif light.type == Settings.LightSourceTypes.LightSourceType_Point and lightsCount_Point < self.GLSL_LightSourceNumber_Point:
                f = self.mfLights_Point[lightsCount_Point]
                glUniform1i(f.gl_InUse, 1)

                # light
                glUniform3f(f.gl_Position, light.matrixModel[3].x, light.matrixModel[3].y, light.matrixModel[3].z)

                # factors﻿
                glUniform1f(f.gl_Constant, light.lConstant.point)
                glUniform1f(f.gl_Linear, light.lLinear.point)
                glUniform1f(f.gl_Quadratic, light.lQuadratic.point)

                # color
                glUniform3f(f.gl_Ambient, light.ambient.color.r, light.ambient.color.g, light.ambient.color.b)
                glUniform3f(f.gl_Diffuse, light.diffuse.color.r, light.diffuse.color.g, light.diffuse.color.b)
                glUniform3f(f.gl_Specular, light.specular.color.r, light.specular.color.g, light.specular.color.b)

                # light factors
                glUniform1f(f.gl_StrengthAmbient, light.ambient.strength)
                glUniform1f(f.gl_StrengthDiffuse, light.diffuse.strength)
                glUniform1f(f.gl_StrengthSpecular, light.specular.strength)

                lightsCount_Point += 1
            elif light.type == Settings.LightSourceTypes.LightSourceType_Spot and lightsCount_Spot < self.GLSL_LightSourceNumber_Spot:
                f = self.mfLights_Spot[lightsCount_Spot]
                glUniform1i(f.gl_InUse, 1)

                # light
                glUniform3f(f.gl_Direction, light.positionX.point, light.positionY.point, light.positionZ.point)
                glUniform3f(f.gl_Position, light.matrixModel[3].x, light.matrixModel[3].y, light.matrixModel[3].z)

                # cutoff
                glUniform1f(f.gl_CutOff, cos(radians(light.lCutOff.point)))
                glUniform1f(f.gl_OuterCutOff, cos(radians(light.lOuterCutOff.point)))

                # factors﻿
                glUniform1f(f.gl_Constant, light.lConstant.point)
                glUniform1f(f.gl_Linear, light.lLinear.point)
                glUniform1f(f.gl_Quadratic, light.lQuadratic.point)

                # color
                glUniform3f(f.gl_Ambient, light.ambient.color.r, light.ambient.color.g, light.ambient.color.b)
                glUniform3f(f.gl_Diffuse, light.diffuse.color.r, light.diffuse.color.g, light.diffuse.color.b)
                glUniform3f(f.gl_Specular, light.specular.color.r, light.specular.color.g, light.specular.color.b)

                # light factors
                glUniform1f(f.gl_StrengthAmbient, light.ambient.strength)
                glUniform1f(f.gl_StrengthDiffuse, light.diffuse.strength)
                glUniform1f(f.gl_StrengthSpecular, light.specular.strength)

                lightsCount_Spot += 1

        for i in range(lightsCount_Directional, self.GLSL_LightSourceNumber_Directional):
            glUniform1i(self.mfLights_Directional[i].gl_InUse, 0)

        for i in range(lightsCount_Point, self.GLSL_LightSourceNumber_Point):
            glUniform1i(self.mfLights_Point[i].gl_InUse, 0)

        for i in range(lightsCount_Spot, self.GLSL_LightSourceNumber_Spot):
            glUniform1i(self.mfLights_Spot[i].gl_InUse, 0)

        # Also send light relevant uniforms
        if mo.Setting_DeferredTestLights:
            for i in range(mo.Setting_DeferredTestLightsNumber):
                glUniform3f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Position")), self.lightPositions[i].x, self.lightPositions[i].y, self.lightPositions[i].z)
                glUniform3f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Color")), self.lightColors[i].r, self.lightColors[i].g, self.lightColors[i].b)

                # Update attenuation parameters and calculate radius
                constant = 1.0 # Note that we don't send this to the shader, we assume it is always 1.0 (in our case)
                linear = 0.7
                quadratic = 1.8
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Linear")), linear)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Quadratic")), quadratic)

                # Then calculate radius of light volume/sphere
                lightThreshold = 5.0 # 5 / 256
                maxBrightness = max(max(self.lightColors[i].r, self.lightColors[i].g), self.lightColors[i].b)
                radius = (-linear + (sqrt(linear * linear - 4 * quadratic * (constant - (256 / lightThreshold)) * maxBrightness))) / (2 * quadratic)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Radius")), radius)
            for i in range(len(self.lightPositions)):
                glUniform3f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Position")), self.lightPositions[i].x, self.lightPositions[i].y, self.lightPositions[i].z)
                glUniform3f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Color")), self.lightColors[i].r, self.lightColors[i].g, self.lightColors[i].b)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Linear")), 0.0)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Quadratic")), 0.0)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Radius")), 0.0)
        else:
            for i in range(len(self.lightPositions)):
                glUniform3f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Position")), self.lightPositions[i].x, self.lightPositions[i].y, self.lightPositions[i].z)
                glUniform3f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Color")), self.lightColors[i].r, self.lightColors[i].g, self.lightColors[i].b)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Linear")), 0.0)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Quadratic")), 0.0)
                glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, ("lights[" + str(i) + "].Radius")), 0.0)
        glUniform3f(glGetUniformLocation(self.shaderProgram_LightingPass, "viewPos"), mo.camera.cameraPosition.x, mo.camera.cameraPosition.y, mo.camera.cameraPosition.z)
        glUniform1i(glGetUniformLocation(self.shaderProgram_LightingPass, "draw_mode"), mo.Setting_LightingPass_DrawMode + 1)
        glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, "ambientStrength"), mo.Setting_DeferredAmbientStrength)
        glUniform1f(glGetUniformLocation(self.shaderProgram_LightingPass, "gammaCoeficient"), mo.Setting_GammaCoeficient)
        self.renderQuad()

    def renderLightObjects(self, mo):
        # 2.5. Copy content of geometry's depth buffer to default framebuffer's depth buffer﻿
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.gBuffer)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0) # Write to default framebuffer
        # blit to default framebuffer. Note that this may or may not work as the internal formats of both the FBO and default framebuffer have to match.
        # the internal formats are implementation defined. This works on all of my systems, but if it doesn't on yours you'll likely have to write to the
        # depth buffer in another stage (or somehow see to match the default framebuffer's internal format with the FBO's internal format).
        glBlitFramebuffer(0, 0,
                          Settings.AppWindowWidth, Settings.AppWindowHeight,
                          0, 0,
                          Settings.AppWindowWidth, Settings.AppWindowHeight,
                          GL_DEPTH_BUFFER_BIT, GL_NEAREST)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # 3. Render lights on top of scene, by blitting
        glUseProgram(self.shaderProgram_LightBox)
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram_LightBox, "projection"), 1, GL_FALSE, MathOps.matrix_to_gl(self.matrixProject))
        glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram_LightBox, "view"), 1, GL_FALSE, MathOps.matrix_to_gl(self.matrixCamera))
        for i in range(mo.Setting_DeferredTestLightsNumber):
            matrixModel = Matrix4x4(1.0)
            matrixModel = MathOps.matrix_translate(matrixModel, self.lightPositions[i])
            matrixModel = MathOps.matrix_scale( matrixModel, Vector3(0.25))
            glUniformMatrix4fv(glGetUniformLocation(self.shaderProgram_LightBox, "model"), 1, GL_FALSE, MathOps.matrix_to_gl(matrixModel))
            glUniform3f(glGetUniformLocation(self.shaderProgram_LightBox, "lightColor"), self.lightColors[i].r, self.lightColors[i].g, self.lightColors[i].b)
            self.renderCube()

    def renderQuad(self):
        if self.quadVAO == 0:
            quadVertices = [-1.0,  1.0, 0.0, -1.0, -1.0, 0.0, 1.0,  1.0, 0.0, 1.0, -1.0, 0.0]
            data_vertices = numpy.array(quadVertices, dtype=numpy.float32)

            quadTC = [0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0]
            data_texCoords = numpy.array(quadTC, dtype=numpy.float32)

            self.quadVAO = glGenVertexArrays(1)
            glBindVertexArray(self.quadVAO)

            quadVBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, quadVBO)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            quadTBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, quadTBO)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_texCoords), data_texCoords, GL_STATIC_DRAW)
            glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(1)

            glBindVertexArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glDeleteBuffers(3, [quadVBO, quadTBO])

        glBindVertexArray(self.quadVAO)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glBindVertexArray(0)

    def renderCube(self):
        if self.cubeVAO == 0:
            vertices = [
                # Back face
                -0.5, -0.5, -0.5, # bottom-left
                 0.5,  0.5, -0.5, # top-right
                 0.5, -0.5, -0.5, # bottom-right
                 0.5,  0.5, -0.5, # top-right
                -0.5, -0.5, -0.5, # bottom-left
                -0.5,  0.5, -0.5, # top-left
                # Front face
                -0.5, -0.5,  0.5, # bottom-left
                 0.5, -0.5,  0.5, # bottom-right
                 0.5,  0.5,  0.5, # top-right
                 0.5,  0.5,  0.5, # top-right
                -0.5,  0.5,  0.5, # top-left
                -0.5, -0.5,  0.5, # bottom-left
                # Left face
                -0.5,  0.5,  0.5, # top-right
                -0.5,  0.5, -0.5, # top-left
                -0.5, -0.5, -0.5, # bottom-left
                -0.5, -0.5, -0.5, # bottom-left
                -0.5, -0.5,  0.5, # bottom-right
                -0.5,  0.5,  0.5, # top-right
                # Right face
                 0.5,  0.5,  0.5, # top-left
                 0.5, -0.5, -0.5, # bottom-right
                 0.5,  0.5, -0.5, # top-right
                 0.5, -0.5, -0.5, # bottom-right
                 0.5,  0.5,  0.5, # top-left
                 0.5, -0.5,  0.5, # bottom-left
                # Bottom face
                -0.5, -0.5, -0.5, # top-right
                 0.5, -0.5, -0.5, # top-left
                 0.5, -0.5,  0.5, # bottom-left
                 0.5, -0.5,  0.5, # bottom-left
                -0.5, -0.5,  0.5, # bottom-right
                -0.5, -0.5, -0.5, # top-right
                # Top face
                -0.5,  0.5, -0.5, # top-left
                 0.5,  0.5,  0.5, # bottom-right
                 0.5,  0.5, -0.5, # top-right
                 0.5,  0.5,  0.5, # bottom-right
                -0.5,  0.5, -0.5, # top-left
                -0.5,  0.5,  0.5, # bottom-left
            ]
            normals = [
                0.0,  0.0, -1.0, 0.0,  0.0, -1.0, 0.0,  0.0, -1.0, 0.0,  0.0, -1.0, 0.0,  0.0, -1.0, 0.0,  0.0, -1.0, # Back face
                0.0,  0.0,  1.0, 0.0,  0.0,  1.0, 0.0,  0.0,  1.0, 0.0,  0.0,  1.0, 0.0,  0.0,  1.0, 0.0,  0.0,  1.0, # Front face
                1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, # Left face
                1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, 1.0,  0.0,  0.0, # Right face
                0.0, -1.0,  0.0, 0.0, -1.0,  0.0, 0.0, -1.0,  0.0, 0.0, -1.0,  0.0, 0.0, -1.0,  0.0, 0.0, -1.0,  0.0, # Bottom face
                0.0,  1.0,  0.0, 0.0,  1.0,  0.0, 0.0,  1.0,  0.0, 0.0,  1.0,  0.0, 0.0,  1.0,  0.0, 0.0,  1.0,  0.0  # Top face
            ]
            texCoords = [
                0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, # Back face
                0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, # Front face
                1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, # Left face
                1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, # Right face
                0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, # Bottom face
                0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0  # Top face
            ]
            data_vertices = numpy.array(vertices, dtype=numpy.float32)
            data_normals = numpy.array(normals, dtype=numpy.float32)
            data_texCoords = numpy.array(texCoords, dtype=numpy.float32)

            self.cubeVAO = glGenVertexArrays(1)
            glBindVertexArray(self.cubeVAO)

            # vertices
            cubeVBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, cubeVBO)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_vertices), data_vertices, GL_STATIC_DRAW)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            # normals
            cubeNBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, cubeNBO)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_normals), data_normals, GL_STATIC_DRAW)
            glVertexAttribPointer(1, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(1)

            # texture coordinates
            cubeTBO = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, cubeTBO)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_texCoords), data_texCoords, GL_STATIC_DRAW)
            glVertexAttribPointer(2, 2, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(2)

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
            glDeleteBuffers(3, [cubeVBO, cubeNBO, cubeTBO])

        # Render Cube
        glBindVertexArray(self.cubeVAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
