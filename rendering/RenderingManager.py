# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

from OpenGL.GL import *
from math import cos, radians
from settings import Settings
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
from maths.types.Matrix4x4 import Matrix4x4
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from maths import MathOps


__author__ = 'supudo'
__version__ = "1.0.0"


class RenderingManager:
    def __init__(self):
        self.model_faces = []
        self.shader_program = None

        self.glFS_showShadows = -1
        self.glFS_ShadowPass = -1

        self.glFS_planeClose = -1
        self.glFS_planeFar = -1
        self.glFS_showDepthColor = -1

        self.glGS_GeomDisplacementLocation = -1
        self.glTCS_UseCullFace = -1
        self.glTCS_UseTessellation = -1
        self.glTCS_TessellationSubdivision = -1

        self.glFS_AlphaBlending = -1
        self.glFS_CelShading = -1
        self.glFS_CameraPosition = -1
        self.glVS_IsBorder = -1
        self.glFS_OutlineColor = -1
        self.glFS_UIAmbient = -1
        self.glFS_GammaCoeficient = -1

        self.glVS_MVPMatrix = -1
        self.glFS_MMatrix = -1
        self.glVS_WorldMatrix = -1
        self.glFS_MVMatrix = -1
        self.glVS_NormalMatrix = -1

        self.glFS_ScreenResX = -1
        self.glFS_ScreenResY = -1

        self.glMaterial_ParallaxMapping = -1

        self.gl_ModelViewSkin = -1
        self.glFS_solidSkin_materialColor = -1

        self.solidLight = ModelFace_LightSource_Directional()

        self.GLSL_LightSourceNumber_Directional = 8
        self.GLSL_LightSourceNumber_Point = 4
        self.GLSL_LightSourceNumber_Spot = 4
        self.mfLights_Directional = []
        self.mfLights_Point = []
        self.mfLights_Spot = []

    def initShaderProgram(self):
        # vertex shader
        file_vs = open('resources/shaders/model_face.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())

        # tessellation control shader
        file_tcs = open('resources/shaders/model_face.tcs', 'r', encoding='utf-8')
        tcs_str = str(file_tcs.read())

        # tessellation evaluation shader
        file_tes = open('resources/shaders/model_face.tes', 'r', encoding='utf-8')
        tes_str = str(file_tes.read())

        # geometry shader
        file_geom = open('resources/shaders/model_face.geom', 'r', encoding='utf-8')
        geom_str = str(file_geom.read())

        # fragment shader
        fs_str = ''
        fs_components = ["vars", "effects", "lights", "mapping", "shadow_mapping", "misc"]
        for comp in fs_components:
            file_fs = open('resources/shaders/model_face_' + comp + '.frag', 'r', encoding='utf-8')
            fs_str += str(file_fs.read())

        file_fs = open('resources/shaders/model_face.frag', 'r', encoding='utf-8')
        fs_str += str(file_fs.read())

        self.shader_program = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileShader(self.shader_program, GL_TESS_CONTROL_SHADER, tcs_str)
        shader_compilation &= GLUtils.compileShader(self.shader_program, GL_TESS_EVALUATION_SHADER, tes_str)
        shader_compilation &= GLUtils.compileShader(self.shader_program, GL_GEOMETRY_SHADER, geom_str)
        shader_compilation &= GLUtils.compileShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        file_vs.close()
        file_tcs.close()
        file_tes.close()
        file_geom.close()
        file_fs.close()

        if not shader_compilation:
            Settings.log_error("[RenderingManager] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[RenderingManager] Shader linking failed! " + str(self.shader_program))
            GLUtils.printProgramLog(self.shader_program)
            return False

        glPatchParameteri(GL_PATCH_VERTICES, 3)

        self.glFS_showShadows = GLUtils.glGetUniform(self.shader_program, "fs_showShadows")
        self.glFS_ShadowPass = GLUtils.glGetUniform(self.shader_program, "fs_shadowPass")

        self.glFS_planeClose = GLUtils.glGetUniform(self.shader_program, "fs_planeClose")
        self.glFS_planeFar = GLUtils.glGetUniform(self.shader_program, "fs_planeFar")
        self.glFS_showDepthColor = GLUtils.glGetUniform(self.shader_program, "fs_showDepthColor")

        self.glGS_GeomDisplacementLocation = GLUtils.glGetUniform(self.shader_program, "vs_displacementLocation")
        self.glTCS_UseCullFace = GLUtils.glGetUniform(self.shader_program, "tcs_UseCullFace")
        self.glTCS_UseTessellation = GLUtils.glGetUniform(self.shader_program, "tcs_UseTessellation")
        self.glTCS_TessellationSubdivision = GLUtils.glGetUniform(self.shader_program, "tcs_TessellationSubdivision")

        self.glFS_AlphaBlending = GLUtils.glGetUniform(self.shader_program, "fs_alpha")
        self.glFS_CelShading = GLUtils.glGetUniform(self.shader_program, "fs_celShading")
        self.glFS_CameraPosition = GLUtils.glGetUniform(self.shader_program, "fs_cameraPosition")
        self.glVS_IsBorder = GLUtils.glGetUniform(self.shader_program, "vs_isBorder")
        self.glFS_OutlineColor = GLUtils.glGetUniform(self.shader_program, "fs_outlineColor")
        self.glFS_UIAmbient = GLUtils.glGetUniform(self.shader_program, "fs_UIAmbient")
        self.glFS_GammaCoeficient = GLUtils.glGetUniform(self.shader_program, "fs_gammaCoeficient")

        self.glVS_MVPMatrix = GLUtils.glGetUniform(self.shader_program, "vs_MVPMatrix")
        self.glFS_MMatrix = GLUtils.glGetUniform(self.shader_program, "fs_ModelMatrix")
        self.glVS_WorldMatrix = GLUtils.glGetUniform(self.shader_program, "vs_WorldMatrix")
        self.glFS_MVMatrix = GLUtils.glGetUniform(self.shader_program, "vs_MVMatrix")
        self.glVS_NormalMatrix = GLUtils.glGetUniform(self.shader_program, "vs_normalMatrix")

        self.glFS_ScreenResX = GLUtils.glGetUniform(self.shader_program, "fs_screenResX")
        self.glFS_ScreenResY = GLUtils.glGetUniform(self.shader_program, "fs_screenResY")

        self.glMaterial_ParallaxMapping = GLUtils.glGetUniform(self.shader_program, "fs_userParallaxMapping")

        self.gl_ModelViewSkin = GLUtils.glGetUniform(self.shader_program, "fs_modelViewSkin")
        self.glFS_solidSkin_materialColor = GLUtils.glGetUniform(self.shader_program, "solidSkin_materialColor")

        self.solidLight.gl_InUse = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.inUse")
        self.solidLight.gl_Direction = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.direction")
        self.solidLight.gl_Ambient = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.ambient")
        self.solidLight.gl_Diffuse = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.diffuse")
        self.solidLight.gl_Specular = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.specular")
        self.solidLight.gl_StrengthAmbient = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.strengthAmbient")
        self.solidLight.gl_StrengthDiffuse = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.strengthDiffuse")
        self.solidLight.gl_StrengthSpecular = GLUtils.glGetUniform(self.shader_program, "solidSkin_Light.strengthSpecular")

        # light - directional
        for i in range(self.GLSL_LightSourceNumber_Directional):
            f = ModelFace_LightSource_Directional()
            f.gl_InUse = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].inUse"))
            f.gl_Direction = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].direction"))

            f.gl_Ambient = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].ambient"))
            f.gl_Diffuse = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].diffuse"))
            f.gl_Specular = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].specular"))

            f.gl_StrengthAmbient = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].strengthAmbient"))
            f.gl_StrengthDiffuse = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].strengthDiffuse"))
            f.gl_StrengthSpecular = GLUtils.glGetUniform(self.shader_program, ("directionalLights[" + str(i) + "].strengthSpecular"))
            self.mfLights_Directional.append(f)

        # light - point
        for i in range(self.GLSL_LightSourceNumber_Point):
            f = ModelFace_LightSource_Point()
            f.gl_InUse = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].inUse"))
            f.gl_Position = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].position"))

            f.gl_Constant = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].constant"))
            f.gl_Linear = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].linear"))
            f.gl_Quadratic = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].quadratic"))

            f.gl_Ambient = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].ambient"))
            f.gl_Diffuse = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].diffuse"))
            f.gl_Specular = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].specular"))

            f.gl_StrengthAmbient = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].strengthAmbient"))
            f.gl_StrengthDiffuse = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].strengthDiffuse"))
            f.gl_StrengthSpecular = GLUtils.glGetUniform(self.shader_program, ("pointLights[" + str(i) + "].strengthSpecular"))
            self.mfLights_Point.append(f)

        # light - spot
        for i in range(self.GLSL_LightSourceNumber_Spot):
            f = ModelFace_LightSource_Spot()
            f.gl_InUse = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].inUse"))
            f.gl_Position = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].position"))
            f.gl_Direction = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].direction"))

            f.gl_CutOff = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].cutOff"))
            f.gl_OuterCutOff = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].outerCutOff"))

            f.gl_Constant = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].constant"))
            f.gl_Linear = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].linear"))
            f.gl_Quadratic = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].quadratic"))

            f.gl_Ambient = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].ambient"))
            f.gl_Diffuse = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].diffuse"))
            f.gl_Specular = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].specular"))

            f.gl_StrengthAmbient = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].strengthAmbient"))
            f.gl_StrengthDiffuse = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].strengthDiffuse"))
            f.gl_StrengthSpecular = GLUtils.glGetUniform(self.shader_program, ("spotLights[" + str(i) + "].strengthSpecular"))
            self.mfLights_Spot.append(f)

        # material
        self.glMaterial_Refraction = GLUtils.glGetUniform(self.shader_program, "material.refraction")
        self.glMaterial_SpecularExp = GLUtils.glGetUniform(self.shader_program, "material.specularExp")
        self.glMaterial_IlluminationModel = GLUtils.glGetUniform(self.shader_program, "material.illumination_model")
        self.glMaterial_HeightScale = GLUtils.glGetUniform(self.shader_program, "material.heightScale")

        self.glMaterial_Ambient = GLUtils.glGetUniform(self.shader_program, "material.ambient")
        self.glMaterial_Diffuse = GLUtils.glGetUniform(self.shader_program, "material.diffuse")
        self.glMaterial_Specular = GLUtils.glGetUniform(self.shader_program, "material.specular")
        self.glMaterial_Emission = GLUtils.glGetUniform(self.shader_program, "material.emission")

        self.glMaterial_SamplerAmbient = GLUtils.glGetUniform(self.shader_program, "material.sampler_ambient")
        self.glMaterial_SamplerDiffuse = GLUtils.glGetUniform(self.shader_program, "material.sampler_diffuse")
        self.glMaterial_SamplerSpecular = GLUtils.glGetUniform(self.shader_program, "material.sampler_specular")
        self.glMaterial_SamplerSpecularExp = GLUtils.glGetUniform(self.shader_program, "material.sampler_specularExp")
        self.glMaterial_SamplerDissolve = GLUtils.glGetUniform(self.shader_program, "material.sampler_dissolve")
        self.glMaterial_SamplerBump = GLUtils.glGetUniform(self.shader_program, "material.sampler_bump")
        self.glMaterial_SamplerDisplacement = GLUtils.glGetUniform(self.shader_program, "material.sampler_displacement")

        self.glMaterial_HasTextureAmbient = GLUtils.glGetUniform(self.shader_program, "material.has_texture_ambient")
        self.glMaterial_HasTextureDiffuse = GLUtils.glGetUniform(self.shader_program, "material.has_texture_diffuse")
        self.glMaterial_HasTextureSpecular = GLUtils.glGetUniform(self.shader_program, "material.has_texture_specular")
        self.glMaterial_HasTextureSpecularExp = GLUtils.glGetUniform(self.shader_program, "material.has_texture_specularExp")
        self.glMaterial_HasTextureDissolve = GLUtils.glGetUniform(self.shader_program, "material.has_texture_dissolve")
        self.glMaterial_HasTextureBump = GLUtils.glGetUniform(self.shader_program, "material.has_texture_bump")
        self.glMaterial_HasTextureDisplacement = GLUtils.glGetUniform(self.shader_program, "material.has_texture_displacement")

        # effects - gaussian blur
        self.glEffect_GB_W = GLUtils.glGetUniform(self.shader_program, "effect_GBlur.gauss_w")
        self.glEffect_GB_Radius = GLUtils.glGetUniform(self.shader_program, "effect_GBlur.gauss_radius")
        self.glEffect_GB_Mode = GLUtils.glGetUniform(self.shader_program, "effect_GBlur.gauss_mode")

        # effects - bloom
        self.glEffect_Bloom_doBloom = GLUtils.glGetUniform(self.shader_program, "effect_Bloom.doBloom")
        self.glEffect_Bloom_WeightA = GLUtils.glGetUniform(self.shader_program, "effect_Bloom.bloom_WeightA")
        self.glEffect_Bloom_WeightB = GLUtils.glGetUniform(self.shader_program, "effect_Bloom.bloom_WeightB")
        self.glEffect_Bloom_WeightC = GLUtils.glGetUniform(self.shader_program, "effect_Bloom.bloom_WeightC")
        self.glEffect_Bloom_WeightD = GLUtils.glGetUniform(self.shader_program, "effect_Bloom.bloom_WeightD")
        self.glEffect_Bloom_Vignette = GLUtils.glGetUniform(self.shader_program, "effect_Bloom.bloom_Vignette")
        self.glEffect_Bloom_VignetteAtt = GLUtils.glGetUniform(self.shader_program, "effect_Bloom.bloom_VignetteAtt")

        #﻿effects - tone mapping
        self.glEffect_ToneMapping_ACESFilmRec2020 = GLUtils.glGetUniform(self.shader_program, "fs_ACESFilmRec2020")

        GLUtils.printProgramLog(self.shader_program)
        return True

    def render(self, mo, selectedModel):
        self.matrixProjection = mo.matrixProjection
        self.matrixCamera = mo.camera.matrixCamera
        self.vecCameraPosition = mo.camera.cameraPosition
        self.uiAmbientLight = mo.Setting_UIAmbientLight
        self.lightingPass_DrawMode = mo.Setting_LightingPass_DrawMode
        self.render_models(mo, selectedModel)

    def render_models(self, mo, selectedModel):
        glUseProgram(self.shader_program)

        selectedModelID = -1
        for model in self.model_faces:

            if model.so_selectedYn:
                so_selectedYn = selectedModelID

            matrixModel = Matrix4x4(1.0)
            # grid
            matrixModel *= mo.grid.matrixModel
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
            model.matrixModel = self.matrixProjection * self.matrixCamera * matrixModel

            model.Setting_ModelViewSkin = mo.viewModelSkin
            model.lightSources = mo.lightSources

            mvpMatrix = self.matrixProjection * self.matrixCamera * matrixModel

            glUniformMatrix4fv(self.glVS_MVPMatrix, 1, GL_FALSE, MathOps.matrix_to_gl(mvpMatrix))

            matrixModelView = self.matrixCamera * matrixModel
            glUniformMatrix4fv(self.glFS_MMatrix, 1, GL_FALSE, MathOps.matrix_to_gl(matrixModelView))

            matrixNormal = MathOps.matrix_inverse_transpose(self.matrixCamera * matrixModel)
            matrixNormal = MathOps.to_matrix3(matrixNormal)
            glUniformMatrix3fv(self.glVS_NormalMatrix, 1, GL_FALSE, MathOps.matrix3_to_gl(matrixNormal))

            glUniformMatrix4fv(self.glVS_WorldMatrix, 1, GL_FALSE, MathOps.matrix_to_gl(matrixModel))

            # blending
            if model.mesh_model.ModelMaterial.transparency < 1.0 or model.Setting_Alpha < 1.0:
                glDisable(GL_DEPTH_TEST)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glEnable(GL_BLEND)
                if model.mesh_model.ModelMaterial.transparency < 1.0:
                    glUniform1f(self.glFS_AlphaBlending, model.mesh_model.ModelMaterial.transparency)
                else:
                    glUniform1f(self.glFS_AlphaBlending, model.Setting_Alpha)
            else:
                glEnable(GL_DEPTH_TEST)
                glDepthFunc(GL_LESS)
                glDisable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glUniform1f(self.glFS_AlphaBlending, 1.0)

            # depth color
            pc = 1.0
            if mo.Setting_PlaneClose >= 1.0:
                pc = mo.Setting_PlaneClose
            glUniform1f(self.glFS_planeClose, pc)
            glUniform1f(self.glFS_planeFar, mo.Setting_PlaneFar / 100.0)
            glUniform1i(self.glFS_showDepthColor, int(mo.Setting_Rendering_Depth))
            glUniform1i(self.glFS_ShadowPass, 0)

            # tessellation
            glUniform1i(self.glTCS_UseCullFace, int(model.Setting_UseCullFace))
            glUniform1i(self.glTCS_UseTessellation, model.Setting_UseTessellation)
            glUniform1i(self.glTCS_TessellationSubdivision, int(model.Setting_TessellationSubdivision))

            # cel - shading
            glUniform1i(self.glFS_CelShading, int(model.Setting_CelShading))

            # camera position
            glUniform3f(
                self.glFS_CameraPosition,
                mo.camera.cameraPosition.x,
                mo.camera.cameraPosition.y,
                mo.camera.cameraPosition.z
            )

            # screen size
            glUniform1f(self.glFS_ScreenResX, Settings.AppWindowWidth)
            glUniform1f(self.glFS_ScreenResY, Settings.AppWindowHeight)

            # Outline color
            glUniform3f(
                self.glFS_OutlineColor,
                model.so_outlineColor.r,
                model.so_outlineColor.g,
                model.so_outlineColor.b
            )

            # ambient color for editor
            glUniform3f(
                self.glFS_UIAmbient,
                mo.Setting_UIAmbientLight.r,
                mo.Setting_UIAmbientLight.g,
                mo.Setting_UIAmbientLight.b
            )

            # geometry shader displacement
            glUniform3f(
                self.glGS_GeomDisplacementLocation,
                model.displaceX['point'],
                model.displaceY['point'],
                model.displaceZ['point']
            )

            # mapping
            glUniform1i(self.glMaterial_ParallaxMapping, int(model.Setting_ParallaxMapping))

            # gamma correction
            glUniform1f(self.glFS_GammaCoeficient, mo.Setting_GammaCoeficient)

            # render skin
            glUniform1i(self.gl_ModelViewSkin,
                        int(model.Setting_ModelViewSkin.value))
            glUniform3f(
                self.glFS_solidSkin_materialColor,
                model.solidLightSkin_MaterialColor.r,
                model.solidLightSkin_MaterialColor.g,
                model.solidLightSkin_MaterialColor.b
            )

            # shadows
            glUniform1i(self.glFS_showShadows, 0)

            glUniform1i(self.solidLight.gl_InUse, 1)
            glUniform3f(self.solidLight.gl_Direction, mo.SolidLight_Direction.x, mo.SolidLight_Direction.y, mo.SolidLight_Direction.z)
            glUniform3f(self.solidLight.gl_Ambient, mo.SolidLight_Ambient.r, mo.SolidLight_Ambient.g, mo.SolidLight_Ambient.b)
            glUniform3f(self.solidLight.gl_Diffuse, mo.SolidLight_Diffuse.r, mo.SolidLight_Diffuse.g, mo.SolidLight_Diffuse.b)
            glUniform3f(self.solidLight.gl_Specular, mo.SolidLight_Specular.r, mo.SolidLight_Specular.g, mo.SolidLight_Specular.b)
            glUniform1f(self.solidLight.gl_StrengthAmbient, mo.SolidLight_Ambient_Strength)
            glUniform1f(self.solidLight.gl_StrengthDiffuse, mo.SolidLight_Diffuse_Strength)
            glUniform1f(self.solidLight.gl_StrengthSpecular, mo.SolidLight_Specular_Strength)

            lightsCount_Directional = 0
            lightsCount_Point = 0
            lightsCount_Spot = 0
            for i in range(len(model.lightSources)):
                light = model.lightSources[i]
                if light.type == Settings.LightSourceTypes.LightSourceType_Directional and \
                                lightsCount_Directional < self.GLSL_LightSourceNumber_Directional:
                    f = self.mfLights_Directional[lightsCount_Directional]
                    glUniform1i(f.gl_InUse, 1)

                    # light
                    glUniform3f(f.gl_Direction, light.positionX['point'], light.positionY['point'], light.positionZ['point'])

                    # color
                    glUniform3f(f.gl_Ambient, light.ambient.color.r, light.ambient.color.g, light.ambient.color.b)
                    glUniform3f(f.gl_Diffuse, light.diffuse.color.r, light.diffuse.color.g, light.diffuse.color.b)
                    glUniform3f(f.gl_Specular, light.specular.color.r, light.specular.color.g, light.specular.color.b)

                    # light factors
                    glUniform1f(f.gl_StrengthAmbient, light.ambient.strength)
                    glUniform1f(f.gl_StrengthDiffuse, light.diffuse.strength)
                    glUniform1f(f.gl_StrengthSpecular, light.specular.strength)

                    lightsCount_Directional += 1
                if light.type == Settings.LightSourceTypes.LightSourceType_Point and\
                    lightsCount_Point < self.GLSL_LightSourceNumber_Point:
                    f = self.mfLights_Point[lightsCount_Point]
                    glUniform1i(f.gl_InUse, 1)

                    # light
                    glUniform3f(f.gl_Position, light.matrixModel[3].x, light.matrixModel[3].y, light.matrixModel[3].z)

                    # factors﻿
                    glUniform1f(f.gl_Constant, light.lConstant['point'])
                    glUniform1f(f.gl_Linear, light.lLinear['point'])
                    glUniform1f(f.gl_Quadratic, light.lQuadratic['point'])

                    # color
                    glUniform3f(f.gl_Ambient, light.ambient.color.r, light.ambient.color.g, light.ambient.color.b)
                    glUniform3f(f.gl_Diffuse, light.diffuse.color.r, light.diffuse.color.g, light.diffuse.color.b)
                    glUniform3f(f.gl_Specular, light.specular.color.r, light.specular.color.g, light.specular.color.b)

                    # light factors
                    glUniform1f(f.gl_StrengthAmbient, light.ambient.strength)
                    glUniform1f(f.gl_StrengthDiffuse, light.diffuse.strength)
                    glUniform1f(f.gl_StrengthSpecular, light.specular.strength)

                    lightsCount_Point += 1
                if light.type == Settings.LightSourceTypes.LightSourceType_Spot and\
                    lightsCount_Spot < self.GLSL_LightSourceNumber_Spot:
                    f = self.mfLights_Spot[lightsCount_Spot]
                    glUniform1i(f.gl_InUse, 1)

                    # light
                    glUniform3f(f.gl_Direction, light.positionX['point'], light.positionY['point'], light.positionZ['point'])
                    glUniform3f(f.gl_Position, light.matrixModel[3].x, light.matrixModel[3].y, light.matrixModel[3].z)

                    # cutoff
                    glUniform1f(f.gl_CutOff, cos(radians(light.lCutOff['point'])))
                    glUniform1f(f.gl_OuterCutOff, cos(radians(light.lOuterCutOff['point'])))

                    # factors﻿
                    glUniform1f(f.gl_Constant, light.lConstant['point'])
                    glUniform1f(f.gl_Linear, light.lLinear['point'])
                    glUniform1f(f.gl_Quadratic, light.lQuadratic['point'])

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

            # material
            glUniform1f(self.glMaterial_Refraction, model.Setting_MaterialRefraction['point'])
            glUniform1f(self.glMaterial_SpecularExp, model.Setting_MaterialSpecularExp['point'])
            glUniform1i(self.glMaterial_IlluminationModel, int(model.materialIlluminationModel))
            glUniform1f(self.glMaterial_HeightScale, model.displacementHeightScale['point'])
            glUniform3f(self.glMaterial_Ambient,
                        model.materialAmbient.color.r,
                        model.materialAmbient.color.g,
                        model.materialAmbient.color.b)
            glUniform3f(self.glMaterial_Diffuse,
                        model.materialDiffuse.color.r,
                        model.materialDiffuse.color.g,
                        model.materialDiffuse.color.b)
            glUniform3f(self.glMaterial_Specular,
                        model.materialSpecular.color.r,
                        model.materialSpecular.color.g,
                        model.materialSpecular.color.b)
            glUniform3f(self.glMaterial_Emission,
                        model.materialEmission.color.r,
                        model.materialEmission.color.g,
                        model.materialEmission.color.b)

            # textures - ambient
            if model.vbo_tex_ambient is not None and\
                model.mesh_model.ModelMaterial.texture_ambient.UseTexture:
                glUniform1i(self.glMaterial_HasTextureAmbient, 1)
                glUniform1i(self.glMaterial_SamplerAmbient, 0)
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, model.vbo_tex_ambient)
            else:
                glUniform1i(self.glMaterial_HasTextureAmbient, 0)

            # textures - diffuse
            if model.vbo_tex_diffuse is not None and\
                model.mesh_model.ModelMaterial.texture_diffuse.UseTexture:
                glUniform1i(self.glMaterial_HasTextureDiffuse, 1)
                glUniform1i(self.glMaterial_SamplerDiffuse, 1)
                glActiveTexture(GL_TEXTURE1)
                glBindTexture(GL_TEXTURE_2D, model.vbo_tex_diffuse)
            else:
                glUniform1i(self.glMaterial_HasTextureDiffuse, 0)

            # textures - specular
            if model.vbo_tex_specular is not None and\
                model.mesh_model.ModelMaterial.texture_specular.UseTexture:
                glUniform1i(self.glMaterial_HasTextureSpecular, 1)
                glUniform1i(self.glMaterial_SamplerSpecular, 2)
                glActiveTexture(GL_TEXTURE2)
                glBindTexture(GL_TEXTURE_2D, model.vbo_tex_specular)
            else:
                glUniform1i(self.glMaterial_HasTextureSpecular, 0)

            # textures - specular exp
            if model.vbo_tex_specular_exp is not None and\
                model.mesh_model.ModelMaterial.texture_specular_exp.UseTexture:
                glUniform1i(self.glMaterial_HasTextureSpecularExp, 1)
                glUniform1i(self.glMaterial_SamplerSpecularExp, 3)
                glActiveTexture(GL_TEXTURE3)
                glBindTexture(GL_TEXTURE_2D, model.vbo_tex_specular_exp)
            else:
                glUniform1i(self.glMaterial_HasTextureSpecularExp, 0)

            # textures - dissolve
            if model.vbo_tex_dissolve is not None and\
                    model.mesh_model.ModelMaterial.texture_dissolve.UseTexture:
                glUniform1i(self.glMaterial_HasTextureDissolve, 1)
                glUniform1i(self.glMaterial_SamplerDissolve, 4)
                glActiveTexture(GL_TEXTURE4)
                glBindTexture(GL_TEXTURE_2D, model.vbo_tex_dissolve)
            else:
                glUniform1i(self.glMaterial_HasTextureDissolve, 0)

            # textures - normal
            if model.vbo_tex_normal is not None and\
                    model.mesh_model.ModelMaterial.texture_normal.UseTexture:
                glUniform1i(self.glMaterial_HasTextureBump, 1)
                glUniform1i(self.glMaterial_SamplerBump, 5)
                glActiveTexture(GL_TEXTURE5)
                glBindTexture(GL_TEXTURE_2D, model.vbo_tex_normal)
            else:
                glUniform1i(self.glMaterial_HasTextureBump, 0)

            # textures - displacement
            if model.vbo_tex_displacement is not None and\
                model.mesh_model.ModelMaterial.texture_displacement.UseTexture:
                glUniform1i(self.glMaterial_HasTextureDisplacement, 1)
                glUniform1i(self.glMaterial_SamplerDisplacement, 6)
                glActiveTexture(GL_TEXTURE6)
                glBindTexture(GL_TEXTURE_2D, model.vbo_tex_displacement)
            else:
                glUniform1i(self.glMaterial_HasTextureDisplacement, 0)

            # effects - gaussian blur
            glUniform1i(self.glEffect_GB_Mode, model.Effect_GBlur_Mode - 1)
            glUniform1f(self.glEffect_GB_W, model.Effect_GBlur_Width['point'])
            glUniform1f(self.glEffect_GB_Radius, model.Effect_GBlur_Radius['point'])

            # effects - bloom
            # TODO: Bloom effect
            glUniform1i(self.glEffect_Bloom_doBloom, model.Effect_Bloom_doBloom)
            glUniform1f(self.glEffect_Bloom_WeightA, model.Effect_Bloom_WeightA)
            glUniform1f(self.glEffect_Bloom_WeightB, model.Effect_Bloom_WeightB)
            glUniform1f(self.glEffect_Bloom_WeightC, model.Effect_Bloom_WeightC)
            glUniform1f(self.glEffect_Bloom_WeightD, model.Effect_Bloom_WeightD)
            glUniform1f(self.glEffect_Bloom_Vignette, model.Effect_Bloom_Vignette)
            glUniform1f(self.glEffect_Bloom_VignetteAtt, model.Effect_Bloom_VignetteAtt)

            # effects - tone mapping
            glUniform1i(self.glEffect_ToneMapping_ACESFilmRec2020, int(model.Effect_ToneMapping_ACESFilmRec2020))

            # border
            glUniform1f(self.glVS_IsBorder, 0.0)

            # render VAO
            model.render(True)

        glUseProgram(0)
