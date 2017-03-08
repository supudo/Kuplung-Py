# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
import time
from settings import Settings
from meshes.artefacts.StructuredVolumetricSampling import StructuredVolumetricSampling


class DialogSVS():
    def __init__(self):
        self.windowWidth = 0
        self.windowHeight = 0
        self.textureWidth = 0
        self.textureHeight = 0
        self.viewPaddingHorizontal = 20.0
        self.viewPaddingVertical = 40.0
        self.vboTexture = -1

        self.structured_Volumetric_Sampling = StructuredVolumetricSampling()
        self.structured_Volumetric_Sampling.initShaderProgram()
        self.structured_Volumetric_Sampling.initBuffers()
        self.vboTexture = self.structured_Volumetric_Sampling.initFBO(Settings.AppWindowWidth, Settings.AppWindowHeight, self.vboTexture)

    def render(self, is_opened):
        imgui.set_next_window_size(800, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(60, 80, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('Structured Volumetric Sampling', is_opened, imgui.WINDOW_SHOW_BORDERS)

        imgui_io = imgui.get_io()

        self.windowWidth = imgui.get_window_width()
        self.windowHeight = imgui.get_window_height()
        self.textureWidth = int(self.windowWidth - self.viewPaddingHorizontal)
        self.textureHeight = int(self.windowHeight - self.viewPaddingVertical)

        app_time = time.time() - Settings.ApplicationStartTime
        self.vboTexture = self.structured_Volumetric_Sampling.renderToTexture(imgui_io.mouse_pos.x, imgui_io.mouse_pos.y, app_time, self.vboTexture)

        imgui.image(self.vboTexture, self.textureWidth, self.textureHeight)

        imgui.end()

        return is_opened
