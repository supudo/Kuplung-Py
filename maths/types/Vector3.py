# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"


class Vector3(object):
    def __init__(self, *args, **kwargs):
        if kwargs:
            self.x = kwargs.get('x', .0)
            self.y = kwargs.get('y', .0)
            self.z = kwargs.get('z', .0)
        elif args:
            lenArgs = len(args)
            if lenArgs == 1:
                inarg = args[0]
                if isinstance(inarg, int) or isinstance(inarg, float):
                    self.x = inarg
                    self.y = inarg
                    self.z = inarg
                elif isinstance(inarg, list) or isinstance(inarg, tuple):
                    il = []
                    if len(inarg) == 1:
                        il.append(inarg[0])
                        il += [.0, .0]
                    elif len(inarg) == 2:
                        il = list(inarg)
                        il.append(0.0)
                    elif len(inarg) == 3:
                        il = inarg
                    else:
                        il = inarg[:3]
                    self.x, self.y, self.z = il
                elif isinstance(inarg, Vector3):
                    self.x = inarg.x
                    self.y = inarg.y
                    self.z = inarg.z
            elif lenArgs == 2:
                self.x, self.y = args
                self.z = .0
            elif lenArgs == 3:
                self.x, self.y, self.z = args
            else:
                self.x, self.y, self.z = args[:3]
        else:
            self.x = .0
            self.y = .0
            self.z = .0

    def __len__(self):
        return 3

    def __getitem__(self, index):
        if index > 2 or index < -3:
            raise IndexError('out of range')

        if index == 0 or index == -3:
            return self.x
        elif index == 1 or index == -2:
            return self.y
        elif index == 2 or index == -1:
            return self.z

        return super(Vector3, self).__getitem__(index)

    def __setitem__(self, index, value):
        if index > 2 or index < -3:
            raise IndexError('out of range')

        if index == 0 or index == -3:
            self.x = value
        elif index == 1 or index == -2:
            self.y = value
        elif index == 2 or index == -1:
            self.z = value

    def __iadd__(self, value):
        if isinstance(value, Vector3):
            self.x += value.x
            self.y += value.y
            self.z += value.z
        else:
            self.x += value
            self.y += value
            self.z += value
        return self

    def __isub__(self, value):
        if isinstance(value, Vector3):
            self.x -= value.x
            self.y -= value.y
            self.z -= value.z
        else:
            self.x -= value
            self.y -= value
            self.z -= value
        return self

    def __imul__(self, value):
        if isinstance(value, Vector3):
            self.x *= value.x
            self.y *= value.y
            self.z *= value.z
        else:
            self.x *= value
            self.y *= value
            self.z *= value
        return self

    def __idiv__(self, value):
        if isinstance(value, Vector3):
            self.x /= value.x
            self.y /= value.y
            self.z /= value.z
        else:
            self.x /= value
            self.y /= value
            self.z /= value
        return self

    def __itruediv__(self, value):
        if isinstance(value, Vector3):
            self.x /= float(value.x)
            self.y /= float(value.y)
            self.z /= float(value.z)
        else:
            self.x /= float(value)
            self.y /= float(value)
            self.z /= float(value)
        return self

    def __imod__(self, value):
        if isinstance(value, Vector3):
            self.x %= value.x
            self.y %= value.y
            self.z %= value.z
        else:
            self.x %= value
            self.y %= value
            self.z %= value
        return self

    def __iand__(self, value):
        if isinstance(value, Vector3):
            self.x &= value.x
            self.y &= value.y
            self.z &= value.z
        else:
            self.x &= value
            self.y &= value
            self.z &= value
        return self

    def __ior__(self, value):
        if isinstance(value, Vector3):
            self.x |= value.x
            self.y |= value.y
            self.z |= value.z
        else:
            self.x |= value
            self.y |= value
            self.z |= value
        return self

    def __ixor__(self, value):
        if isinstance(value, Vector3):
            self.x ^= value.x
            self.y ^= value.y
            self.z ^= value.z
        else:
            self.x ^= value
            self.y ^= value
            self.z ^= value
        return self

    def __ilshift__(self, value):
        if isinstance(value, Vector3):
            self.x <<= value.x
            self.y <<= value.y
            self.z <<= value.z
        else:
            self.x <<= value
            self.y <<= value
            self.z <<= value
        return self

    def __irshift__(self, value):
        if isinstance(value, Vector3):
            self.x >>= value.x
            self.y >>= value.y
            self.z >>= value.z
        else:
            self.x >>= value
            self.y >>= value
            self.z >>= value
        return self

    def __add__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x + value.x, self.y + value.y, self.z + value.z)
        else:
            return Vector3(self.x + value, self.y + value, self.z + value)

    def __radd__(self, value):
        return Vector3(value + self.x, value + self.y, value + self.z)

    def __sub__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x - value.x, self.y - value.y, self.z - value.z)
        else:
            return Vector3(self.x - value, self.y - value, self.z - value)

    def __rsub__(self, value):
        return Vector3(value - self.x, value - self.y, value - self.z)

    def __mul__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x * value.x, self.y * value.y, self.z * value.z)
        else:
            return Vector3(self.x * value, self.y * value, self.z * value)

    def __rmul__(self, value):
        return Vector3(value * self.x, value * self.y, value * self.z)

    def __div__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x / value.x, self.y / value.y, self.z / value.z)
        else:
            return Vector3(self.x / value, self.y / value, self.z / value)

    def __rdiv__(self, value):
        return Vector3(value / self.x, value / self.y, value / self.z)

    def __truediv__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x / float(value.x), self.y / float(value.y), self.z / float(value.z))
        else:
            return Vector3(self.x / float(value), self.y / float(value), self.z / float(value))

    def __rtruediv__(self, value):
        v = float(value)
        return Vector3(v / self.x, v / self.y, v / self.z)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y and self.z != other.z

    def __mod__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x % value.x, self.y % value.y, self.z % value.z)
        else:
            return Vector3(self.x % value, self.y % value, self.z % value)

    def __rmod__(self, value):
        return Vector3(value % self.x, value % self.y, value % self.z)

    def __and__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x & value.x, self.y & value.y, self.z & value.z)
        else:
            return Vector3(self.x & value, self.y & value, self.z & value)

    def __rand__(self, value):
        return Vector3(value & self.x, value & self.y, value & self.z)

    def __or__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x | value.x, self.y | value.y, self.z | value.z)
        else:
            return Vector3(self.x | value, self.y | value, self.z | value)

    def __ror__(self, value):
        return Vector3(value | self.x, value | self.y, value | self.z)

    def __xor__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x ^ value.x, self.y ^ value.y, self.z ^ value.z)
        else:
            return Vector3(self.x ^ value, self.y ^ value, self.z ^ value)

    def __rxor__(self, value):
        return Vector3(value ^ self.x, value ^ self.y, value ^ self.z)

    def __lshift__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x << value.x, self.y << value.y, self.z << value.z)
        else:
            return Vector3(self.x << value, self.y << value, self.z << value)

    def __rlshift__(self, value):
        return Vector3(value << self.x, value << self.y, value << self.z)

    def __rshift__(self, value):
        if isinstance(value, Vector3):
            return Vector3(self.x >> value.x, self.y >> value.y, self.z >> value.z)
        else:
            return Vector3(self.x >> value, self.y >> value, self.z >> value)

    def __rrshift__(self, value):
        return Vector3(value >> self.x, value >> self.y, value >> self.z)

    def __invert__(self):
        return Vector3(~self.x, ~self.y, ~self.z)

    @property
    def r(self):
        return self.x

    @r.setter
    def r(self, value):
        self.x = value

    @property
    def g(self):
        return self.y

    @g.setter
    def g(self, value):
        self.y = value

    @property
    def b(self):
        return self.z

    @b.setter
    def b(self, value):
        self.z = value

    s = r
    t = g
    p = b

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __nonzero__(self):
        return self.x == 0 and self.y == 0 and self.z == 0

    def __str__(self):
        return "Vector3 (%.3f, %.3f, %.3f)" % (self.x, self.y, self.z)

    __repr__ = __str__

    def __getattribute__(self, name):
        if len(name) == 3:
            xyzw = (self.x, self.y, self.z) * 3
            return Vector3([xyzw['xyzrgbstp'.index(i)] for i in name])
        return super(Vector3, self).__getattribute__(name)