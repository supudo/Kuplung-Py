# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import copy
import os
import numpy
import imgui
from OpenGL.GL import *
from PIL import Image
from settings import Settings
from ui.ui_helpers import UIHelpers
from gl_utils.objects.Material import MaterialTextureType


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
        self.vboTextureAmbient = -1
        self.vboTextureDiffuse = -1
        self.vboTextureDissolve = -1
        self.vboTextureBump = -1
        self.vboTextureDisplacement = -1
        self.vboTextureSpecular = -1
        self.vboTextureSpecularExp = -1

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

        self.height_top_panel = 170.0
        self.ui_helper = UIHelpers

        self.multi_handler_ro = False

    def render(self, delegate, is_opened, managerObjects, meshModelFaces, is_frame, sceneSelectedModelObject):
        self.selectedObject = sceneSelectedModelObject
        self.is_frame = is_frame

        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(10, 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('Scene Settings', is_opened, 0)

        tab_labels = ['Models', 'Create']
        tab_icons = ['ICON_MD_BUILD', 'ICON_MD_ADD']
        self.selectedTabPanel = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabPanel)

        if self.selectedTabPanel == 0:
            if meshModelFaces is not None and len(meshModelFaces) > 0:
                meshModelFaces = self.render_models(meshModelFaces, managerObjects, delegate)
            else:
                imgui.text_colored('No models in the current scene.', 255, 0, 0, 255)
        else:
            self.render_create(delegate)

        imgui.end()

        sceneSelectedModelObject = self.selectedObject

        return is_opened, meshModelFaces, sceneSelectedModelObject

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

    def render_models(self, mmfs, mo, delegate):
        # reset defaults button
        imgui.push_style_color(imgui.COLOR_BUTTON, .6, .1, .1, 1)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, .9, .1, .1, 1)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, .8, .2, .2, 1)
        if imgui.button('Reset values to default', -1, 0):
            for i in range(len(mmfs)):
                mmfs[i].initModelProperties()
        imgui.pop_style_color(3)

        # scene items
        imgui.begin_child("Scene Items", 0.0, self.height_top_panel, True)

        scene_items = []
        for item in mmfs:
            scene_items.append(item.mesh_model.ModelTitle)

        imgui.push_item_width(-1)
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 6))
        imgui.push_style_var(imgui.STYLE_WINDOW_MIN_SIZE, (0, 100))
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 0, 0, 0, 1)
        _, self.selectedObject = imgui.listbox('', self.selectedObject, scene_items)
        imgui.pop_style_color(1)
        imgui.pop_style_var(2)
        if self.selectedObject > -1 and imgui.begin_popup_context_item('Actions'):
            _, clicked_rename = imgui.menu_item('Rename', None, None, False)
            _, clicked_duplicate = imgui.menu_item('Duplicate')
            if clicked_duplicate:
                new_model = copy.deepcopy(mmfs[self.selectedObject])
                mmfs.append(new_model)
            if imgui.begin_menu('Delete'):
                _, clicked_delete_ok = imgui.menu_item('OK')
                if clicked_delete_ok:
                    delegate.remove_model(self.selectedObject)
                imgui.end_menu()
            imgui.end_popup()

        imgui.pop_item_width()

        imgui.end_child()

        imgui_io = imgui.get_io()
        imgui_io.mouse_draw_cursor = True
        imgui.push_style_color(imgui.COLOR_BUTTON, 89 / 255.0,
                               91 / 255.0, 94 / 255.0, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 119 / 255.0,
                               122 / 255.0, 124 / 255.0, 1.0)
        imgui.push_style_color(imgui.COLOR_BORDER, 0, 0, 0, 1)
        imgui.button("###splitterModels", -1, 8.0)
        imgui.pop_style_color(3)
        if imgui.is_item_active():
            self.height_top_panel += imgui.get_mouse_drag_delta().y
        if imgui.is_item_hovered():
            imgui.set_mouse_cursor(imgui.MOUSE_CURSOR_RESIZE_NS)
        else:
            imgui_io.mouse_draw_cursor = False

        # properties
        imgui.begin_child("Properties Pane", 0.0, 0.0, False)
        imgui.push_item_width(imgui.get_window_width() * 0.75)

        if self.selectedObject > -1:
            mmf = mmfs[self.selectedObject]
            imgui.text_colored('OBJ File:', 255, 0, 0, 255)
            imgui.same_line()
            imgui.text(mmf.mesh_model.file.replace('resources/shapes/', ''))
            imgui.text_colored('Model Face:', 255, 0, 0, 255)
            imgui.same_line()
            imgui.text(mmf.mesh_model.ModelTitle)
            imgui.text_colored('Material:', 255, 0, 0, 255)
            imgui.same_line()
            imgui.text(mmf.mesh_model.MaterialTitle)
            imgui.text_colored('Vertices:', 255, 0, 0, 255)
            imgui.same_line()
            imgui.text(str(mmf.mesh_model.countVertices))
            imgui.text_colored('Normals:', 255, 0, 0, 255)
            imgui.same_line()
            imgui.text(str(mmf.mesh_model.countNormals))
            imgui.text_colored('Indices:', 255, 0, 0, 255)
            imgui.same_line()
            imgui.text(str(mmf.mesh_model.countIndices))

            has_textures = False
            if mmf.mesh_model.ModelMaterial.texture_ambient.Image != '':
                has_textures = True
            if mmf.mesh_model.ModelMaterial.texture_diffuse.Image != '':
                has_textures = True
            if mmf.mesh_model.ModelMaterial.texture_normal.Image != '':
                has_textures = True
            if mmf.mesh_model.ModelMaterial.texture_displacement.Image != '':
                has_textures = True
            if mmf.mesh_model.ModelMaterial.texture_specular.Image != '':
                has_textures = True
            if mmf.mesh_model.ModelMaterial.texture_specular_exp.Image != '':
                has_textures = True
            if mmf.mesh_model.ModelMaterial.texture_dissolve.Image != '':
                has_textures = True

            if has_textures:
                imgui.separator()
                imgui.text_colored('Textures:', 255, 0, 0, 255)

            mmfs, self.showTextureWindow_Ambient, self.showTexture_Ambient = self.show_texture_line('##001', mmfs, MaterialTextureType.MaterialTextureType_Ambient, self.showTextureWindow_Ambient, self.showTexture_Ambient)
            mmfs, self.showTextureWindow_Diffuse, self.showTexture_Diffuse = self.show_texture_line('##002', mmfs, MaterialTextureType.MaterialTextureType_Diffuse, self.showTextureWindow_Diffuse, self.showTexture_Diffuse)
            mmfs, self.showTextureWindow_Dissolve, self.showTexture_Dissolve = self.show_texture_line('##003', mmfs, MaterialTextureType.MaterialTextureType_Dissolve, self.showTextureWindow_Dissolve, self.showTexture_Dissolve)
            mmfs, self.showTextureWindow_Bump, self.showTexture_Bump = self.show_texture_line('##004', mmfs, MaterialTextureType.MaterialTextureType_Bump, self.showTextureWindow_Bump, self.showTexture_Bump)
            mmfs, self.showTextureWindow_Displacement, self.showTexture_Displacement = self.show_texture_line('##005', mmfs, MaterialTextureType.MaterialTextureType_Displacement, self.showTextureWindow_Displacement, self.showTexture_Displacement)
            mmfs, self.showTextureWindow_Specular, self.showTexture_Specular = self.show_texture_line('##006', mmfs, MaterialTextureType.MaterialTextureType_Specular, self.showTextureWindow_Specular, self.showTexture_Specular)
            mmfs, self.showTextureWindow_SpecularExp, self.showTexture_SpecularExp = self.show_texture_line('##007', mmfs, MaterialTextureType.MaterialTextureType_SpecularExp, self.showTextureWindow_SpecularExp, self.showTexture_SpecularExp)

            if self.showTextureWindow_Ambient:
                self.showTextureWindow_Ambient, self.showTexture_Ambient, self.vboTextureAmbient, self.textureAmbient_Width, self.textureAmbient_Height = self.show_texture_image(mmfs[self.selectedObject], MaterialTextureType.MaterialTextureType_Ambient, 'Ambient', self.showTextureWindow_Ambient, self.showTexture_Ambient, self.vboTextureAmbient, self.textureAmbient_Width, self.textureAmbient_Height)
            if self.showTextureWindow_Diffuse:
                self.showTextureWindow_Diffuse, self.showTexture_Diffuse, self.vboTextureDiffuse, self.textureDiffuse_Width, self.textureDiffuse_Height = self.show_texture_image(mmfs[self.selectedObject], MaterialTextureType.MaterialTextureType_Diffuse, 'Diffuse', self.showTextureWindow_Diffuse, self.showTexture_Diffuse, self.vboTextureDiffuse, self.textureDiffuse_Width, self.textureDiffuse_Height)
            if self.showTextureWindow_Dissolve:
                self.showTextureWindow_Dissolve, self.showTexture_Dissolve, self.vboTextureDissolve, self.textureDissolve_Width, self.textureDissolve_Height = self.show_texture_image(mmfs[self.selectedObject], MaterialTextureType.MaterialTextureType_Dissolve, 'Dissolve', self.showTextureWindow_Dissolve, self.showTexture_Dissolve, self.vboTextureDissolve, self.textureDissolve_Width, self.textureDissolve_Height)
            if self.showTextureWindow_Bump:
                self.showTextureWindow_Bump, self.showTexture_Bump, self.vboTextureBump, self.textureBump_Width, self.textureBump_Height = self.show_texture_image(mmfs[self.selectedObject], MaterialTextureType.MaterialTextureType_Bump, 'Normal', self.showTextureWindow_Bump, self.showTexture_Bump, self.vboTextureBump, self.textureBump_Width, self.textureBump_Height)
            if self.showTextureWindow_Displacement:
                self.showTextureWindow_Displacement, self.showTexture_Displacement, self.vboTextureDisplacement, self.textureDisplacement_Width, self.textureDisplacement_Height = self.show_texture_image(mmfs[self.selectedObject], MaterialTextureType.MaterialTextureType_Displacement, 'Displacement', self.showTextureWindow_Displacement, self.showTexture_Displacement, self.vboTextureDisplacement, self.textureDisplacement_Width, self.textureDisplacement_Height)
            if self.showTextureWindow_Specular:
                self.showTextureWindow_Specular, self.showTexture_Specular, self.vboTextureSpecular, self.textureSpecular_Width, self.textureSpecular_Height = self.show_texture_image(mmfs[self.selectedObject], MaterialTextureType.MaterialTextureType_Specular, 'Specular', self.showTextureWindow_Specular, self.showTexture_Specular, self.vboTextureSpecular, self.textureSpecular_Width, self.textureSpecular_Height)
            if self.showTextureWindow_SpecularExp:
                self.showTextureWindow_SpecularExp, self.showTexture_SpecularExp, self.vboTextureSpecularExp, self.textureSpecularExp_Width, self.textureSpecularExp_Height = self.show_texture_image(mmfs[self.selectedObject], MaterialTextureType.MaterialTextureType_SpecularExp, 'Specular Exp', self.showTextureWindow_SpecularExp, self.showTexture_SpecularExp, self.vboTextureSpecularExp, self.textureSpecularExp_Width, self.textureSpecularExp_Height)

            imgui.separator()

            tab_labels = [
                'General', 'Scale', 'Rotate', 'Translate', 'Displace',
                'Material', 'Effects', 'Illumination'
            ]
            tab_icons = [
                'ICON_MD_TRANSFORM', 'ICON_MD_PHOTO_SIZE_SELECT_SMALL',
                'ICON_MD_3D_ROTATION', 'ICON_MD_OPEN_WITH',
                'ICON_MD_TOLL', 'ICON_MD_FORMAT_PAINT', 'ICON_MD_BLUR_ON',
                'ICON_MD_LIGHTBULB_OUTLINE'
            ]
            self.selectedTabScene = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabScene, 4, 1.0)

            if self.selectedTabScene == 0:
                mmfs = self.render_properties(mmfs)
            if self.selectedTabScene == 1:
                mmfs = self.render_scale(mmfs, mo.Setting_GridSize)
            if self.selectedTabScene == 2:
                mmfs = self.render_rotate(mmfs)
            if self.selectedTabScene == 3:
                mmfs = self.render_translate(mmfs, mo.Setting_GridSize)
            if self.selectedTabScene == 4:
                mmfs = self.render_displace(mmfs, mo.Setting_GridSize)
            if self.selectedTabScene == 5:
                mmfs = self.render_material(mmfs)
            if self.selectedTabScene == 6:
                mmfs = self.render_effects(mmfs)
            if self.selectedTabScene == 7:
                mmfs = self.render_illumination_type(mmfs)

            imgui.separator()

        imgui.pop_item_width()
        imgui.end_child()

        return mmfs

    def render_properties(self, mmfs):
        imgui.text_colored('Properties', 1, 0, 0, 1)
        _, mmfs[self.selectedObject].Setting_CelShading = imgui.checkbox('Cel Shading', mmfs[self.selectedObject].Setting_CelShading)
        _, mmfs[self.selectedObject].Setting_Wireframe = imgui.checkbox('Wireframe', mmfs[self.selectedObject].Setting_Wireframe)
        _, mmfs[self.selectedObject].Setting_EditMode = imgui.checkbox('Edit Mode', mmfs[self.selectedObject].Setting_EditMode)
        _, mmfs[self.selectedObject].Setting_ShowShadows = imgui.checkbox('Shadows', mmfs[self.selectedObject].Setting_ShowShadows)
        imgui.text_colored('Alpha Blending', 1, 0, 0, mmfs[self.selectedObject].Setting_Alpha)
        mmfs[self.selectedObject].Setting_Alpha = self.ui_helper.add_slider_control('', 1, 0.0, 1.0, mmfs[self.selectedObject].Setting_Alpha)
        return mmfs

    def render_scale(self, mmfs, gs):
        imgui.text_colored('Scale Model', 1, 0, 0, 1)
        _, mmfs[self.selectedObject].Setting_ScaleAllParts = imgui.checkbox('Scale All', mmfs[self.selectedObject].Setting_ScaleAllParts)
        if mmfs[self.selectedObject].Setting_ScaleAllParts:
            _, mmfs[self.selectedObject].scaleX.point = imgui.slider_float('##001', mmfs[self.selectedObject].scaleX.point, 0.05, gs / 2, "%.03f", 1.0)
            imgui.same_line()
            imgui.text('X')
            _, mmfs[self.selectedObject].scaleY.point = imgui.slider_float('##001', mmfs[self.selectedObject].scaleY.point, 0.05, gs / 2, "%.03f", 1.0)
            imgui.same_line()
            imgui.text('Y')
            _, mmfs[self.selectedObject].scaleZ.point = imgui.slider_float('##001', mmfs[self.selectedObject].scaleZ.point, 0.05, gs / 2, "%.03f", 1.0)
            imgui.same_line()
            imgui.text('Z')
        else:
            _, mmfs[self.selectedObject].scaleX.point = imgui.slider_float('##001', mmfs[self.selectedObject].scaleX.point, 0.05, gs / 2, "%.03f", 1.0)
            imgui.same_line()
            imgui.text('X')
            _, mmfs[self.selectedObject].scaleY.point = imgui.slider_float('##002', mmfs[self.selectedObject].scaleY.point, 0.05, gs / 2, "%.03f", 1.0)
            imgui.same_line()
            imgui.text('Y')
            _, mmfs[self.selectedObject].scaleZ.point = imgui.slider_float('##003', mmfs[self.selectedObject].scaleZ.point, 0.05, gs / 2, "%.03f", 1.0)
            imgui.same_line()
            imgui.text('Z')
        return mmfs

    def render_rotate(self, mmfs):
        imgui.text_colored('Rotate model around axis', 1, 0, 0, 1)
        mmfs[self.selectedObject].rotateX.animate, mmfs[self.selectedObject].rotateX.point = self.ui_helper.add_controls_slider_same_line('X', 4, 1.0, -180.0, 180.0, True, mmfs[self.selectedObject].rotateX.animate, mmfs[self.selectedObject].rotateX.point, True, self.is_frame)
        mmfs[self.selectedObject].rotateY.animate, mmfs[self.selectedObject].rotateY.point = self.ui_helper.add_controls_slider_same_line('Y', 5, 1.0, -180.0, 180.0, True, mmfs[self.selectedObject].rotateY.animate, mmfs[self.selectedObject].rotateY.point, True, self.is_frame)
        mmfs[self.selectedObject].rotateZ.animate, mmfs[self.selectedObject].rotateZ.point = self.ui_helper.add_controls_slider_same_line('Z', 6, 1.0, -180.0, 180.0, True, mmfs[self.selectedObject].rotateZ.animate, mmfs[self.selectedObject].rotateZ.point, True, self.is_frame)
        return mmfs

    def render_translate(self, mmfs, gs):
        imgui.text_colored('Translate model by axis', 1, 0, 0, 1)
        mmfs[self.selectedObject].positionX.animate, mmfs[self.selectedObject].positionX.point = self.ui_helper.add_controls_slider_same_line('X', 7, 1.0, -1 * gs, gs, True, mmfs[self.selectedObject].positionX.animate, mmfs[self.selectedObject].positionX.point, True, self.is_frame)
        mmfs[self.selectedObject].positionY.animate, mmfs[self.selectedObject].positionY.point = self.ui_helper.add_controls_slider_same_line('Y', 8, 1.0, -1 * gs, gs, True, mmfs[self.selectedObject].positionY.animate, mmfs[self.selectedObject].positionY.point, True, self.is_frame)
        mmfs[self.selectedObject].positionZ.animate, mmfs[self.selectedObject].positionZ.point = self.ui_helper.add_controls_slider_same_line('Z', 9, 1.0, -1 * gs, gs, True, mmfs[self.selectedObject].positionZ.animate, mmfs[self.selectedObject].positionZ.point, True, self.is_frame)
        return mmfs

    def render_displace(self, mmfs, gs):
        imgui.text_colored('Displace model', 1, 0, 0, 1)
        mmfs[self.selectedObject].displaceX.animate, mmfs[self.selectedObject].displaceX.point = self.ui_helper.add_controls_slider_same_line('X', 10, 1.0, -1 * gs, gs, True, mmfs[self.selectedObject].displaceX.animate, mmfs[self.selectedObject].displaceX.point, True, self.is_frame)
        mmfs[self.selectedObject].displaceY.animate, mmfs[self.selectedObject].displaceY.point = self.ui_helper.add_controls_slider_same_line('Y', 11, 1.0, -1 * gs, gs, True, mmfs[self.selectedObject].displaceY.animate, mmfs[self.selectedObject].displaceY.point, True, self.is_frame)
        mmfs[self.selectedObject].displaceZ.animate, mmfs[self.selectedObject].displaceZ.point = self.ui_helper.add_controls_slider_same_line('Z', 12, 1.0, -1 * gs, gs, True, mmfs[self.selectedObject].displaceZ.animate, mmfs[self.selectedObject].displaceZ.point, True, self.is_frame)
        return mmfs

    def render_material(self, mmfs):
        imgui.text_colored('Material of the model', 1, 0, 0, 1)
        # TODO: material editor
        _, mmfs[self.selectedObject].Setting_ParallaxMapping = imgui.checkbox('Parallax Mapping', mmfs[self.selectedObject].Setting_ParallaxMapping)
        imgui.separator()
        _, mmfs[self.selectedObject].Setting_UseTessellation = imgui.checkbox('Use Tessellation', mmfs[self.selectedObject].Setting_UseTessellation)
        if mmfs[self.selectedObject].Setting_UseTessellation:
            _, mmfs[self.selectedObject].Setting_UseCullFace = imgui.checkbox('Culling', mmfs[self.selectedObject].Setting_UseCullFace)
            mmfs[self.selectedObject].Setting_TessellationSubdivision = self.ui_helper.add_int_slider_control('Subdivision', 24, 0, 100, mmfs[self.selectedObject].Setting_TessellationSubdivision)
            imgui.separator()
            if mmfs[self.selectedObject].mesh_model.ModelMaterial.texture_displacement.UseTexture:
                mmfs[self.selectedObject].displacementHeightScale.animate, mmfs[self.selectedObject].displacementHeightScale.point = self.ui_helper.add_slider('Displacement', 15, 0.05, -2.0, 2.0, True, mmfs[self.selectedObject].displacementHeightScale.animate, mmfs[self.selectedObject].displacementHeightScale.point, False, self.is_frame)
                imgui.separator()
        else:
            imgui.separator()
        imgui.text('Refraction')
        mmfs[self.selectedObject].Setting_MaterialRefraction.animate, mmfs[self.selectedObject].Setting_MaterialRefraction.point = self.ui_helper.add_controls_slider_same_line('', 13, 0.05, -10, 10, True, mmfs[self.selectedObject].Setting_MaterialRefraction.animate, mmfs[self.selectedObject].Setting_MaterialRefraction.point, True, self.is_frame)
        imgui.text('Specular Exponent')
        mmfs[self.selectedObject].Setting_MaterialSpecularExp.animate, mmfs[self.selectedObject].Setting_MaterialSpecularExp.point = self.ui_helper.add_controls_slider_same_line('', 14, 10, 0, 1000, True, mmfs[self.selectedObject].Setting_MaterialSpecularExp.animate, mmfs[self.selectedObject].Setting_MaterialSpecularExp.point, True, self.is_frame)
        imgui.separator()
        mmfs[self.selectedObject].materialAmbient.color, mmfs[self.selectedObject].materialAmbient.colorPickerOpen = self.ui_helper.add_color3('Ambient Color', mmfs[self.selectedObject].materialAmbient.color, mmfs[self.selectedObject].materialAmbient.colorPickerOpen)
        mmfs[self.selectedObject].materialDiffuse.color, mmfs[self.selectedObject].materialDiffuse.colorPickerOpen = self.ui_helper.add_color3('Diffuse Color', mmfs[self.selectedObject].materialDiffuse.color, mmfs[self.selectedObject].materialDiffuse.colorPickerOpen)
        mmfs[self.selectedObject].materialSpecular.color, mmfs[self.selectedObject].materialSpecular.colorPickerOpen = self.ui_helper.add_color3('Specular Color', mmfs[self.selectedObject].materialSpecular.color, mmfs[self.selectedObject].materialSpecular.colorPickerOpen)
        mmfs[self.selectedObject].materialEmission.color, mmfs[self.selectedObject].materialEmission.colorPickerOpen = self.ui_helper.add_color3('Emission Color', mmfs[self.selectedObject].materialEmission.color, mmfs[self.selectedObject].materialEmission.colorPickerOpen)
        return mmfs

    def render_effects(self, mmfs):
        opened_gb, _ = imgui.collapsing_header('Gaussian Blur')
        if opened_gb:
            imgui.indent()
            imgui.begin_group()
            gb_items = ['No Blur', 'Horizontal', 'Vertical']
            _, mmfs[self.selectedObject].Effect_GBlur_Mode = imgui.combo("Mode##228", mmfs[self.selectedObject].Effect_GBlur_Mode, gb_items)
            mmfs[self.selectedObject].Effect_GBlur_Radius.animate, mmfs[self.selectedObject].Effect_GBlur_Radius.point = self.ui_helper.add_controls_slider_same_line('Radius', 16, 0.0, 0.0, 1000.0, True, mmfs[self.selectedObject].Effect_GBlur_Radius.animate, mmfs[self.selectedObject].Effect_GBlur_Radius.point, True, self.is_frame)
            mmfs[self.selectedObject].Effect_GBlur_Width.animate, mmfs[self.selectedObject].Effect_GBlur_Width.point = self.ui_helper.add_controls_slider_same_line('Radius', 17, 0.0, 0.0, 1000.0, True, mmfs[self.selectedObject].Effect_GBlur_Width.animate, mmfs[self.selectedObject].Effect_GBlur_Width.point, True, self.is_frame)
            imgui.end_group()
            imgui.unindent()
        opened_ftm, _ = imgui.collapsing_header('Filmic Tone Mapping')
        if opened_ftm:
            imgui.indent()
            imgui.begin_group()
            _, mmfs[self.selectedObject].Effect_ToneMapping_ACESFilmRec2020 = imgui.checkbox('ACES Film Rec2020', mmfs[self.selectedObject].Effect_ToneMapping_ACESFilmRec2020)
            imgui.end_group()
            imgui.unindent()
        return mmfs

    def render_illumination_type(self, mmfs):
        imgui.text('Illumination type')
        ilt_items = [
            '[0] Color on and Ambient off',
            '[1] Color on and Ambient on',
            '[2] Highlight on',
            '[3] Reflection on and Raytrace on',
            '[4] Transparency: Glass on\n    Reflection: Raytrace on',
            '[5] Reflection: Fresnel on\n    Raytrace on',
            '[6] Transparency: Refraction on\n    Reflection: Fresnel off\n    Raytrace on',
            '[7] Transparency: Refraction on\n    Reflection: Fresnel on\n    Raytrace on',
            '[8] Reflection on\n    Raytrace off',
            '[9] Transparency: Glass on\n    Reflection: Raytrace off',
            '[10] Casts shadows onto invisible surfaces'
        ]
        _, mmfs[self.selectedObject].materialIlluminationModel = imgui.combo("", mmfs[self.selectedObject].materialIlluminationModel, ilt_items)
        return mmfs

    def show_texture_line(self, chkLabel, meshModelFaces, texType, showWindow, loadTexture):
        mmf = meshModelFaces[self.selectedObject]
        title = ''
        useTexture = False
        image = ''

        if texType == MaterialTextureType.MaterialTextureType_Ambient:
            title = 'Ambient'
            useTexture = mmf.mesh_model.ModelMaterial.texture_ambient.UseTexture
            image = mmf.mesh_model.ModelMaterial.texture_ambient.Image
        elif texType == MaterialTextureType.MaterialTextureType_Diffuse:
            title = 'Diffuse'
            useTexture = mmf.mesh_model.ModelMaterial.texture_diffuse.UseTexture
            image = mmf.mesh_model.ModelMaterial.texture_diffuse.Image
        elif texType == MaterialTextureType.MaterialTextureType_Dissolve:
            title = 'Dissolve'
            useTexture = mmf.mesh_model.ModelMaterial.texture_dissolve.UseTexture
            image = mmf.mesh_model.ModelMaterial.texture_dissolve.Image
        elif texType == MaterialTextureType.MaterialTextureType_Bump:
            title = 'Normal'
            useTexture = mmf.mesh_model.ModelMaterial.texture_normal.UseTexture
            image = mmf.mesh_model.ModelMaterial.texture_normal.Image
        elif texType == MaterialTextureType.MaterialTextureType_Specular:
            title = 'Specular'
            useTexture = mmf.mesh_model.ModelMaterial.texture_specular.UseTexture
            image = mmf.mesh_model.ModelMaterial.texture_specular.Image
        elif texType == MaterialTextureType.MaterialTextureType_SpecularExp:
            title = 'Specular Exp'
            useTexture = mmf.mesh_model.ModelMaterial.texture_specular_exp.UseTexture
            image = mmf.mesh_model.ModelMaterial.texture_specular_exp.Image
        elif texType == MaterialTextureType.MaterialTextureType_Displacement:
            title = 'Displacement'
            useTexture = mmf.mesh_model.ModelMaterial.texture_displacement.UseTexture
            image = mmf.mesh_model.ModelMaterial.texture_displacement.Image

        if image != '':
            _, useTexture = imgui.checkbox(chkLabel, useTexture)
            if imgui.is_item_hovered():
                imgui.set_tooltip('Show/Hide ' + title + ' Texture')
            if texType == MaterialTextureType.MaterialTextureType_Ambient:
                meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_ambient.UseTexture = useTexture
            elif texType == MaterialTextureType.MaterialTextureType_Diffuse:
                meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_diffuse.UseTexture = useTexture
            elif texType == MaterialTextureType.MaterialTextureType_Dissolve:
                meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_dissolve.UseTexture = useTexture
            elif texType == MaterialTextureType.MaterialTextureType_Bump:
                meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_normal.UseTexture = useTexture
            elif texType == MaterialTextureType.MaterialTextureType_Specular:
                meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_specular.UseTexture = useTexture
            elif texType == MaterialTextureType.MaterialTextureType_SpecularExp:
                meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_specular_exp.UseTexture = useTexture
            elif texType == MaterialTextureType.MaterialTextureType_Displacement:
                meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_displacement.UseTexture = useTexture
            imgui.same_line()
            if imgui.button('X' + chkLabel):
                loadTexture = False
                if texType == MaterialTextureType.MaterialTextureType_Ambient:
                    meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_ambient.UseTexture = False
                elif texType == MaterialTextureType.MaterialTextureType_Diffuse:
                    meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_diffuse.UseTexture = False
                elif texType == MaterialTextureType.MaterialTextureType_Dissolve:
                    meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_dissolve.UseTexture = False
                elif texType == MaterialTextureType.MaterialTextureType_Bump:
                    meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_normal.UseTexture = False
                elif texType == MaterialTextureType.MaterialTextureType_Specular:
                    meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_specular.UseTexture = False
                elif texType == MaterialTextureType.MaterialTextureType_SpecularExp:
                    meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_specular_exp.UseTexture = False
                elif texType == MaterialTextureType.MaterialTextureType_Displacement:
                    meshModelFaces[self.selectedObject].mesh_model.ModelMaterial.texture_displacement.UseTexture = False
            imgui.same_line()
            if imgui.button('V' + chkLabel):
                showWindow = not showWindow
                loadTexture = True
            imgui.same_line()
            if imgui.button('E' + chkLabel):
                # TODO: show UV editor
                pass
            imgui.same_line()
            k = image.rfind('/')
            if k == 0:
                tex_image = image
            else:
                tex_image = image[k + 1:]
            imgui.text(title + ': ' + tex_image)
        else:
            btnLabel = 'Add Texture ' + title
            if imgui.button(btnLabel, -1, 0):
                # TODO: show UV editor
                pass

        return meshModelFaces, showWindow, loadTexture

    def show_texture_image(self, mmf, texType, title, showWindow, genTexture, vboBuffer, width, height):
        wWidth = Settings.AppWindowWidth
        wHeight = Settings.AppWindowHeight
        img = ''
        if texType == MaterialTextureType.MaterialTextureType_Ambient:
            img = mmf.mesh_model.ModelMaterial.texture_ambient.Image
        elif texType == MaterialTextureType.MaterialTextureType_Diffuse:
            img = mmf.mesh_model.ModelMaterial.texture_diffuse.Image
        elif texType == MaterialTextureType.MaterialTextureType_Dissolve:
            img = mmf.mesh_model.ModelMaterial.texture_dissolve.Image
        elif texType == MaterialTextureType.MaterialTextureType_Bump:
            img = mmf.mesh_model.ModelMaterial.texture_normal.Image
        elif texType == MaterialTextureType.MaterialTextureType_Displacement:
            img = mmf.mesh_model.ModelMaterial.texture_displacement.Image
        elif texType == MaterialTextureType.MaterialTextureType_Specular:
            img = mmf.mesh_model.ModelMaterial.texture_specular.Image
        elif texType == MaterialTextureType.MaterialTextureType_SpecularExp:
            img = mmf.mesh_model.ModelMaterial.texture_specular_exp.Image

        if genTexture:
            vboBuffer, width, height = self.create_texture_buffer(img, vboBuffer, width, height)

        tWidth = width + 20
        if tWidth > wWidth:
            tWidth = wWidth - 20
        tHeight = height + 20
        if tHeight > wHeight:
            tHeight = wHeight - 40

        imgui.set_next_window_position(20, 30, imgui.FIRST_USE_EVER)
        imgui.set_next_window_size(tWidth, tHeight, imgui.FIRST_USE_EVER)

        title = title + ' Texture'
        imgui.begin(title, showWindow, imgui.WINDOW_HORIZONTAL_SCROLLING_BAR)

        imgui.text('Image: ' + img)
        imgui.text('Image Dimensions: ' + str(width) + ' x ' + str(height))
        imgui.separator()
        imgui.image(vboBuffer, width, height)

        imgui.end()

        genTexture = False

        return showWindow, genTexture, vboBuffer, width, height

    def create_texture_buffer(self, imageFile, vboBuffer, width, height):
        if not os.path.exists(imageFile):
            imageFile = Settings.Settings_CurrentFolder + '/' + imageFile

        texture_image = Image.open(imageFile, 'r')
        texture_image_data = numpy.array(list(texture_image.getdata()), numpy.uint8)
        width = texture_image.width
        height = texture_image.height
        vboBuffer = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, vboBuffer)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)
        if texture_image.mode == "RGBA":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_data)
        elif texture_image.mode == "RGB":
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_image_data)
        texture_image.close()

        return vboBuffer, width, height
