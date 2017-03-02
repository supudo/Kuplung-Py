# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import imgui
from ui.ui_helpers import UIHelpers
from settings import Settings

class DialogControlsGUI():

    def __init__(self):
        self.selectedObject = 0
        self.selectedObjectLight = -1
        self.selectedTabScene = 0
        self.selectedTabGUICamera = 0
        self.selectedTabGUICameraModel = 0
        self.selectedTabGUIGrid = 0
        self.selectedTabGUILight = 0
        self.selectedTabGUITerrain = 0
        self.selectedTabGUISpaceship = 0
        self.selectedObjectArtefact = 0
        self.lightRotateX = 0.0
        self.lightRotateY = 0.0
        self.lightRotateZ = 0.0

        self.heightmapWidth = 0
        self.heightmapHeight = 0
        self.newHeightmap = False

        self.generateNewTerrain = False
        self.generateNewSpaceship = False
        self.lockCameraWithLight = False

        self.is_frame = True
        self.height_top_panel = 170.0
        self.ui_helper = UIHelpers

    def render(self, is_opened, mo, is_frame):
        self.is_frame = is_frame

        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position((300 * 2) + 200 , 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('GUI Controls', is_opened, imgui.WINDOW_SHOW_BORDERS)

        # reset defaults button
        imgui.push_style_color(imgui.COLOR_BUTTON, 153 / 255, 68 / 255, 61 / 255, 255 / 255)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 178 / 255, 64 / 255, 53 / 255, 255 / 255)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 204 / 255, 54 / 255, 40 / 255, 255 / 255)
        if imgui.button('Reset values to default', -1, 0):
            mo.reset_properties_system()
            if self.selectedObjectLight > -1:
                self.lightRotateX = mo.lightSources[self.selectedObjectLight].rotateX['point']
                self.lightRotateY = mo.lightSources[self.selectedObjectLight].rotateY['point']
                self.lightRotateZ = mo.lightSources[self.selectedObjectLight].rotateZ['point']
        imgui.pop_style_color(3)

        # GUI items listbox
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (10.0, 0.0))
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 255, 0, 0, 255)
        imgui.push_item_width(imgui.get_window_width() * 0.95)
        imgui.begin_child("Global Items".encode('utf-8'), 0.0, self.height_top_panel, True)

        items = ['General', 'Camera', 'Camera Model',
                 'Grid', 'Scene Lights', 'Skybox', 'Lights', 'Artefacts']
        for i in range(len(items)):
            if i == 6:
                if len(mo.lightSources) == 0:
                    imgui.indent()
                    imgui.selectable(items[i], False, 0, 0, 18.0)
                    imgui.unindent()
                    self.selectedObjectLight = -1
                    self.selectedObjectArtefact = -1
                else:
                    #TODO: add icon
                    opened = imgui.tree_node('Lights')
                    if opened:
                        for j in range(len(mo.lightSources)):
                            imgui.bullet()
                            light_name = mo.lightSources[j].title
                            _, light_sel = imgui.selectable(light_name, True if self.selectedObjectLight == j else False, 0, 0, 18.0)
                            if light_sel:
                                self.selectedObjectLight = j
                                self.selectedObject = i
                                self.selectedObjectArtefact = -1
                        imgui.tree_pop()
            elif i == 7:
                opened = imgui.tree_node('Artefacts')
                if opened:
                    imgui.bullet()
                    _, sel_terrain = imgui.selectable('Terrain', True if self.selectedObjectArtefact == 0 else False, 0, 0, 18.0)
                    if sel_terrain:
                        self.selectedObjectArtefact = 0
                        self.selectedObject = i
                        self.selectedObjectLight = -1
                    imgui.bullet()
                    _, sel_spaceship = imgui.selectable('Spaceship', True if self.selectedObjectArtefact == 1 else False, 0, 0, 18.0)
                    if sel_spaceship:
                        self.selectedObjectArtefact = 1
                        self.selectedObject = i
                        self.selectedObjectLight = -1
                    imgui.tree_pop()
            else:
                imgui.indent()
                _, sel = imgui.selectable(items[i], True if self.selectedObject == i else False, 0, 0, 18.0)
                if sel:
                    self.selectedObject = i
                    self.selectedObjectLight = -1
                    self.selectedObjectArtefact = -1
                imgui.unindent()

        imgui.end_child()
        imgui.pop_item_width()
        imgui.pop_style_color(1)
        imgui.pop_style_var(1)

        imgui.separator()

        # GUI items
        imgui.begin_child("﻿Properties Pane".encode('utf-8'), 0.0, 0.0, False)
        if self.selectedObject == 0:
            mo = self.render_general_view_options(mo)
            mo = self.render_general_editor_artefacts(mo)
            mo = self.render_general_rays(mo)
            mo = self.render_general_bounding_box(mo)
            mo = self.render_general_edit_mode(mo)
            mo = self.render_render_buffer(mo)
            if Settings.Setting_RendererType == Settings.InAppRendererType.InAppRendererType_Deferred:
                mo = self.render_defered_rendering_options(mo)
        elif self.selectedObject == 1:
            mo = self.render_camera(mo)
        elif self.selectedObject == 2:
            mo = self.render_camera_model(mo)
        elif self.selectedObject == 3:
            mo = self.render_grid(mo)
        elif self.selectedObject == 4:
            mo = self.render_scene_lights(mo)
        elif self.selectedObject == 5:
            mo = self.render_skybox(mo)
        elif self.selectedObject == 6:
            mo = self.render_lights(mo)
        elif self.selectedObject == 7:
            mo = self.render_artefacts(mo)
        imgui.end_child()

        imgui.end()

        if len(mo.lightSources) > 0 and self.selectedObjectLight > -1 and len(mo.lightSources) > self.selectedObjectLight:
            slp_x = mo.lightSources[self.selectedObjectLight].rotateX['point']
            slp_y = mo.lightSources[self.selectedObjectLight].rotateY['point']
            slp_z = mo.lightSources[self.selectedObjectLight].rotateZ['point']
            if self.lightRotateX < slp_x or self.lightRotateX > slp_x or\
                self.lightRotateY < slp_y or self.lightRotateY > slp_y or\
                self.lightRotateZ < slp_z or self.lightRotateZ > slp_z:
                mo.lightSources[self.selectedObjectLight].rotateX['point'] = self.lightRotateX
                mo.lightSources[self.selectedObjectLight].rotateY['point'] = self.lightRotateY
                mo.lightSources[self.selectedObjectLight].rotateZ['point'] = self.lightRotateZ

        return is_opened, mo

    #region General

    def render_general_view_options(self, mo):
        opened, _ = imgui.collapsing_header('View Options')
        if opened:
            imgui.indent()
            _, mo.Setting_FOV = self.ui_helper.add_slider('Field of View', 1, 1.0, -180.0, 180.0, False, None, mo.Setting_FOV, True, self.is_frame)
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
        return mo

    def render_general_editor_artefacts(self, mo):
        opened, _ = imgui.collapsing_header('Editor Artefacts')
        if opened:
            imgui.indent()
            _, mo.Setting_ShowAxisHelpers = imgui.checkbox('Axis Helpers', mo.Setting_ShowAxisHelpers)
            _, mo.Settings_ShowZAxis = imgui.checkbox('Z Axis', mo.Settings_ShowZAxis)
            imgui.unindent()
        return mo

    def render_general_rays(self, mo):
        opened, _ = imgui.collapsing_header('Rays')
        if opened:
            imgui.indent()
            _, Settings.Setting_showPickRays = imgui.checkbox('Show Rays', Settings.Setting_showPickRays)
            _, Settings.Setting_showPickRaysSingle = imgui.checkbox('Single Ray', Settings.Setting_showPickRaysSingle)
            opened_add_ray, _ = imgui.collapsing_header('Add Ray', None, imgui.TREE_NODE_DEFAULT_OPEN)
            if opened_add_ray:
                imgui.indent()
                imgui.text('Origin')
                if imgui.button('Set to camera position', imgui.get_window_width() * .75, .0):
                    Settings.Setting_mRayOriginX = mo.camera.positionX['point']
                    Settings.Setting_mRayOriginY = mo.camera.positionY['point']
                    Settings.Setting_mRayOriginZ = mo.camera.positionZ['point']
                # InputFloat for  Settings.mRayOriginX
                # InputFloat for  Settings.mRayOriginY
                # InputFloat for  Settings.mRayOriginZ
                _, Settings.Setting_mRayAnimate = imgui.checkbox('Animate', Settings.Setting_mRayAnimate)
                imgui.text('Direction')
                if Settings.Setting_mRayAnimate:
                    _, Settings.Setting_mRayDirectionX = imgui.slider_float('X##9930', Settings.Setting_mRayDirectionX, -1.0, 1.0, '%.3f', 1.0)
                    _, Settings.Setting_mRayDirectionY = imgui.slider_float('Y##9931', Settings.Setting_mRayDirectionY, -1.0, 1.0, '%.3f', 1.0)
                    _, Settings.Setting_mRayDirectionZ = imgui.slider_float('Z##9932', Settings.Setting_mRayDirectionZ, -1.0, 1.0, '%.3f', 1.0)
                else:
                    _, Settings.Setting_mRayDirectionX = imgui.slider_float('X##9930', Settings.Setting_mRayDirectionX, 0.0, 8.0, '%.3f', 1.0)
                    _, Settings.Setting_mRayDirectionY = imgui.slider_float('Y##9931', Settings.Setting_mRayDirectionY, 0.0, 8.0, '%.3f', 1.0)
                    _, Settings.Setting_mRayDirectionZ = imgui.slider_float('Z##9932', Settings.Setting_mRayDirectionZ, 0.0, 8.0, '%.3f', 1.0)
                if imgui.button('Draw', imgui.get_window_width() * 0.75, 0.0):
                    Settings.Setting_mRayDraw = True
                imgui.unindent()
            imgui.unindent()
        return mo

    def render_general_bounding_box(self, mo):
        opened, _ = imgui.collapsing_header('Bounding Box')
        if opened:
            imgui.indent()
            _, Settings.Setting_BoundingBoxShow = imgui.checkbox('Bounding Box##999', Settings.Setting_BoundingBoxShow)
            if Settings.Setting_BoundingBoxShow:
                changed, Settings.Setting_BoundingBoxPadding = self.ui_helper.add_slider('Padding', 3, 0.001, 0.0, 0.1, False, None, Settings.Setting_BoundingBoxPadding, True, self.is_frame)
                if changed:
                    Settings.Setting_BoundingBoxRefresh = True
                mo.Setting_OutlineColor, mo.Setting_OutlineColorPickerOpen = self.ui_helper.add_color4('Color', mo.Setting_OutlineColor, mo.Setting_OutlineColorPickerOpen)
                _, mo.Setting_OutlineThickness = self.ui_helper.add_slider('Thickness', 2, 1.01, 0.0, 2.0, False, None, mo.Setting_OutlineThickness, True, self.is_frame)
            imgui.unindent()
        return mo

    def render_general_edit_mode(self, mo):
        opened, _ = imgui.collapsing_header('Edit Mode')
        if opened:
            imgui.indent()
            imgui.text_colored('Manipualte mode:', 1, 0, 0, 1)
            imgui.begin_group()
            width = imgui.get_content_region_available_width() * 0.3

            for mode in Settings.GeometryEditMode:
                do_pop = False
                if Settings.Setting_GeometryEditMode == mode:
                    imgui.push_style_color(imgui.COLOR_BUTTON, 121 / 255.0, 5 / 255.0, 5 / 255.0, 1.0)
                    do_pop = True

                if imgui.button(mode.value[1], width, 0):
                    Settings.Setting_GeometryEditMode = mode

                if Settings.Setting_GeometryEditMode == mode and do_pop:
                    imgui.pop_style_color()

                imgui.same_line()

            imgui.end_group()

            imgui.separator()

            _, mo.Setting_VertexSphere_Visible = imgui.checkbox('Vertex Sphere', mo.Setting_VertexSphere_Visible)
            if mo.Setting_VertexSphere_Visible:
                _, mo.Setting_VertexSphere_IsSphere = imgui.checkbox('Sphere', mo.Setting_VertexSphere_IsSphere)
                _, mo.Setting_VertexSphere_ShowWireframes = imgui.checkbox('Wireframes', mo.Setting_VertexSphere_ShowWireframes)
                _, mo.Setting_VertexSphere_Segments = imgui.slider_int('Segments', mo.Setting_VertexSphere_Segments, 3, 32, '%.3f')
                _, mo.Setting_VertexSphere_Radius = self.ui_helper.add_slider('Radius', 1.0, 0.5, 0.0, 2.0, False, None, mo.Setting_VertexSphere_Radius, True, self.is_frame)
                mo.Setting_VertexSphere_Color, mo.Setting_VertexSphere_ColorPickerOpen = self.ui_helper.add_color4('Color', mo.Setting_VertexSphere_Color, mo.Setting_VertexSphere_ColorPickerOpen)

            imgui.unindent()
        return mo

    def render_render_buffer(self, mo):
        opened, _ = imgui.collapsing_header('Render Buffer')
        if opened:
            imgui.indent()
            imgui.text('Rendering View Options')
            if imgui.button('Depth Colors', -1, 0):
                mo.Setting_Rendering_Depth = not mo.Setting_Rendering_Depth
            if imgui.button('Shadow Texture', -1, 0):
                mo.Setting_DebugShadowTexture = not mo.Setting_DebugShadowTexture
            imgui.unindent()
        return mo

    def render_defered_rendering_options(self, mo):
        opened, _ = imgui.collapsing_header('Deferred Rendering')
        if opened:
            imgui.indent()
            imgui.text('Deferred Rendering')
            deferred_texture_items = ['Lighting', 'Position', 'Normal', 'Diffuse', 'Specular']
            _, mo.Setting_LightingPass_DrawMode = imgui.combo(
                "##110", mo.Setting_LightingPass_DrawMode, deferred_texture_items
            )
            imgui.text('Ambient Strength')
            _, mo.Setting_DeferredAmbientStrength = imgui.slider_float('##210', mo.Setting_DeferredAmbientStrength, 0.0, 1.0)
            mo.Setting_DeferredTestMode = imgui.checkbox('Test Mode', mo.Setting_DeferredTestMode)
            mo.Setting_DeferredTestLights = imgui.checkbox('Test Lights', mo.Setting_DeferredTestLights)
            imgui.separator()
            imgui.text('Number of test lights')
            _, mo.Setting_DeferredTestLightsNumber = imgui.slider_int('##209', mo.Setting_DeferredTestLightsNumber, 0, 32)
            imgui.unindent()
        return mo

    #endregion

    def render_camera(self, mo):
        tab_labels = ['Look At', 'Rotate', 'Translate']
        tab_icons = ['ICON_MD_REMOVE_RED_EYE', 'ICON_MD_3D_ROTATION', 'ICON_MD_OPEN_WITH']
        self.selectedTabGUICamera = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabGUICamera)
        imgui.separator()
        if self.selectedTabGUICamera == 0:
            imgui.text_colored('Look-At Matrix', 1, 0, 0, 1)
            imgui.separator()
            imgui.text('Eye')
            _, mo.camera.View_Eye.x = self.ui_helper.add_controls_slider_same_line('X', 1, 1.0, - mo.Setting_PlaneFar, mo.Setting_PlaneFar, False, None, mo.camera.View_Eye.x, True, self.is_frame)
            _, mo.camera.View_Eye.y = self.ui_helper.add_controls_slider_same_line('Y', 2, 1.0, - mo.Setting_PlaneFar, mo.Setting_PlaneFar, False, None, mo.camera.View_Eye.y, True, self.is_frame)
            _, mo.camera.View_Eye.z = self.ui_helper.add_controls_slider_same_line('Z', 3, 1.0, - mo.Setting_PlaneFar, mo.Setting_PlaneFar, False, None, mo.camera.View_Eye.z, True, self.is_frame)
            imgui.separator()
            imgui.text('Center')
            _, mo.camera.View_Center.x = self.ui_helper.add_controls_slider_same_line('X', 4, 1.0, -10.0, 10.0, False, None, mo.camera.View_Center.x, True, self.is_frame)
            _, mo.camera.View_Center.y = self.ui_helper.add_controls_slider_same_line('Y', 5, 1.0, -10.0, 10.0, False, None, mo.camera.View_Center.y, True, self.is_frame)
            _, mo.camera.View_Center.z = self.ui_helper.add_controls_slider_same_line('Z', 6, 1.0, 0.0, 45.0, False, None, mo.camera.View_Center.z, True, self.is_frame)
            imgui.separator()
            imgui.text('Up')
            _, mo.camera.View_Up.x = self.ui_helper.add_controls_slider_same_line('X', 7, 1.0, -1.0, 1.0, False, None, mo.camera.View_Up.x, True, self.is_frame)
            _, mo.camera.View_Up.y = self.ui_helper.add_controls_slider_same_line('Y', 8, 1.0, -1.0, 1.0, False, None, mo.camera.View_Up.y, True, self.is_frame)
            _, mo.camera.View_Up.z = self.ui_helper.add_controls_slider_same_line('Z', 9, 1.0, -1.0, 1.0, False, None, mo.camera.View_Up.z, True, self.is_frame)
        elif self.selectedTabGUICamera == 1:
            imgui.text_colored('Rotate object around axis', 1, 0, 0, 1)
            mo.camera.rotateX['animate'], mo.camera.rotateX['point'] = self.ui_helper.add_controls_slider_same_line('X', 13, 1.0, 0.0, 360.0, True, mo.camera.rotateX['animate'], mo.camera.rotateX['point'], True, self.is_frame)
            mo.camera.rotateY['animate'], mo.camera.rotateY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 14, 1.0, 0.0, 360.0, True, mo.camera.rotateY['animate'], mo.camera.rotateY['point'], True, self.is_frame)
            mo.camera.rotateZ['animate'], mo.camera.rotateZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 15, 1.0, 0.0, 360.0, True, mo.camera.rotateZ['animate'], mo.camera.rotateZ['point'], True, self.is_frame)
            imgui.separator()
            imgui.text_colored('Rotate object around center', 1, 0, 0, 1)
            mo.camera.rotateCenterX['animate'], mo.camera.rotateCenterX['point'] = self.ui_helper.add_controls_slider_same_line('X', 16, 1.0, -180.0, 180.0, True, mo.camera.rotateCenterX['animate'], mo.camera.rotateCenterX['point'], True, self.is_frame)
            mo.camera.rotateCenterY['animate'], mo.camera.rotateCenterY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 17, 1.0, -180.0, 180.0, True, mo.camera.rotateCenterY['animate'], mo.camera.rotateCenterY['point'], True, self.is_frame)
            mo.camera.rotateCenterZ['animate'], mo.camera.rotateCenterZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 18, 1.0, -180.0, 180.0, True, mo.camera.rotateCenterZ['animate'], mo.camera.rotateCenterZ['point'], True, self.is_frame)
        elif self.selectedTabGUICamera == 2:
            imgui.text_colored('Move object by axis', 1, 0, 0, 1)
            mo.camera.positionX['animate'], mo.camera.positionX['point'] = self.ui_helper.add_controls_slider_same_line('X', 19, 0.05, -2 * mo.Setting_GridSize, 2 * mo.Setting_GridSize, True, mo.camera.positionX['animate'], mo.camera.positionX['point'], True, self.is_frame)
            mo.camera.positionY['animate'], mo.camera.positionY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 20, 0.05, -2 * mo.Setting_GridSize, 2 * mo.Setting_GridSize, True, mo.camera.positionY['animate'], mo.camera.positionY['point'], True, self.is_frame)
            mo.camera.positionZ['animate'], mo.camera.positionZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 21, 0.05, -2 * mo.Setting_GridSize, 2 * mo.Setting_GridSize, True, mo.camera.positionZ['animate'], mo.camera.positionZ['point'], True, self.is_frame)
        return mo

    def render_camera_model(self, mo):
        tab_labels = ['General', 'Position', 'Rotate']
        tab_icons = ['ICON_MD_TRANSFORM', 'ICON_MD_OPEN_WITH', 'ICON_MD_3D_ROTATION']
        self.selectedTabGUICameraModel = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabGUICameraModel)

        imgui.separator()

        if self.selectedTabGUICameraModel == 0:
            _, mo.camera_model.showCameraObject = imgui.checkbox('Camera', mo.camera_model.showCameraObject)
            _, mo.camera_model.showInWire = imgui.checkbox('Wireframe', mo.camera_model.showInWire)
            imgui.separator()
            imgui.text('Inner Light Direction')
            mo.camera_model.innerLightDirectionX['animate'], mo.camera_model.innerLightDirectionX['point'] = self.ui_helper.add_controls_slider_same_line('X', 1, 0.001, -1.0, 1.0, True, mo.camera_model.innerLightDirectionX['animate'], mo.camera_model.innerLightDirectionX['point'], True, self.is_frame)
            mo.camera_model.innerLightDirectionY['animate'], mo.camera_model.innerLightDirectionY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 2, 0.001, -1.0, 1.0, True, mo.camera_model.innerLightDirectionY['animate'], mo.camera_model.innerLightDirectionY['point'], True, self.is_frame)
            mo.camera_model.innerLightDirectionZ['animate'], mo.camera_model.innerLightDirectionZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 3, 0.001, -1.0, 1.0, True, mo.camera_model.innerLightDirectionZ['animate'], mo.camera_model.innerLightDirectionZ['point'], True, self.is_frame)
            imgui.separator()
            imgui.text('Model Color')
            mo.camera_model.colorR['animate'], mo.camera_model.colorR['point'] = self.ui_helper.add_controls_slider_same_line('R', 4, 0.01, 0.0, 1.0, True, mo.camera_model.colorR['animate'], mo.camera_model.colorR['point'], True, self.is_frame)
            mo.camera_model.colorG['animate'], mo.camera_model.colorG['point'] = self.ui_helper.add_controls_slider_same_line('G', 5, 0.01, 0.0, 1.0, True, mo.camera_model.colorG['animate'], mo.camera_model.colorG['point'], True, self.is_frame)
            mo.camera_model.colorB['animate'], mo.camera_model.colorB['point'] = self.ui_helper.add_controls_slider_same_line('B', 6, 0.01, 0.0, 1.0, True, mo.camera_model.colorB['animate'], mo.camera_model.colorB['point'], True, self.is_frame)
        elif self.selectedTabGUICameraModel == 1:
            imgui.text_colored('Move object by axis', 1, 0, 0, 1)
            mo.camera_model.positionX['animate'], mo.camera_model.positionX['point'] = self.ui_helper.add_controls_slider_same_line('X', 7, 0.05, -2 * mo.Setting_GridSize, 2 * mo.Setting_GridSize, True, mo.camera_model.positionX['animate'], mo.camera_model.positionX['point'], True, self.is_frame)
            mo.camera_model.positionY['animate'], mo.camera_model.positionY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 8, 0.05, -2 * mo.Setting_GridSize, 2 * mo.Setting_GridSize, True, mo.camera_model.positionY['animate'], mo.camera_model.positionY['point'], True, self.is_frame)
            mo.camera_model.positionZ['animate'], mo.camera_model.positionZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 9, 0.05, -2 * mo.Setting_GridSize, 2 * mo.Setting_GridSize, True, mo.camera_model.positionZ['animate'], mo.camera_model.positionZ['point'], True, self.is_frame)
        elif self.selectedTabGUICameraModel == 2:
            imgui.text_colored('Rotate object around axis', 1, 0, 0, 1)
            mo.camera_model.rotateX['animate'], mo.camera_model.rotateX['point'] = self.ui_helper.add_controls_slider_same_line('X', 7, 1.0, 0.0, 360.0, True, mo.camera_model.rotateX['animate'], mo.camera_model.rotateX['point'], True, self.is_frame)
            mo.camera_model.rotateY['animate'], mo.camera_model.rotateY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 8, 1.0, 0.0, 360.0, True, mo.camera_model.rotateY['animate'], mo.camera_model.rotateY['point'], True, self.is_frame)
            mo.camera_model.rotateZ['animate'], mo.camera_model.rotateZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 9, 1.0, 0.0, 360.0, True, mo.camera_model.rotateZ['animate'], mo.camera_model.rotateZ['point'], True, self.is_frame)
            imgui.separator()
            imgui.text_colored('Rotate object around center', 1, 0, 0, 1)
            mo.camera_model.rotateCenterX['animate'], mo.camera_model.rotateCenterX['point'] = self.ui_helper.add_controls_slider_same_line('X', 10, 1.0, -180.0, 180.0, True, mo.camera_model.rotateCenterX['animate'], mo.camera_model.rotateCenterX['point'], True, self.is_frame)
            mo.camera_model.rotateCenterY['animate'], mo.camera_model.rotateCenterY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 11, 1.0, -180.0, 180.0, True, mo.camera_model.rotateCenterY['animate'], mo.camera_model.rotateCenterY['point'], True, self.is_frame)
            mo.camera_model.rotateCenterZ['animate'], mo.camera_model.rotateCenterZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 12, 1.0, -180.0, 180.0, True, mo.camera_model.rotateCenterZ['animate'], mo.camera_model.rotateCenterZ['point'], True, self.is_frame)
        return mo

    def render_grid(self, mo):
        tab_labels = ['General', 'Scale', 'Rotate', 'Translate']
        tab_icons = ['ICON_MD_TRANSFORM', 'ICON_MD_PHOTO_SIZE_SELECT_SMALL', 'ICON_MD_3D_ROTATION', 'ICON_MD_OPEN_WITH']
        self.selectedTabGUIGrid = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabGUIGrid)

        imgui.separator()

        if self.selectedTabGUIGrid == 0:
            imgui.text_colored('General grid settings', 1, 0, 0, 1)
            imgui.text('Grid Size')
            if imgui.is_item_hovered():
                imgui.set_tooltip('Squares')
            _, mo.Setting_GridSize = imgui.slider_int('##109', mo.Setting_GridSize, 0, 100)
            imgui.separator()
            _, mo.Setting_FixedGridWorld = imgui.checkbox('Grid fixed with World', mo.Setting_FixedGridWorld)
            _, mo.grid.showGrid = imgui.checkbox('Grid', mo.grid.showGrid)
            _, mo.grid.act_as_mirror = imgui.checkbox('Act as mirror', mo.grid.act_as_mirror)
            if mo.grid.act_as_mirror:
                _, mo.grid.transparency = self.ui_helper.add_controls_slider_same_line('Alpha', 999, 0.01, 0.0, 1.0, False, None, mo.grid.transparency, False, self.is_frame)
            imgui.separator()
            if mo.grid.act_as_mirror:
                imgui.text_colored('Mirror Position', 1, 0, 0, 1)
                imgui.separator()
                imgui.text_colored('Move mirror by axis', 1, 0, 0, 1)
                _, mo.grid.mirror_translateX = self.ui_helper.add_controls_slider_same_line('X', 71, 0.5, -1 * mo.Setting_GridSize, mo.Setting_GridSize, False, None, mo.grid.mirror_translateX, True, self.is_frame)
                _, mo.grid.mirror_translateY = self.ui_helper.add_controls_slider_same_line('Y', 81, 0.5, -1 * mo.Setting_GridSize, mo.Setting_GridSize, False, None, mo.grid.mirror_translateY, True, self.is_frame)
                _, mo.grid.mirror_translateZ = self.ui_helper.add_controls_slider_same_line('Z', 91, 0.5, -1 * mo.Setting_GridSize, mo.Setting_GridSize, False, None, mo.grid.mirror_translateZ, True, self.is_frame)
                imgui.text_colored('Rotate mirror around axis', 1, 0, 0, 1)
                _, mo.grid.mirror_rotateX = self.ui_helper.add_controls_slider_same_line('X', 41, 0.5, -180.0, 180.0, False, None, mo.grid.mirror_rotateX, True, self.is_frame)
                _, mo.grid.mirror_rotateY = self.ui_helper.add_controls_slider_same_line('Y', 51, 0.5, -180.0, 180.0, False, None, mo.grid.mirror_rotateY, True, self.is_frame)
                _, mo.grid.mirror_rotateZ = self.ui_helper.add_controls_slider_same_line('Z', 61, 0.5, -180.0, 180.0, False, None, mo.grid.mirror_rotateZ, True, self.is_frame)
        if self.selectedTabGUIGrid == 1:
            imgui.text_colored('Scale object', 1, 0, 0, 1)
            mo.grid.scaleX['animate'], mo.grid.scaleX['point'] = self.ui_helper.add_controls_slider_same_line('X', 1, 0.05, 0.0, 1.0, True, mo.grid.scaleX['animate'], mo.grid.scaleX['point'], True, self.is_frame)
            mo.grid.scaleY['animate'], mo.grid.scaleY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 2, 0.05, 0.0, 1.0, True, mo.grid.scaleY['animate'], mo.grid.scaleY['point'], True, self.is_frame)
            mo.grid.scaleZ['animate'], mo.grid.scaleZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 3, 0.05, 0.0, 1.0, True, mo.grid.scaleZ['animate'], mo.grid.scaleZ['point'], True, self.is_frame)
        if self.selectedTabGUIGrid == 2:
            imgui.text_colored('Rotate object around axis', 1, 0, 0, 1)
            mo.grid.rotateX['animate'], mo.grid.rotateX['point'] = self.ui_helper.add_controls_slider_same_line('X', 4, 1.0, -180.0, 180.0, True, mo.grid.rotateX['animate'], mo.grid.rotateX['point'], True, self.is_frame)
            mo.grid.rotateY['animate'], mo.grid.rotateY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 5, 1.0, -180.0, 180.0, True, mo.grid.rotateY['animate'], mo.grid.rotateY['point'], True, self.is_frame)
            mo.grid.rotateZ['animate'], mo.grid.rotateZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 6, 1.0, -180.0, 180.0, True, mo.grid.rotateZ['animate'], mo.grid.rotateZ['point'], True, self.is_frame)
        if self.selectedTabGUIGrid == 3:
            imgui.text_colored('Move object by axis', 1, 0, 0, 1)
            mo.grid.positionX['animate'], mo.grid.positionX['point'] = self.ui_helper.add_controls_slider_same_line('X', 7, 0.5, -1 * mo.Setting_GridSize, mo.Setting_GridSize, True, mo.grid.positionX['animate'], mo.grid.positionX['point'], True, self.is_frame)
            mo.grid.positionY['animate'], mo.grid.positionY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 8, 0.5, -1 * mo.Setting_GridSize, mo.Setting_GridSize, True, mo.grid.positionY['animate'], mo.grid.positionY['point'], True, self.is_frame)
            mo.grid.positionZ['animate'], mo.grid.positionZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 9, 0.5, -1 * mo.Setting_GridSize, mo.Setting_GridSize, True, mo.grid.positionZ['animate'], mo.grid.positionZ['point'], True, self.is_frame)
        return mo

    def render_scene_lights(self, mo):
        imgui.text_colored('Scene Ambient Light', 1, 0, 0, 1)
        _, mo.Setting_UIAmbientLight.r = self.ui_helper.add_controls_slider_same_line('X', 1, 0.001, 0, 1, False, None, mo.Setting_UIAmbientLight.r, True, self.is_frame)
        _, mo.Setting_UIAmbientLight.g = self.ui_helper.add_controls_slider_same_line('Y', 2, 0.001, 0, 1, False, None, mo.Setting_UIAmbientLight.g, True, self.is_frame)
        _, mo.Setting_UIAmbientLight.b = self.ui_helper.add_controls_slider_same_line('Z', 3, 0.001, 0, 1, False, None, mo.Setting_UIAmbientLight.b, True, self.is_frame)
        imgui.separator()
        imgui.text_colored('Solid Skin Light', 1, 0, 0, 1)

        mo.SolidLight_Ambient, mo.SolidLight_Ambient_ColorPicker = self.ui_helper.add_color3('Ambient', mo.SolidLight_Ambient, mo.SolidLight_Ambient_ColorPicker)
        _, mo.SolidLight_Ambient_Strength = self.ui_helper.add_slider('Intensity', 4, 0.01, 0.0, 1.0, False, None, mo.SolidLight_Ambient_Strength, True, self.is_frame)

        mo.SolidLight_Diffuse, mo.SolidLight_Diffuse_ColorPicker = self.ui_helper.add_color3('Diffuse', mo.SolidLight_Diffuse, mo.SolidLight_Diffuse_ColorPicker)
        _, mo.SolidLight_Diffuse_Strength = self.ui_helper.add_slider('Intensity', 5, 0.01, 0.0, 1.0, False, None, mo.SolidLight_Diffuse_Strength, True, self.is_frame)

        mo.SolidLight_Specular, mo.SolidLight_Specular_ColorPicker = self.ui_helper.add_color3('Specular', mo.SolidLight_Specular, mo.SolidLight_Specular_ColorPicker)
        _, mo.SolidLight_Specular_Strength = self.ui_helper.add_slider('Intensity', 6, 0.01, 0.0, 1.0, False, None, mo.SolidLight_Specular_Strength, True, self.is_frame)

        mo.SolidLight_MaterialColor, mo.SolidLight_MaterialColor_ColorPicker = self.ui_helper.add_color3('Material Color', mo.SolidLight_MaterialColor, mo.SolidLight_MaterialColor_ColorPicker)
        imgui.separator()
        imgui.text('Direction')
        _, mo.SolidLight_Direction.x = self.ui_helper.add_controls_slider_same_line('X', 7, 0, 0, 10, False, None, mo.SolidLight_Direction.x, True, self.is_frame)
        _, mo.SolidLight_Direction.y = self.ui_helper.add_controls_slider_same_line('Y', 8, 1, 0, 10, False, None, mo.SolidLight_Direction.y, True, self.is_frame)
        _, mo.SolidLight_Direction.z = self.ui_helper.add_controls_slider_same_line('Z', 9, 0, 0, 10, False, None, mo.SolidLight_Direction.z, True, self.is_frame)
        return mo

    def render_skybox(self, mo):
        imgui.text_colored('Skybox', 1, 0, 0, 1)
        skybox_items = []
        for item in enumerate(mo.skybox.skyboxItems):
            skybox_items.append(item[1][0])
        _, mo.skybox.Setting_Skybox_Item = imgui.combo("##987", mo.skybox.Setting_Skybox_Item, skybox_items)
        return mo

    #region Artefacts

    def render_artefacts(self, mo):
        if self.selectedObjectArtefact == 0:
            self.render_artefacts_terrain(mo)
        elif self.selectedObjectArtefact == 1:
            self.render_artefacts_spaceship(mo)
        return mo

    def render_artefacts_terrain(self, mo):
        imgui.text_colored('Terrain', 1, 0, 0, 1)
        _, mo.Setting_ShowTerrain = imgui.checkbox('Terrain', mo.Setting_ShowTerrain)
        if mo.Setting_ShowTerrain:
            imgui.separator()
            if imgui.button('Generate Terrain', -1, 0):
                self.generateNewTerrain = not self.generateNewTerrain
            # TODO: terrain settings
        return mo

    def render_artefacts_spaceship(self, mo):
        imgui.text_colored('Spaceship Generator', 1, 0, 0, 1)
        _, mo.Setting_ShowSpaceship = imgui.checkbox('Spaceship', mo.Setting_ShowSpaceship)
        if mo.Setting_ShowSpaceship:
            imgui.separator()
            if imgui.button('Generate Spaceship', -1, 0):
                mo.Setting_GenerateSpaceship = True
            _, _ = imgui.checkbox('Wireframe', False)
        return mo

    #endregion

    def render_lights(self, mo):
        tab_labels = ['General', 'Scale', 'Rotate', 'Translate', 'Colors']
        tab_icons = ['ICON_MD_TRANSFORM', 'ICON_MD_PHOTO_SIZE_SELECT_SMALL', 'ICON_MD_3D_ROTATION', 'ICON_MD_OPEN_WITH', 'ICON_MD_COLOR_LENS']
        self.selectedTabGUILight = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabGUILight)

        imgui.separator()

        if self.selectedTabGUILight == 0:
            imgui.text_colored('Properties', 1, 0, 0, 1)
            imgui.text(mo.lightSources[self.selectedObjectLight].description)
            _, mo.lightSources[self.selectedObjectLight].showLampObject = imgui.checkbox('Lamp', mo.lightSources[self.selectedObjectLight].showLampObject)
            _, mo.lightSources[self.selectedObjectLight].showLampDirection = imgui.checkbox('Direction', mo.lightSources[self.selectedObjectLight].showLampDirection)
            _, mo.lightSources[self.selectedObjectLight].showInWire = imgui.checkbox('Wireframe', mo.lightSources[self.selectedObjectLight].showInWire)
            _, self.lockCameraWithLight = imgui.checkbox('Lock with Camera', self.lockCameraWithLight)
            if imgui.button('View from Here', -1, 0):
                mo = self.lock_camera_once(mo)
            imgui.separator()
            if imgui.button('Delete Light Source', -1, 0):
                self.selectedObject = 0
                del mo.lightSources[self.selectedObjectLight]
                self.selectedObjectLight = -1
        elif self.selectedTabGUILight == 1:
            imgui.text_colored('Scale Object', 1, 0, 0, 1)
            mo.lightSources[self.selectedObjectLight].scaleX['animate'], mo.lightSources[self.selectedObjectLight].scaleX['point'] = self.ui_helper.add_controls_slider_same_line('X', 10, 0.05, 0.0, mo.Setting_GridSize, True, mo.lightSources[self.selectedObjectLight].scaleX['animate'], mo.lightSources[self.selectedObjectLight].scaleX['point'], True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].scaleY['animate'], mo.lightSources[self.selectedObjectLight].scaleY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 11, 0.05, 0.0, mo.Setting_GridSize, True, mo.lightSources[self.selectedObjectLight].scaleY['animate'], mo.lightSources[self.selectedObjectLight].scaleY['point'], True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].scaleZ['animate'], mo.lightSources[self.selectedObjectLight].scaleZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 12, 0.05, 0.0, mo.Setting_GridSize, True, mo.lightSources[self.selectedObjectLight].scaleZ['animate'], mo.lightSources[self.selectedObjectLight].scaleZ['point'], True, self.is_frame)
        elif self.selectedTabGUILight == 2:
            imgui.text_colored('Around Axis', 1, 0, 0, 1)
            mo.lightSources[self.selectedObjectLight].rotateCenterX['animate'], mo.lightSources[self.selectedObjectLight].rotateCenterX['point'] = self.ui_helper.add_controls_slider_same_line('X', 13, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].rotateCenterX['animate'], mo.lightSources[self.selectedObjectLight].rotateCenterX['point'], True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].rotateCenterY['animate'], mo.lightSources[self.selectedObjectLight].rotateCenterY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 14, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].rotateCenterY['animate'], mo.lightSources[self.selectedObjectLight].rotateCenterY['point'], True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].rotateCenterZ['animate'], mo.lightSources[self.selectedObjectLight].rotateCenterZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 15, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].rotateCenterZ['animate'], mo.lightSources[self.selectedObjectLight].rotateCenterZ['point'], True, self.is_frame)
            imgui.text_colored('Around World center', 1, 0, 0, 1)
            mo.lightSources[self.selectedObjectLight].rotateX['animate'], self.lightRotateX = self.ui_helper.add_controls_slider_same_line('X', 16, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].rotateX['animate'], self.lightRotateX, True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].rotateY['animate'], self.lightRotateY = self.ui_helper.add_controls_slider_same_line('Y', 17, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].rotateY['animate'], self.lightRotateY, True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].rotateZ['animate'], self.lightRotateZ = self.ui_helper.add_controls_slider_same_line('Z', 18, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].rotateZ['animate'], self.lightRotateZ, True, self.is_frame)
        elif self.selectedTabGUILight == 3:
            imgui.text_colored('Move object by Axis', 1, 0, 0, 1)
            mo.lightSources[self.selectedObjectLight].positionX['animate'], mo.lightSources[self.selectedObjectLight].positionX['point'] = self.ui_helper.add_controls_slider_same_line('X', 19, 0.5, -1 * mo.Setting_GridSize, mo.Setting_GridSize, True, mo.lightSources[self.selectedObjectLight].positionX['animate'], mo.lightSources[self.selectedObjectLight].positionX['point'], True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].positionY['animate'], mo.lightSources[self.selectedObjectLight].positionY['point'] = self.ui_helper.add_controls_slider_same_line('Y', 20, 1.0, -1 * mo.Setting_GridSize, mo.Setting_GridSize, True, mo.lightSources[self.selectedObjectLight].positionY['animate'], mo.lightSources[self.selectedObjectLight].positionY['point'], True, self.is_frame)
            mo.lightSources[self.selectedObjectLight].positionZ['animate'], mo.lightSources[self.selectedObjectLight].positionZ['point'] = self.ui_helper.add_controls_slider_same_line('Z', 21, 1.0, -1 * mo.Setting_GridSize, mo.Setting_GridSize, True, mo.lightSources[self.selectedObjectLight].positionZ['animate'], mo.lightSources[self.selectedObjectLight].positionZ['point'], True, self.is_frame)
        elif self.selectedTabGUILight == 4:
            imgui.text_colored('Light Colors', 1, 0, 0, 1)
            mo.lightSources[self.selectedObjectLight].ambient.color, mo.lightSources[self.selectedObjectLight].ambient.colorPickerOpen = self.ui_helper.add_color3('Ambient Color', mo.lightSources[self.selectedObjectLight].ambient.color, mo.lightSources[self.selectedObjectLight].ambient.colorPickerOpen)
            mo.lightSources[self.selectedObjectLight].ambient.animate, mo.lightSources[self.selectedObjectLight].ambient.strength = self.ui_helper.add_slider('Ambient Intensity', 22, 0.01, 0.0, 1.0, True, mo.lightSources[self.selectedObjectLight].ambient.animate, mo.lightSources[self.selectedObjectLight].ambient.strength, True, self.is_frame)

            mo.lightSources[self.selectedObjectLight].diffuse.color, mo.lightSources[self.selectedObjectLight].diffuse.colorPickerOpen = self.ui_helper.add_color3('Diffuse Color', mo.lightSources[self.selectedObjectLight].diffuse.color, mo.lightSources[self.selectedObjectLight].diffuse.colorPickerOpen)
            mo.lightSources[self.selectedObjectLight].diffuse.animate, mo.lightSources[self.selectedObjectLight].diffuse.strength = self.ui_helper.add_slider('Diffuse Intensity', 23, 0.01, 0.0, 1.0, True, mo.lightSources[self.selectedObjectLight].diffuse.animate, mo.lightSources[self.selectedObjectLight].diffuse.strength, True, self.is_frame)

            mo.lightSources[self.selectedObjectLight].specular.color, mo.lightSources[self.selectedObjectLight].specular.colorPickerOpen = self.ui_helper.add_color3('Specular Color', mo.lightSources[self.selectedObjectLight].specular.color, mo.lightSources[self.selectedObjectLight].specular.colorPickerOpen)
            mo.lightSources[self.selectedObjectLight].specular.animate, mo.lightSources[self.selectedObjectLight].specular.strength = self.ui_helper.add_slider('Specular Intensity', 24, 0.01, 0.0, 1.0, True, mo.lightSources[self.selectedObjectLight].specular.animate, mo.lightSources[self.selectedObjectLight].specular.strength, True, self.is_frame)
            imgui.separator()
            if mo.lightSources[self.selectedObjectLight].type != Settings.LightSourceTypes.LightSourceType_Directional:
                mo.lightSources[self.selectedObjectLight].lConstant['animate'], mo.lightSources[self.selectedObjectLight].lConstant['point'] = self.ui_helper.add_slider('Constant', 25, 0.01, 0.0, 1.0, True, mo.lightSources[self.selectedObjectLight].lConstant['animate'], mo.lightSources[self.selectedObjectLight].lConstant['point'], True, self.is_frame)
                mo.lightSources[self.selectedObjectLight].lLinear['animate'], mo.lightSources[self.selectedObjectLight].lLinear['point'] = self.ui_helper.add_slider('Literal', 26, 0.01, 0.0, 1.0, True, mo.lightSources[self.selectedObjectLight].lLinear['animate'], mo.lightSources[self.selectedObjectLight].lLinear['point'], True, self.is_frame)
                mo.lightSources[self.selectedObjectLight].lQuadratic['animate'], mo.lightSources[self.selectedObjectLight].lQuadratic['point'] = self.ui_helper.add_slider('Quadratic', 27, 0.01, 0.0, 1.0, True, mo.lightSources[self.selectedObjectLight].lQuadratic['animate'], mo.lightSources[self.selectedObjectLight].lQuadratic['point'], True, self.is_frame)
            if mo.lightSources[self.selectedObjectLight].type == Settings.LightSourceTypes.LightSourceType_Spot:
                imgui.separator()
                mo.lightSources[self.selectedObjectLight].lCutOff['animate'], mo.lightSources[self.selectedObjectLight].lCutOff['point'] = self.ui_helper.add_slider('Cutoff', 28, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].lCutOff['animate'], mo.lightSources[self.selectedObjectLight].lCutOff['point'], True, self.is_frame)
                mo.lightSources[self.selectedObjectLight].lOuterCutOff['animate'], mo.lightSources[self.selectedObjectLight].lOuterCutOff['point'] = self.ui_helper.add_slider('Outer Cutoff', 29, 1.0, -180.0, 180.0, True, mo.lightSources[self.selectedObjectLight].lOuterCutOff['animate'], mo.lightSources[self.selectedObjectLight].lOuterCutOff['point'], True, self.is_frame)
        return mo

    def lock_camera_once(self, mo):
        self.lockCameraWithLight = True
        self.lock_camera(mo)
        self.lockCameraWithLight = False

    def lock_camera(self, mo):
        if self.lockCameraWithLight:
            mo.camera.positionX['point'] = mo.lightSources[self.selectedObjectLight].positionX['point']
            mo.camera.positionY['point'] = mo.lightSources[self.selectedObjectLight].positionY['point']
            mo.camera.positionZ['point'] = mo.lightSources[self.selectedObjectLight].positionZ['point']
            mo.camera.rotateX['point'] = mo.lightSources[self.selectedObjectLight].rotateX['point']
            mo.camera.rotateY['point'] = mo.lightSources[self.selectedObjectLight].rotateY['point']
            mo.camera.rotateZ['point'] = mo.lightSources[self.selectedObjectLight].rotateZ['point']
            mo.camera.cameraPosition = mo.lightSources[self.selectedObjectLight].matrixModel[3]
            mo.camera.matrixCamera = mo.lightSources[self.selectedObjectLight].matrixModel
        return mo

