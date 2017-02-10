"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import numpy
from pyrr import Matrix44 as mat4
from pyrr import Vector3 as vec3


class Camera():
    def __init__(self):
        self.matrixCamera = numpy.array(numpy.ones((4, 4)), dtype=numpy.float32)
        self.View_Eye = vec3([0, 0, 0])
        self.View_Center = vec3([0, 0, 0])
        self.View_Up = vec3([0, 0, 0])
        self.positionX = {'animate': False, 'point': 0}
        self.positionY = {'animate': False, 'point': 0}
        self.positionZ = {'animate': False, 'point': 0}
        self.rotateX = {'animate': False, 'point': 0}
        self.rotateY = {'animate': False, 'point': 0}
        self.rotateZ = {'animate': False, 'point': 0}
        self.rotateCenterX = {'animate': False, 'point': 0}
        self.rotateCenterY = {'animate': False, 'point': 0}
        self.rotateCenterZ = {'animate': False, 'point': 0}
        self.cameraPosition = (0, 0, 0)


    def init_properties(self):
        self.View_Eye = vec3([0, 0, 10])
        self.view_Center = vec3([0, 0, 0])
        self.View_Up = vec3([0, -1, 0])

        self.positionX["point"] = 0
        self.positionY["point"] = 0
        self.positionZ["point"] = -16.0

        self.rotateX["point"] = 160
        self.rotateY["point"] = 140
        self.rotateZ["point"] = 0

        self.rotateCenterX["point"] = 0
        self.rotateCenterY["point"] = 0
        self.rotateCenterZ["point"] = 0

        self.matrixCamera = numpy.array(numpy.ones((4, 4)), dtype=numpy.float32)


    def render(self):
        mtx = self.lookAt(self.View_Eye, self.View_Center, self.View_Up)

        mtx *= mat4.from_translation((self.positionX['point'], self.positionY['point'], self.positionZ['point']), dtype='f')

        mtx *= mat4.from_translation((0, 0, 0), dtype='f')
        mtx *= mat4.from_x_rotation(self.rotateX['point'], dtype='f')
        mtx *= mat4.from_y_rotation(self.rotateY['point'], dtype='f')
        mtx *= mat4.from_z_rotation(self.rotateZ['point'], dtype='f')
        mtx *= mat4.from_translation((0, 0, 0), dtype='f')

        mtx *= mat4.from_x_rotation(self.rotateCenterX['point'], dtype='f')
        mtx *= mat4.from_y_rotation(self.rotateCenterY['point'], dtype='f')
        mtx *= mat4.from_z_rotation(self.rotateCenterZ['point'], dtype='f')

        # debug
        # mtx[0][0] = 0.766044
        # mtx[0][1] = -0.219846
        # mtx[0][2] = 0.604023
        # mtx[0][3] = 0.0
        # mtx[1][0] = 0.000000
        # mtx[1][1] = 0.939693
        # mtx[1][2] = 0.342020
        # mtx[1][3] = 0.0
        # mtx[2][0] = -0.642788
        # mtx[2][1] = -0.262003
        # mtx[2][2] = 0.719846
        # mtx[2][3] = 0.0
        # mtx[3][0] = 0.0
        # mtx[3][1] = 0.0
        # mtx[3][2] = -26.0
        # mtx[3][3] = 1.0
        print(mtx)

        self.matrixCamera = numpy.array(mtx, dtype=numpy.float32)

        self.cameraPosition = (mtx[3][0], mtx[3][1], mtx[3][2])


    def lookAt(self, eye, target, up):
        forward = (target - eye).normalised
        side = (forward ^ up).normalised
        up = (side ^ forward).normalised

        mat = mat4(dtype='f')
        mat[0][0] = side[0]
        mat[1][0] = side[1]
        mat[2][0] = side[2]

        mat[0][1] = up[0]
        mat[1][1] = up[1]
        mat[2][1] = up[2]

        mat[0][2] = -forward[0]
        mat[1][2] = -forward[1]
        mat[2][2] = -forward[2]

        mat[3][0] = - (side | eye)
        mat[3][1] = - (up | eye)
        mat[3][2] = forward | eye
        mat[3][3] = 1.0

        return mat