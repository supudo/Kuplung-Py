"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import glfw
import OpenGL.GL as gl

import imgui
from imgui.impl import GlfwImpl
from settings import Settings
from consumption import Consumption


class ImGuiWindow():
    gui_controls_visible = True
    scene_controls_visible = True
    visual_artefacts_visible = True
    app_is_running = False

    # Main menu
    show_save_image = False
    show_render_ui = False
    show_imgui_test_window = False

    def show_main_window(self):
        self.init_gl()
        self.init_window()
        self.init_imgui_impl()

        self.imgui_style = imgui.GuiStyle()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.imgui_context.new_frame()
            self.render_main_menu()
            self.render_dialogs()
            self.render_ui_content()
            self.render_scene()
            imgui.render()
            glfw.swap_buffers(self.window)

        glfw.terminate()

    def init_gl(self):
        if not glfw.init():
            Settings.log_error("Could not initialize OpenGL context")
            exit(1)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    def init_window(self):
        self.window = glfw.create_window(
            int(Settings.AppMainWindowWidth),
            int(Settings.AppMainWindowHeight),
            Settings.AppMainWindowTitle, None, None
        )
        glfw.make_context_current(self.window)
        if not self.window:
            glfw.terminate()
            Settings.log_error("Could not initialize Window")
            exit(1)

    def init_imgui_impl(self):
        self.imgui_context = GlfwImpl(self.window)
        self.imgui_context.enable()
        self.app_is_running = True

    def render_main_menu(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File".encode('utf-8'), True):
                imgui.menu_item("New".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Open ...".encode('utf-8'), ''.encode('utf-8'), False, True)
                if imgui.begin_menu("Open Recent".encode('utf-8'), True):
                    imgui.end_menu()
                imgui.menu_item("Save ...".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.separator()
                if imgui.begin_menu("Import".encode('utf-8'), True):
                    imgui.menu_item("Wavefront (.OBJ)".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.end_menu()
                if imgui.begin_menu("Import Recent".encode('utf-8'), True):
                    imgui.end_menu()
                if imgui.begin_menu("Export".encode('utf-8'), True):
                    imgui.menu_item("Wavefront (.OBJ)".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.end_menu()
                imgui.separator()
                imgui.menu_item("Quit".encode('utf-8'), 'Cmd+Q'.encode('utf-8'), False, True)
                imgui.end_menu()

            if imgui.begin_menu("Scene".encode('utf-8'), True):
                if imgui.begin_menu("Add Light".encode('utf-8'), True):
                    imgui.menu_item("Directional (Sun)".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.menu_item("Point (Light bulb)".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.menu_item("Spot (Flashlight)".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.end_menu()
                imgui.separator()
                if imgui.begin_menu("Scene Rendering".encode('utf-8'), True):
                    imgui.menu_item("Solid".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.menu_item("Material".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.menu_item("Texture".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.menu_item("Wireframe".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.menu_item("Rendered".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.separator()
                    imgui.menu_item("Render - Depth".encode('utf-8'), ''.encode('utf-8'), False, True)
                    imgui.end_menu()
                imgui.separator()
                opened_show_render_image, self.show_save_image = imgui.menu_item("Render Image".encode('utf-8'), ''.encode('utf-8'), self.show_save_image, True)
                opened_show_render_ui, self.show_render_ui = imgui.menu_item("Render UI".encode('utf-8'), ''.encode('utf-8'), self.show_render_ui, True)
                imgui.end_menu()

            if imgui.begin_menu("View".encode('utf-8'), True):
                imgui.menu_item("GUI Controls".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Scene Controls".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Hide Visual Artefacts".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.separator()
                imgui.menu_item("Show Log Window".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Screenshot".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Scene Statistics".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Structured Volumetric Sampling".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Shadertoy".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.separator()
                imgui.menu_item("Shadertoy".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("Options".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.end_menu()

            if imgui.begin_menu("Help".encode('utf-8'), True):
                imgui.menu_item("Metrics".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("About ImGui".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("About PyImGui".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.menu_item("About Kuplung".encode('utf-8'), ''.encode('utf-8'), False, True)
                imgui.separator()
                opened_show_imgui_test_window, self.show_imgui_test_window = imgui.menu_item("ImGui Demo Window".encode('utf-8'), ''.encode('utf-8'), self.show_imgui_test_window, True)
                imgui.end_menu()

            imgui.text(self.getAppConsumption().encode('utf-8'))
            imgui.end_main_menu_bar()

    def render_dialogs(self):
        if self.show_imgui_test_window:
            imgui.show_test_window()

    def render_ui_content(self):
        pass
        # imgui.show_user_guide()
        # imgui.show_test_window()

        # if self.app_is_running:
        #     imgui.begin("fooo".encode('utf-8'), True)
        #     imgui.text("Bar".encode('utf-8'))
        #     imgui.text_colored("Eggs".encode('utf-8'), 0.2, 1., 0.)
        #     imgui.end()
        #
        # with imgui.styled(imgui.STYLE_ALPHA, 1):
        #     imgui.show_metrics_window()
        #
        # imgui.show_style_editor(self.imgui_style)

    def render_scene(self):
        width, height = glfw.get_framebuffer_size(self.window)
        gl.glViewport(0, 0, int(width / 2), int(height))
        gl.glClearColor(Settings.guiClearColor[0],
                        Settings.guiClearColor[1],
                        Settings.guiClearColor[2],
                        Settings.guiClearColor[3])
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def getAppConsumption(self):
        consumption_str = Consumption.memory()
        return "﻿--> {0} FPS | {1} objs, {2} verts, {3} indices ({4} tris, {5} faces) | {6}".format(
            0,
            Settings.SceneCountObjects, Settings.SceneCountVertices,
            Settings.SceneCountIndices, Settings.SceneCountTriangles,
            Settings.SceneCountFaces,
            consumption_str)