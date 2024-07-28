from engine.vector import Vec2
from engine.camera import PersistentRender
from cmu_graphics import drawCircle

PLAYER_MOVE_SPEED = 3


class Player(PersistentRender):
    def __init__(self, pos=None, health=100):
        if pos is None:
            pos = Vec2(100, 100)

        self.pos = pos
        self.health = health

    def move(self, app, vec):
        vec *= PLAYER_MOVE_SPEED  # * dt

        if not self.is_position_safe(app, vec):
            return

        self.pos += vec
        app.camera.follow_player(app, vec)

    def is_position_safe(self, app, vec):
        current_spot = self.pos // app.cell_size
        next_spot = (self.pos + vec) // app.cell_size

        # no need to check anything else,
        # spots are equal.
        if current_spot == next_spot:
            return True

        # outer boundaries
        if (next_spot.x < 0 or next_spot.y < 0 or
                next_spot.x >= app.cols or next_spot.y >= app.rows):
            return False

        cell = app.grid[next_spot.y, next_spot.x]

        return bool(cell)

    def render(self, app):
        screen_pos = app.camera.get_screen_coords(app, self.pos)

        drawCircle(screen_pos.x.item(), screen_pos.y.item(), 60)

        drawCircle(screen_pos.x.item(), screen_pos.y.item(), 60)
