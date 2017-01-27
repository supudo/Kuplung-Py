"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from PyQt5 import QtOpenGL
from PyQt5 import QtCore
from OpenGL.GL import *
from settings import Settings


class WidgetViewer(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        print("GL version:" + str(glGetString(GL_VERSION)))
        print("MAX_TEXTURE_SIZE: %d" % glGetIntegerv(GL_MAX_TEXTURE_SIZE))
        print("MAX_3D_TEXTURE_SIZE: %d" % glGetIntegerv(GL_MAX_3D_TEXTURE_SIZE))
        print("Extensions: " + str(glGetString(GL_EXTENSIONS)))

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateGL)
        timer.start(100)

    def initializeGL(self):
        glClearColor(Settings.guiClearColor[0],
                     Settings.guiClearColor[1],
                     Settings.guiClearColor[2],
                     Settings.guiClearColor[3])
