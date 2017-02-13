# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

import math
import numpy
from maths.types.Matrix4x4 import Matrix4x4
from maths.types.Vector3 import Vector3


#region Operations

def matrix_translate(m, v):
    result = Matrix4x4(m)
    result[3] = m[0] * v[0] + m[1] * v[1] + m[2] * v[2] + m[3]
    return result


def matrix_rotate(m, angle, v):
    a = math.radians(angle)
    c = math.cos(a)
    s = math.sin(a)

    axis = Vector3(normalize(v))
    temp = (1. - c) * axis

    rmat = Matrix4x4()
    rmat[0][0] = c + temp[0] * axis[0]
    rmat[0][1] = 0 + temp[0] * axis[1] + s * axis[2]
    rmat[0][2] = 0 + temp[0] * axis[2] - s * axis[1]

    rmat[1][0] = 0 + temp[1] * axis[0] - s * axis[2]
    rmat[1][1] = c + temp[1] * axis[1]
    rmat[1][2] = 0 + temp[1] * axis[2] + s * axis[0]

    rmat[2][0] = 0 + temp[2] * axis[0] + s * axis[1]
    rmat[2][1] = 0 + temp[2] * axis[1] - s * axis[0]
    rmat[2][2] = c + temp[2] * axis[2]

    result = Matrix4x4()
    result[0] = m[0] * rmat[0][0] + m[1] * rmat[0][1] + m[2] * rmat[0][2]
    result[1] = m[0] * rmat[1][0] + m[1] * rmat[1][1] + m[2] * rmat[1][2]
    result[2] = m[0] * rmat[2][0] + m[1] * rmat[2][1] + m[2] * rmat[2][2]
    result[3] = m[3]
    return result


def matrix_scale(m, v):
    result = Matrix4x4()
    result[0] = m[0] * v[0]
    result[1] = m[1] * v[1]
    result[2] = m[2] * v[2]
    result[3] = m[3]
    return result

#endregion

#region Vectors

def magnitude(vec):
    return math.sqrt(sum(vec[i] * vec[i] for i in range(len(vec))))


def normalize(vec):
    vmag = magnitude(vec)
    v = [vec[i] / vmag for i in range(len(vec))]
    return Vector3(v)

def cross(u, v):
    return (u.y * v.z - u.z * v.y,
	        u.z * v.x - u.x * v.z,
	        u.x * v.y - u.y * v.x)

def dot(u, v):
    return numpy.dot(u, v)

#endregion

#region Matrix

def matrix_to_gl(mtx):
    return list(mtx)

def lookAt(eye, center, up):
    f = Vector3(normalize(center - eye))
    s = Vector3(normalize(cross(f, up)))
    u = Vector3(cross(s, f))

    result = Matrix4x4(1.0)
    result[0][0] = s.x
    result[1][0] = s.y
    result[2][0] = s.z
    result[0][1] = u.x
    result[1][1] = u.y
    result[2][1] = u.z
    result[0][2] = -f.x
    result[1][2] = -f.y
    result[2][2] = -f.z
    result[3][0] = -dot(s, eye)
    result[3][1] = -dot(u, eye)
    result[3][2] = dot(f, eye)

    return result

def perspective(fovy, aspect, zNear, zFar):
    rad = math.radians(fovy)
    tanHalfFovy = math.tan((rad / 2))

    result = Matrix4x4(0.0)
    result[0][0] = 1. / (aspect * tanHalfFovy)
    result[1][1] = 1. / tanHalfFovy
    result[2][2] = -(zFar + zNear) / (zFar - zNear)
    result[2][3] = -1.
    result[3][2] = -(2. * zFar * zNear) / (zFar - zNear)
    return result

#endregion

def print_matrix(mtx):
    print_vec4(mtx[0])
    print_vec4(mtx[1])
    print_vec4(mtx[2])
    print_vec4(mtx[3])
    print("========")

def print_vec4(vec):
    print("x = " + str(vec.x) + ", y = " + str(vec.y) + ", z = " + str(vec.z) + ", w = " + str(vec.w))