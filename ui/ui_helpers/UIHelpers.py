# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui

def add_slider(title, idx, step, min, limit, show_animate=True,
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
    return imgui.slider_float(s_id, animated_value, min, limit, "%.03f", 1.0)

def add_color4(title, color, animate):
    ce_id = '##101' + title
    imgui.text_colored(title, color.r, color.g, color.b, color.a)
    _, new_color = imgui.color_edit4(ce_id.encode('utf-8'), color.r, color.g, color.b, color.a, True)
    color.r = new_color[0]
    color.g = new_color[1]
    color.b = new_color[2]
    color.a = new_color[3]
    imgui.same_line()
    imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BORDER, 0, 0, 0, 0)
    #TODO: show color picker
    imgui.pop_style_color(4)
    imgui.new_line()
    return color, animate
