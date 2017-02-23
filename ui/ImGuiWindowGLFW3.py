# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import OpenGL.GL as gl
import glfw
import imgui
from imgui.impl import GlfwImpl

from consumption import Consumption
from parsers.ParserManager import ParserManager
from objects.ObjectsManager import ObjectsManager
from rendering.RenderingManager import RenderingManager
from objects.ControlsManagerGLFW import ControlsManagerGLFW
from settings import Settings
from meshes.scene.ModelFace import ModelFace
from ui.components.Log import Log
from ui.dialogs.DialogControlsModels import DialogControlsModels
from ui.dialogs.DialogControlsGUI import DialogControlsGUI


class ImGuiWindowGLFW3():

    # app
    managerParser = None
    controlsModels = None
    controlsGUI = None

    # dialogs
    gui_controls_visible = True
    scene_controls_visible = True
    visual_artefacts_visible = True
    app_is_running = False
    new_scene_clear = False

    # Main menu
    show_save_image = False
    show_render_ui = False
    show_imgui_test_window = False
    show_about_imgui = False
    show_about_pyimgui = False
    show_about_kuplung = False
    show_scene_metrics = False
    show_log_window = True
    show_controls_models = True
    show_controls_gui = True

    sceneSelectedModelObject = -1

    def show_main_window(self):
        self.init_gl()
        self.init_window()
        self.init_imgui_impl()
        self.init_sub_windows()
        self.init_components()
        self.init_glfw_handlers()
        self.init_rendering_manager()
        self.imgui_style = imgui.GuiStyle()
        self.init_objects_manager()

        self.printGLStrings()

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            self.handle_controls_events()

            w_width, w_height = glfw.get_window_size(self.window)
            Settings.AppWindowWidth, Settings.AppWindowHeight = w_width, w_height
            width, height = glfw.get_framebuffer_size(self.window)
            Settings.AppFramebufferWidth, Settings.AppFramebufferHeight = width, height
            gl.glViewport(0, 0, int(w_width / 2), int(w_height))
            gl.glClearColor(Settings.guiClearColor[0],
                            Settings.guiClearColor[1],
                            Settings.guiClearColor[2],
                            Settings.guiClearColor[3])
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)

            self.imgui_context.new_frame()
            self.render_screen()
            imgui.render()

            glfw.swap_buffers(self.window)

        glfw.terminate()

    def init_gl(self):
        if not glfw.init():
            Settings.log_error("[ImGuiWindow] Could not initialize OpenGL context!")
            exit(1)
        glfw.window_hint(glfw.DOUBLEBUFFER, 1)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.STENCIL_BITS, 8)
        glfw.window_hint(glfw.SAMPLES, 16)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    def init_window(self):
        self.window = glfw.create_window(
            int(Settings.AppFramebufferWidth),
            int(Settings.AppFramebufferHeight),
            Settings.AppMainWindowTitle,
            None, None
        )
        glfw.make_context_current(self.window)
        if not self.window:
            glfw.terminate()
            Settings.log_error("[ImGuiWindow] Could not initialize Window!")
            exit(1)

    def init_glfw_handlers(self):
        self.managerControls = ControlsManagerGLFW()
        self.managerControls.init_handlers(self.window)
        Settings.do_log("Control events initialized.")

    def init_sub_windows(self):
        self.controlsModels = DialogControlsModels()
        self.controlsGUI = DialogControlsGUI()
        Settings.do_log("GUI sub windows initialized.")

    def init_components(self):
        self.component_log = Log()
        Settings.FuncDoLog = self.component_log.add_to_log
        Settings.do_log("GUI components initialized.")

    def init_imgui_impl(self):
        self.imgui_context = GlfwImpl(self.window)
        self.imgui_context.enable()
        self.app_is_running = True
        Settings.do_log("PyImGui initialized.")


    def render_screen(self):
        self.render_main_menu()
        self.render_ui_content()
        self.render_scene()

    def handle_controls_events(self):
        if not imgui.is_mouse_hovering_any_window():
            if self.managerControls.keyPressed_LALT:
                if self.managerControls.mouseWheel['y'] < 0:
                    self.managerObjects.Setting_FOV += 4
                if self.managerControls.mouseWheel['y'] > 0:
                    self.managerObjects.Setting_FOV -= 4

                if self.managerObjects.Setting_FOV > 180:
                    self.managerObjects.Setting_FOV = 180
                if self.managerObjects.Setting_FOV < -180:
                    self.managerObjects.Setting_FOV = -180
            else:
                self.managerObjects.camera.positionZ['point'] += self.managerControls.mouseWheel['y']

            self.managerControls.reset_mouse_scroll()

            if self.managerControls.mouseButton_MIDDLE:
                # if self.managerControls.mouseGoUp or self.managerControls.mouseGoDown:
                #     self.managerObjects.camera.rotateX['point'] += self.managerControls.mouse_rel_y
                if self.managerControls.mouseGoDown:
                    self.managerObjects.camera.rotateX['point'] -= 2
                if self.managerControls.mouseGoUp:
                    self.managerObjects.camera.rotateX['point'] += 2
                if self.managerObjects.camera.rotateX['point'] > 360:
                    self.managerObjects.camera.rotateX['point'] = .0
                if self.managerObjects.camera.rotateX['point'] < .0:
                    self.managerObjects.camera.rotateX['point'] = 360

                # if self.managerControls.mouseGoLeft or self.managerControls.mouseGoRight:
                #     self.managerObjects.camera.rotateY['point'] += self.managerControls.mouse_rel_x
                if self.managerControls.mouseGoLeft:
                    self.managerObjects.camera.rotateY['point'] += 2
                if self.managerControls.mouseGoRight:
                    self.managerObjects.camera.rotateY['point'] -= 2
                if self.managerObjects.camera.rotateY['point'] > 360:
                    self.managerObjects.camera.rotateY['point'] = .0
                if self.managerObjects.camera.rotateY['point'] < .0:
                    self.managerObjects.camera.rotateY['point'] = 360

            self.managerControls.reset_mouse_motion()

    def render_main_menu(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                _, self.new_scene_clear = imgui.menu_item("New", '', False, True)
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
                    clicked_sc_solid, selected_sc_solid = imgui.menu_item("Solid", '', Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Solid, True)
                    if selected_sc_solid:
                        Settings.Setting_ModelViewSkin = Settings.ViewModelSkin.ViewModelSkin_Solid

                    clicked_sc_material, selected_sc_material = imgui.menu_item("Material", '', Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Material, True)
                    if selected_sc_material:
                        Settings.Setting_ModelViewSkin = Settings.ViewModelSkin.ViewModelSkin_Material

                    clicked_sc_texture, selected_sc_texture = imgui.menu_item("Texture", '', Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Texture, True)
                    if selected_sc_texture:
                        Settings.Setting_ModelViewSkin = Settings.ViewModelSkin.ViewModelSkin_Texture

                    clicked_sc_wireframe, selected_sc_wireframe = imgui.menu_item("Wireframe", '', Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Wireframe, True)
                    if selected_sc_wireframe:
                        Settings.Setting_ModelViewSkin = Settings.ViewModelSkin.ViewModelSkin_Wireframe

                    clicked_sc_rendered, selected_sc_rendered = imgui.menu_item("Rendered", '', Settings.Setting_ModelViewSkin == Settings.ViewModelSkin.ViewModelSkin_Rendered, True)
                    if selected_sc_rendered:
                        Settings.Setting_ModelViewSkin = Settings.ViewModelSkin.ViewModelSkin_Rendered

                    imgui.separator()

                    clicked_r_depth, selected_r_depth = imgui.menu_item("Render - Depth", '', Settings.Setting_Rendering_Depth, True)
                    if clicked_r_depth:
                        Settings.Setting_Rendering_Depth = not Settings.Setting_Rendering_Depth

                    imgui.end_menu()

                imgui.separator()
                opened_show_render_image, self.show_save_image = imgui.menu_item("Render Image", '', self.show_save_image, True)
                opened_show_render_ui, self.show_render_ui = imgui.menu_item("Render UI", '', self.show_render_ui, True)
                imgui.end_menu()

            if imgui.begin_menu("View", True):
                _, self.show_controls_gui = imgui.menu_item("GUI Controls", '', self.show_controls_gui, True)
                _, self.show_controls_models = imgui.menu_item("Scene Controls", '', self.show_controls_models, True)
                imgui.menu_item("Hide Visual Artefacts", '', False, True)
                imgui.separator()
                _, self.show_log_window = imgui.menu_item("Show Log Window", '', self.show_log_window, True)
                imgui.menu_item("Screenshot", '', False, True)
                imgui.menu_item("Scene Statistics", '', False, True)
                imgui.menu_item("Structured Volumetric Sampling", '', False, True)
                imgui.menu_item("Shadertoy", '', False, True)
                imgui.separator()
                imgui.menu_item("Shadertoy", '', False, True)
                imgui.menu_item("Options", '', False, True)
                imgui.end_menu()

            if imgui.begin_menu("Help", True):
                clicked_scene_metrics, _ = imgui.menu_item("Metrics", '', self.show_scene_metrics, True)
                if clicked_scene_metrics:
                    self.show_scene_metrics = not self.show_scene_metrics

                clicked_about_imgui, _ = imgui.menu_item("About ImGui", '', self.show_about_imgui, True)
                if clicked_about_imgui:
                    self.show_about_imgui = not self.show_about_imgui

                clicked_about_pyimgui, _ = imgui.menu_item("About PyImGui", '', self.show_about_pyimgui, True)
                if clicked_about_pyimgui:
                    self.show_about_pyimgui = not self.show_about_pyimgui

                clicked_about_kuplung, _ = imgui.menu_item("About Kuplung", '', self.show_about_kuplung, True)
                if clicked_about_kuplung:
                    self.show_about_kuplung = not self.show_about_kuplung

                imgui.separator()

                opened_test_window, self.show_imgui_test_window = imgui.menu_item("ImGui Demo Window", '', self.show_imgui_test_window, True)

                imgui.end_menu()

            imgui.text(self.get_app_consumption())
            imgui.end_main_menu_bar()

        self.render_dialogs()

    def render_dialogs(self):
        if self.show_imgui_test_window:
            imgui.show_test_window()

        if self.show_about_imgui:
            self.dialog_about_imgui()

        if self.show_about_pyimgui:
            self.dialog_about_pyimgui()

        if self.show_about_kuplung:
            self.dialog_about_kuplung()

        if self.show_scene_metrics:
            self.dialog_scene_metrics()

        if self.show_log_window:
            self.dialog_log_window()

        # actions
        if self.new_scene_clear:
            self.gui_clear_scene()

    def render_controls(self):
        if self.show_controls_models:
            self.show_controls_models = self.controlsModels.render(self, self.show_controls_models)

        if self.show_controls_gui:
            self.show_controls_gui = self.controlsGUI.render(self.show_controls_gui)

    def add_shape(self, shapeType):
        models = self.managerParser.parse_file('resources/shapes/', shapeType.value[0] + '.obj')
        for i in range(len(models)):
            model_face = ModelFace()
            model_face.initModelProperties(models[i])
            model_face.initBuffers()
            self.renderingManager.model_faces.append(model_face)

    def add_light(self, lightType):
        self.managerObjects.add_light(lightType)

    def render_ui_content(self):
        self.managerObjects.render(self.window)
        self.render_controls()

    def render_scene(self):
        self.renderingManager.render(
            self.managerObjects,
            self.sceneSelectedModelObject
        )

    def get_app_consumption(self):
        consumption_str = Consumption.memory()
        return " --> {0} FPS | {1} objs, {2} verts, {3} indices ({4} tris, {5} faces) | {6}".format(
            ("%.1f" % imgui.get_io().framerate),
            Settings.SceneCountObjects,
            Settings.SceneCountVertices,
            Settings.SceneCountIndices,
            Settings.SceneCountTriangles,
            Settings.SceneCountFaces,
            consumption_str)

    def init_rendering_manager(self):
        self.renderingManager = RenderingManager()
        self.renderingManager.initShaderProgram()
        Settings.do_log("Rendering Manager initialized.")

        self.managerParser = ParserManager()
        self.managerParser.init_parser()

    def init_objects_manager(self):
        self.managerObjects = ObjectsManager()
        self.managerObjects.load_system_models()
        self.managerObjects.init_manager()
        Settings.do_log("Objects Manager initialized.")

    def printGLStrings(self):
        Settings.do_log("OpenGL Vendor: " +
                        str(gl.glGetString(gl.GL_VENDOR)))
        Settings.do_log("OpenGL version: " +
                        str(gl.glGetString(gl.GL_VERSION)))
        Settings.do_log("GLSL version: " +
                        str(gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)))
        Settings.do_log("OpenGL Renderer: " +
                        str(gl.glGetString(gl.GL_RENDERER)))

    def dialog_about_imgui(self):
        imgui.set_next_window_centered()
        _, self.show_about_imgui = imgui.begin("About ImGui",self.show_about_imgui, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
        imgui.text("ImGui 1.49")
        imgui.separator()
        imgui.text("By Omar Cornut and all github contributors.")
        imgui.text("ImGui is licensed under the MIT License, see LICENSE for more information.")
        imgui.text("https://github.com/swistakm/pyimgui")
        imgui.end()

    def dialog_about_pyimgui(self):
        imgui.set_next_window_centered()
        _, self.show_about_pyimgui = imgui.begin("About PyImGui", self.show_about_pyimgui, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
        imgui.text("Cython-based Python bindings for dear imgui")
        imgui.text("https://github.com/swistakm/pyimgui")
        imgui.end()

    def dialog_about_kuplung(self):
        imgui.set_next_window_centered()
        _, self.show_about_kuplung = imgui.begin("About Kuplung", self.show_about_kuplung, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_COLLAPSE)
        imgui.text("Kuplung " + Settings.AppVersion)
        imgui.separator()
        imgui.text("By supudo.net + github.com/supudo")
        imgui.text("Whatever license...")
        imgui.separator()
        imgui.text("Hold mouse wheel to rotate around")
        imgui.text("Left Alt + Mouse wheel to increase/decrease the FOV")
        imgui.text("Left Shift + Mouse wheel to increase/decrease the FOV")
        imgui.end()

    def dialog_scene_metrics(self):
        _, self.show_scene_metrics = imgui.begin("Scene Metrics", self.show_scene_metrics, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_TITLE_BAR)
        imgui_io = imgui.get_io()
        imgui.text("OpenGL version: " + str(gl.glGetString(gl.GL_VERSION)))
        imgui.text("GLSL version: " + str(gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)))
        imgui.text("Vendor: " + str(gl.glGetString(gl.GL_VENDOR)))
        imgui.text("Renderer: " + str(gl.glGetString(gl.GL_RENDERER)))
        imgui.separator()
        imgui.text("Mouse Position: (" + ("%.1f" % imgui_io.mouse_pos.x) + ", " + ("%.1f" % imgui_io.mouse_pos.y) + ")")
        imgui.separator()
        framerate = imgui_io.framerate
        imgui.text("Application average " + ("%.3f" % (1000.0 / framerate)) + " ms/frame (" + ("%.1f" % framerate) + " FPS)")
        imgui.text(str(imgui_io.metrics_render_vertices) + " vertices, 0 indices (0 triangles)")
        imgui.text(str(imgui_io.metrics_allocs) + " allocations")
        imgui.end()

    def dialog_log_window(self):
        self.show_log_window = self.component_log.draw_window('Log Window', self.show_log_window)

    def gui_clear_scene(self):
        self.renderingManager.model_faces.clear()
        self.managerObjects.lightSources.clear()
        self.new_scene_clear = False