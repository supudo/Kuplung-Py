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
from parsers.OBJ.ParserObj import ParserObj
from rendering.RenderingManager import RenderingManager
from rendering.ModelFace import ModelFace


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
        self.init_rendering_manager()
        self.imgui_style = imgui.GuiStyle()

        self.printGLStrings()

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
            Settings.log_error("[ImGuiWindow] Could not initialize OpenGL context")
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
            Settings.log_error("[ImGuiWindow] Could not initialize Window")
            exit(1)

    def init_imgui_impl(self):
        self.imgui_context = GlfwImpl(self.window)
        self.imgui_context.enable()
        self.app_is_running = True

    def render_main_menu(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                clicked_new, selected_new = imgui.menu_item("New", '', False, True)
                if clicked_new:
                    print("new was clicked")
                imgui.menu_item("Open ...", '', False, True)
                if imgui.begin_menu("Open Recent", True):
                    imgui.end_menu()
                imgui.menu_item("Save ...", '', False, True)
                imgui.separator()
                if imgui.begin_menu("Import", True):
                    imgui.menu_item("Wavefront (.OBJ)", '', False, True)
                    imgui.end_menu()
                if imgui.begin_menu("Import Recent", True):
                    imgui.menu_item("file 1...", '', False, True)
                    imgui.end_menu()
                if imgui.begin_menu("Export", True):
                    imgui.menu_item("Wavefront (.OBJ)", '', False, True)
                    imgui.end_menu()
                imgui.separator()
                clicked_quit, selected_quit = imgui.menu_item("Quit", 'Cmd+Q', False, True)
                if clicked_quit:
                    exit(1)
                imgui.end_menu()

            if imgui.begin_menu("Scene", True):
                if imgui.begin_menu("Add Light", True):
                    imgui.menu_item("Directional (Sun)", '', False, True)
                    imgui.menu_item("Point (Light bulb)", '', False, True)
                    imgui.menu_item("Spot (Flashlight)", '', False, True)
                    imgui.end_menu()
                imgui.separator()
                if imgui.begin_menu("Scene Rendering", True):
                    imgui.menu_item("Solid", '', False, True)
                    imgui.menu_item("Material", '', False, True)
                    imgui.menu_item("Texture", '', False, True)
                    imgui.menu_item("Wireframe", '', False, True)
                    imgui.menu_item("Rendered", '', False, True)
                    imgui.separator()
                    imgui.menu_item("Render - Depth", '', False, True)
                    imgui.end_menu()
                imgui.separator()
                opened_show_render_image, self.show_save_image = imgui.menu_item("Render Image", '', self.show_save_image, True)
                opened_show_render_ui, self.show_render_ui = imgui.menu_item("Render UI", '', self.show_render_ui, True)
                imgui.end_menu()

            if imgui.begin_menu("View", True):
                imgui.menu_item("GUI Controls", '', False, True)
                imgui.menu_item("Scene Controls", '', False, True)
                imgui.menu_item("Hide Visual Artefacts", '', False, True)
                imgui.separator()
                imgui.menu_item("Show Log Window", '', False, True)
                imgui.menu_item("Screenshot", '', False, True)
                imgui.menu_item("Scene Statistics", '', False, True)
                imgui.menu_item("Structured Volumetric Sampling", '', False, True)
                imgui.menu_item("Shadertoy", '', False, True)
                imgui.separator()
                imgui.menu_item("Shadertoy", '', False, True)
                imgui.menu_item("Options", '', False, True)
                imgui.end_menu()

            if imgui.begin_menu("Help", True):
                imgui.menu_item("Metrics", '', False, True)
                imgui.menu_item("About ImGui", '', False, True)
                imgui.menu_item("About PyImGui", '', False, True)
                imgui.menu_item("About Kuplung", '', False, True)
                imgui.separator()
                opened_test_window, self.show_imgui_test_window = imgui.menu_item("ImGui Demo Window", '', self.show_imgui_test_window, True)
                imgui.end_menu()

            imgui.text(self.getAppConsumption())
            imgui.end_main_menu_bar()

    def render_dialogs(self):
        if self.show_imgui_test_window:
            imgui.show_test_window()

    def render_ui_content(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT |
                   gl.GL_DEPTH_BUFFER_BIT |
                   gl.GL_STENCIL_BUFFER_BIT)
        self.renderingManager.render(glfw.get_current_context())

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

    def init_rendering_manager(self):
        self.renderingManager = RenderingManager()
        self.renderingManager.initShaderProgram(glfw.get_current_context())

        self.parser = ParserObj()
        self.parser.parse_file('resources/shapes/', 'monkey_head.obj')

        for model in self.parser.mesh_models:
            model_face = ModelFace()
            model_face.initBuffers(glfw.get_current_context(), self.parser.mesh_models[model])
            self.renderingManager.model_faces.append(model_face)
        Settings.log_info("[ImGuiWindow] Models initialized...")

    def printGLStrings(self):
        Settings.log_info("[ImGuiWindow] Vendor: " + str(gl.glGetString(gl.GL_VENDOR)))
        Settings.log_info("[ImGuiWindow] OpenGL version: " + str(gl.glGetString(gl.GL_VERSION)))
        Settings.log_info("[ImGuiWindow] GLSL version: " + str(gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)))
        Settings.log_info("[ImGuiWindow] Renderer: " + str(gl.glGetString(gl.GL_RENDERER)))
