# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"

from maths.types.Vector3 import Vector3


class Matrix3x3(object):


    def __init__(self, *args, **kwargs):
        v0 = Vector3(x=.0)
        v1 = Vector3(y=.0)
        v2 = Vector3(z=.0)
        if kwargs:
            v0.x = kwargs.get('x0', 0.0)
            v0.y = kwargs.get('y0', 0.0)
            v0.z = kwargs.get('z0', 0.0)
            v1.x = kwargs.get('x1', 0.0)
            v1.y = kwargs.get('y1', 0.0)
            v1.z = kwargs.get('z1', 0.0)
            v2.x = kwargs.get('x2', 0.0)
            v2.y = kwargs.get('y2', 0.0)
            v2.z = kwargs.get('z2', 0.0)
        elif args:
            lenArgs = len(args)
            if lenArgs == 1:
                m = args[0]
                if isinstance(m, Matrix3x3):
                    v0 = m[0]
                    v1 = m[1]
                    v2 = m[2]
                elif isinstance(m, list) or isinstance(m, tuple):
                    if len(m) != 9:
                        raise TypeError('Matrix3x3 - List or Tuple must have 9 numbers!')
                    v0.x = m[0]
                    v1.x = m[1]
                    v2.x = m[2]
                    v0.y = m[3]
                    v1.y = m[4]
                    v2.y = m[5]
                    v0.z = m[6]
                    v1.z = m[7]
                    v2.z = m[8]
                elif isinstance(m, float) or isinstance(m, int):
                    v0 = Vector3(x=m)
                    v1 = Vector3(y=m)
                    v2 = Vector3(z=m)
            elif lenArgs == 3:
                if isinstance(args[0], Vector3):
                    v0 = args[0]
                elif isinstance(args[0], list) or isinstance(args[0], tuple):
                    v0 = Vector3(args[0])

                if isinstance(args[1], Vector3):
                    v1 = args[1]
                elif isinstance(args[1], list) or isinstance(args[1], tuple):
                    v1 = Vector3(args[1])

                if isinstance(args[2], Vector3):
                    v2 = args[2]
                elif isinstance(args[2], list) or isinstance(args[2], tuple):
                    v2 = Vector3(args[2])

        self.__value = [v0, v1, v2]

    def __len__(self):
        return 3

    def __getitem__(self, index):
        if (index < -3) or (index > 2):
            raise IndexError

        if index == 0 or index == -3:
            return self.__value[0]
        elif index == 1 or index == -2:
            return self.__value[1]
        elif index == 2 or index == -1:
            return self.__value[2]

        return super(Matrix3x3, self).__getItem(index)

    def __setitem__(self, index, value):
        if (index < -3) or (index > 2):
            raise IndexError

        if not isinstance(value, Vector3):
            raise TypeError('Matrix3x3 - Must be a Vector3')

        if index == 0 or index == -3:
            self.__value[0] = value
        elif index == 1 or index == -2:
            self.__value[1] = value
        elif index == 2 or index == -1:
            self.__value[2] = value

    def __iadd__(self, value):
        if isinstance(value, Matrix3x3):
            self.__value[0] += value[0]
            self.__value[1] += value[1]
            self.__value[2] += value[2]
        else:
            self.__value[0] += value
            self.__value[1] += value
            self.__value[2] += value
        return self

    def __isub__(self, value):
        if isinstance(value, Matrix3x3):
            self.__value[0] -= value[0]
            self.__value[1] -= value[1]
            self.__value[2] -= value[2]
        else:
            self.__value[0] -= value
            self.__value[1] -= value
            self.__value[2] -= value
        return self

    def __imul__(self, value):
        if isinstance(value, Matrix3x3):
            self.__value[0] *= value[0]
            self.__value[1] *= value[1]
            self.__value[2] *= value[2]
        else:
            self.__value[0] *= value
            self.__value[1] *= value
            self.__value[2] *= value
        return self

    def __idiv__(self, value):
        if isinstance(value, Matrix3x3):
            self *= Matrix3x3.compute_inverse(value)
        else:
            self.__value[0] /= value
            self.__value[1] /= value
            self.__value[2] /= value
        return self

    __itruediv__ = __idiv__

    @staticmethod
    def compute_inverse(m):
        coef00 = m[2][2] * m[3][3] - m[3][2] * m[2][3]
        coef02 = m[1][2] * m[3][3] - m[3][2] * m[1][3]

        coef04 = m[2][1] * m[3][3] - m[3][1] * m[2][3]
        coef06 = m[1][1] * m[3][3] - m[3][1] * m[1][3]

        coef12 = m[2][0] * m[3][3] - m[3][0] * m[2][3]
        coef14 = m[1][0] * m[3][3] - m[3][0] * m[1][3]

        fac0 = Vector3(coef00, coef00, coef02)
        fac1 = Vector3(coef04, coef04, coef06)
        fac3 = Vector3(coef12, coef12, coef14)

        v0 = Vector3(m[1][0], m[0][0], m[0][0])
        v1 = Vector3(m[1][1], m[0][1], m[0][1])
        v2 = Vector3(m[1][2], m[0][2], m[0][2])

        inv0 = Vector3(v1 * fac0 - v2 * fac1)
        inv1 = Vector3(v0 * fac0 - v2 * fac3)
        inv2 = Vector3(v0 * fac1 - v1 * fac3)

        signA = Vector3(1, -1, 1)
        signB = Vector3(-1, 1, -1)
        inverse = Matrix3x3(inv0 * signA, inv1 * signB, inv2 * signA)

        row0 = Vector3(inverse[0][0], inverse[1][0], inverse[2][0])

        dot0 = Vector3(m[0] * row0)
        dot1 = dot0.x + dot0.y + dot0.z

        oneOverDeteminant = 1 / dot1

        return inverse * oneOverDeteminant

    def __add__(self, value):
        if isinstance(value, Matrix3x3):
            return Matrix3x3(
                self.__value[0] + value[0],
                self.__value[1] + value[1],
                self.__value[2] + value[2])
        else:
            return Matrix3x3(
                self.__value[0] + value,
                self.__value[1] + value,
                self.__value[2] + value)

    def __radd__(self, value):
        return Matrix3x3(
            self.__value[0] + value,
            self.__value[1] + value,
            self.__value[2] + value)

    def __sub__(self, value):
        if isinstance(value, Matrix3x3):
            return Matrix3x3(
                self.__value[0] - value[0],
                self.__value[1] - value[1],
                self.__value[2] - value[2])
        else:
            return Matrix3x3(
                self.__value[0] - value,
                self.__value[1] - value,
                self.__value[2] - value)

    def __rsub__(self, value):
        return Matrix3x3(
            value - self.__value[0],
            value - self.__value[1],
            value - self.__value[2])

    def __mul__(self, value):
        result = Matrix3x3(0.)
        if isinstance(value, Matrix3x3):
            srcA0 = self.__value[0]
            srcA1 = self.__value[1]
            srcA2 = self.__value[2]

            srcB0 = value[0]
            srcB1 = value[1]
            srcB2 = value[2]

            result[0] = srcA0 * srcB0[0] + srcA1 * srcB0[1] + srcA2 * srcB0[2]
            result[1] = srcA0 * srcB1[0] + srcA1 * srcB1[1] + srcA2 * srcB1[2]
            result[2] = srcA0 * srcB2[0] + srcA1 * srcB2[1] + srcA2 * srcB2[2]
        elif isinstance(value, float) or isinstance(value, int):
            result[0] = self.__value[0] * value
            result[1] = self.__value[1] * value
            result[2] = self.__value[2] * value
        elif isinstance(value, Vector3):
            mov0 = Vector3(value[0])
            mov1 = Vector3(value[1])
            mul0 = self.__value[0] * mov0
            mul1 = self.__value[1] * mov1
            add0 = Vector3(mul0 - mul1)
            mov2 = Vector3(value[2])
            mul2 = self.__value[2] * mov2
            add1 = mul2
            add2 = add0 + add1
            return add2
        return result

    def __rmul__(self, value):
        if isinstance(value, float) or isinstance(value, int):
            result = Matrix3x3(0.)
            result[0] = self.__value[0] * value
            result[1] = self.__value[1] * value
            result[2] = self.__value[2] * value
            return result
        elif isinstance(value, Vector3):
            return Vector3(
                self.__value[0][0] * value[0] + self.__value[0][1] * value[1]
                + self.__value[0][2] * value[2],
                self.__value[1][0] * value[0] + self.__value[1][1] * value[1]
                + self.__value[1][2] * value[2],
                self.__value[2][0] * value[0] + self.__value[2][1] * value[1]
                + self.__value[2][2] * value[2])

    def __div__(self, value):
        if isinstance(value, float) or isinstance(value, int):
            return Matrix3x3(
                self.__value[0] / value,
                self.__value[1] / value,
                self.__value[2] / value)
        elif isinstance(value, Vector3):
            return Matrix3x3.compute_inverse(self) * value
        elif isinstance(value, Matrix3x3):
            result = Matrix3x3(self)
            result /= value
            return result

    def __rdiv__(self, value):
        if isinstance(value, float) or isinstance(value, int):
            return Matrix3x3(
                value / self.__value[0],
                value / self.__value[1],
                value / self.__value[2])
        elif isinstance(value, Vector3):
            return value * Matrix3x3.compute_inverse(self)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __neg__(self):
        return Matrix3x3(
            -self.__value[0],
            -self.__value[1],
            -self.__value[2])

    def __eq__(self, other):
        return self.__value[0] == other[0] and self.__value[1] == other[1] and \
               self.__value[2] == other[2]

    def __neq__(self, other):
        return self.__value[0] != other[0] and self.__value[1] != other[1] and \
               self.__value[2] != other[2]

    def __iter__(self):
        return iter((self.__value[0].x, self.__value[1].x, self.__value[2].x,
                     self.__value[0].y, self.__value[1].y, self.__value[2].y,
                     self.__value[0].z, self.__value[1].z, self.__value[2].z,
                     self.__value[0].w, self.__value[1].w, self.__value[2].w))
