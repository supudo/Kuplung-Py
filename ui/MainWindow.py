"""
Kuplung - OpenGL Viewer, python port
supudo.net

https://www.python.org/dev/peps/pep-0008/
http://zetcode.com/gui/pyqt5/menustoolbars/
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from PyQt5.QtWidgets import (
    QMainWindow, QAction, QApplication, QScrollArea, QSizePolicy,
    QGridLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QRect
from settings import Settings
from consumption import Consumption
from ui.OpenGLWindow import OpenGLWindow


class KuplungMainWindow(QMainWindow):
    gui_controls_visible = True
    scene_controls_visible = True
    visual_artefacts_visible = True

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.init_window()
        self.init_dock_windows()

    def init_window(cls):
        # title
        cls.setWindowTitle('Kuplung')

        # icon
        cls.setWindowIcon(QIcon("resources/Kuplung.png"))

        # main menu
        cls.init_main_menu()

        # status bar
        cls.statusBar().showMessage('Ready')

        # screen
        dw = QApplication.desktop()
        screen = dw.screen()
        size = screen.geometry()
        posX = (size.width() - Settings.AppMainWindowWidth) / 2
        posY = (size.height() - Settings.AppMainWindowHeight) / 2
        cls.setGeometry(posX, posY,
                        Settings.AppMainWindowWidth,
                        Settings.AppMainWindowHeight)

        # set theme
        # cls.setStyleSheet(Stylesheet.KuplungTheme)

        # show window
        cls.show()

    def init_main_menu(cls):
        # menu bar
        menu_bar = cls.menuBar()
        menu_bar.clear()

        if Settings.is_osx():
            menu_bar.setNativeMenuBar(False)

    # File menu
        fileMenu = menu_bar.addMenu('&File')

        action_new = QAction(QIcon('resources/gui/file-o.png'), 'New', cls)
        action_new.setStatusTip('New Scene')
        action_new.triggered.connect(cls.newScene)
        fileMenu.addAction(action_new)

        action_open = QAction(QIcon('resources/gui/folder-open-o.png'), 'Open ...', cls)
        action_open.setStatusTip('Open Existing Scene')
        action_open.triggered.connect(cls.openScene)
        fileMenu.addAction(action_open)

        action_open_recent = QAction(QIcon('resources/gui/files-o.png'), 'Open Recent', cls)
        action_open_recent.setStatusTip('Open Recent Scene')
        action_open_recent.triggered.connect(cls.openRecent)
        fileMenu.addAction(action_open_recent)

        action_save = QAction(QIcon('resources/gui/floppy-o.png'), 'Save ...', cls)
        action_save.setStatusTip('Save Scene')
        action_save.triggered.connect(cls.saveScene)
        fileMenu.addAction(action_save)

        fileMenu.addSeparator()

        menu_import = fileMenu.addMenu("Import")
        menu_import_obj = QAction('Wavefront (.obj)', cls)
        menu_import_obj.setStatusTip('Import OBJ scene and MTL material files')
        menu_import_obj.triggered.connect(cls.importFormat_OBJ)
        menu_import.addAction(menu_import_obj)

        action_import_recent = QAction('Import Recent', cls)
        action_import_recent.setStatusTip('Import Recent Scene')
        fileMenu.addAction(action_import_recent)

        menu_export = fileMenu.addMenu("Export")
        menu_export_obj = QAction('Wavefront (.obj)', cls)
        menu_export_obj.setStatusTip('Export OBJ scene and MTL material files')
        menu_export_obj.triggered.connect(cls.exportFormat_OBJ)
        menu_export.addAction(menu_export_obj)

        fileMenu.addSeparator()

        action_exit = QAction(QIcon('resources/gui/power-off.png'), 'Quit', cls)
        if Settings.is_osx():
            action_exit.setShortcut('Cmd+Q')
        else:
            action_exit.setShortcut('Alt+F4')
        action_exit.setStatusTip('Exit Kuplung')
        action_exit.triggered.connect(cls.close)
        fileMenu.addAction(action_exit)

    # Scene menu
        sceneMenu = menu_bar.addMenu('&Scene')

        menu_add_light = sceneMenu.addMenu(QIcon('resources/gui/lightbulb-o.png'), "Add Light")

        menu_add_light_directional = QAction('Directional (Sun)', cls)
        menu_add_light_directional.triggered.connect(cls.addLight_Directional)
        menu_add_light.addAction(menu_add_light_directional)

        menu_add_light_point = QAction('Point (Light bulb)', cls)
        menu_add_light_point.triggered.connect(cls.addLight_Point)
        menu_add_light.addAction(menu_add_light_point)

        menu_add_light_spot = QAction('Spot (Flashlight)', cls)
        menu_add_light_spot.triggered.connect(cls.addLight_Spot)
        menu_add_light.addAction(menu_add_light_spot)

        sceneMenu.addSeparator()

        menu_scene_rendering = sceneMenu.addMenu(QIcon('resources/gui/certificate.png'), "Scene Rendering")

        menu_skin_solid = QAction('Solid', cls)
        menu_skin_solid.triggered.connect(cls.renderSkin_Solid)
        menu_scene_rendering.addAction(menu_skin_solid)

        menu_skin_material = QAction('Material', cls)
        menu_skin_material.triggered.connect(cls.renderSkin_Material)
        menu_scene_rendering.addAction(menu_skin_material)

        menu_skin_texture = QAction('Texture', cls)
        menu_skin_texture.triggered.connect(cls.renderSkin_Texture)
        menu_scene_rendering.addAction(menu_skin_texture)

        menu_skin_wireframe = QAction('Wireframe', cls)
        menu_skin_wireframe.triggered.connect(cls.renderSkin_Wireframe)
        menu_scene_rendering.addAction(menu_skin_wireframe)

        menu_skin_rendered = QAction('Rendered', cls)
        menu_skin_rendered.triggered.connect(cls.renderSkin_Rendered)
        menu_scene_rendering.addAction(menu_skin_rendered)

        sceneMenu.addSeparator()

        menu_render_image = QAction(QIcon('resources/gui/file-image-o.png'), 'Render Image', cls)
        menu_render_image.triggered.connect(cls.renderImage)
        sceneMenu.addAction(menu_render_image)

        menu_render_ui = QAction(QIcon('resources/gui/cubes.png'), 'Render UI', cls)
        menu_render_ui.triggered.connect(cls.showRenderUI)
        sceneMenu.addAction(menu_render_ui)

    # View
        viewMenu = menu_bar.addMenu('&View')

        menu_item_gui_controls = QAction('GUI Controls', cls)
        if cls.gui_controls_visible:
            menu_item_gui_controls.setIcon(QIcon('resources/gui/toggle-on.png'))
        else:
            menu_item_gui_controls.setIcon(QIcon('resources/gui/toggle-off.png'))
        menu_item_gui_controls.triggered.connect(cls.toggleGuiControls)
        viewMenu.addAction(menu_item_gui_controls)

        menu_item_scene_controls = QAction('Scene Controls', cls)
        if cls.scene_controls_visible:
            menu_item_scene_controls.setIcon(QIcon('resources/gui/toggle-on.png'))
        else:
            menu_item_scene_controls.setIcon(QIcon('resources/gui/toggle-off.png'))
        menu_item_scene_controls.triggered.connect(cls.toggleSceneControls)
        viewMenu.addAction(menu_item_scene_controls)

        menu_item_visual_artefacts = QAction('Visual Artefacts', cls)
        if cls.visual_artefacts_visible:
            menu_item_visual_artefacts.setIcon(QIcon('resources/gui/toggle-on.png'))
        else:
            menu_item_visual_artefacts.setIcon(QIcon('resources/gui/toggle-off.png'))
        menu_item_visual_artefacts.triggered.connect(cls.toggleVisualArtefacts)
        viewMenu.addAction(menu_item_visual_artefacts)

        viewMenu.addSeparator()

        action_show_log_window = QAction(QIcon('resources/gui/bug.png'), 'Log Window', cls)
        action_show_log_window.setStatusTip('Toggle Log Window')
        action_show_log_window.triggered.connect(cls.toggleLogWindow)
        viewMenu.addAction(action_show_log_window)

        action_screenshot_window = QAction(QIcon('resources/gui/desktop.png'), 'Screenshot Window', cls)
        action_screenshot_window.setStatusTip('Toggle Screenshot Window')
        action_screenshot_window.triggered.connect(cls.toggleScreenshotWindow)
        viewMenu.addAction(action_screenshot_window)

        action_scene_statistics = QAction(QIcon('resources/gui/tachometer.png'), 'Scene Statistics', cls)
        action_scene_statistics.setStatusTip('Toggle Screen Statistics')
        action_scene_statistics.triggered.connect(cls.toggleScreenStatistics)
        viewMenu.addAction(action_scene_statistics)

        action_svs = QAction(QIcon('resources/gui/paper-plane-o.png'), 'Structured Volumetric Sampling', cls)
        action_svs.setStatusTip('Toggle Structured Volumetric Sampling')
        action_svs.triggered.connect(cls.toggleSVS)
        viewMenu.addAction(action_svs)

        action_shadertoy = QAction(QIcon('resources/gui/bicycle.png'), 'Shadertoy', cls)
        action_shadertoy.setStatusTip('Toggle Shadertoy')
        action_shadertoy.triggered.connect(cls.toggleShadertoy)
        viewMenu.addAction(action_shadertoy)

        viewMenu.addSeparator()

        action_options = QAction(QIcon('resources/gui/cog.png'), 'Options', cls)
        action_options.setStatusTip('Toggle Options')
        action_options.triggered.connect(cls.toggleOptions)
        viewMenu.addAction(action_options)

    # Help
        helpMenu = menu_bar.addMenu('&Help')

        action_about_kuplung = QAction(QIcon('resources/gui/info-circle.png'), 'About Kuplung', cls)
        action_about_kuplung.setStatusTip('Toggle About Kuplung')
        action_about_kuplung.triggered.connect(cls.toggleAboutKuplung)
        helpMenu.addAction(action_about_kuplung)

    # Stats
        menu_bar.addSeparator()
        menu_bar.addMenu(cls.getAppConsumption())

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

    def init_dock_windows(self):
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        self.init_system_ui()
        self.init_models_ui()
        self.init_opengl_ui()

        centralLayout = QGridLayout()
        centralLayout.setGeometry(QRect(0, 0, 200, 200))
        centralLayout.addWidget(self.glWidgetArea, 0, 0)
        centralWidget.setLayout(centralLayout)

    def init_system_ui(self):
        return NotImplementedError

    def init_models_ui(self):
        return NotImplementedError

    def init_opengl_ui(self):
        self.opengl_widget = OpenGLWindow(self)
        self.opengl_widget.initializeGL()

        self.glWidgetArea = QScrollArea()
        self.glWidgetArea.setWidget(self.opengl_widget)
        self.glWidgetArea.setWidgetResizable(True)
        self.glWidgetArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.glWidgetArea.setMinimumSize(50, 50)

