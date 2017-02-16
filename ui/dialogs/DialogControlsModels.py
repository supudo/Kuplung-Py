# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
from settings import Settings


class DialogControlsModels():


    def __init__(self):
        pass


    def render(self, delegate, is_opened):
        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(10, 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('Scene Settings', is_opened, imgui.WINDOW_SHOW_BORDERS)
        imgui.begin_child('tabs_list'.encode('utf-8'))

        self.draw_shapes_tab(delegate)

        imgui.end_child()
        imgui.end()

        return is_opened


    def draw_shapes_tab(self, delegate):
        simple_shapes = {
            "Triangle": Settings.ShapeTypes.ShapeType_Triangle,
            "Cone": Settings.ShapeTypes.ShapeType_Cone,
            "Cube": Settings.ShapeTypes.ShapeType_Cube,
            "Cylinder": Settings.ShapeTypes.ShapeType_Cylinder,
            "Grid": Settings.ShapeTypes.ShapeType_Grid,
            "Ico Sphere": Settings.ShapeTypes.ShapeType_IcoSphere,
            "Plane": Settings.ShapeTypes.ShapeType_Plane,
            "Torus": Settings.ShapeTypes.ShapeType_Torus,
            "Tube": Settings.ShapeTypes.ShapeType_Tube,
            "UV Sphere": Settings.ShapeTypes.ShapeType_UVSphere,
            "Monkey Head": Settings.ShapeTypes.ShapeType_MonkeyHead
        }
        for shape_name in simple_shapes:
            if imgui.button(shape_name, -1, 0):
                delegate.add_shape(simple_shapes[shape_name])

        imgui.separator()
        imgui.separator()

        complex_shapes = {
            "Epcot": Settings.ShapeTypes.ShapeType_Epcot,
            "Brick Wall": Settings.ShapeTypes.ShapeType_BrickWall,
            "Plane Objects": Settings.ShapeTypes.ShapeType_PlaneObjects,
            "Plane Objects - Large Plane": Settings.ShapeTypes.ShapeType_PlaneObjectsLargePlane,
            "Material Ball": Settings.ShapeTypes.ShapeType_MaterialBall,
            "Material Ball - Blender": Settings.ShapeTypes.ShapeType_MaterialBallBlender
        }
        for shape_name in complex_shapes:
            if imgui.button(shape_name, -1, 0):
                delegate.add_shape(complex_shapes[shape_name])

        imgui.separator()
        imgui.separator()

        lights = {
            "Directional (Sun)": Settings.LightSourceType.LightSourceType_Directional,
            "Point (Light bulb)": Settings.LightSourceType.LightSourceType_Point,
            "Spot (Flashlight)": Settings.LightSourceType.LightSourceType_Spot
        }
        for light_name in lights:
            if imgui.button(light_name, -1, 0):
                delegate.add_light(lights[light_name])
