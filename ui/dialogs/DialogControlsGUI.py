# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
from ui.ui_helpers.UIHelpers import UIHelpers
from settings import Settings

class DialogControlsGUI():

    def __init__(self):
        self.selectedObject = 0
        self.selectedObjectLight = -1
        self.selectedTabScene = -1
        self.selectedTabGUICamera = -1
        self.selectedTabGUICameraModel = -1
        self.selectedTabGUIGrid = -1
        self.selectedTabGUILight = -1
        self.selectedTabGUITerrain = -1
        self.selectedTabGUISpaceship = -1
        self.lightRotateX = 0.0
        self.lightRotateY = 0.0
        self.lightRotateZ = 0.0

        self.heightmapWidth = 0
        self.heightmapHeight = 0

        self.newHeightmap = False
        self.generateNewTerrain = False
        self.generateNewSpaceship = False
        self.lockCameraWithLight = False

        self.height_top_panel = 170.0

        self.ui_helper = UIHelpers()

    def render(self, is_opened, managerObjects):
        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position((300 * 2) + 200 , 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('GUI Controls', is_opened, imgui.WINDOW_SHOW_BORDERS)

        # reset defaults button
        imgui.push_style_color(imgui.COLOR_BUTTON, .6, .1, .1, 1)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, .9, .1, .1, 1)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, .8, .2, .2, 1)
        if imgui.button('Reset values to default', -1, 0):
            managerObjects.reset_properties_system()
        imgui.pop_style_color(3)

        # GUI items listbox
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (6.0, 0.0))
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 255, 0, 0, 255)
        imgui.push_item_width(imgui.get_window_width() * 0.95)
        imgui.begin_child("Global Items".encode('utf-8'), 0.0, self.height_top_panel, True)

        items = ['General', 'Camera', 'Camera Model',
                 'Grid', 'Scene Lights', 'Skybox', 'Lights',
                 'Terrain', 'Artefacts']
        for i in range(len(items)):
            if i == 6:
                if len(managerObjects.lightSources) == 0:
                    imgui.selectable(items[i], False, 0, 0, 18.0)
                elif imgui.tree_node('Lights'):
                    for j in range(len(managerObjects.lightSources)):
                        imgui.bullet()
                        light_name = managerObjects.lightSources[j].title
                        _, light_sel = imgui.selectable(light_name, True if self.selectedObjectLight == j else False, 0, 0, 18.0)
                        if light_sel:
                            self.selectedObjectLight = j
                            self.selectedObject = i
                    imgui.tree_pop()
            else:
                _, sel = imgui.selectable(items[i], True if self.selectedObject == i else False, 0, 0, 18.0)
                if sel:
                    self.selectedObject = i
                    self.selectedObjectLight = -1

        imgui.end_child()
        imgui.pop_item_width()
        imgui.pop_style_color(1)
        imgui.pop_style_var(1)

        imgui.separator()

        # GUI items
        imgui.begin_child("﻿Properties Pane".encode('utf-8'), 0.0, 0.0, False)
        if self.selectedObject == 0:
            self.render_view_options(managerObjects)
            self.render_editor_artefacts(managerObjects)
            self.render_rays(managerObjects)
        elif self.selectedObject == 1:
            self.render_camera_lookat(managerObjects)
        imgui.end_child()

        imgui.end()

        return is_opened

    #region General
    def render_view_options(self, mo):
        opened, _ = imgui.collapsing_header('View Options')
        if opened:
            imgui.indent()
            mo.Setting_FOV = self.ui_helper.add_slider('Field of View', 1, 1.0, -180.0, 180.0, False, None, mo.Setting_FOV, True, True)
            imgui.separator()

            imgui.text('Ratio')
            if imgui.is_item_hovered():
                imgui.set_tooltip('W & H')
            _, mo.Setting_RatioWidth = imgui.slider_float('W##105', mo.Setting_RatioWidth, 0.0, 5.0, "%.0f", 1.0)
            _, mo.Setting_RatioHeight = imgui.slider_float('H##105', mo.Setting_RatioHeight, 0.0, 5.0, "%.0f", 1.0)
            imgui.separator()

            imgui.text('Planes')
            if imgui.is_item_hovered():
                imgui.set_tooltip('Far & Close')
            _, mo.Setting_PlaneClose = imgui.slider_float('Close##107', mo.Setting_PlaneClose, 0.0, 1.0, "%.1f", 1.0)
            _, mo.Setting_PlaneFar = imgui.slider_float('Far##108', mo.Setting_PlaneFar, 0.0, 1000.0, "%.1f", 1.0)
            imgui.separator()

            imgui.text('Gamma')
            if imgui.is_item_hovered():
                imgui.set_tooltip('Gamma Correction')
            _, mo.Setting_GammaCoeficient = imgui.slider_float('##109', mo.Setting_GammaCoeficient, 1.0, 4.0, "%.2f", 1.0)
            imgui.unindent()

    def render_editor_artefacts(self, mo):
        opened, _ = imgui.collapsing_header('Editor Artefacts')
        if opened:
            imgui.indent()
            _, mo.Setting_ShowAxisHelpers = imgui.checkbox('Axis Helpers', mo.Setting_ShowAxisHelpers)
            _, mo.Settings_ShowZAxis = imgui.checkbox('Z Axis', mo.Settings_ShowZAxis)
            imgui.unindent()

    def render_rays(self, mo):
        opened, _ = imgui.collapsing_header('Rays')
        if opened:
            imgui.indent()
            _, Settings.Setting_showPickRays = imgui.checkbox('Show Rays', Settings.Setting_showPickRays)
            _, Settings.Setting_showPickRaysSingle = imgui.checkbox('Single Ray', Settings.Setting_showPickRaysSingle)
            _, sel = imgui.collapsing_header('Add Ray', imgui.TREE_NODE_DEFAULT_OPEN)
            if sel:
                imgui.indent()
                imgui.text('Origin')
                if imgui.button('Set to camera position', imgui.get_window_width() * .75, .0):
                    Settings.Setting_mRayOriginX = mo.camera.positionX['point']
                    Settings.Setting_mRayOriginY = mo.camera.positionY['point']
                    Settings.Setting_mRayOriginZ = mo.camera.positionZ['point']
            imgui.unindent()
    #endregion

    #region Camera
    def render_camera_lookat(self, mo):
        imgui.text_colored('Look-At Matrix', 1, 0, 0, 1)
