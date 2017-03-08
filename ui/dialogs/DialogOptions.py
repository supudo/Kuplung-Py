# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
from ui.ui_helpers import UIHelpers
from settings import Settings

class DialogOptions():

    def __init__(self):
        self.ui_helper = UIHelpers
        self.parser_model = Settings.ModelFileParser.value
        self.rendering_types = Settings.Setting_RendererType.value

    def render(self, is_opened):
        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position((300 * 2) + 200 , 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('Options', is_opened, imgui.WINDOW_SHOW_BORDERS)

        opened, _ = imgui.collapsing_header('General', None, imgui.TREE_NODE_DEFAULT_OPEN)
        if opened:
            imgui.indent()
            _, Settings.ShowLogWindow = imgui.checkbox('Log Messages', Settings.ShowLogWindow)
            imgui.push_style_var(imgui.STYLE_CHILD_WINDOW_ROUNDING, 5.0)
            imgui.begin_child("RefreshRate".encode('utf-8'), 0.0, 98.0, True)
            imgui.text("Consumption Refresh Interval (in seconds, 0 - disabled)")
            _, Settings.Consumption_Interval_Memory = imgui.slider_int('Memory', Settings.Consumption_Interval_Memory, 0, 100, '%.f')
            _, Settings.Consumption_Interval_CPU = imgui.slider_int('CPU', Settings.Consumption_Interval_CPU, 0, 100, '%.f')
            imgui.end_child()
            imgui.pop_style_var()
            imgui.unindent()

        opened, _ = imgui.collapsing_header('Rendering')
        if opened:
            imgui.indent()
            rendering_engines = ['Forward', 'Forward with Shadow Mapping', 'Deferred']
            _, self.rendering_types = imgui.combo('Renderer', self.rendering_types, rendering_engines)
            Settings.Setting_RendererType = self.rendering_types

            parser_items = ['Kuplung Obj Parser 1.0', 'Kuplung Obj Parser 2.0', 'Assimp']
            _, self.parser_model = imgui.combo('Model Parser', self.parser_model, parser_items)
            Settings.ModelFileParser = self.parser_model
            imgui.unindent()

        opened, _ = imgui.collapsing_header('Look & Feel')
        if opened:
            imgui.indent()
            imgui.unindent()

        imgui.end()

        return is_opened
