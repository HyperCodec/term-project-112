from engine.vector import Vec2
from engine.camera import PersistentRender
from cmu_graphics import drawCircle
from maze import getRowColFromCoordinate

PLAYER_MOVE_SPEED = 3
PLAYER_COLLIDER_RADIUS = 50
PLAYER_OFFSET_FROM_WALL = 1e-8


class Player(PersistentRender):
    def __init__(self, pos=None, health=100):
        if pos is None:
            pos = Vec2(100, 100)

        self.pos = pos
        self.health = health

    def move(self, app, vec):
        vec *= PLAYER_MOVE_SPEED  # * dt

        self.make_move_safe(app, vec)

        self.pos += vec
        app.camera.follow_player(app, vec)

    def make_move_safe(self, app, vec):
        current_row, current_col = getRowColFromCoordinate(app, self.pos)
        next_pos = self.pos + vec

        # really spaghetti way of handling all this but it works.
        # TODO fix collisions with corners. also breaks on the bottom border
        # with index out of bounds for some reason.
        if next_pos.x < PLAYER_COLLIDER_RADIUS:
            vec.x = -self.pos.x + PLAYER_OFFSET_FROM_WALL + PLAYER_COLLIDER_RADIUS
        elif next_pos.x >= app.cols*app.cell_size - PLAYER_COLLIDER_RADIUS:
            vec.x = app.cols*app.cell_size - PLAYER_COLLIDER_RADIUS - \
                PLAYER_OFFSET_FROM_WALL - self.pos.x
        elif (next_pos.x - PLAYER_COLLIDER_RADIUS) // app.cell_size != current_col:
            left = next_pos.x - PLAYER_COLLIDER_RADIUS
            next_col = left // app.cell_size

            if not app.grid[current_row, next_col]:
                vec.x = next_col*app.cell_size + app.cell_size + PLAYER_COLLIDER_RADIUS + \
                    PLAYER_OFFSET_FROM_WALL - self.pos.x
        elif (next_pos.x + PLAYER_COLLIDER_RADIUS) // app.cell_size != current_col:
            right = next_pos.x + PLAYER_COLLIDER_RADIUS
            next_col = right // app.cell_size

            if not app.grid[current_row, next_col]:
                vec.x = next_col*app.cell_size - PLAYER_COLLIDER_RADIUS - \
                    PLAYER_OFFSET_FROM_WALL - self.pos.x

        if next_pos.y < PLAYER_COLLIDER_RADIUS:
            vec.y = -self.pos.y + PLAYER_OFFSET_FROM_WALL + PLAYER_COLLIDER_RADIUS
        elif next_pos.x >= app.rows*app.cell_size - PLAYER_COLLIDER_RADIUS:
            vec.y = app.rows*app.cell_size - PLAYER_COLLIDER_RADIUS - \
                PLAYER_OFFSET_FROM_WALL - self.pos.y
        elif (next_pos.y - PLAYER_COLLIDER_RADIUS) // app.cell_size != current_row:
            top = next_pos.y - PLAYER_COLLIDER_RADIUS
            next_row = top // app.cell_size

            if not app.grid[next_row, current_col]:
                vec.y = next_row*app.cell_size + app.cell_size + PLAYER_COLLIDER_RADIUS + \
                    PLAYER_OFFSET_FROM_WALL - self.pos.y
        elif (next_pos.y + PLAYER_COLLIDER_RADIUS) // app.cell_size != current_row:
            bottom = next_pos.y + PLAYER_COLLIDER_RADIUS
            next_row = bottom // app.cell_size

            if not app.grid[next_row, current_col]:
                vec.y = next_row*app.cell_size - PLAYER_COLLIDER_RADIUS - \
                    PLAYER_OFFSET_FROM_WALL - self.pos.y

    def render(self, app):
        screen_pos = app.camera.get_screen_coords(app, self.pos)

        drawCircle(screen_pos.x.item(), screen_pos.y.item(),
                   PLAYER_COLLIDER_RADIUS)
