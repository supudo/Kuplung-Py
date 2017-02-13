# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"


from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QSizePolicy
)


class WidgetModelsUI(QTabWidget):

    def __init__(self, parent=None):
        QTabWidget.__init__(self, parent)
        self.widgetModelUI = QTabWidget()
        self.widgetModelUI.setEnabled(True)

        self.widgetModelUI.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.widgetModelUI.setMinimumSize(300, 16777215)
        self.widgetModelUI.setBaseSize(300, 0)
        self.widgetModelUI.setCurrentIndex(1)

        self.tab_properties = QWidget()
        self.tab_properties.setWindowTitle("Models")

        self.tab_create = QWidget()
        self.tab_create.setWindowTitle("Create")

    def initializeUI(self):
        pass
