# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

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

    def render(self, delegate, is_opened, managerObjects, meshModelFaces, is_frame):
        self.is_frame = is_frame

        imgui.set_next_window_size(300, 600, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(10, 28, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('Scene Settings', is_opened, imgui.WINDOW_SHOW_BORDERS)

        tab_labels = ['Models', 'Create']
        tab_icons = ['ICON_MD_BUILD', 'ICON_MD_ADD']
        self.selectedTabPanel = self.ui_helper.draw_tabs(tab_labels, tab_icons, self.selectedTabPanel)

        if self.selectedTabPanel == 0:
            if meshModelFaces is not None and len(meshModelFaces) > 0:
                meshModelFaces = self.render_models(meshModelFaces)
            else:
                imgui.text_colored('No models in the current scene.', 255, 0, 0, 255)
        else:
            self.render_create(delegate)

        imgui.end()

        return is_opened, meshModelFaces

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
        # reset defaults button
        imgui.push_style_color(imgui.COLOR_BUTTON, .6, .1, .1, 1)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, .9, .1, .1, 1)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, .8, .2, .2, 1)
        if imgui.button('Reset values to default', -1, 0):
            for i in range(len(meshModelFaces)):
                meshModelFaces[i].initModelProperties()
        imgui.pop_style_color(3)

        # scene items
        imgui.begin_child("Scene Items".encode('utf-8'), 0.0, self.height_top_panel, True)

        scene_items = []
        for item in meshModelFaces:
            scene_items.append(item.mesh_model.ModelTitle)

        imgui.push_item_width(-1)
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 6))
        imgui.push_style_var(imgui.STYLE_WINDOW_MIN_SIZE, (0, 100))
        imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, 0, 0, 0, 1)
        _, self.selectedObject = imgui.listbox('', self.selectedObject, scene_items)
        imgui.pop_style_color(1)
        imgui.pop_style_var(2)
        # TODO: context menu for actions
        imgui.pop_item_width()

        imgui.end_child()

        # properties
        imgui.begin_child("Properties Pane".encode('utf-8'), 0.0, 0.0, False)
        imgui.push_item_width(imgui.get_window_width() * 0.75)

        if self.selectedObject > -1:
            mmf = meshModelFaces[self.selectedObject]
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

            meshModelFaces, self.showTextureWindow_Ambient, self.showTexture_Ambient = self.show_texture_line('##001', meshModelFaces, MaterialTextureType.MaterialTextureType_Ambient, self.showTextureWindow_Ambient, self.showTexture_Ambient)
            meshModelFaces, self.showTextureWindow_Diffuse, self.showTexture_Diffuse = self.show_texture_line('##002', meshModelFaces, MaterialTextureType.MaterialTextureType_Diffuse, self.showTextureWindow_Diffuse, self.showTexture_Diffuse)
            meshModelFaces, self.showTextureWindow_Dissolve, self.showTexture_Dissolve = self.show_texture_line('##003', meshModelFaces, MaterialTextureType.MaterialTextureType_Dissolve, self.showTextureWindow_Dissolve, self.showTexture_Dissolve)
            meshModelFaces, self.showTextureWindow_Bump, self.showTexture_Bump = self.show_texture_line('##004', meshModelFaces, MaterialTextureType.MaterialTextureType_Bump, self.showTextureWindow_Bump, self.showTexture_Bump)
            meshModelFaces, self.showTextureWindow_Displacement, self.showTexture_Displacement = self.show_texture_line('##005', meshModelFaces, MaterialTextureType.MaterialTextureType_Displacement, self.showTextureWindow_Displacement, self.showTexture_Displacement)
            meshModelFaces, self.showTextureWindow_Specular, self.showTexture_Specular = self.show_texture_line('##006', meshModelFaces, MaterialTextureType.MaterialTextureType_Specular, self.showTextureWindow_Specular, self.showTexture_Specular)
            meshModelFaces, self.showTextureWindow_SpecularExp, self.showTexture_SpecularExp = self.show_texture_line('##007', meshModelFaces, MaterialTextureType.MaterialTextureType_SpecularExp, self.showTextureWindow_SpecularExp, self.showTexture_SpecularExp)

            if self.showTextureWindow_Ambient:
                self.showTextureWindow_Ambient, self.showTexture_Ambient, self.vboTextureAmbient, self.textureAmbient_Width, self.textureAmbient_Height = self.show_texture_image(meshModelFaces[self.selectedObject], MaterialTextureType.MaterialTextureType_Ambient, 'Ambient', self.showTextureWindow_Ambient, self.showTexture_Ambient, self.vboTextureAmbient, self.textureAmbient_Width, self.textureAmbient_Height)
            if self.showTextureWindow_Diffuse:
                self.showTextureWindow_Diffuse, self.showTexture_Diffuse, self.vboTextureDiffuse, self.textureDiffuse_Width, self.textureDiffuse_Height = self.show_texture_image(meshModelFaces[self.selectedObject], MaterialTextureType.MaterialTextureType_Diffuse, 'Diffuse', self.showTextureWindow_Diffuse, self.showTexture_Diffuse, self.vboTextureDiffuse, self.textureDiffuse_Width, self.textureDiffuse_Height)

        imgui.pop_item_width()
        imgui.end_child()

        return meshModelFaces

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
            if imgui.button(btnLabel):
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
        imgui.begin(title, showWindow, imgui.WINDOW_SHOW_BORDERS | imgui.WINDOW_HORIZONTAL_SCROLLING_BAR)

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
