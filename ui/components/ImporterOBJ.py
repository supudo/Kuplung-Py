# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
from settings import Settings


class ImporterOBJ():

    def __init__(self):
        self.position_x = 10
        self.position_y = 10
        self.width = 700
        self.height = 500
        self.parser_model = -1

    def draw_window(self, title, is_opened):
        imgui.set_next_window_size(self.width, self.height, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(self.position_x, self.position_y, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin(title, is_opened, imgui.WINDOW_SHOW_BORDERS)

        imgui.text('Select OBJ File')
        imgui.separator()
        imgui.text(Settings.Settings_CurrentFolder)
        imgui.separator()

        imgui.text('Parser Model:')
        imgui.same_line()
        parser_items = ['Kuplung Obj Parser 1.0', 'Kuplung Obj Parser 2.0', 'Assimp']
        _, self.parser_model = imgui.combo('##00392', self.parser_model, parser_items)
        Settings.ModelFileParser = self.parser_model

        imgui.separator()

        imgui.begin_child('scrolling'.encode('utf-8'))
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2(0, 1))

        # ....

        imgui.pop_style_var(1)
        imgui.end_child()

        imgui.end()

        return is_opened
