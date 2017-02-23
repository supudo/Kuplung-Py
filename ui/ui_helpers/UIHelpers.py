# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui

class UIHelpers():

    def __init__(self):
        pass

    def add_slider(self, title, idx, step, min, limit, show_animate=True,
                   animated_flag=False, animated_value=0.0,
                   do_minus=False, is_frame=True):
        if title != '':
            imgui.text(title)
        if show_animate:
            c_id = "##00" + str(idx)
            if animated_flag is not None:
                clicked, animated_flag = imgui.checkbox(c_id, animated_flag)
                if animated_flag:
                    pass # animate the value
            if imgui.is_item_hovered():
                imgui.set_tooltip('Animate ' + title)
            imgui.same_line()
        s_id = '##10' + str(idx)
        _, animated_value = imgui.slider_float(
            s_id, animated_value, min, limit, "%.0f", 1.0
        )
        return animated_value
