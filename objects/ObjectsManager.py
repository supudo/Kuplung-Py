# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from collections import defaultdict
from OpenGL.GL import *
from settings import Settings
from meshes.helpers.Camera import Camera
from meshes.helpers.AxisHelpers import AxisHelpers
from meshes.helpers.AxisSystem import AxisSystem
from meshes.helpers.CameraModel import CameraModel
from meshes.helpers.Light import Light
from meshes.helpers.Skybox import Skybox
from meshes.helpers.WorldGrid import WorldGrid
from parsers.OBJ.AssimpObj import AssimpObj
from parsers.OBJ.ParserObj2 import ParserObj2
from maths import MathOps
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from maths.types.Matrix4x4 import Matrix4x4


class ObjectsManager():
    def __init__(self):
        self.lightSources = []
        self.systemModels = defaultdict(dict)

        self.viewModelSkin = Settings.ViewModelSkin.ViewModelSkin_Rendered

        self.matrixProjection = Matrix4x4()

        self.reset_settings()

        self.camera = Camera()
        self.grid = WorldGrid()
        self.camera_model = CameraModel()
        self.axis_system = AxisSystem()
        self.axis_helpers_x_minus = AxisHelpers()
        self.axis_helpers_x_plus = AxisHelpers()
        self.axis_helpers_y_minus = AxisHelpers()
        self.axis_helpers_y_plus = AxisHelpers()
        self.axis_helpers_z_minus = AxisHelpers()
        self.axis_helpers_z_plus = AxisHelpers()
        self.skybox = Skybox()

        self.Setting_FOV = 45.0
        self.Setting_RatioWidth = 4.0
        self.Setting_RatioHeight = 3.0
        self.Setting_PlaneClose = 1.0
        self.Setting_PlaneFar = 1000.0
        self.Setting_GridSize = 30
        self.Setting_GridUnitSize = 1
        self.Setting_FixedGridWorld = True
        self.Setting_ShowAxisHelpers = True
        self.Settings_ShowZAxis = True
        self.Setting_FixedGridWorld = True
        self.Setting_Rendering_Depth = False
        self.Setting_UIAmbientLight = Vector3(0.2)
        self.Setting_GammaCoeficient = 1.0
        self.viewModelSkin = Settings.ViewModelSkin.ViewModelSkin_Rendered
        self.Setting_OutlineColor = Vector4(1, 0, 0, 0)
        self.Setting_OutlineColorPickerOpen = False

        self.SolidLight_Direction = Vector3(0.0, 1.0, 0.0)
        self.SolidLight_MaterialColor = Vector3(0.7)
        self.SolidLight_MaterialColor_ColorPicker = False
        self.SolidLight_Ambient = Vector3(1.0)
        self.SolidLight_Diffuse = Vector3(1.0)
        self.SolidLight_Specular = Vector3(1.0)
        self.SolidLight_Ambient_Strength = 0.3
        self.SolidLight_Diffuse_Strength = 1.0
        self.SolidLight_Specular_Strength = 0.0
        self.SolidLight_Ambient_ColorPicker = False
        self.SolidLight_Diffuse_ColorPicker = False
        self.SolidLight_Specular_ColorPicker = False
        self.Setting_LightingPass_DrawMode = 0

        self.Setting_OutlineThickness = 1.0
        self.Setting_VertexSphere_Visible = False
        self.Setting_VertexSphere_IsSphere = True
        self.Setting_VertexSphere_ShowWireframes = True
        self.Setting_VertexSphere_Segments = 8
        self.Setting_VertexSphere_Radius = 0.5
        self.Setting_VertexSphere_Color = Vector4(1.0)
        self.Setting_VertexSphere_ColorPickerOpen = False
        self.Setting_Rendering_Depth = False
        self.Setting_DebugShadowTexture = False
        self.Setting_DeferredAmbientStrength = 0.1
        self.Setting_DeferredTestMode = False
        self.Setting_DeferredTestLights = True
        self.Setting_DeferredRandomizeLightPositions = False
        self.Setting_DeferredTestLightsNumber = 32
        self.Setting_Skybox = -1
        self.Setting_ShowSpaceship = False
        self.Setting_ShowTerrain = False

    def render(self, window):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glDisable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.matrixProjection = MathOps.perspective(
            self.Setting_FOV,
            self.Setting_RatioWidth / self.Setting_RatioHeight,
            self.Setting_PlaneClose,
            self.Setting_PlaneFar
        )

        self.camera.render()

        if Settings.AppShowAllVisualArtefacts:
            win_width, win_height = Settings.AppWindowWidth, Settings.AppWindowHeight
            self.axis_system.render(window, self.matrixProjection, self.camera.matrixCamera, win_width, win_height)

            if self.Setting_GridSize != self.grid.grid_size:
                self.grid.grid_size = self.Setting_GridSize
                self.grid.init_buffers(self.Setting_GridSize, 1)
            self.grid.render(self.matrixProjection, self.camera.matrixCamera, self.Settings_ShowZAxis)

            if self.Setting_ShowAxisHelpers:
                ahPosition = self.Setting_GridSize / 2

                self.axis_helpers_x_plus.render(self.matrixProjection, self.camera.matrixCamera, Vector3(ahPosition, .0, .0))
                self.axis_helpers_x_minus.render(self.matrixProjection, self.camera.matrixCamera, Vector3(-ahPosition, .0, .0))
                self.axis_helpers_y_minus.render(self.matrixProjection, self.camera.matrixCamera, Vector3(.0, -ahPosition, .0))
                self.axis_helpers_y_plus.render(self.matrixProjection, self.camera.matrixCamera, Vector3(.0, ahPosition, .0))
                self.axis_helpers_z_minus.render(self.matrixProjection, self.camera.matrixCamera, Vector3(.0, .0, -ahPosition))
                self.axis_helpers_z_plus.render(self.matrixProjection, self.camera.matrixCamera, Vector3(.0, .0, ahPosition))

            self.camera_model.render(self.matrixProjection, self.camera.matrixCamera, self.grid.matrixModel, self.Setting_FixedGridWorld)

            for light in self.lightSources:
                light.render(self.matrixProjection, self.camera.matrixCamera)

            if self.Setting_Skybox != self.skybox.Setting_Skybox_Item:
                self.skybox.init_buffers()
                self.Setting_Skybox = self.skybox.Setting_Skybox_Item
            self.skybox.render(self.camera.matrixCamera, self.Setting_PlaneClose, self.Setting_PlaneFar, self.Setting_FOV)

    def reset_properties_system(self):
        self.reset_settings()

        if self.camera is not None:
            self.camera.init_properties()
        if self.camera_model is not None:
            self.camera_model.init_properties()
        if self.grid is not None:
            self.grid.init_properties()
        if self.axis_system is not None:
            self.axis_system.init_properties()
        for i in range(len(self.lightSources)):
            self.lightSources[i].init_properties(self.lightSources[i].type)

    def reset_settings(self):
        self.Setting_FOV = 45.0
        self.Setting_RatioWidth = 4.0
        self.Setting_RatioHeight = 3.0
        self.Setting_PlaneClose = 1.0
        self.Setting_PlaneFar = 1000.0
        self.Setting_GridSize = 30
        self.Setting_GridUnitSize = 1
        self.Setting_FixedGridWorld = True
        self.Setting_ShowAxisHelpers = True
        self.Settings_ShowZAxis = True
        self.Setting_FixedGridWorld = True
        self.Setting_Rendering_Depth = False
        self.Setting_UIAmbientLight = Vector3(0.2)
        self.Setting_GammaCoeficient = 1.0
        self.SolidLight_Direction = Vector3(0.0, 1.0, 0.0)
        self.SolidLight_MaterialColor = Vector3(0.7)
        self.SolidLight_MaterialColor_ColorPicker = False
        self.Setting_OutlineColorPickerOpen = False
        self.Setting_OutlineColor = Vector4(1, 0, 0, 0)
        self.SolidLight_Ambient = Vector3(1.0)
        self.SolidLight_Diffuse = Vector3(1.0)
        self.SolidLight_Specular = Vector3(1.0)
        self.SolidLight_Ambient_Strength = 0.3
        self.SolidLight_Diffuse_Strength = 1.0
        self.SolidLight_Specular_Strength = 0.0
        self.SolidLight_Ambient_ColorPicker = False
        self.SolidLight_Diffuse_ColorPicker = False
        self.SolidLight_Specular_ColorPicker = False
        self.Setting_LightingPass_DrawMode = 0
        self.Setting_OutlineThickness = 1.0
        self.Setting_VertexSphere_Visible = False
        self.Setting_VertexSphere_IsSphere = True
        self.Setting_VertexSphere_ShowWireframes = True
        self.Setting_VertexSphere_Segments = 8
        self.Setting_VertexSphere_Radius = 0.5
        self.Setting_VertexSphere_Color = Vector4(1.0)
        self.Setting_VertexSphere_ColorPickerOpen = False
        self.Setting_Rendering_Depth = False
        self.Setting_DebugShadowTexture = False
        self.Setting_DeferredAmbientStrength = 0.1
        self.Setting_DeferredTestMode = False
        self.Setting_DeferredTestLights = True
        self.Setting_DeferredRandomizeLightPositions = False
        self.Setting_DeferredTestLightsNumber = 32
        self.Setting_Skybox = -1
        self.Setting_ShowSpaceship = False
        self.Setting_GenerateSpaceship = False
        self.Setting_ShowTerrain = False

    def init_manager(self):
        self.init_camera()
        self.init_camera_model()
        self.init_grid()
        self.init_axis_system()
        self.init_axis_helpers()
        self.init_skybox()

    def init_camera(self):
        self.camera.init_properties()

    def init_camera_model(self):
        self.camera_model.init_properties()
        self.camera_model.init_shader_program()
        self.camera_model.set_model(self.systemModels["camera"])
        self.camera_model.init_buffers()

    def init_grid(self):
        self.grid.init_properties()
        self.grid.init_shader_program()
        self.grid.init_buffers(self.Setting_GridSize, self.Setting_GridUnitSize)

    def init_axis_system(self):
        success = self.axis_system.init_shader_program()
        if success:
            self.axis_system.init_buffers()

    def init_skybox(self):
        self.skybox.init_properties(self.Setting_GridSize)
        success = self.skybox.init_buffers()
        if not success:
            Settings.do_log('[ObjectsManager] Skybox cannot be initialized!')

    def init_axis_helpers(self):
        self.axis_helpers_x_plus.set_model(self.systemModels["axis_x_plus"])
        self.axis_helpers_x_plus.init_shader_program()
        self.axis_helpers_x_plus.init_buffers()

        self.axis_helpers_x_minus.set_model(self.systemModels["axis_x_minus"])
        self.axis_helpers_x_minus.init_shader_program()
        self.axis_helpers_x_minus.init_buffers()

        self.axis_helpers_y_minus.set_model(self.systemModels["axis_y_minus"])
        self.axis_helpers_y_minus.init_shader_program()
        self.axis_helpers_y_minus.init_buffers()

        self.axis_helpers_y_plus.set_model(self.systemModels["axis_y_plus"])
        self.axis_helpers_y_plus.init_shader_program()
        self.axis_helpers_y_plus.init_buffers()

        self.axis_helpers_z_minus.set_model(self.systemModels["axis_z_minus"])
        self.axis_helpers_z_minus.init_shader_program()
        self.axis_helpers_z_minus.init_buffers()

        self.axis_helpers_z_plus.set_model(self.systemModels["axis_z_plus"])
        self.axis_helpers_z_plus.init_shader_program()
        self.axis_helpers_z_plus.init_buffers()

    def load_system_models(self):
        if Settings.ModelFileParser == Settings.ModelFileParserTypes.ModelFileParser_Own2 :
            self.parser = ParserObj2()
        else:
            self.parser = AssimpObj()

        self.parser.parse_file('resources/gui/', 'light_directional.obj')
        self.systemModels["light_directional"] = self.parser.mesh_models['LightDirectional']

        self.parser.parse_file('resources/gui/', 'light_point.obj')
        self.systemModels["light_point"] = self.parser.mesh_models['LightPoint']

        self.parser.parse_file('resources/gui/', 'light_spot.obj')
        self.systemModels["light_spot"] = self.parser.mesh_models['LightSpot']

        self.parser.parse_file('resources/gui/', 'camera.obj')
        self.systemModels["camera"] = self.parser.mesh_models['Camera']

        self.parser.parse_file('resources/axis_helpers/', 'x_plus.obj')
        self.systemModels["axis_x_plus"] = self.parser.mesh_models['XPlus']

        self.parser.parse_file('resources/axis_helpers/', 'x_minus.obj')
        self.systemModels["axis_x_minus"] = self.parser.mesh_models['XMinus']

        self.parser.parse_file('resources/axis_helpers/', 'y_plus.obj')
        self.systemModels["axis_y_plus"] = self.parser.mesh_models['YPlus']

        self.parser.parse_file('resources/axis_helpers/', 'y_minus.obj')
        self.systemModels["axis_y_minus"] = self.parser.mesh_models['YMinus']

        self.parser.parse_file('resources/axis_helpers/', 'z_plus.obj')
        self.systemModels["axis_z_plus"] = self.parser.mesh_models['ZPlus']

        self.parser.parse_file('resources/axis_helpers/', 'z_minus.obj')
        self.systemModels["axis_z_minus"] = self.parser.mesh_models['ZMinus']

    def add_light(self, lightType, title='', description=''):
        l = Light()
        l.type = lightType
        l.init_properties(lightType)
        l.title = title
        l.description = description
        l.set_model(self.systemModels[lightType.value[1]])
        if lightType == Settings.LightSourceTypes.LightSourceType_Directional:
            if title == '':
                l.title = 'Directional ' + str(len(self.lightSources) + 1)
            if description == '':
                l.description = 'Directional ' + str(len(self.lightSources) + 1)
        if lightType == Settings.LightSourceTypes.LightSourceType_Point:
            if title == '':
                l.title = 'Point ' + str(len(self.lightSources) + 1)
            if description == '':
                l.description = 'Point ' + str(len(self.lightSources) + 1)
        if lightType == Settings.LightSourceTypes.LightSourceType_Spot:
            if title == '':
                l.title = 'Spot ' + str(len(self.lightSources) + 1)
            if description == '':
                l.description = 'Spot ' + str(len(self.lightSources) + 1)
        l.init_shader_program()
        l.init_buffers()
        self.lightSources.append(l)

    def clear_all_lights(self):
        self.lightSources.clear()
