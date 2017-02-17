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
from maths.types.Matrix3x3 import Matrix3x3
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


def matrix_inverse_transpose(m):
    subfactor00 = m[2][2] * m[3][3] - m[3][2] * m[2][3]
    subfactor01 = m[2][1] * m[3][3] - m[3][1] * m[2][3]
    subfactor02 = m[2][1] * m[3][2] - m[3][1] * m[2][2]
    subfactor03 = m[2][0] * m[3][3] - m[3][0] * m[2][3]
    subfactor04 = m[2][0] * m[3][2] - m[3][0] * m[2][2]
    subfactor05 = m[2][0] * m[3][1] - m[3][0] * m[2][1]
    subfactor06 = m[1][2] * m[3][3] - m[3][2] * m[1][3]
    subfactor07 = m[1][1] * m[3][3] - m[3][1] * m[1][3]
    subfactor08 = m[1][1] * m[3][2] - m[3][1] * m[1][2]
    subfactor09 = m[1][0] * m[3][3] - m[3][0] * m[1][3]
    subfactor10 = m[1][0] * m[3][2] - m[3][0] * m[1][2]
    subfactor11 = m[1][1] * m[3][3] - m[3][1] * m[1][3]
    subfactor12 = m[1][0] * m[3][1] - m[3][0] * m[1][1]
    subfactor13 = m[1][2] * m[2][3] - m[2][2] * m[1][3]
    subfactor14 = m[1][1] * m[2][3] - m[2][1] * m[1][3]
    subfactor15 = m[1][1] * m[2][2] - m[2][1] * m[1][2]
    subfactor16 = m[1][0] * m[2][3] - m[2][0] * m[1][3]
    subfactor17 = m[1][0] * m[2][2] - m[2][0] * m[1][2]
    subfactor18 = m[1][0] * m[2][1] - m[2][0] * m[1][1]

    inverse = Matrix4x4()
    inverse[0][0] = + (m[1][1] * subfactor00 - m[1][2] * subfactor01 + m[1][3] * subfactor02)
    inverse[0][1] = - (m[1][0] * subfactor00 - m[1][2] * subfactor03 + m[1][3] * subfactor04)
    inverse[0][2] = + (m[1][0] * subfactor01 - m[1][1] * subfactor03 + m[1][3] * subfactor05)
    inverse[0][3] = - (m[1][0] * subfactor02 - m[1][1] * subfactor04 + m[1][2] * subfactor05)

    inverse[1][0] = - (m[0][1] * subfactor00 - m[0][2] * subfactor01 + m[0][3] * subfactor02)
    inverse[1][1] = + (m[0][0] * subfactor00 - m[0][2] * subfactor03 + m[0][3] * subfactor04)
    inverse[1][2] = - (m[0][0] * subfactor01 - m[0][1] * subfactor03 + m[0][3] * subfactor05)
    inverse[1][3] = + (m[0][0] * subfactor02 - m[0][1] * subfactor04 + m[0][2] * subfactor05)

    inverse[2][0] = + (m[0][1] * subfactor06 - m[0][2] * subfactor07 + m[0][3] * subfactor08)
    inverse[2][1] = - (m[0][0] * subfactor06 - m[0][2] * subfactor09 + m[0][3] * subfactor10)
    inverse[2][2] = + (m[0][0] * subfactor11 - m[0][1] * subfactor09 + m[0][3] * subfactor12)
    inverse[2][3] = - (m[0][0] * subfactor08 - m[0][1] * subfactor10 + m[0][2] * subfactor12)

    inverse[3][0] = - (m[0][1] * subfactor13 - m[0][2] * subfactor14 + m[0][3] * subfactor15)
    inverse[3][1] = + (m[0][0] * subfactor13 - m[0][2] * subfactor16 + m[0][3] * subfactor17)
    inverse[3][2] = - (m[0][0] * subfactor14 - m[0][1] * subfactor16 + m[0][3] * subfactor18)
    inverse[3][3] = + (m[0][0] * subfactor15 - m[0][1] * subfactor17 + m[0][2] * subfactor18)

    determinant = m[0][0] * inverse[0][0] + m[0][1] * inverse[0][1] + m[0][2] * inverse[0][2] + m[0][3] * inverse[0][3]

    inverse /= determinant

    return inverse


def compute_tangent_basis(vertices, uvs, normals):
    tangents = []
    bitangents = []

    for i in range(len(vertices)):
        # Shortcuts for vertices
        v0 = vertices[i + 0]
        v1 = vertices[i + 1]
        v2 = vertices[i + 2]

        # Shortcuts for UVs
        uv0 = uvs[i + 0]
        uv1 = uvs[i + 1]
        uv2 = uvs[i + 2]

        # Edges of the triangle: postion delta
        deltaPos1 = v1 - v0
        deltaPos2 = v2 - v0

        # UV delta
        deltaUV1 = uv1 - uv0
        deltaUV2 = uv2 - uv0

        r = 1 / (deltaUV1.x * deltaUV2.y - deltaUV1.y * deltaUV2.x)
        tangent = (deltaPos1 * deltaUV2.y - deltaPos2 * deltaUV1.y) * r
        bitangent = (deltaPos2 * deltaUV1.x - deltaPos1 * deltaUV2.x) * r

        # Set the same tangent for all three vertices of the triangle.
        # They will be merged later, in vboindexer.cpp
        tangents.append(tangent)
        tangents.append(tangent)
        tangents.append(tangent)

        # Same thing for binormals
        bitangents.append(bitangent)
        bitangents.append(bitangent)
        bitangents.append(bitangent)

    for i in range(len(vertices)):
        n = normals[i]
        t = tangents[i]
        b = bitangents[i]

        # Gram-Schmidt orthogonalize
        t = normalize(t - n * dot(n, t))

        # Calculate handedness
        if dot(cross(n, t), b) < 0.0:
            t = t * -1.0

    return tangents, bitangents

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
    mtx_ptr = []
    mtx_ptr.append(list(mtx[0]))
    mtx_ptr.append(list(mtx[1]))
    mtx_ptr.append(list(mtx[2]))
    mtx_ptr.append(list(mtx[3]))
    return mtx_ptr

def matrix3_to_gl(mtx):
    mtx_ptr = []
    mtx_ptr.append(list(mtx[0]))
    mtx_ptr.append(list(mtx[1]))
    mtx_ptr.append(list(mtx[2]))
    return mtx_ptr

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

def print_vec3(vec):
    if not vec is None:
        print("x = " + str(vec.x) + ", y = " + str(vec.y) + ", z = " + str(vec.z))
    else:
        print("Vector3 is None!")
