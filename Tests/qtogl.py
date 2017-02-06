from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QOpenGLContext
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtCore import Qt
from OpenGL.GL import *

class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super(MyGLWidget, self).__init__(parent, flags)

    def initializeGL(self):
        con = QOpenGLContext().currentContext()
        fun = con.versionFunctions()
        fun.glClearColor(0.27, 0.27, 0.27, 1.0)
        self.glFun = fun
        print("OpenGL version: " + str(glGetString(GL_VERSION)))
        print("GLSL version: " + str(glGetString(GL_SHADING_LANGUAGE_VERSION)))
        print("Vendor: " + str(glGetString(GL_VENDOR)))
        print("Renderer: " + str(glGetString(GL_RENDERER)))

def main():
    app = QApplication([])

    fmt = QSurfaceFormat()
    fmt.setDepthBufferSize(24)
    fmt.setStencilBufferSize(8)
    fmt.setVersion(4, 1)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(fmt)

    mWin = QMainWindow()
    mWin.setGeometry(
        QStyle.alignedRect(
            Qt.LeftToRight,
            Qt.AlignCenter,
            mWin.size(),
            app.desktop().availableGeometry()
        )
    )
    glWIn = MyGLWidget()

    mWin.setCentralWidget(glWIn)
    try:
        mWin.show()
    except Exception as e:
        print(e)
    app.exec_()

if __name__ == '__main__':
    main()