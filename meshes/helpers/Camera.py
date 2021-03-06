# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import numpy
from maths.types.Vector3 import Vector3
from maths.types.Vector4 import Vector4
from maths import MathOps
from gl_utils.GLUtils import ObjectCoordinate


class Camera():
    def __init__(self):
        self.matrixCamera = numpy.array(numpy.ones((4, 4)), dtype=numpy.float32)
        self.View_Eye = Vector3()
        self.View_Center = Vector3()
        self.View_Up = Vector3()
        self.positionX = ObjectCoordinate(animate=False, point=.0)
        self.positionY = ObjectCoordinate(animate=False, point=.0)
        self.positionZ = ObjectCoordinate(animate=False, point=.0)
        self.rotateX = ObjectCoordinate(animate=False, point=.0)
        self.rotateY = ObjectCoordinate(animate=False, point=.0)
        self.rotateZ = ObjectCoordinate(animate=False, point=.0)
        self.rotateCenterX = ObjectCoordinate(animate=False, point=.0)
        self.rotateCenterY = ObjectCoordinate(animate=False, point=.0)
        self.rotateCenterZ = ObjectCoordinate(animate=False, point=.0)
        self.cameraPosition = Vector3()

    def init_properties(self):
        self.View_Eye = Vector3(.0, .0, 10.0)
        self.view_Center = Vector3(.0, .0, .0)
        self.View_Up = Vector3(.0, -1.0, .0)

        self.positionX.point = 0.0
        self.positionY.point = 0.0
        self.positionZ.point = -16.0

        self.rotateX.point = 160.0
        self.rotateY.point = 140.0
        self.rotateZ.point = 0.0

        self.rotateCenterX.point = 0.0
        self.rotateCenterY.point = 0.0
        self.rotateCenterZ.point = 0.0

        self.matrixCamera = MathOps.lookAt(self.View_Eye, self.View_Center, self.View_Up)

    def render(self):
        self.matrixCamera = MathOps.lookAt(self.View_Eye, self.View_Center, self.View_Up)

        self.matrixCamera = MathOps.matrix_translate(
            self.matrixCamera,
            Vector4(self.positionX.point,
                    self.positionY.point,
                    self.positionZ.point,
                    .0)
        )

        self.matrixCamera = MathOps.matrix_translate(self.matrixCamera, Vector4(.0))
        self.matrixCamera = MathOps.matrix_rotate(self.matrixCamera, self.rotateX.point, Vector3(1, 0, 0))
        self.matrixCamera = MathOps.matrix_rotate(self.matrixCamera, self.rotateY.point, Vector3(0, 1, 0))
        self.matrixCamera = MathOps.matrix_rotate(self.matrixCamera, self.rotateZ.point, Vector3(0, 0, 1))
        self.matrixCamera = MathOps.matrix_translate(self.matrixCamera, Vector4(.0))

        self.matrixCamera = MathOps.matrix_rotate(self.matrixCamera, self.rotateCenterX.point, Vector3(1, 0, 0))
        self.matrixCamera = MathOps.matrix_rotate(self.matrixCamera, self.rotateCenterY.point, Vector3(0, 1, 0))
        self.matrixCamera = MathOps.matrix_rotate(self.matrixCamera, self.rotateCenterZ.point, Vector3(0, 0, 1))

        self.cameraPosition.x = self.matrixCamera[3].x
        self.cameraPosition.y = self.matrixCamera[3].y
        self.cameraPosition.z = self.matrixCamera[3].z

        # if Settings.Setting_ZScroll != 999:
        #     self.positionZ.point = Settings.Setting_ZScroll
