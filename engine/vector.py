import numpy as np


class VecN:
    def __init__(self, args):
        if isinstance(args, np.ndarray):
            self.data = args
            return

        self.data = np.array(args)

    def __add__(self, other):
        if isinstance(other, VecN):
            return VecN(self.data + other.data)
        return VecN(self.data + other)

    def __sub__(self, other):
        if isinstance(other, VecN):
            return VecN(self.data - other.data)
        return VecN(self.data - other)

    def __mul__(self, other):
        if isinstance(other, VecN):
            return VecN(self.data * other.data)

        return VecN(self.data * other)

    def __truediv__(self, other):
        if isinstance(other, VecN):
            return VecN(self.data / other.data)
        return VecN(self.data / other)

    def __floordiv__(self, other):
        if isinstance(other, VecN):
            return VecN(self.data // other.data)
        return VecN(self.data // other)

    def __pow__(self, other):
        if isinstance(other, VecN):
            return VecN(self.data ** other.data)
        return VecN(self.data ** other)

    def __repr__(self):
        return f"VecN({', '.join(self.data.astype(str))})"

    def normalize(self):
        return VecN(np.linalg.vector_norm(self.data))

    def is_zero(self):
        return not np.any(self.data)

    # moved these to superclass bc
    # it constructs an instance of the superclass
    # on each operation instead of the current class itself,
    # idk any workarounds aside from this ugly code.

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, val):
        self.data[0] = val

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, val):
        self.data[1] = val

    @property
    def z(self):
        return self.data[2]

    @z.setter
    def z(self, val):
        self.data[2] = val


class Vec2(VecN):
    def __init__(self, x, y):
        super().__init__([x, y])


class Vec3(VecN):
    def __init__(self, x, y, z):
        super().__init__([x, y, z])
