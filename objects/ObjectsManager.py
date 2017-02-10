"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from settings import Settings
from meshes.helpers.Camera import Camera
from meshes.helpers.AxisHelpers import AxisHelpers
from meshes.helpers.AxisSystem import AxisSystem
from meshes.helpers.CameraModel import CameraModel
from meshes.helpers.WorldGrid import WorldGrid
from parsers.OBJ.ParserObj import ParserObj
from OpenGL.GL import *
import numpy
from pyrr import Matrix44 as mat4


class ObjectsManager():
    def __init__(self):
        self.lightSources = []
        self.systemModels = {}
        self.viewModelSkin = Settings.ViewModelSkin.ViewModelSkin_Rendered

        self.matrixProjection = numpy.array(numpy.ones((4, 4)), dtype=numpy.float32)

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


    def render(self):
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glDisable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.matrixProjection = mat4.perspective_projection(
            self.Setting_FOV,
            float(self.Setting_RatioWidth / self.Setting_RatioHeight),
            self.Setting_PlaneClose,
            self.Setting_PlaneFar,
            dtype='f')

        # debug
        # self.matrixProjection[0][0] = 1.810660
        # self.matrixProjection[0][1] = 0.000000
        # self.matrixProjection[0][2] = 0.000000
        # self.matrixProjection[0][3] = 0.000000
        #
        # self.matrixProjection[1][0] = 0.000000
        # self.matrixProjection[1][1] = 2.414213
        # self.matrixProjection[1][2] = 0.000000
        # self.matrixProjection[1][3] = 0.000000
        #
        # self.matrixProjection[2][0] = 0.000000
        # self.matrixProjection[2][1] = 0.000000
        # self.matrixProjection[2][2] = -1.002002
        # self.matrixProjection[2][3] = -1.000000
        #
        # self.matrixProjection[3][0] = 0.000000
        # self.matrixProjection[3][1] = 0.000000
        # self.matrixProjection[3][2] = -2.002002
        # self.matrixProjection[3][3] = 0.000000

        self.camera.render()
        self.axis_system.render(self.matrixProjection, self.camera.matrixCamera)


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


    def init_manager(self):
        self.init_camera()
        self.init_cameraModel()
        self.init_grid()
        self.init_axis_system()
        self.init_axis_helpers()


    def init_camera(self):
        self.camera.init_properties()


    def init_cameraModel(self):
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


    def init_axis_helpers(self):
        self.axis_helpers_x_minus.set_model(self.systemModels["axis_x_minus"])
        self.axis_helpers_x_minus.init_shader_program()
        self.axis_helpers_x_minus.init_buffers()

        self.axis_helpers_x_plus.set_model(self.systemModels["axis_x_plus"])
        self.axis_helpers_x_plus.init_shader_program()
        self.axis_helpers_x_plus.init_buffers()

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
        self.parser = ParserObj()

        self.parser.parse_file('resources/gui/', 'light_directional.obj')
        self.systemModels["light_directional"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/gui/', 'light_point.obj')
        self.systemModels["light_point"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/gui/', 'light_spot.obj')
        self.systemModels["light_spot"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/gui/', 'camera.obj')
        self.systemModels["camera"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/axis_helpers/', 'x_plus.obj')
        self.systemModels["axis_x_plus"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/axis_helpers/', 'x_minus.obj')
        self.systemModels["axis_x_minus"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/axis_helpers/', 'y_plus.obj')
        self.systemModels["axis_y_plus"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/axis_helpers/', 'y_minus.obj')
        self.systemModels["axis_y_minus"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/axis_helpers/', 'z_plus.obj')
        self.systemModels["axis_z_plus"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]

        self.parser.parse_file('resources/axis_helpers/', 'z_minus.obj')
        self.systemModels["axis_z_minus"] = self.parser.mesh_models[list(self.parser.mesh_models.keys())[0]]
