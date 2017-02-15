# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"


class Vector4(object):

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.x = kwargs.get('x', .0)
            self.y = kwargs.get('y', .0)
            self.z = kwargs.get('z', .0)
            self.w = kwargs.get('w', .0)
        elif args:
            lenArgs = len(args)
            if lenArgs == 1:
                inarg = args[0]
                if isinstance(inarg, int) or isinstance(inarg, float):
                    self.x = inarg
                    self.y = inarg
                    self.z = inarg
                    self.w = inarg
                elif isinstance(inarg, list) or isinstance(inarg, tuple):
                    il = []
                    if len(inarg) == 1:
                        il.append(inarg[0])
                        il += [.0, .0, .0]
                    elif len(inarg) == 2:
                        il = list(inarg) + [.0, .0]
                    elif len(inarg) == 3:
                        il = list(inarg) + [.0,]
                    elif len(inarg) == 4:
                        il = inarg
                    else:
                        il = inarg[:4]
                    self.x, self.y, self.z, self.w = il
                elif isinstance(inarg, Vector4):
                    self.x = inarg.x
                    self.y = inarg.y
                    self.z = inarg.z
                    self.w = inarg.w
            elif lenArgs == 2:
                self.x, self.y = args
                self.z = .0
                self.w = .0
            elif lenArgs == 3:
                self.x, self.y, self.z = args
                self.w = .0
            elif lenArgs == 4:
                self.x, self.y, self.z, self.w = args
            else:
                self.x, self.y, self.z, self.w = args[:4]
        else:
            self.x = .0
            self.y = .0
            self.z = .0
            self.w = .0

    def __len__(self):
        return 4

    def __getitem__(self, index):
        if index > 3 or index < -4:
            raise IndexError('out of range')

        if index == 0 or index == -4:
            return self.x
        elif index == 1 or index == -3:
            return self.y
        elif index == 2 or index == -2:
            return self.z
        elif index == 3 or index == -1:
            return self.w
        return super(Vector4, self).__getitem__(index)

    def __setitem__(self, index, value):
        if index > 3 or index < -4:
            raise IndexError('out of range')

        if index == 0 or index == -4:
            self.x = value
        elif index == 1 or index == -3:
            self.y = value
        elif index == 2 or index == -2:
            self.z = value
        elif index == 3 or index == -1:
            self.w = value

        #return super(Vector4, self).__setitem__(index, value)

    def __iadd__(self, value):
        if isinstance(value, Vector4):
            self.x += value.x
            self.y += value.y
            self.z += value.z
            self.w += value.w
        else:
            self.x += value
            self.y += value
            self.z += value
            self.w += value
        return self

    def __isub__(self, value):
        if isinstance(value, Vector4):
            self.x -= value.x
            self.y -= value.y
            self.z -= value.z
            self.w -= value.w
        else:
            self.x -= value
            self.y -= value
            self.z -= value
            self.w -= value
        return self

    def __imul__(self, value):
        if isinstance(value, Vector4):
            self.x *= value.x
            self.y *= value.y
            self.z *= value.z
            self.w *= value.w
        else:
            self.x *= value
            self.y *= value
            self.z *= value
            self.w *= value
        return self

    def __idiv__(self, value):
        if isinstance(value, Vector4):
            self.x /= value.x
            self.y /= value.y
            self.z /= value.z
            self.w /= value.w
        else:
            self.x /= value
            self.y /= value
            self.z /= value
            self.w /= value
        return self

    def __itruediv__(self, value):
        if isinstance(value, Vector4):
            self.x /= float(value.x)
            self.y /= float(value.y)
            self.z /= float(value.z)
            self.w /= float(value.w)
        else:
            self.x /= float(value)
            self.y /= float(value)
            self.z /= float(value)
            self.w /= float(value)
        return self

    def __imod__(self, value):
        if isinstance(value, Vector4):
            self.x %= value.x
            self.y %= value.y
            self.z %= value.z
            self.w %= value.w
        else:
            self.x %= value
            self.y %= value
            self.z %= value
            self.w %= value
        return self

    def __iand__(self, value):
        if isinstance(value, Vector4):
            self.x &= value.x
            self.y &= value.y
            self.z &= value.z
            self.w &= value.w
        else:
            self.x &= value
            self.y &= value
            self.z &= value
            self.w &= value
        return self

    def __ior__(self, value):
        if isinstance(value, Vector4):
            self.x |= value.x
            self.y |= value.y
            self.z |= value.z
            self.w |= value.w
        else:
            self.x |= value
            self.y |= value
            self.z |= value
            self.w |= value
        return self

    def __ixor__(self, value):
        if isinstance(value, Vector4):
            self.x ^= value.x
            self.y ^= value.y
            self.z ^= value.z
            self.w ^= value.w
        else:
            self.x ^= value
            self.y ^= value
            self.z ^= value
            self.w ^= value
        return self

    def __ilshift__(self, value):
        if isinstance(value, Vector4):
            self.x <<= value.x
            self.y <<= value.y
            self.z <<= value.z
            self.w <<= value.w
        else:
            self.x <<= value
            self.y <<= value
            self.z <<= value
            self.w <<= value
        return self

    def __irshift__(self, value):
        if isinstance(value, Vector4):
            self.x >>= value.x
            self.y >>= value.y
            self.z >>= value.z
            self.w >>= value.w
        else:
            self.x >>= value
            self.y >>= value
            self.z >>= value
            self.w >>= value
        return self

    def __add__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x + value.x, self.y + value.y,
                        self.z + value.z, self.w + value.w)
        else:
            return Vector4(self.x + value, self.y + value,
                        self.z + value, self.w + value)

    def __radd__(self, value):
        return Vector4(value + self.x, value + self.y,
                    value + self.z, value + self.w)

    def __sub__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x - value.x, self.y - value.y,
                        self.z - value.z, self.w - value.w)
        else:
            return Vector4(self.x - value, self.y - value,
                        self.z - value, self.w - value)

    def __rsub__(self, value):
        return Vector4(value - self.x, value - self.y,
                    value - self.z, value - self.w)

    def __mul__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x * value.x, self.y * value.y,
                        self.z * value.z, self.w * value.w)
        else:
            return Vector4(self.x * value, self.y * value,
                        self.z * value, self.w * value)

    def __rmul__(self, value):
        return Vector4(value * self.x, value * self.y,
                    value * self.z, value * self.w)

    def __div__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x / value.x, self.y / value.y,
                        self.z / value.z, self.w / value.w)
        else:
            return Vector4(self.x / value, self.y / value,
                        self.z / value, self.w / value)

    def __rdiv__(self, value):
        return Vector4(value / self.x, value / self.y,
                    value / self.z, value / self.w)

    def __truediv__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x / float(value.x), self.y / float(value.y),
                        self.z / float(value.z), self.w / float(value.w))
        else:
            return Vector4(self.x / float(value), self.y / float(value),
                        self.z / float(value), self.w / float(value))

    def __rtruediv__(self, value):
        v = float(value)
        return Vector4(v / self.x, v / self.y, v / self.z, v / self.w)

    def __neg__(self):
        return Vector4(-self.x, -self.y, -self.z, -self.w)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y and self.z != other.z and self.w != other.w

    def __mod__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x % value.x, self.y % value.y,
                        self.z % value.z, self.w % value.w)
        else:
            return Vector4(self.x % value, self.y % value,
                        self.z % value, self.w % value)

    def __rmod__(self, value):
        return Vector4(value % self.x, value % self.y, value % self.z, value.w % self.w)

    def __and__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x & value.x, self.y & value.y,
                        self.z & value.z, self.w & value.w)
        else:
            return Vector4(self.x & value, self.y & value,
                        self.z & value, self.w & value)

    def __rand__(self, value):
        return Vector4(value & self.x, value & self.y, value & self.z, value & self.w)

    def __or__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x | value.x, self.y | value.y,
                        self.z | value.z, self.w | value.w)
        else:
            return Vector4(self.x | value, self.y | value,
                        self.z | value, self.w | value)

    def __ror__(self, value):
        return Vector4(value | self.x, value | self.y, value | self.z, value | self.w)

    def __xor__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x ^ value.x, self.y ^ value.y,
                        self.z ^ value.z, self.w ^ value.w)
        else:
            return Vector4(self.x ^ value, self.y ^ value,
                        self.z ^ value, self.w ^ value)

    def __rxor__(self, value):
        return Vector4(value ^ self.x, value ^ self.y, value ^ self.z, value ^ self.w)

    def __lshift__(self, value):
        if isinstance(value, Vector4):
            return Vector4(self.x << value.x, self.y << value.y,
                        self.z << value.z, self.w << value.w)
        else:
            return Vector4(self.x << value, self.y << value,
                        self.z << value, self.w << value)

    def __rlshift__(self, value):
        return Vector4(
            value << self.x, value << self.y,
            value << self.z, value << self.w)

    def __rshift__(self, value):
        if isinstance(value, Vector4):
            return Vector4(
                self.x >> value.x, self.y >> value.y,
                self.z >> value.z, self.w >> value.w)
        else:
            return Vector4(
                self.x >> value, self.y >> value,
                self.z >> value, self.w >> value)

    def __rrshift__(self, value):
        return Vector4(
            value >> self.x, value >> self.y,
            value >> self.z, value >> self.w)

    def __invert__(self):
        return Vector4(~self.x, ~self.y, ~self.z, ~self.w)

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

    @property
    def a(self):
        return self.w

    @a.setter
    def a(self, value):
        self.w = value

    s = r
    t = g
    p = b
    q = a

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.w))

    def __nonzero__(self):
        return self.x == 0 and self.y == 0 and self.z == 0 and self.w == 0

    def __str__(self):
        return "Vector4 (%.3f, %.3f, %.3f, %.3f)" % (self.x, self.y, self.z, self.w)

    __repr__ = __str__

    def __getattribute__(self, name):
        if len(name) == 4:
            xyzw = (self.x, self.y, self.z, self.w) * 3
            return Vector4([xyzw['xyzwrgbastpq'.index(i)] for i in name])
        return super(Vector4, self).__getattribute__(name)