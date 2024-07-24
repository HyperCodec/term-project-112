class VecN:
    def __init__(self, **kwargs):
        self._known_keys = kwargs.keys()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __len__(self):
        return len(self._known_keys)

    def __eq__(self, other):
        if not isinstance(other, VecN):
            return False

        larger, smaller = twoObjectSort(self, other)

        for key in larger._known_keys:
            if not hasattr(other, key):
                return False

            if getattr(self, key) != getattr(other, key):
                return False

        return True

    def __setitem__(self, key, val):
        if key not in self._known_keys:
            raise KeyError(f"{key} not found in {self}")

        setattr(self, key, val)

    def __repr__(self):
        kv_pairs = []

        for key in self._known_keys:
            val = getattr(self, key)

            kv_pairs.append(f"{key}={val}")

        inner = ", ".join(kv_pairs)

        return f"VecN({inner})"

    def _perform_vec_op(self, other, callback, default_uninit=0):
        larger, smaller = twoObjectSort(self, other)

        selfIsLarger = self == larger

        kwargs = {}

        for key in larger._known_keys:
            v1 = getattr(larger, key)
            v2 = getattr(smaller, key) if hasattr(
                smaller, key) else default_uninit

            # still have to compare objects in initial order
            # for things like sub and div. not the most efficient
            # way to do things but whatever.
            if selfIsLarger:
                first = v1
                second = v2
            else:
                first = v2
                second = v1

            kwargs[key] = callback(first, second)

        return VecN(**kwargs)

    def _perform_op(self, callback):
        kwargs = {}

        for key in self._known_keys:
            kwargs[key] = callback(getattr(self, key))

        return VecN(**kwargs)

    def __add__(self, other):
        if not isinstance(other, VecN):
            return self._perform_op(lambda v: v + other)

        return self._perform_vec_op(other, lambda a, b: a + b)

    def __sub__(self, other):
        if not isinstance(other, VecN):
            return self._perform_op(lambda v: v - other)

        return self._perform_vec_op(other, lambda a, b: a - b)

    def __mul_(self, other):
        if not isinstance(other, VecN):
            return self._perform_op(lambda v: v * other)

        return self._perform_vec_op(other, lambda a, b: a * b, 1)

    def __div__(self, other):
        if not isinstance(other, VecN):
            return self._perform_op(other, lambda v: v / other)

        return self._perform_vec_op(other, lambda a, b: a / b, 1)

    def distanceSquared(self):
        dsq = 0

        for key in self._known_keys:
            val = getattr(self, key)

            dsq += val ** 2

        return dsq

    def distance(self):
        return self.distanceSquared() ** 0.5

    def normalize(self):
        magnitude = self.distance()
        return self / magnitude


def twoObjectSort(a, b):
    if len(a) >= len(b):
        return a, b

    return b, a


class Vec2(VecN):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)


# idk if im actually going to use this but I
# already wrote that huge class so it can't all be for nothing
class Vec3(VecN):
    def __init__(self, x, y, z):
        super().__init__(x=x, y=y, z=z)
