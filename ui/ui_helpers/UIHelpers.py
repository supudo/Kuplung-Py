# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
import _thread
import time
from settings import Settings

def add_slider(title, idx, step, min, limit, show_animate=True,
               animated_flag=False, animated_value=0.0,
               do_minus=False, is_frame=True):
    if title != '':
        imgui.text(title)
    if show_animate:
        c_id = "##00" + str(idx)
        if animated_flag is not None and show_animate:
            _, animated_flag = imgui.checkbox(c_id, animated_flag)
            if animated_flag:
                animate_value(is_frame, animated_flag, animated_value, step,
                              limit, do_minus)
        if imgui.is_item_hovered():
            imgui.set_tooltip('Animate ' + title)
        imgui.same_line()
    s_id = '##10' + str(idx)
    _, values = imgui.slider_float(s_id, animated_value, min, limit, "%.03f", 1.0)
    return animated_flag, values

def add_slider_control(title, idx, min, limit, value=0.0):
    if title != '':
        imgui.text(title)
    s_id = '##10' + str(idx)
    _, values = imgui.slider_float(s_id, value, min, limit, "%.03f", 1.0)
    return values

def add_int_slider_control(title, idx, min, limit, value=0):
    if title != '':
        imgui.text(title)
    s_id = '##10' + str(idx)
    _, values = imgui.slider_int(s_id, value, min, limit, "%.f")
    return values

def add_color3(title, color, animate):
    ce_id = '##101' + title
    imgui.text_colored(title, color.r, color.g, color.b, 255.0)
    _, new_color = imgui.color_edit3(ce_id, color.r, color.g, color.b)
    color.r = new_color[0]
    color.g = new_color[1]
    color.b = new_color[2]
    imgui.same_line()
    imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BORDER, 0, 0, 0, 0)
    # TODO: show color picker
    imgui.pop_style_color(4)
    imgui.new_line()
    return color, animate

def add_color4(title, color, animate):
    ce_id = '##101' + title
    imgui.text_colored(title, color.r, color.g, color.b, color.a)
    _, new_color = imgui.color_edit4(ce_id, color.r, color.g, color.b, color.a, True)
    color.r = new_color[0]
    color.g = new_color[1]
    color.b = new_color[2]
    color.a = new_color[3]
    imgui.same_line()
    imgui.push_style_color(imgui.COLOR_BUTTON, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0, 0, 0, 0)
    imgui.push_style_color(imgui.COLOR_BORDER, 0, 0, 0, 0)
    # TODO: show color picker
    imgui.pop_style_color(4)
    imgui.new_line()
    return color, animate

def add_controls_slider_same_line(title, idx, step, min, limit, show_animate,
                                  animated_flag, animated_value, do_minus,
                                  is_frame):
    if show_animate:
        c_id = "##00" + str(idx)
        _, animated_flag = imgui.checkbox(c_id, animated_flag)
        if animated_flag:
            animate_value(is_frame, animated_flag, animated_value, step,
                          limit, do_minus)
        if imgui.is_item_hovered():
            imgui.set_tooltip("Animate " + title)
        imgui.same_line()
    s_id = "##10" + str(idx)
    _, animated_value = imgui.slider_float(s_id, animated_value, min,
                                           limit, "%.03f", 1.0)
    imgui.same_line()
    imgui.text(title)
    return animated_flag, animated_value

def animate_value(isFrame, animatedFlag, animatedValue, step, limit, doMinus):
    try:
        # TODO: animate in thread
            # _thread.start_new_thread(
        #     animate_value_async,
        #     (1, isFrame, animatedFlag, animatedValue, step, limit, doMinus)
        # )
        pass
    except:
        Settings.do_log("[UIHelpers] Error: cannot start animating thread!")

def animate_value_async(delay, is_frame, animated_flag,
                        animated_value, step, limit, do_minus):
    while (animated_flag):
        if is_frame:
            v = animated_value
            v += step
            if v > limit:
                v = (-1 * limit) if do_minus else 0
                animated_value = v
            is_frame = False
            time.sleep(delay)


def draw_tabs(tabs_labels, tabs_icons, value_init, style_padding=10.0, font_scale=2.0):
    selected_item = value_init

    imgui.push_style_color(imgui.COLOR_BUTTON, 153 / 255, 68 / 255, 61 / 255, 255 / 255)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 178 / 255, 64 / 255, 53 / 255, 255 / 255)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 204 / 255, 54 / 255, 40 / 255, 255 / 255)
    imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (style_padding, style_padding))
    imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 2.0)
    imgui.set_window_font_scale(font_scale)

    for i in range(len(tabs_labels)):
        clicked = imgui.button(' ' + tabs_labels[i][0] + ' ')
        if imgui.is_item_hovered():
            imgui.set_tooltip(tabs_labels[i])
        if clicked:
            selected_item = i
        imgui.same_line()

    imgui.set_window_font_scale(1.0)
    imgui.pop_style_var(2)
    imgui.pop_style_color(3)

    imgui.new_line()

    return selected_item