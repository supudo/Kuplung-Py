# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from sdl2 import *
from settings import Settings


class ControlsManagerSDL2():
    def __init__(self):
        self.gameIsRunning = True
        self.keyPressed_ESC = False
        self.keyPressed_DELETE = False

        self.mouseButton_LEFT = False
        self.mouseButton_MIDDLE = False
        self.mouseButton_RIGHT = False

        self.keyPressed_LALT = False
        self.keyPressed_LSHIFT = False
        self.keyPressed_LCTRL = False
        self.keyPressed_RALT = False
        self.keyPressed_RSHIFT = False
        self.keyPressed_RCTRL = False

        self.keyPresset_TAB = False

        self.mouseWheel = {'x': 0, 'y': 0}
        self.mousePosition = {'x': 0, 'y': 0}
        self.xrel = 0
        self.yrel = 0

    def process_event(self, event):
        if event.type == SDL_QUIT:
            self.gameIsRunning = False
        if event.type == SDL_KEYDOWN:
            self.handle_input(event)
        if event.type == SDL_MOUSEBUTTONDOWN:
            self.handle_input(event)
        if event.type == SDL_MOUSEBUTTONUP:
            self.handle_input(event)
        if event.type == SDL_MOUSEMOTION:
            self.handle_input(event)
        if event.type == SDL_MOUSEWHEEL:
            self.handle_input(event)

    def handle_input(self, event):
        self.mouseWheel = {'x': 0, 'y': 0}
        self.mousePosition = {'x': 0, 'y': 0}

        self.handle_key_down(event)
        self.handle_mouse(event)
        self.handle_mouse_wheel(event)
        self.handle_mouse_motion(event)

    def handle_key_down(self, event):
        m = SDL_GetModState()
        self.keyPressed_ESC = False
        self.keyPressed_DELETE = False
        self.keyPressed_LALT = m & KMOD_LALT
        self.keyPressed_LSHIFT = m & KMOD_LSHIFT
        self.keyPressed_LCTRL = m & KMOD_LCTRL
        self.keyPressed_RALT = m & KMOD_RALT
        self.keyPressed_RSHIFT = m & KMOD_RSHIFT
        self.keyPressed_RCTRL = m & KMOD_RCTRL

        if event.type == SDL_KEYDOWN:
            if event.key.keysym.sym == SDLK_ESCAPE:
                self.keyPressed_ESC = True
                self.keyPressed_DELETE = False
                self.mouseButton_LEFT = False
                self.mouseButton_MIDDLE = False
                self.mouseButton_RIGHT = False
                self.mouseGoLeft = False
                self.mouseGoRight = False
                self.mouseGoUp = False
                self.mouseGoDown = False
            if event.key.keysym.sym == SDLK_DELETE:
                self.keyPressed_ESC = False
                self.keyPressed_DELETE = True
                self.mouseButton_LEFT = False
                self.mouseButton_MIDDLE = False
                self.mouseButton_RIGHT = False
                self.mouseGoLeft = False
                self.mouseGoRight = False
                self.mouseGoUp = False
                self.mouseGoDown = False
            if event.key.keysym.sym == SDLK_TAB:
                self.keyPressed_ESC = False
                self.keyPressed_DELETE = False
                self.keyPresset_TAB = not self.keyPresset_TAB
                self.mouseButton_LEFT = False
                self.mouseButton_MIDDLE = False
                self.mouseButton_RIGHT = False
                self.mouseGoLeft = False
                self.mouseGoRight = False
                self.mouseGoUp = False
                self.mouseGoDown = False

    def handle_mouse(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            self.mouseButton_LEFT = False
            self.mouseButton_MIDDLE = False
            self.mouseButton_RIGHT = False

            self.mouseButton_LEFT = event.button.button == SDL_BUTTON_LEFT
            self.mouseButton_MIDDLE = event.button.button == SDL_BUTTON_MIDDLE
            self.mouseButton_RIGHT = event.button.button == SDL_BUTTON_RIGHT
        if event.type == SDL_MOUSEBUTTONUP:
            self.mouseButton_LEFT = False
            self.mouseButton_MIDDLE = False
            self.mouseButton_RIGHT = False

    def handle_mouse_wheel(self, event):
        self.mouseWheel = {'x': 0, 'y': 0}
        if event.type == SDL_MOUSEWHEEL:
            self.mouseWheel['x'] = event.wheel.x
            self.mouseWheel['y'] = event.wheel.y
        self.mousePosition['x'] = event.motion.x
        self.mousePosition['y'] = event.motion.y

    def handle_mouse_motion(self, event):
        if event.type == SDL_MOUSEMOTION:
            self.mouseGoLeft = False
            self.mouseGoRight = False
            self.mouseGoUp = False
            self.mouseGoDown = False

            self.xrel = event.motion.xrel
            self.yrel = event.motion.yrel

            if event.motion.xrel < 0:
                self.mouseGoLeft = True
            elif event.motion.xrel > 0:
                self.mouseGoRight = True
            elif event.motion.yrel < 0:
                self.mouseGoUp = True
            elif event.motion.yrel > 0:
                self.mouseGoDown = True

    def reset_mouse_scroll(self):
        self.mouseWheel = {'x': 0, 'y': 0}

    def reset_mouse_motion(self):
        self.mouse_rel_x = 0
        self.mouse_rel_y = 0
        self.mouseGoLeft = False
        self.mouseGoRight = False
        self.mouseGoUp = False
        self.mouseGoDown = False
