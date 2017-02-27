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
from gl_utils.objects.MaterialColor import MaterialColor
from maths import MathOps
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from maths.types.Matrix4x4 import Matrix4x4


class Light():

    def __init__(self):
        self.gl_mvp_matrix = -1
        self.gl_fs_useColor = -1
        self.gl_fs_color = -1
        self.gl_u_sampler = -1
        self.vbo_texture_diffuse = -1

        self.mesh_model = None
        self.title = ''
        self.description = ''
        self.showLampObject = True
        self.showLampDirection = False
        self.showInWire = False
        self.turnOff_Position = False
        self.type = Settings.LightSourceTypes.LightSourceType_Directional

        self.positionX = {'animate': False, 'point': .0}
        self.positionY = {'animate': False, 'point': .0}
        self.positionZ = {'animate': False, 'point': .0}

        self.directionX = {'animate': False, 'point': .0}
        self.directionY = {'animate': False, 'point': .0}
        self.directionZ = {'animate': False, 'point': .0}

        self.scaleX = {'animate': False, 'point': 1.}
        self.scaleY = {'animate': False, 'point': 1.}
        self.scaleZ = {'animate': False, 'point': 1.}

        self.rotateX = {'animate': False, 'point': .0}
        self.rotateY = {'animate': False, 'point': .0}
        self.rotateZ = {'animate': False, 'point': .0}

        self.rotateCenterX = {'animate': False, 'point': .0}
        self.rotateCenterY = {'animate': False, 'point': .0}
        self.rotateCenterZ = {'animate': False, 'point': .0}

        self.ambient = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.diffuse = MaterialColor(False, False, 1.0, Vector3(1.0))
        self.specular = MaterialColor(False, False, 1.0, Vector3(1.0))

        self.lCutOff = {'animate': False, 'point': .0}
        self.lOuterCutOff = {'animate': False, 'point': .0}
        self.lConstant = {'animate': False, 'point': .0}
        self.lLinear = {'animate': False, 'point': .0}
        self.lQuadratic = {'animate': False, 'point': .0}

        self.matrixModel = Matrix4x4(1.0)

    def init_properties(self, lightType):
        self.mesh_model = None
        self.title = ''
        self.description = ''
        self.showLampObject = True
        self.showLampDirection = False
        self.showInWire = False
        self.turnOff_Position = False
        self.type = lightType

        self.positionX = {'animate': False, 'point': .0}
        self.positionY = {'animate': False, 'point': 5.0}
        self.positionZ = {'animate': False, 'point': .0}

        self.directionX = {'animate': False, 'point': .0}
        self.directionY = {'animate': False, 'point': 1.0}
        self.directionZ = {'animate': False, 'point': .0}

        self.scaleX = {'animate': False, 'point': 1.}
        self.scaleY = {'animate': False, 'point': 1.}
        self.scaleZ = {'animate': False, 'point': 1.}

        self.rotateX = {'animate': False, 'point': .0}
        self.rotateY = {'animate': False, 'point': .0}
        self.rotateZ = {'animate': False, 'point': .0}

        self.rotateCenterX = {'animate': False, 'point': .0}
        self.rotateCenterY = {'animate': False, 'point': .0}
        self.rotateCenterZ = {'animate': False, 'point': .0}

        self.ambient = MaterialColor(False, False, 0.3, Vector3(1.0))
        self.diffuse = MaterialColor(False, False, 1.0, Vector3(1.0))

        if self.type == Settings.LightSourceTypes.LightSourceType_Directional:
            self.lConstant = {'animate': False, 'point': .0}
            self.lLinear = {'animate': False, 'point': .0}
            self.lQuadratic = {'animate': False, 'point': .0}
            self.specular = MaterialColor(False, False, .0, Vector3(1.0))
            self.lCutOff = {'animate': False, 'point': -180.0}
            self.lOuterCutOff = {'animate': False, 'point': 160.0}
        elif self.type == Settings.LightSourceTypes.LightSourceType_Point:
            self.lConstant = {'animate': False, 'point': .0}
            self.lLinear = {'animate': False, 'point': 0.2}
            self.lQuadratic = {'animate': False, 'point': 0.05}
            self.specular = MaterialColor(False, False, .0, Vector3(1.0))
            self.lCutOff = {'animate': False, 'point': -180.0}
            self.lOuterCutOff = {'animate': False, 'point': 160.0}
        elif self.type == Settings.LightSourceTypes.LightSourceType_Spot:
            self.lConstant = {'animate': False, 'point': 1.0}
            self.lLinear = {'animate': False, 'point': 0.09}
            self.lQuadratic = {'animate': False, 'point': 0.032}
            self.specular = MaterialColor(False, False, .0, Vector3(1.0))
            self.lCutOff = {'animate': False, 'point': -12.5}
            self.lOuterCutOff = {'animate': False, 'point': 15.0}

        self.matrixModel = Matrix4x4(1.0)

    def set_model(self, mesh_model):
        self.mesh_model = mesh_model

    def init_shader_program(self):
        file_vs = open('resources/shaders/light.vert', 'r', encoding='utf-8')
        vs_str = str(file_vs.read())
        file_fs = open('resources/shaders/light.frag', 'r', encoding='utf-8')
        fs_str = str(file_fs.read())

        self.shader_program = glCreateProgram()

        shader_compilation = True
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_VERTEX_SHADER, vs_str)
        shader_compilation &= GLUtils.compileAndAttachShader(self.shader_program, GL_FRAGMENT_SHADER, fs_str)

        if not shader_compilation:
            Settings.do_log("[Light] Shader compilation failed!")
            return False

        glLinkProgram(self.shader_program)
        if glGetProgramiv(self.shader_program, GL_LINK_STATUS) != GL_TRUE:
            Settings.do_log("[Light] Shader linking failed! " + str(glGetProgramInfoLog(self.shader_program)))
            return False

        self.gl_mvp_matrix = GLUtils.glGetUniform(self.shader_program, "u_MVPMatrix")
        self.gl_fs_useColor = GLUtils.glGetUniform(self.shader_program, "fs_useColor")
        self.gl_fs_color = GLUtils.glGetUniform(self.shader_program, "fs_color")
        self.gl_u_sampler = GLUtils.glGetUniform(self.shader_program, "u_sampler")

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

        if len(self.mesh_model.texture_coordinates) > 0:
            data_texCoords = numpy.array(self.mesh_model.texture_coordinates, dtype=numpy.float32)
            vboTextureCoordinates = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, vboTextureCoordinates)
            glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_texCoords), data_texCoords, GL_STATIC_DRAW)
            glVertexAttribPointer(2, 2, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(2)

        self.vbo_tex_diffuse = self.loadTexture(self.mesh_model.ModelMaterial.texture_diffuse, 'diffuse')

        # indices
        data_indices = numpy.array(self.mesh_model.indices, dtype=numpy.uint32)
        vboIndices = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vboIndices)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_indices), data_indices, GL_STATIC_DRAW)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glDeleteBuffers(3, [vboVertices, vboNormals, vboIndices])

    def loadTexture(self, texture, type):
        if texture is not None:
            if not texture.image_url == '':
                image_file = Settings.ApplicationAssetsPath + texture.image_url
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
                    return vbo_tex
                else:
                    Settings.do_log("[Light] - Can't load " + type + " texture image! File doesn't exist!")
        return None

    def render(self, matrixProjection, matrixCamera):
        if self.glVAO > 0 and self.showLampObject:
            glUseProgram(self.shader_program)

            self.matrixModel = Matrix4x4(1.0)

            # scale
            self.matrixModel = MathOps.matrix_scale(
                self.matrixModel,
                (self.scaleX['point'],
                 self.scaleY['point'],
                 self.scaleZ['point'])
            )

            # rotate
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateX['point'], Vector3(1, 0, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateY['point'], Vector3(0, 1, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateZ['point'], Vector3(0, 0, 1))
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))

            if not self.turnOff_Position:
                self.matrixModel = MathOps.matrix_translate(
                    self.matrixModel,
                    (self.positionX['point'],
                     self.positionY['point'],
                     self.positionZ['point'])
                )

            # rotate center
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateCenterX['point'], Vector3(1, 0, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateCenterY['point'], Vector3(0, 1, 0))
            self.matrixModel = MathOps.matrix_rotate(self.matrixModel, self.rotateCenterZ['point'], Vector3(0, 0, 1))
            self.matrixModel = MathOps.matrix_translate(self.matrixModel, Vector4(.0))

            if self.vbo_texture_diffuse > 0:
                glBindTexture(GL_TEXTURE_2D, self.vbo_texture_diffuse)

            mvpMatrix = matrixProjection * matrixCamera * self.matrixModel
            glUniformMatrix4fv(self.gl_mvp_matrix, 1, GL_FALSE, MathOps.matrix_to_gl(mvpMatrix))

            if self.vbo_texture_diffuse < 0:
                glUniform1i(self.gl_fs_useColor, True)
                glUniform3f(
                    self.gl_fs_color,
                    self.mesh_model.ModelMaterial.color_diffuse.r,
                    self.mesh_model.ModelMaterial.color_diffuse.g,
                    self.mesh_model.ModelMaterial.color_diffuse.b
                )

            glBindVertexArray(self.glVAO)
            if self.showInWire:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDrawElements(GL_TRIANGLES, self.mesh_model.countIndices, GL_UNSIGNED_INT, None)
            if self.showInWire:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glBindVertexArray(0)

            if self.vbo_texture_diffuse > 0:
                glBindTexture(GL_TEXTURE_2D, 0)

            glUseProgram(0)
