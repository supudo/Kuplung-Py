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
        # shapes
        for shape in Settings.ShapeTypes:
            if shape.name != 'ShapeType_None' and shape.name != 'ShapeType_Separator':
                if imgui.button(shape.value[1], -1, 0):
                    delegate.add_shape(shape)
            if shape.name == 'ShapeType_Separator':
                imgui.separator()
                imgui.separator()

        imgui.separator()
        imgui.separator()

        # lights
        for light in Settings.LightSourceTypes:
            if imgui.button(light.value[0], -1, 0):
                delegate.add_light(light)
