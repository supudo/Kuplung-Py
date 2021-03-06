# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui


class Log():

    def __init__(self):
        self.position_x = 10
        self.position_y = 10
        self.width = 300
        self.height = 200
        self.log_text = ''

    def draw_window(self, title, is_opened):
        imgui.set_next_window_size(self.width, self.height, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(self.position_x, self.position_y, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin(title, is_opened, 0)

        btn_clear_pressed = imgui.button('Clear')

        imgui.separator()

        imgui.begin_child('scrolling')
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, imgui.Vec2(0, 1))

        imgui.text_unformatted(self.log_text)

        imgui.pop_style_var(1)
        imgui.end_child()

        imgui.end()

        if btn_clear_pressed:
            self.clear_log()

        return is_opened

    def clear_log(self):
        self.log_text = ''

    def add_to_log(self, message):
        self.log_text = message + '\n' + self.log_text
