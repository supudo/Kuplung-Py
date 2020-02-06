# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""

import imgui
import time
from settings import Settings
from meshes.artefacts.Shadertoy import Shadertoy


__author__ = 'supudo'
__version__ = "1.0.0"

class DialogShadertoy():

    def __init__(self):
        self.viewPaddingHorizontal = 20.0
        self.viewPaddingVertical = 40.0
        self.heightTopPanel = 200.0
        self.widthTexturesPanel = 140.0
        self.buttonCompileHeight = 44.0
        self.windowWidth = 0
        self.windowHeight = 0
        self.textureWidth = self.windowWidth - self.viewPaddingHorizontal
        self.textureHeight = self.windowHeight - self.viewPaddingVertical
        self.scrolling = [0, 0]

        self.channel0Cube = False
        self.channel1Cube = False
        self.channel2Cube = False
        self.channel3Cube = False
        self.cubemapImage0 = -1
        self.cubemapImage1 = -1
        self.cubemapImage2 = -1
        self.cubemapImage3 = -1
        self.texImage0 = -1
        self.texImage1 = -1
        self.texImage2 = -1
        self.texImage3 = -1

        self.vboTexture = -1

        self.shadertoyEditorText = "void mainImage(out vec4 fragColor, in vec2 fragCoord)\n" +\
        "{\n" +\
        "   vec2 uv = fragCoord.xy / iResolution.xy;\n" +\
        "   fragColor = vec4(uv, 0.5 + 0.5 * sin(iGlobalTime), 1.0);\n" +\
        "}\n"

        self.engineShadertoy = Shadertoy()
        self.engineShadertoy.iChannel0_Image = 'noise16.png'
        self.engineShadertoy.initShaderProgram(self.shadertoyEditorText)
        self.engineShadertoy.initBuffers()
        self.vboTexture = self.engineShadertoy.initFBO(Settings.AppWindowWidth, Settings.AppWindowHeight, self.vboTexture)

    def render(self, is_opened):
        imgui.set_next_window_size(1238, 793, imgui.FIRST_USE_EVER)
        imgui.set_next_window_position(26, 34, imgui.FIRST_USE_EVER)

        _, is_opened = imgui.begin('Shadertoy.com', is_opened, 0)

        imgui_io = imgui.get_io()

        self.windowWidth = imgui.get_window_width()
        self.windowHeight = imgui.get_window_height()
        self.textureWidth = int(self.windowWidth - self.viewPaddingHorizontal)
        self.textureHeight = int(self.windowHeight - self.viewPaddingVertical)

        if self.heightTopPanel < self.engineShadertoy.textureHeight or self.heightTopPanel > self.engineShadertoy.textureHeight:
            self.vboTexture = self.engineShadertoy.initFBO(self.windowWidth, self.heightTopPanel, self.vboTexture)

        app_time = time.time() - Settings.ApplicationStartTime
        self.vboTexture = self.engineShadertoy.renderToTexture(imgui_io.mouse_pos.x, imgui_io.mouse_pos.y, app_time, self.vboTexture)

        # shader render
        imgui.begin_child('Preview', 0, self.heightTopPanel, True)
        imgui.image(self.vboTexture, self.textureWidth, self.textureHeight)
        imgui.end_child()

        # splitter
        imgui_io.mouse_draw_cursor = True
        imgui.push_style_color(imgui.COLOR_BUTTON, 89 / 255.0, 91 / 255.0, 94 / 255.0, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 119 / 255.0, 122 / 255.0, 124 / 255.0, 1.0)
        imgui.push_style_color(imgui.COLOR_BORDER, 0, 0, 0, 1)
        imgui.button("###splitterShadertoy", -1, 6.0)
        imgui.pop_style_color(3)
        if imgui.is_item_active():
            self.heightTopPanel += imgui.get_mouse_drag_delta().y
        if imgui.is_item_hovered():
            imgui.set_mouse_cursor(3)
        else:
            imgui_io.mouse_draw_cursor = False

        # editor
        imgui.begin_child('Editor')

        if imgui.button('COMPILE', imgui.get_window_width() * 0.85, self.buttonCompileHeight):
            self.compileShader()
        imgui.same_line()
        if imgui.button('PASTE', imgui.get_window_width() * 0.14, self.buttonCompileHeight):
            self.getFromClipboard()

        # textures
        imgui.begin_child('Options', self.widthTexturesPanel, 0, False)
        imgui.text('Examples')

        if imgui.button('Artificial', -1, 0):
            self.openExample('/shaders/stoy/4ljGW1.stoy')
        if imgui.is_item_hovered():
            imgui.set_tooltip('Artificial')

        if imgui.button('Combustible\nVoronoi Layers', -1, 0):
            self.openExample('/shaders/stoy/4tlSzl.stoy')
        if imgui.is_item_hovered():
            imgui.set_tooltip('Combustible Voronoi Layers')

        if imgui.button('Seascape', -1, 0):
            self.openExample('/shaders/stoy/Ms2SD1.stoy')
        if imgui.is_item_hovered():
            imgui.set_tooltip('Seascape')

        if imgui.button('Star Nest', -1, 0):
            self.openExample('/shaders/stoy/XlfGRj.stoy')
        if imgui.is_item_hovered():
            imgui.set_tooltip('Star Nest')

        if imgui.button('Sun Surface', -1, 0):
            self.openExample('/shaders/stoy/XlSSzK.stoy')
        if imgui.is_item_hovered():
            imgui.set_tooltip('Sun Surface')

        imgui.separator()

        textureImages = [
            " -- NONE -- ",
            "tex00.jpg", "tex01.jpg", "tex02.jpg", "tex03.jpg", "tex04.jpg",
            "tex05.jpg", "tex06.jpg", "tex07.jpg", "tex08.jpg", "tex09.jpg",
            "tex10.jpg", "tex11.jpg", "tex12.jpg", "tex13.jpg", "tex14.jpg",
            "tex15.jpg", "tex16.jpg", "tex17.jpg", "tex18.jpg", "tex19.jpg",
            "tex20.jpg"
        ]

        cubemapImages = [
            " -- NONE -- ",
            "cube00_0.jpg", "cube00_1.jpg", "cube00_2.jpg", "cube00_3.jpg",
            "cube00_4.jpg", "cube00_5.jpg", "cube01_0.png", "cube01_1.png",
            "cube01_2.png", "cube01_3.png", "cube01_4.png", "cube01_5.png",
            "cube02_0.jpg", "cube02_1.jpg", "cube02_2.jpg", "cube02_3.jpg",
            "cube02_4.jpg", "cube02_5.jpg", "cube03_0.png", "cube03_1.png",
            "cube03_2.png", "cube03_3.png", "cube03_4.png", "cube03_5.png",
            "cube04_0.png", "cube04_1.png", "cube04_2.png", "cube04_3.png",
            "cube04_4.png", "cube04_5.png", "cube05_0.png", "cube05_1.png",
            "cube05_2.png", "cube05_3.png", "cube05_4.png", "cube05_5.png"
        ]

        imgui.push_item_width(-1)
        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 6))
        imgui.push_style_var(imgui.STYLE_WINDOW_MIN_SIZE, (0, 100))

        imgui.text_colored('Channel #0', 1, 0, 0, 1)
        _, self.channel0Cube = imgui.checkbox('Cubemap?##001', self.channel0Cube)
        if self.channel0Cube:
            _, self.cubemapImage0 = imgui.listbox('##cubemap0', self.cubemapImage0, cubemapImages, 3)
        else:
            _, self.texImage0 = imgui.listbox('##texImage0', self.texImage0, textureImages, 3)

        imgui.separator()

        imgui.text_colored('Channel #0', 1, 0, 0, 1)
        _, self.channel1Cube = imgui.checkbox('Cubemap?##002', self.channel1Cube)
        if self.channel1Cube:
            _, self.cubemapImage1 = imgui.listbox('##cubemap1', self.cubemapImage1, cubemapImages, 3)
        else:
            _, self.texImage1 = imgui.listbox('##texImage1', self.texImage1, textureImages, 3)

        imgui.separator()

        imgui.text_colored('Channel #2', 1, 0, 0, 1)
        _, self.channel2Cube = imgui.checkbox('Cubemap?##003', self.channel2Cube)
        if self.channel2Cube:
            _, self.cubemapImage02 = imgui.listbox('##cubemap2', self.cubemapImage2, cubemapImages, 3)
        else:
            _, self.texImage2 = imgui.listbox('##texImage2', self.texImage2, textureImages, 3)

        imgui.separator()

        imgui.text_colored('Channel #3', 1, 0, 0, 1)
        _, self.channel3Cube = imgui.checkbox('Cubemap?##004', self.channel3Cube)
        if self.channel3Cube:
            _, self.cubemapImage3 = imgui.listbox('##cubemap3', self.cubemapImage3, cubemapImages, 3)
        else:
            _, self.texImage3 = imgui.listbox('##texImage3', self.texImage3, textureImages, 3)

        imgui.pop_style_var(2)
        # imgui.pop_item_width()

        if self.texImage0 > 0:
            self.engineShadertoy.iChannel0_CubeImage = ''
            self.engineShadertoy.iChannel0_Image = 'tex' + ('0' if self.texImage0 < 0 else '') + str(self.texImage0) + '.jpg'
            self.texImage0 = 0
        if self.cubemapImage0 > 0:
            self.engineShadertoy.iChannel0_CubeImage = cubemapImages[self.cubemapImage0]
            self.engineShadertoy.iChannel0_Image = ''
            self.cubemapImage0 = 0

        if self.texImage1 > 0:
            self.engineShadertoy.iChannel1_CubeImage = ''
            self.engineShadertoy.iChannel1_Image = 'tex' + ('0' if self.texImage1 < 0 else '') + str(self.texImage1) + '.jpg'
            self.texImage1 = 0
        if self.cubemapImage1 > 0:
            self.engineShadertoy.iChannel1_CubeImage = cubemapImages[self.cubemapImage1]
            self.engineShadertoy.iChannel1_Image = ''
            self.cubemapImage1 = 0

        if self.texImage2 > 0:
            self.engineShadertoy.iChannel2_CubeImage = ''
            self.engineShadertoy.iChannel2_Image = 'tex' + ('0' if self.texImage2 < 0 else '') + str(self.texImage2) + '.jpg'
            self.texImage2 = 0
        if self.cubemapImage2 > 0:
            self.engineShadertoy.iChannel2_CubeImage = cubemapImages[self.cubemapImage2]
            self.engineShadertoy.iChannel2_Image = ''
            self.cubemapImage2 = 0

        if self.texImage3 > 0:
            self.engineShadertoy.iChannel3_CubeImage = ''
            self.engineShadertoy.iChannel3_Image = 'tex' + ('0' if self.texImage3 < 0 else '') + str(self.texImage3) + '.jpg'
            self.texImage3 = 0
        if self.cubemapImage3 > 0:
            self.engineShadertoy.iChannel3_CubeImage = cubemapImages[self.cubemapImage3]
            self.engineShadertoy.iChannel3_Image = ''
            self.cubemapImage3 = 0

        imgui.end_child()

        # texture delimiter
        imgui.same_line()
        imgui_io.mouse_draw_cursor = True
        imgui.push_style_color(imgui.COLOR_BUTTON, 89 / 255.0, 91 / 255.0, 94 / 255.0, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 119 / 255.0, 122 / 255.0, 124 / 255.0, 1.0)
        imgui.push_style_color(imgui.COLOR_BORDER, 0, 0, 0, 1)
        imgui.button("###splitterShadertoyTextures", 4, -1)
        imgui.pop_style_color(3)
        if imgui.is_item_active():
            self.widthTexturesPanel += imgui.get_mouse_drag_delta().x
        if imgui.is_item_hovered():
            imgui.set_mouse_cursor(4)
        else:
            imgui_io.mouse_draw_cursor = False
        imgui.same_line()

        # editor
        imgui.begin_child('IDE', 0, 0, False)
        # lines = (imgui.get_window_height() - 4.0) / imgui.get_text_line_height()
        # imgui.input_text_multiline('##source', self.shadertoyEditorText, -1, imgui.get_text_line_height() * lines, imgui.INPUT_TEXT_FLAGS_ALLOW_TAB_INPUT)
        imgui.end_child()

        imgui.end_child()

        if imgui.is_window_hovered() and not imgui.is_any_item_active() and imgui.is_mouse_dragging(2, 0):
            self.scrolling = self.scrolling - imgui_io.mouse_delta

        imgui.end()

        return is_opened

    def compileShader(self):
        self.engineShadertoy = Shadertoy()
        self.engineShadertoy.initShaderProgram(self.shadertoyEditorText)
        self.engineShadertoy.initBuffers()
        self.vboTexture = self.engineShadertoy.initFBO(Settings.AppWindowWidth, Settings.AppWindowHeight, self.vboTexture)

    def getFromClipboard(self):
        pass

    def openExample(self, fileName):
        file_fs = open('resources' + fileName, 'r', encoding='utf-8')
        fs_str = str(file_fs.read())
        self.shadertoyEditorText = fs_str
