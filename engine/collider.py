class Collider:
    def is_point_colliding(self, point):
        pass


class RectCollider(Collider):
    def __init__(self, top_left, shape):
        self.top_left = top_left
        self.shape = shape

    def is_point_colliding(self, point):
        bottom_right = self.top_left + self.shape

        return (point.x >= self.top_left.x and point.x <= bottom_right.x and
                point.y >= self.top_left.y and point.y <= bottom_right.y)


class CircleCollider(Collider):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def is_point_colliding(self, point):
        distSq = (self.center - point).distanceSquared()
        return distSq <= self.radius ** 2
