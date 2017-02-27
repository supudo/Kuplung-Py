# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
from settings import Settings
from ui.ui_helpers import UIHelpers


class DialogControlsModels():

    def __init__(self):
        self.cmenu_deleteYn = False
        self.cmenu_renameModel = False

        self.showTextureWindow_Ambient = False
        self.showTexture_Ambient = False
        self.showTextureWindow_Diffuse = False
        self.showTexture_Diffuse = False
        self.showTextureWindow_Dissolve = False
        self.showTexture_Dissolve = False
        self.showTextureWindow_Bump = False
        self.showTexture_Bump = False
        self.showTextureWindow_Specular = False
        self.showTexture_Specular = False
        self.showTextureWindow_SpecularExp = False
        self.showTexture_SpecularExp = False
        self.showTextureWindow_Displacement = False
        self.showTexture_Displacement = False
        self.showUVEditor = False

        self.textureAmbient_Width = self.textureAmbient_Height = self.textureDiffuse_Width = self.textureDiffuse_Height = 0
        self.textureDissolve_Width = self.textureDissolve_Height = self.textureBump_Width = self.textureBump_Height = 0
        self.textureSpecular_Width = self.textureSpecular_Height = self.textureSpecularExp_Width = self.textureSpecularExp_Height = 0
        self.textureDisplacement_Width = self.textureDisplacement_Height = 0

        self.selectedObject = 0
        self.selectedTabScene = 0
        self.selectedTabGUICamera = 0
        self.selectedTabGUIGrid = 0
        self.selectedTabGUILight = 0
        self.selectedTabPanel = 1

        self.ui_helper = UIHelpers

    def render(self, delegate, is_opened, managerObjects, meshModelFaces, is_frame):
        self.is_frame = is_frame

        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(10, 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('Scene Settings', is_opened, imgui.WINDOW_SHOW_BORDERS)

        imgui.push_style_color(imgui.COLOR_BUTTON, 153, 68, 61, 255)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 178, 64, 53, 255)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 204, 54, 40, 255)
        tab_labels = ['Models', 'Create']
        tab_icons = ['ICON_MD_BUILD', 'ICON_MD_ADD']
        self.selectedTabPanel = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabPanel)
        imgui.pop_style_color(3)

        if self.selectedTabPanel == 0:
            if meshModelFaces is not None and len(meshModelFaces) > 0:
                self.render_models(meshModelFaces)
            else:
                imgui.text_colored('No models in the current scene.', 255, 0, 0, 255)
        else:
            self.render_create(delegate)

        imgui.end()

        return is_opened

    def render_create(self, delegate):
        # shapes
        for shape in Settings.ShapeTypes:
            if shape.name != 'ShapeType_None' and shape.name != 'ShapeType_Separator':
                if imgui.button(shape.value[1], -1, 0):
                    delegate.add_shape(shape)
            if shape.name == 'ShapeType_Separator':
                imgui.separator()
                imgui.separator()

        imgui.separator()
        imgui.separator()

        # lights
        for light in Settings.LightSourceTypes:
            if imgui.button(light.value[0], -1, 0):
                delegate.add_light(light)

    def render_models(self, meshModelFaces):
        pass
