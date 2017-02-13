# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import glfw


class ControlsManager():
    def __init__(self):
        self.gameIsRunning = True
        self.keyPressed_ESC = False
        self.keyPressed_DELETE = False
        self.mouseButton_LEFT = False
        self.mouseButton_MIDDLE = False
        self.mouseButton_RIGHT = False
        self.mouseScroll_Moving = False
        self.keyPressed_LALT = False
        self.keyPressed_LSHIFT = False
        self.keyPressed_LCTRL = False
        self.keyPressed_RALT = False
        self.keyPressed_RSHIFT = False
        self.keyPressed_RCTRL = False
        self.keyPresset_TAB = False
        self.mouseWheel = {'x': 0, 'y': 0}
        self.mousePosition = {'x': 0, 'y': 0}


    def init_handlers(self, glfw_window):
        glfw.set_scroll_callback(glfw_window, self.glfw_on_mouse_scroll_callback)
        glfw.set_mouse_button_callback(glfw_window, self.glfw_mouse_button_callback)
        glfw.set_cursor_pos_callback(glfw_window, self.glfw_mouse_cursor_pos_callback)
        glfw.set_key_callback(glfw_window, self.glfw_key_callback)


    def glfw_key_callback(self, window, key, scancode, action, mods):
        self.keyPressed_ESC = False
        self.keyPressed_DELETE = False
        self.keyPressed_LALT = (mods == glfw.MOD_ALT) & (key == glfw.KEY_LEFT_ALT)
        self.keyPressed_LSHIFT = (mods == glfw.MOD_SHIFT) and (key == glfw.KEY_LEFT_SHIFT)
        self.keyPressed_LCTRL = (mods == glfw.MOD_CONTROL) and (key == glfw.KEY_LEFT_CONTROL)
        self.keyPressed_RALT = (mods == glfw.MOD_ALT) & (key == glfw.KEY_RIGHT_ALT)
        self.keyPressed_RSHIFT = (mods == glfw.MOD_SHIFT) and (key == glfw.KEY_RIGHT_SHIFT)
        self.keyPressed_RCTRL = (mods == glfw.MOD_CONTROL) and (key == glfw.KEY_RIGHT_CONTROL)

        if action == glfw.KEY_DOWN:
            if key == glfw.KEY_ESCAPE:
                self.keyPressed_ESC = True
                self.keyPressed_DELETE = False
                self.mouseButton_LEFT = False
                self.mouseButton_MIDDLE = False
                self.mouseButton_RIGHT = False
                self.mouseScroll_Moving = False
                self.mouseGoLeft = False
                self.mouseGoRight = False
                self.mouseGoUp = False
                self.mouseGoDown = False
            if key == glfw.KEY_DELETE:
                self.keyPressed_ESC = False
                self.keyPressed_DELETE = True
                self.mouseButton_LEFT = False
                self.mouseButton_MIDDLE = False
                self.mouseButton_RIGHT = False
                self.mouseScroll_Moving = False
                self.mouseGoLeft = False
                self.mouseGoRight = False
                self.mouseGoUp = False
                self.mouseGoDown = False
            if key == glfw.KEY_TAB:
                self.keyPressed_ESC = True
                self.keyPressed_DELETE = False
                self.keyPresset_TAB = not self.keyPresset_TAB
                self.mouseButton_LEFT = False
                self.mouseButton_MIDDLE = False
                self.mouseButton_RIGHT = False
                self.mouseScroll_Moving = False
                self.mouseGoLeft = False
                self.mouseGoRight = False
                self.mouseGoUp = False
                self.mouseGoDown = False


    def glfw_mouse_cursor_pos_callback(self, window, pos_x, pos_y):
        self.mousePosition['x'] = pos_x
        self.mousePosition['y'] = pos_y


    def glfw_on_mouse_scroll_callback(self, window, x_offset, y_offset):
        self.reset_mouse_scroll()
        self.mouseWheel['x'] = x_offset
        self.mouseWheel['y'] = y_offset


    def reset_mouse_scroll(self):
        self.mouseWheel = {'x': 0, 'y': 0}


    def glfw_mouse_button_callback(self, window, button, action, mods):
        if glfw.PRESS:
            self.mouseButton_LEFT = False
            self.mouseButton_MIDDLE = False
            self.mouseButton_RIGHT = False

            self.mouseButton_LEFT = (button == glfw.MOUSE_BUTTON_LEFT)
            self.mouseButton_MIDDLE = (button == glfw.MOUSE_BUTTON_MIDDLE)
            self.mouseButton_RIGHT = (button == glfw.MOUSE_BUTTON_RIGHT)

        if glfw.RELEASE:
            self.mouseButton_LEFT = False
            self.mouseButton_MIDDLE = False
            self.mouseButton_RIGHT = False
