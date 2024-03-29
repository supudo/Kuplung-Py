# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import os
import numpy
from gl_utils.GLUtils import ObjectCoordinate
from OpenGL.GL import *
from OpenGL.arrays import ArrayDatatype
from PIL import Image
from settings import Settings
from maths import MathOps
from maths.types.Matrix4x4 import Matrix4x4
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from gl_utils.objects.MaterialColor import MaterialColor
from meshes.helpers.BoundingBox import BoundingBox


class ModelFace:

    def __init__(self):
        self.positionX = ObjectCoordinate(animate=False, point=0.0)
        self.positionY = ObjectCoordinate(animate=False, point=0.0)
        self.positionZ = ObjectCoordinate(animate=False, point=0.0)

        self.rotateX = ObjectCoordinate(animate=False, point=0.0)
        self.rotateY = ObjectCoordinate(animate=False, point=0.0)
        self.rotateZ = ObjectCoordinate(animate=False, point=0.0)

        self.scaleX = ObjectCoordinate(animate=False, point=1.0)
        self.scaleY = ObjectCoordinate(animate=False, point=1.0)
        self.scaleZ = ObjectCoordinate(animate=False, point=1.0)

        self.displaceX = ObjectCoordinate(animate=False, point=.0)
        self.displaceY = ObjectCoordinate(animate=False, point=.0)
        self.displaceZ = ObjectCoordinate(animate=False, point=.0)

        self.so_outlineColor = Vector4(1.0, 0.0, 0.0, 1.0)
        self.Setting_UseCullFace = False
        self.Setting_UseTessellation = True
        self.Setting_TessellationSubdivision = 1
        self.showMaterialEditor = False
        self.Setting_LightingPass_DrawMode = 2

        # light
        self.Setting_LightStrengthAmbient = 0.5
        self.Setting_LightStrengthDiffuse = 1.0
        self.Setting_LightStrengthSpecular = 0.5
        self.Setting_LightAmbient = Vector3(1.0, 1.0, 1.0)
        self.Setting_LightDiffuse = Vector3(1.0, 1.0, 1.0)
        self.Setting_LightSpecular = Vector3(1.0, 1.0, 1.0)

        # material
        self.Setting_MaterialRefraction = ObjectCoordinate(animate=False, point=.0)
        self.materialAmbient = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.materialDiffuse = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.materialSpecular = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.materialEmission = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.displacementHeightScale = ObjectCoordinate(animate=False, point=.0)
        self.Setting_ParallaxMapping = False

        # effects
        self.Effect_GBlur_Mode = -1
        self.Effect_GBlur_Radius = ObjectCoordinate(animate=False, point=.0)
        self.Effect_GBlur_Width = ObjectCoordinate(animate=False, point=.0)
        self.Effect_ToneMapping_ACESFilmRec2020 = False

        # gizmo controls
        self.Setting_Gizmo_Translate = False
        self.Setting_Gizmo_Rotate = False
        self.Setting_Gizmo_Scale = False

        self.matrixGrid = Matrix4x4(1.)
        self.matrixProjection = Matrix4x4(1.)
        self.matrixCamera = Matrix4x4(1.)
        self.matrixModel = Matrix4x4(1.)
        self.mesh_model = None

        self.Setting_Alpha = 1.0
        self.Setting_CelShading = False
        self.so_outlineColor = Vector4(1.0, 0.0, 0.0, 1.0)
        self.Setting_ParallaxMapping = False
        self.Setting_UseCullFace = False
        self.Setting_UseTessellation = True
        self.Setting_TessellationSubdivision = 1
        self.Setting_ModelViewSkin = Settings.ViewModelSkin.ViewModelSkin_Wireframe
        self.Setting_MaterialRefraction = ObjectCoordinate(animate=False, point=.0)
        self.Setting_MaterialSpecularExp = ObjectCoordinate(animate=False, point=.0)
        self.Setting_ScaleAllParts = True

        self.Effect_GBlur_Mode = -1
        self.Effect_GBlur_Radius = ObjectCoordinate(animate=False, point=.0)
        self.Effect_GBlur_Width = ObjectCoordinate(animate=False, point=.0)

        self.Effect_Bloom_doBloom = False
        self.Effect_Bloom_WeightA = 0.0
        self.Effect_Bloom_WeightB = 0.0
        self.Effect_Bloom_WeightC = 0.0
        self.Effect_Bloom_WeightD = 0.0
        self.Effect_Bloom_Vignette = 0.0
        self.Effect_Bloom_VignetteAtt = 0.0

        self.Effect_ToneMapping_ACESFilmRec2020 = False

        self.lightSources = []

        self.so_selectedYn = False
        self.so_outlineColor = Vector4(1.0, 0.0, 0.0, 1.0)
        self.so_outlineThickness = 1.0
        self.solidLightSkin_MaterialColor = Vector3(0, 0, 0)

        self.initBuffersAgain = False

        self.boundingBox = BoundingBox()

    def init_own(self, model):
        self.set_model(model)
        self.initBuffersAgain = False
        self.Settings_DeferredRender = False
        self.Settings_EditMode = False

        self.so_outlineColor = Vector4(1, 0, 0, 1)
        self.Setting_UseCullFace = False
        self.Setting_UseTessellation = True
        self.Setting_TessellationSubdivision = 1
        self.showMaterialEditor = False
        self.Setting_LightingPass_DrawMode = 2

        # light
        self.Setting_LightStrengthAmbient = 0.5
        self.Setting_LightStrengthDiffuse = 1.0
        self.Setting_LightStrengthSpecular = 0.5
        self.Setting_LightAmbient = Vector3(1.0, 1.0, 1.0)
        self.Setting_LightDiffuse = Vector3(1.0, 1.0, 1.0)
        self.Setting_LightSpecular = Vector3(1.0, 1.0, 1.0)

        # material
        self.Setting_MaterialRefraction = ObjectCoordinate(animate=False, point=self.mesh_model.ModelMaterial.optical_density)
        self.materialAmbient = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.materialDiffuse = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.materialSpecular = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.materialEmission = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.displacementHeightScale = ObjectCoordinate(animate=False, point=.0)
        self.Setting_ParallaxMapping = False

        # effects
        self.Effect_GBlur_Mode = -1
        self.Effect_GBlur_Radius = ObjectCoordinate(animate=False, point=.0)
        self.Effect_GBlur_Width = ObjectCoordinate(animate=False, point=.0)
        self.Effect_ToneMapping_ACESFilmRec2020 = False

        # gizmo controls
        self.Setting_Gizmo_Translate = False
        self.Setting_Gizmo_Rotate = False
        self.Setting_Gizmo_Scale = False

        self.init_buffers()

    def init_bounding_box(self):
        self.boundingBox.init_shader_program()
        self.boundingBox.init_buffers(self.mesh_model)

    def init_vertex_sphere(self):
        pass

    def set_model(self, model):
        self.mesh_model = model

    def initModelProperties(self):
        self.Setting_CelShading = False
        self.Setting_Wireframe = False
        self.Setting_Alpha = 1.0
        self.showMaterialEditor = False
        self.Settings_DeferredRender = False
        self.Setting_EditMode = False
        self.Setting_ScaleAllParts = True

        self.positionX = ObjectCoordinate(animate=False, point=0.0)
        self.positionY = ObjectCoordinate(animate=False, point=0.0)
        self.positionZ = ObjectCoordinate(animate=False, point=0.0)

        self.rotateX= ObjectCoordinate(animate=False, point=0.0)
        self.rotateY = ObjectCoordinate(animate=False, point=0.0)
        self.rotateZ = ObjectCoordinate(animate=False, point=0.0)

        self.scaleX = ObjectCoordinate(animate=False, point=1.0)
        self.scaleY = ObjectCoordinate(animate=False, point=1.0)
        self.scaleZ = ObjectCoordinate(animate=False, point=1.0)

        self.displaceX = ObjectCoordinate(animate=False, point=.0)
        self.displaceY = ObjectCoordinate(animate=False, point=.0)
        self.displaceZ = ObjectCoordinate(animate=False, point=.0)

        self.matrixModel = Matrix4x4(1.)

        self.Setting_MaterialRefraction = ObjectCoordinate(animate=False, point=self.mesh_model.ModelMaterial.optical_density)
        self.Setting_MaterialSpecularExp = ObjectCoordinate(animate=False, point=self.mesh_model.ModelMaterial.specular_exp)

        self.Setting_LightPosition = Vector3(.0)
        self.Setting_LightDirection = Vector3(.0)
        self.Setting_LightAmbient = Vector3(.0)
        self.Setting_LightDiffuse = Vector3(.0)
        self.Setting_LightSpecular = Vector3(.0)
        self.Setting_LightStrengthAmbient = 1.0
        self.Setting_LightStrengthDiffuse = 1.0
        self.Setting_LightStrengthSpecular = 1.0
        self.Setting_TessellationSubdivision = 1
        self.Setting_LightingPass_DrawMode = 1

        self.materialIlluminationModel = self.mesh_model.ModelMaterial.illumination_mode
        self.Setting_ParallaxMapping = False

        self.materialAmbient = MaterialColor(False, False, 1.0, self.mesh_model.ModelMaterial.color_ambient)
        self.materialDiffuse = MaterialColor(False, False, 1.0, self.mesh_model.ModelMaterial.color_diffuse)
        self.materialSpecular = MaterialColor(False, False, 1.0, self.mesh_model.ModelMaterial.color_specular)
        self.materialEmission = MaterialColor(False, False, 1.0, self.mesh_model.ModelMaterial.color_emission)
        self.displacementHeightScale = ObjectCoordinate(animate=False, point=.0)

        self.Effect_GBlur_Mode = -1
        self.Effect_GBlur_Radius = ObjectCoordinate(animate=False, point=.0)
        self.Effect_GBlur_Width = ObjectCoordinate(animate=False, point=.0)

        self.Effect_Bloom_doBloom = False
        self.Effect_Bloom_WeightA = 0.0
        self.Effect_Bloom_WeightB = 0.0
        self.Effect_Bloom_WeightC = 0.0
        self.Effect_Bloom_WeightD = 0.0
        self.Effect_Bloom_Vignette = 0.0
        self.Effect_Bloom_VignetteAtt = 0.0

        self.Effect_ToneMapping_ACESFilmRec2020 = False

        self.Setting_ShowShadows = True

        # gizmo controls
        self.Setting_Gizmo_Translate = False
        self.Setting_Gizmo_Rotate = False
        self.Setting_Gizmo_Scale = False

        self.so_selectedYn = False
        self.so_outlineColor = Vector4(1.0, 0.0, 0.0, 1.0)
        self.so_outlineThickness = 1.0
        self.solidLightSkin_MaterialColor = Vector3(0, 0, 0)

    def init_buffers(self):
        self.glVAO = glGenVertexArrays(1)
        glBindVertexArray(self.glVAO)

        vboTextureCoordinates = -1
        vboTangents = -1
        vboBitangents = -1

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

        # textures
        if self.mesh_model.countTextureCoordinates > 0:
            data_texCoords = numpy.array(self.mesh_model.texture_coordinates, dtype=numpy.float32)
            vboTextureCoordinates = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboTextureCoordinates)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_texCoords), data_texCoords, GL_STATIC_DRAW)
            glVertexAttribPointer(2, 2, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(2)

        self.vbo_tex_ambient = self.loadTexture(self.mesh_model.ModelMaterial.texture_ambient, 'ambient')
        self.vbo_tex_diffuse = self.loadTexture(self.mesh_model.ModelMaterial.texture_diffuse, 'diffuse')
        self.vbo_tex_normal = self.loadTexture(self.mesh_model.ModelMaterial.texture_normal, 'normal')
        self.vbo_tex_displacement = self.loadTexture(self.mesh_model.ModelMaterial.texture_displacement, 'displacement')
        self.vbo_tex_specular = self.loadTexture(self.mesh_model.ModelMaterial.texture_specular, 'specular')
        self.vbo_tex_specular_exp = self.loadTexture(self.mesh_model.ModelMaterial.texture_specular_exp, 'specular_exp')
        self.vbo_tex_dissolve = self.loadTexture(self.mesh_model.ModelMaterial.texture_dissolve, 'dissolve')

        # indices
        data_indices = numpy.array(self.mesh_model.indices, dtype=numpy.uint32)
        vboIndices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboIndices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_indices), data_indices, GL_STATIC_DRAW)

        # bumps
        if self.mesh_model.ModelMaterial.texture_normal.Image != '' and\
            self.mesh_model.countVertices > 0 and\
            self.mesh_model.countTextureCoordinates > 0 and\
            self.mesh_model.countNormals > 0:
            tangents, bitangents = MathOps.compute_tangent_basis(
                self.mesh_model.vertices,
                self.mesh_model.texture_coordinates,
                self.mesh_model.normals
            )

            # tangents
            data_tangents = numpy.array(tangents, dtype=numpy.float32)
            vboTangents = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboTangents)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_tangents), data_tangents, GL_STATIC_DRAW)
            glVertexAttribPointer(3, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(3)

            # bitangents
            data_bitangents = numpy.array(bitangents, dtype=numpy.float32)
            vboBitangents = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboBitangents)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_bitangents), data_bitangents, GL_STATIC_DRAW)
            glVertexAttribPointer(4, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(4)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(6,
                        [vboVertices,
                         vboNormals,
                         vboTextureCoordinates,
                         vboIndices,
                         vboTangents,
                         vboBitangents]
                        )

    def loadTexture(self, texture, type):
        if texture is not None:
            if not texture.Image == '':
                image_file = texture.Image
                if not os.path.exists(image_file):
                    image_file = Settings.ApplicationAssetsPath + image_file
                if os.path.exists(image_file):
                    texture_image = Image.open(image_file, 'r')
                    texture_image_data = numpy.array(list(texture_image.getdata()), numpy.uint8)
                    t_width = texture_image.width
                    t_height = texture_image.height
                    vbo_tex = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, vbo_tex)
                    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
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
                    return vbo_tex
                else:
                    Settings.do_log("[ModelFace] - Can't load " + type + " texture image! File doesn't exist!")
        return None

    def render(self, use_tessellation):
        if self.glVAO > 0:
            if Settings.Setting_Wireframe or Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Wireframe or self.Setting_Wireframe:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBindVertexArray(self.glVAO)
            if use_tessellation:
                glDrawElements(GL_PATCHES, self.mesh_model.countIndices, GL_UNSIGNED_INT, None)
            else:
                glDrawElements(GL_TRIANGLES, self.mesh_model.countIndices, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)
            if Settings.Setting_Wireframe or Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Wireframe or self.Setting_Wireframe:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

            matrixBB = Matrix4x4(1.0)
            matrixBB = matrixBB * self.matrixProjection
            matrixBB = matrixBB * self.matrixCamera
            matrixBB = matrixBB * self.matrixModel

            if Settings.Setting_BoundingBoxShow and self.so_selectedYn:
                self.boundingBox.render(matrixBB, self.so_outlineColor)
