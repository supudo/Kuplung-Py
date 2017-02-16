# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
from settings import Settings


class DialogControlsGUI():


    def __init__(self):
        pass


    def render(self, is_opened):
        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position((300 * 2) + 200 , 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('GUI Controls', is_opened, imgui.WINDOW_SHOW_BORDERS)
        imgui.begin_child('tabs_list'.encode('utf-8'))

        imgui.end_child()
        imgui.end()

        return is_opened
