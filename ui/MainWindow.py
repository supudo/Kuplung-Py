# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net

https://www.python.org/dev/peps/pep-0008/
http://zetcode.com/gui/pyqt5/menustoolbars/
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QAction,
    QScrollArea, QSizePolicy,
    QGridLayout, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect
from settings import Settings
from consumption import Consumption
from ui.WidgetViewer import WidgetViewer
from ui.WidgetModelsUI import WidgetModelsUI
from PyQt5.Qt import QSurfaceFormat


class KuplungMainWindow(QMainWindow):
    gui_controls_visible = True
    scene_controls_visible = True
    visual_artefacts_visible = True

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.init_window()
        self.init_layout()

    def init_window(self):
        # title
        self.setWindowTitle('Kuplung')

        # icon
        self.setWindowIcon(QIcon("resources/Kuplung.png"))

        # main menu
        self.init_main_menu()

        # status bar
        self.statusBar().showMessage('Ready')

        # screen
        dw = QApplication.desktop()
        screen = dw.screen()
        size = screen.geometry()
        posX = (size.width() - Settings.AppMainWindowWidth) / 2
        posY = (size.height() - Settings.AppMainWindowHeight) / 2
        self.setGeometry(posX, posY,
                        Settings.AppMainWindowWidth,
                        Settings.AppMainWindowHeight)

        # set theme
        # self.setStyleSheet(Stylesheet.KuplungTheme)

        # show window
        self.show()

    def init_main_menu(self):
        # menu bar
        menu_bar = self.menuBar()
        menu_bar.clear()

        if Settings.is_osx():
            menu_bar.setNativeMenuBar(False)

    # File menu
        fileMenu = menu_bar.addMenu('&File')

        action_new = QAction(QIcon('resources/gui/file-o.png'), 'New', self)
        action_new.setStatusTip('New Scene')
        action_new.triggered.connect(self.newScene)
        fileMenu.addAction(action_new)

        action_open = QAction(QIcon('resources/gui/folder-open-o.png'), 'Open ...', self)
        action_open.setStatusTip('Open Existing Scene')
        action_open.triggered.connect(self.openScene)
        fileMenu.addAction(action_open)

        action_open_recent = QAction(QIcon('resources/gui/files-o.png'), 'Open Recent', self)
        action_open_recent.setStatusTip('Open Recent Scene')
        action_open_recent.triggered.connect(self.openRecent)
        fileMenu.addAction(action_open_recent)

        action_save = QAction(QIcon('resources/gui/floppy-o.png'), 'Save ...', self)
        action_save.setStatusTip('Save Scene')
        action_save.triggered.connect(self.saveScene)
        fileMenu.addAction(action_save)

        fileMenu.addSeparator()

        menu_import = fileMenu.addMenu("Import")
        menu_import_obj = QAction('Wavefront (.obj)', self)
        menu_import_obj.setStatusTip('Import OBJ scene and MTL material files')
        menu_import_obj.triggered.connect(self.importFormat_OBJ)
        menu_import.addAction(menu_import_obj)

        action_import_recent = QAction('Import Recent', self)
        action_import_recent.setStatusTip('Import Recent Scene')
        fileMenu.addAction(action_import_recent)

        menu_export = fileMenu.addMenu("Export")
        menu_export_obj = QAction('Wavefront (.obj)', self)
        menu_export_obj.setStatusTip('Export OBJ scene and MTL material files')
        menu_export_obj.triggered.connect(self.exportFormat_OBJ)
        menu_export.addAction(menu_export_obj)

        fileMenu.addSeparator()

        action_exit = QAction(QIcon('resources/gui/power-off.png'), 'Quit', self)
        if Settings.is_osx():
            action_exit.setShortcut('Cmd+Q')
        else:
            action_exit.setShortcut('Alt+F4')
        action_exit.setStatusTip('Exit Kuplung')
        action_exit.triggered.connect(self.close)
        fileMenu.addAction(action_exit)

    # Scene menu
        sceneMenu = menu_bar.addMenu('&Scene')

        menu_add_light = sceneMenu.addMenu(QIcon('resources/gui/lightbulb-o.png'), "Add Light")

        menu_add_light_directional = QAction('Directional (Sun)', self)
        menu_add_light_directional.triggered.connect(self.addLight_Directional)
        menu_add_light.addAction(menu_add_light_directional)

        menu_add_light_point = QAction('Point (Light bulb)', self)
        menu_add_light_point.triggered.connect(self.addLight_Point)
        menu_add_light.addAction(menu_add_light_point)

        menu_add_light_spot = QAction('Spot (Flashlight)', self)
        menu_add_light_spot.triggered.connect(self.addLight_Spot)
        menu_add_light.addAction(menu_add_light_spot)

        sceneMenu.addSeparator()

        menu_scene_rendering = sceneMenu.addMenu(QIcon('resources/gui/certificate.png'), "Scene Rendering")

        menu_skin_solid = QAction('Solid', self)
        menu_skin_solid.triggered.connect(self.renderSkin_Solid)
        menu_scene_rendering.addAction(menu_skin_solid)

        menu_skin_material = QAction('Material', self)
        menu_skin_material.triggered.connect(self.renderSkin_Material)
        menu_scene_rendering.addAction(menu_skin_material)

        menu_skin_texture = QAction('Texture', self)
        menu_skin_texture.triggered.connect(self.renderSkin_Texture)
        menu_scene_rendering.addAction(menu_skin_texture)

        menu_skin_wireframe = QAction('Wireframe', self)
        menu_skin_wireframe.triggered.connect(self.renderSkin_Wireframe)
        menu_scene_rendering.addAction(menu_skin_wireframe)

        menu_skin_rendered = QAction('Rendered', self)
        menu_skin_rendered.triggered.connect(self.renderSkin_Rendered)
        menu_scene_rendering.addAction(menu_skin_rendered)

        sceneMenu.addSeparator()

        menu_render_image = QAction(QIcon('resources/gui/file-image-o.png'), 'Render Image', self)
        menu_render_image.triggered.connect(self.renderImage)
        sceneMenu.addAction(menu_render_image)

        menu_render_ui = QAction(QIcon('resources/gui/cubes.png'), 'Render UI', self)
        menu_render_ui.triggered.connect(self.showRenderUI)
        sceneMenu.addAction(menu_render_ui)

    # View
        viewMenu = menu_bar.addMenu('&View')

        menu_item_gui_controls = QAction('GUI Controls', self)
        if self.gui_controls_visible:
            menu_item_gui_controls.setIcon(QIcon('resources/gui/toggle-on.png'))
        else:
            menu_item_gui_controls.setIcon(QIcon('resources/gui/toggle-off.png'))
        menu_item_gui_controls.triggered.connect(self.toggleGuiControls)
        viewMenu.addAction(menu_item_gui_controls)

        menu_item_scene_controls = QAction('Scene Controls', self)
        if self.scene_controls_visible:
            menu_item_scene_controls.setIcon(QIcon('resources/gui/toggle-on.png'))
        else:
            menu_item_scene_controls.setIcon(QIcon('resources/gui/toggle-off.png'))
        menu_item_scene_controls.triggered.connect(self.toggleSceneControls)
        viewMenu.addAction(menu_item_scene_controls)

        menu_item_visual_artefacts = QAction('Visual Artefacts', self)
        if self.visual_artefacts_visible:
            menu_item_visual_artefacts.setIcon(QIcon('resources/gui/toggle-on.png'))
        else:
            menu_item_visual_artefacts.setIcon(QIcon('resources/gui/toggle-off.png'))
        menu_item_visual_artefacts.triggered.connect(self.toggleVisualArtefacts)
        viewMenu.addAction(menu_item_visual_artefacts)

        viewMenu.addSeparator()

        action_show_log_window = QAction(QIcon('resources/gui/bug.png'), 'Log Window', self)
        action_show_log_window.setStatusTip('Toggle Log Window')
        action_show_log_window.triggered.connect(self.toggleLogWindow)
        viewMenu.addAction(action_show_log_window)

        action_screenshot_window = QAction(QIcon('resources/gui/desktop.png'), 'Screenshot Window', self)
        action_screenshot_window.setStatusTip('Toggle Screenshot Window')
        action_screenshot_window.triggered.connect(self.toggleScreenshotWindow)
        viewMenu.addAction(action_screenshot_window)

        action_scene_statistics = QAction(QIcon('resources/gui/tachometer.png'), 'Scene Statistics', self)
        action_scene_statistics.setStatusTip('Toggle Screen Statistics')
        action_scene_statistics.triggered.connect(self.toggleScreenStatistics)
        viewMenu.addAction(action_scene_statistics)

        action_svs = QAction(QIcon('resources/gui/paper-plane-o.png'), 'Structured Volumetric Sampling', self)
        action_svs.setStatusTip('Toggle Structured Volumetric Sampling')
        action_svs.triggered.connect(self.toggleSVS)
        viewMenu.addAction(action_svs)

        action_shadertoy = QAction(QIcon('resources/gui/bicycle.png'), 'Shadertoy', self)
        action_shadertoy.setStatusTip('Toggle Shadertoy')
        action_shadertoy.triggered.connect(self.toggleShadertoy)
        viewMenu.addAction(action_shadertoy)

        viewMenu.addSeparator()

        action_options = QAction(QIcon('resources/gui/cog.png'), 'Options', self)
        action_options.setStatusTip('Toggle Options')
        action_options.triggered.connect(self.toggleOptions)
        viewMenu.addAction(action_options)

    # Help
        helpMenu = menu_bar.addMenu('&Help')

        action_about_kuplung = QAction(QIcon('resources/gui/info-circle.png'), 'About Kuplung', self)
        action_about_kuplung.setStatusTip('Toggle About Kuplung')
        action_about_kuplung.triggered.connect(self.toggleAboutKuplung)
        helpMenu.addAction(action_about_kuplung)

    # Stats
        menu_bar.addSeparator()
        menu_bar.addMenu(self.getAppConsumption())

    def getAppConsumption(self):
        consumption_str = Consumption.memory()
        return "﻿--> {0} FPS | {1} objs, {2} verts, {3} indices ({4} tris, {5} faces) | {6}".format(
            0,
            Settings.SceneCountObjects, Settings.SceneCountVertices,
            Settings.SceneCountIndices, Settings.SceneCountTriangles,
            Settings.SceneCountFaces,
            consumption_str)

    #region Main Menu Events

    # File menu

    def openScene(self):
        return NotImplementedError
        # Get filename and show only .writer files
        # self.filename = QFileDialog.getOpenFileName(self, 'Open File',".","(*.kuplung)")
        # if self.filename:
        #     with open(self.filename, "rt") as file:
        #         self.text.setText(file.read())

    def newScene(self):
        return NotImplementedError

    def openRecent(self):
        return NotImplementedError

    def saveScene(self):
        return NotImplementedError

    def importFormat_OBJ(self):
        return NotImplementedError

    def exportFormat_OBJ(self):
        return NotImplementedError

    # Lights

    def addLight_Directional(self):
        return NotImplementedError

    def addLight_Point(self):
        return NotImplementedError

    def addLight_Spot(self):
        return NotImplementedError

    # Scene Rendering

    def renderSkin_Solid(self):
        return NotImplementedError

    def renderSkin_Material(self):
        return NotImplementedError

    def renderSkin_Texture(self):
        return NotImplementedError

    def renderSkin_Wireframe(self):
        return NotImplementedError

    def renderSkin_Rendered(self):
        return NotImplementedError

    # Renderers

    def renderImage(self):
        return NotImplementedError

    def showRenderUI(self):
        return NotImplementedError

    # View

    def toggleGuiControls(self):
        self.gui_controls_visible = not self.gui_controls_visible
        self.init_main_menu()

    def toggleSceneControls(self):
        self.scene_controls_visible = not self.scene_controls_visible
        self.init_main_menu()

    def toggleVisualArtefacts(self):
        self.visual_artefacts_visible = not self.visual_artefacts_visible
        self.init_main_menu()

    def toggleLogWindow(self):
        Settings.LogDebugWindow = not Settings.LogDebugWindow

    def toggleScreenshotWindow(self):
        return NotImplementedError

    def toggleScreenStatistics(self):
        return NotImplementedError

    def toggleSVS(self):
        return NotImplementedError

    def toggleShadertoy(self):
        return NotImplementedError

    def toggleOptions(self):
        return NotImplementedError

    # Help

    def toggleAboutKuplung(self):
        boxAbout = QMessageBox()
        boxAbout.setModal(True)
        boxAbout.setTextFormat(Qt.RichText)
        boxAbout.setWindowTitle("About Kuplung")
        boxAbout.setIconPixmap(QPixmap('resources/Kuplung_about.png'))
        boxAbout.setWindowIcon(QIcon('resources/Kuplung_about.png'))
        about_str = "Kuplung " + Settings.AppVersion + "<br/>"
        about_str += "By <a href='http://supudo.net'>supudo.net</a><br />"
        about_str += "<a href='http://github.com/supudo'>supudo@github</a>"
        about_str += "<br /><br />"
        about_str += "Whatever license..."
        boxAbout.setText(about_str)
        boxAbout.setStandardButtons(QMessageBox.Ok)
        boxAbout.exec_()

    #endregion

    # GUI

    def init_layout(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout()
        gridLayout.setGeometry(QRect(0, 0, 200, 200))

        self.init_models_ui()
        self.init_opengl_ui()
        self.init_system_ui()

        gridLayout.addWidget(self.glWidgetArea, 0, 0)
        centralWidget.setLayout(gridLayout)

    def init_models_ui(self):
        self.widget_modelsui = WidgetModelsUI(self)
        self.widget_modelsui.initializeUI()

        # self.glWidgetArea = QScrollArea()
        # self.glWidgetArea.setWidget(self.widget_modelsui)
        # self.glWidgetArea.setWidgetResizable(True)
        # self.glWidgetArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.glWidgetArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.glWidgetArea.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.glWidgetArea.setMinimumSize(50, 50)

    def init_system_ui(self):
        return NotImplementedError

    def init_opengl_ui(self):
        gl_format = QSurfaceFormat()
        gl_format.setDepthBufferSize(24)
        gl_format.setStencilBufferSize(8)
        gl_format.setVersion(4, 1)
        gl_format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(gl_format)

        self.widget_opengl = WidgetViewer(self)

        self.glWidgetArea = QScrollArea()
        self.glWidgetArea.setWidget(self.widget_opengl)
        self.glWidgetArea.setWidgetResizable(True)
        self.glWidgetArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.glWidgetArea.setMinimumSize(200, 0)

