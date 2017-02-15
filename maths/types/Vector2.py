# -*- coding: utf-8 -*-

"""
Kuplung - OpenGL Viewer, python port
supudo.net
"""
__author__ = 'supudo'
__version__ = "1.0.0"


class Vector2(object):


    def __init__(self, *args, **kwargs):
        if kwargs:
            self.x = kwargs.get('x', .0)
            self.y = kwargs.get('y', .0)
        elif args:
            lenArgs = len(args)
            if lenArgs == 1:
                inarg = args[0]
                if isinstance(inarg, int) or isinstance(inarg, float):
                    self.x = inarg
                    self.y = inarg
                elif isinstance(inarg, list) or isinstance(inarg, tuple):
                    il = []
                    if len(inarg) == 1:
                        il.append(inarg[0])
                        il.append(0)
                    elif len(inarg) == 2:
                        il = list(inarg)
                    else:
                        il = inarg[:2]
                    self.x, self.y = il
                elif isinstance(inarg, Vector2):
                    self.x = inarg.x
                    self.y = inarg.y
            elif lenArgs == 2:
                self.x, self.y = args
            else:
                self.x, self.y = args[:2]
        else:
            self.x = .0
            self.y = .0

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index > 1 or index < -2:
            raise IndexError('out of range')

        if index == 0 or index == -2:
            return self.x
        elif index == 1 or index == -1:
            return self.y

        return super(Vector2, self).__getitem__(index)

    def __setitem__(self, index, value):
        if index > 1 or index < -2:
            raise IndexError('out of range')

        if index == 0 or index == -2:
            self.x = value
        elif index == 1 or index == -1:
            self.y = value

    def __iadd__(self, value):
        if isinstance(value, Vector2):
            self.x += value.x
            self.y += value.y
        else:
            self.x += value
            self.y += value
        return self

    def __isub__(self, value):
        if isinstance(value, Vector2):
            self.x -= value.x
            self.y -= value.y
        else:
            self.x -= value
            self.y -= value
        return self

    def __imul__(self, value):
        if isinstance(value, Vector2):
            self.x *= value.x
            self.y *= value.y
        else:
            self.x *= value
            self.y *= value
        return self

    def __idiv__(self, value):
        if isinstance(value, Vector2):
            self.x /= value.x
            self.y /= value.y
        else:
            self.x /= value
            self.y /= value
        return self

    def __itruediv__(self, value):
        if isinstance(value, Vector2):
            self.x /= float(value.x)
            self.y /= float(value.y)
        else:
            self.x /= float(value)
            self.y /= float(value)
        return self

    def __imod__(self, value):
        if isinstance(value, Vector2):
            self.x %= value.x
            self.y %= value.y
        else:
            self.x %= value
            self.y %= value
        return self

    def __iand__(self, value):
        if isinstance(value, Vector2):
            self.x &= value.x
            self.y &= value.y
        else:
            self.x &= value
            self.y &= value
        return self

    def __ior__(self, value):
        if isinstance(value, Vector2):
            self.x |= value.x
            self.y |= value.y
        else:
            self.x |= value
            self.y |= value
        return self

    def __ixor__(self, value):
        if isinstance(value, Vector2):
            self.x ^= value.x
            self.y ^= value.y
        else:
            self.x ^= value
            self.y ^= value
        return self

    def __ilshift__(self, value):
        if isinstance(value, Vector2):
            self.x <<= value.x
            self.y <<= value.y
        else:
            self.x <<= value
            self.y <<= value
        return self

    def __irshift__(self, value):
        if isinstance(value, Vector2):
            self.x >>= value.x
            self.y >>= value.y
        else:
            self.x >>= value
            self.y >>= value
        return self

    def __add__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x + value.x, self.y + value.y)
        else:
            return Vector2(self.x + value, self.y + value)

    def __radd__(self, value):
        return Vector2(value + self.x, value + self.y)

    def __sub__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x - value.x, self.y - value.y)
        else:
            return Vector2(self.x - value, self.y - value)

    def __rsub__(self, value):
        return Vector2(value - self.x, value - self.y)

    def __mul__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x * value.x, self.y * value.y)
        else:
            return Vector2(self.x * value, self.y * value)

    def __rmul__(self, value):
        return Vector2(value * self.x, value * self.y)

    def __div__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x / value.x, self.y / value.y)
        else:
            return Vector2(self.x / value, self.y / value)

    def __rdiv__(self, value):
        return Vector2(value / self.x, value / self.y)

    def __truediv__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x / float(value.x), self.y / float(value.y))
        else:
            return Vector2(self.x / float(value), self.y / float(value))

    def __rtruediv__(self, value):
        v = float(value)
        return Vector2(v / self.x, v / self.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y

    def __mod__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x % value.x, self.y % value.y)
        else:
            return Vector2(self.x % value, self.y % value)

    def __rmod__(self, value):
        return Vector2(value % self.x, value % self.y)

    def __and__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x & value.x, self.y & value.y)
        else:
            return Vector2(self.x & value, self.y & value)

    def __rand__(self, value):
        return Vector2(value & self.x, value & self.y)

    def __or__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x | value.x, self.y | value.y)
        else:
            return Vector2(self.x | value, self.y | value)

    def __ror__(self, value):
        return Vector2(value | self.x, value | self.y)

    def __xor__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x ^ value.x, self.y ^ value.y)
        else:
            return Vector2(self.x ^ value, self.y ^ value)

    def __rxor__(self, value):
        return Vector2(value ^ self.x, value ^ self.y)

    def __lshift__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x << value.x, self.y << value.y)
        else:
            return Vector2(self.x << value, self.y << value)

    def __rlshift__(self, value):
        return Vector2(value << self.x, value << self.y)

    def __rshift__(self, value):
        if isinstance(value, Vector2):
            return Vector2(self.x >> value.x, self.y >> value.y)
        else:
            return Vector2(self.x >> value, self.y >> value)

    def __rrshift__(self, value):
        return Vector2(value >> self.x, value >> self.y)

    def __invert__(self):
        return Vector2(~self.x, ~self.y)

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

    s = r
    t = g

    def __iter__(self):
        return iter((self.x, self.y))

    def __nonzero__(self):
        return self.x == 0 and self.y == 0

    def __str__(self):
        return "Vector2 (%.3f, %.3f)" % (self.x, self.y)

    __repr__ = __str__

    def __getattribute__(self, name):
        if len(name) == 2:
            xyw = (self.x, self.y) * 2
            return Vector2([xyw['xyrgst'.index(i)] for i in name])
        return super(Vector2, self).__getattribute__(name)