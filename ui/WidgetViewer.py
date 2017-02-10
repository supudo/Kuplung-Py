"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from OpenGL.GL import *
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QOpenGLContext
from PyQt5.QtWidgets import QOpenGLWidget

from meshes.scene.ModelFace import ModelFace
from parsers.OBJ.ParserObj import ParserObj
from rendering.RenderingManager import RenderingManager
from settings import Settings


class WidgetViewer(QOpenGLWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super(WidgetViewer, self).__init__(parent, flags)

    def initializeGL(self):
        self.gl_context = QOpenGLContext(self.parent()).currentContext()
        if self.gl_context is None:
            Settings.log_error("[Widget Viewer] Cannot get OpenGL Context!")
        self.printGLStrings()
        gl_fun = self.gl_context.versionFunctions()
        gl_fun.glClearColor(Settings.guiClearColor[0],
                            Settings.guiClearColor[1],
                            Settings.guiClearColor[2],
                            Settings.guiClearColor[3])
        self.glFunctions = gl_fun

        self.initRenderingManager()
        super(WidgetViewer, self).initializeGL()

    def paintGL(self):
        glViewport(0, 0, 100, 100)
        glClearColor(0, 1, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

        self.renderingManager.render(self.gl_context, self.glFunctions)
        super(WidgetViewer, self).paintGL()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        super(WidgetViewer, self).resizeGL(width, height)

    def initRenderingManager(self):
        self.renderingManager = RenderingManager()
        self.renderingManager.initShaderProgram(self.gl_context)

        self.parser = ParserObj()
        self.parser.parse_file('resources/shapes/', 'monkey_head.obj')

        for model in self.parser.mesh_models:
            model_face = ModelFace()
            model_face.initBuffers(self.gl_context, self.parser.mesh_models[model])
            self.renderingManager.model_faces.append(model_face)
        Settings.log_info("[Widget Viewer] Models initialized...")

        timer = QTimer(self)
        timer.timeout.connect(self.paintGL)
        timer.start(100)

    def printGLStrings(self):
        Settings.log_info("[Widget Viewer] OpenGL version: " + str(glGetString(GL_VERSION)))
        Settings.log_info("[Widget Viewer] GLSL version: " + str(glGetString(GL_SHADING_LANGUAGE_VERSION)))
        Settings.log_info("[Widget Viewer] Vendor: " + str(glGetString(GL_VENDOR)))
        Settings.log_info("[Widget Viewer] Renderer: " + str(glGetString(GL_RENDERER)))

def main():
    WidgetViewer()

if __name__ == '__main__':
    main()
