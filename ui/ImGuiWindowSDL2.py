# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from os.path import expanduser
from ctypes import byref

import OpenGL.GL as gl
import imgui
from imgui.impl import SDL2Impl
from sdl2 import *

from consumption.Consumption import Consumption
from meshes.scene.ModelFace import ModelFace
from objects.ControlsManagerSDL2 import ControlsManagerSDL2
from objects.ObjectsManager import ObjectsManager
from parsers.ParserManager import ParserManager
from rendering.RenderingManager import RenderingManager
from settings import Settings
from ui.components.ImporterOBJ import ImporterOBJ
from ui.components.Log import Log
from ui.dialogs.DialogControlsGUI import DialogControlsGUI
from ui.dialogs.DialogControlsModels import DialogControlsModels
from ui.dialogs.DialogShadertoy import DialogShadertoy
from ui.dialogs.DialogSVS import DialogSVS
from ui.dialogs.DialogOptions import DialogOptions


class ImGuiWindowSDL2():

    # app
    managerParser = None
    controlsModels = None
    controlsGUI = None
    controlsShadertoy = None
    controlsSVS = None
    controlsOptions = None
    utilConsumption = None

    # dialogs
    gui_controls_visible = True
    scene_controls_visible = True
    visual_artefacts_visible = True
    app_is_running = False
    new_scene_clear = False
    is_loading_open = False

    # Main menu
    show_save_image = False
    show_render_ui = False
    show_imgui_test_window = False
    show_about_imgui = False
    show_about_pyimgui = False
    show_about_kuplung = False
    show_scene_metrics = False
    show_importerobj_window = False
    show_controls_models = True
    show_controls_gui = True
    show_svs_window = False
    show_shadertoy_window = False
    show_scene_stats = False
    show_options = False

    sceneSelectedModelObject = -1

    def show_main_window(self):
        Settings.Settings_CurrentFolder = expanduser("~")
        self.init_gl()
        self.init_window()
        self.init_imgui_impl()
        self.show_loading()
        self.init_sub_windows()
        self.init_components()
        self.init_manager_controls()
        self.init_rendering_manager()
        self.imgui_style = imgui.GuiStyle()
        self.init_objects_manager()

        self.printGLStrings()
        self.hide_loading()

        running = True
        event = SDL_Event()
        while running:
            while SDL_PollEvent(byref(event)) != 0:
                if event.type == SDL_QUIT:
                    running = False
                    self.utilConsumption.stop_pooling()
                    break
                self.imgui_context.process_event(event)
                self.managerControls.process_event(event)

            self.imgui_context.new_frame()

            self.handle_controls_events()

            gl.glViewport(0, 0, int(Settings.AppWindowWidth / 2), int(Settings.AppWindowHeight))
            gl.glClearColor(Settings.guiClearColor[0],
                            Settings.guiClearColor[1],
                            Settings.guiClearColor[2],
                            Settings.guiClearColor[3])
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)

            self.render_screen()
            imgui.render()

            SDL_GL_SwapWindow(self.window)

        # self.imgui_context.shutdown()
        SDL_GL_DeleteContext(self.gl_context)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

    def init_gl(self):
        if SDL_Init(SDL_INIT_EVERYTHING) < 0:
            Settings.log_error("[ImGuiWindow] Could not initialize SDL2!")
            return False

        SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1)
        SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
        SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
        SDL_GL_SetAttribute(SDL_GL_ACCELERATED_VISUAL, 1)
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 16)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 1)
        SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)

        SDL_SetHint(SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK, b"1")
        SDL_SetHint(SDL_HINT_VIDEO_HIGHDPI_DISABLED, b"1")

    def init_window(self):
        self.utilConsumption = Consumption()
        self.utilConsumption.start_pooling()

        self.window = SDL_CreateWindow(
            Settings.AppMainWindowTitle.encode('utf-8'),
            SDL_WINDOWPOS_CENTERED,
            SDL_WINDOWPOS_CENTERED,
            int(Settings.AppFramebufferWidth),
            int(Settings.AppFramebufferHeight),
            SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE)

        if self.window is None:
            Settings.log_error("[ImGuiWindow] Could not initialize Window!! SDL Error: " + SDL_GetError())
            return False

        self.gl_context = SDL_GL_CreateContext(self.window)
        if self.gl_context is None:
            Settings.log_error("[ImGuiWindow] Error: Cannot create OpenGL Context! SDL Error: " + SDL_GetError())
            return False

        SDL_GL_MakeCurrent(self.window, self.gl_context)
        if SDL_GL_SetSwapInterval(1) < 0:
            Settings.log_error("[ImGuiWindow] Warning: Unable to set VSync! SDL Error: " + SDL_GetError())

    def init_manager_controls(self):
        self.managerControls = ControlsManagerSDL2()
        Settings.do_log("[ImGuiWindow] Control events initialized.")

    def init_sub_windows(self):
        self.controlsModels = DialogControlsModels()
        self.controlsGUI = DialogControlsGUI()
        self.controlsShadertoy = DialogShadertoy()
        self.controlsSVS = DialogSVS()
        self.controlsOptions = DialogOptions()
        Settings.do_log("[ImGuiWindow] GUI sub windows initialized.")

    def init_components(self):
        self.component_log = Log()
        Settings.FuncDoLog = self.component_log.add_to_log
        self.component_importerobj = ImporterOBJ()
        Settings.do_log("[ImGuiWindow] GUI components initialized.")

    def init_imgui_impl(self):
        self.imgui_context = SDL2Impl(self.window)
        self.imgui_context.enable()
        self.app_is_running = True
        Settings.do_log("[ImGuiWindow] PyImGui initialized.")

    def render_screen(self):
        self.render_main_menu()

        self.managerObjects.render(self.window)

        if self.show_controls_models:
            self.show_controls_models, self.renderingManager.model_faces = self.controlsModels.render(self, self.show_controls_models, self.managerObjects, self.renderingManager.model_faces, True)

        if self.show_controls_gui:
            self.show_controls_gui, self.managerObjects = self.controlsGUI.render(self.show_controls_gui, self.managerObjects, True)

        if self.show_shadertoy_window:
            self.show_shadertoy_window = self.controlsShadertoy.render(self.show_shadertoy_window)

        if self.show_svs_window:
            self.show_svs_window = self.controlsSVS.render(self.show_svs_window)

        if self.show_options:
            self.show_options = self.controlsOptions.render(self.show_options)

        self.renderingManager.render(
            self.managerObjects,
            self.sceneSelectedModelObject
        )

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
                if self.managerControls.mouseGoUp:
                    self.managerObjects.camera.rotateX['point'] += self.managerControls.yrel
                if self.managerControls.mouseGoDown:
                    self.managerObjects.camera.rotateX['point'] += self.managerControls.yrel
                if self.managerObjects.camera.rotateX['point'] > 360:
                    self.managerObjects.camera.rotateX['point'] = .0
                if self.managerObjects.camera.rotateX['point'] < .0:
                    self.managerObjects.camera.rotateX['point'] = 360

                if self.managerControls.mouseGoLeft:
                    self.managerObjects.camera.rotateY['point'] += self.managerControls.xrel
                if self.managerControls.mouseGoRight:
                    self.managerObjects.camera.rotateY['point'] += self.managerControls.xrel
                if self.managerObjects.camera.rotateY['point'] > 360:
                    self.managerObjects.camera.rotateY['point'] = .0
                if self.managerObjects.camera.rotateY['point'] < .0:
                    self.managerObjects.camera.rotateY['point'] = 360

            self.managerControls.reset_mouse_motion()

    def render_main_menu(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):
                _, self.new_scene_clear = imgui.menu_item("New", '', False, True)
                imgui.menu_item("Open ...", '', False, False)
                if imgui.begin_menu("Open Recent", False):
                    imgui.end_menu()
                imgui.menu_item("Save ...", '', False, False)
                imgui.separator()
                if imgui.begin_menu("Import", True):
                    _, self.show_importerobj_window = imgui.menu_item("Wavefront (.OBJ)", '', self.show_importerobj_window, True)
                    imgui.end_menu()
                if imgui.begin_menu("Import Recent", False):
                    imgui.menu_item("file 1...", '', False, True)
                    imgui.end_menu()
                if imgui.begin_menu("Export", False):
                    imgui.menu_item("Wavefront (.OBJ)", '', False, True)
                    imgui.end_menu()
                imgui.separator()
                clicked_quit, selected_quit = imgui.menu_item("Quit", 'Cmd+Q', False, True)
                if clicked_quit:
                    self.utilConsumption.stop_pooling()
                    self.app_is_running = False
                    exit(1)
                imgui.end_menu()

            if imgui.begin_menu("Scene", True):
                if imgui.begin_menu("Add Light", True):
                    clicked, _ = imgui.menu_item("Directional (Sun)", '', False, True)
                    if clicked:
                        self.add_light(Settings.LightSourceTypes.LightSourceType_Directional)
                    clicked, _ = imgui.menu_item("Point (Light bulb)", '', False, True)
                    if clicked:
                        self.add_light(Settings.LightSourceTypes.LightSourceType_Point)
                    clicked, _ = imgui.menu_item("Spot (Flashlight)", '', False, True)
                    if clicked:
                        self.add_light(Settings.LightSourceTypes.LightSourceType_Spot)
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
                opened_show_render_image, self.show_save_image = imgui.menu_item("Render Image", '', self.show_save_image, False)
                opened_show_render_ui, self.show_render_ui = imgui.menu_item("Render UI", '', self.show_render_ui, False)
                imgui.end_menu()

            if imgui.begin_menu("View", True):
                _, self.show_controls_gui = imgui.menu_item("GUI Controls", '', self.show_controls_gui, True)
                _, self.show_controls_models = imgui.menu_item("Scene Controls", '', self.show_controls_models, True)
                _, Settings.AppShowAllVisualArtefacts = imgui.menu_item(('Hide' if Settings.AppShowAllVisualArtefacts else 'Show') + " Visual Artefacts", '', Settings.AppShowAllVisualArtefacts, True)
                imgui.separator()
                _, Settings.ShowLogWindow = imgui.menu_item("Show Log Window", '', Settings.ShowLogWindow, True)
                imgui.menu_item("Screenshot", '', False, False)
                _, self.show_scene_stats = imgui.menu_item("Scene Statistics", '', self.show_scene_stats, True)
                _, self.show_svs_window = imgui.menu_item("Structured Volumetric Sampling", '', self.show_svs_window, True)
                _, self.show_shadertoy_window = imgui.menu_item("Shadertoy", '', self.show_shadertoy_window, True)
                imgui.separator()
                _, self.show_options = imgui.menu_item('Options', '', self.show_options, True)
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

        if self.show_scene_stats:
            self.dialog_scene_stats()

        if Settings.ShowLogWindow:
            self.dialog_log_window()

        if self.show_importerobj_window:
            self.dialog_importer_obj_window()

        if self.is_loading_open:
            imgui.open_popup('Kuplung Loading')
        loading_opened, _ = imgui.begin_popup_modal('Kuplung Loading', False, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_TITLE_BAR)
        if loading_opened:
            imgui.text('Loading...')
            imgui.end_popup()

        # actions
        if self.new_scene_clear:
            self.gui_clear_scene()

    def process_imported_file(self, folder, imported_file):
        models = self.managerParser.parse_file(folder, imported_file)
        for i in range(len(models)):
            model_face = ModelFace()
            model_face.init_own(models[i])
            model_face.init_bounding_box()
            model_face.init_vertex_sphere()
            model_face.set_model(models[i])
            model_face.initModelProperties()
            self.renderingManager.model_faces.append(model_face)
        if len(self.renderingManager.model_faces) > 0:
            self.controlsModels.selectedTabPanel = 0
        self.hide_loading()
        self.show_importerobj_window = False

    def add_shape(self, shapeType):
        self.show_loading()
        self.process_imported_file('resources/shapes/', shapeType.value[0] + '.obj')

    def add_light(self, lightType):
        self.managerObjects.add_light(lightType)

    def get_app_consumption(self):
        consumption_str = self.utilConsumption.get_consumption()
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
        Settings.do_log("[ImGuiWindow] Rendering Manager initialized.")

        self.managerParser = ParserManager()
        self.managerParser.init_parser()

    def init_objects_manager(self):
        self.managerObjects = ObjectsManager()
        self.managerObjects.load_system_models()
        self.managerObjects.init_manager()
        Settings.do_log("[ImGuiWindow] Objects Manager initialized.")

    def printGLStrings(self):
        Settings.do_log("[ImGuiWindow] OpenGL Vendor: " +
                        str(gl.glGetString(gl.GL_VENDOR)))
        Settings.do_log("[ImGuiWindow] OpenGL version: " +
                        str(gl.glGetString(gl.GL_VERSION)))
        Settings.do_log("[ImGuiWindow] GLSL version: " +
                        str(gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)))
        Settings.do_log("[ImGuiWindow] OpenGL Renderer: " +
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
        self.show_scene_metrics = imgui.show_metrics_window(self.show_scene_metrics)

    def dialog_scene_stats(self):
        _, self.show_scene_stats = imgui.begin("Scene Metrics", self.show_scene_stats, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_TITLE_BAR)
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
        Settings.ShowLogWindow = self.component_log.draw_window('Log Window', Settings.ShowLogWindow)

    def dialog_importer_obj_window(self):
        self.show_importerobj_window = self.component_importerobj.draw_window('Import Wavefront OBJ File', self.show_importerobj_window, self.process_imported_file)

    def gui_clear_scene(self):
        self.renderingManager.model_faces.clear()
        self.managerObjects.lightSources.clear()
        self.new_scene_clear = False

    def show_loading(self):
        self.is_loading_open = True

    def hide_loading(self):
        self.is_loading_open = False
