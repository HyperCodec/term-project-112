import numpy as np
from engine.vector import Vec2
from engine.camera import PersistentRender
from cmu_graphics import drawCircle, setActiveScreen
from maze import getRowColFromCoordinate

PLAYER_MOVE_SPEED = 3
PLAYER_COLLIDER_RADIUS = 30
PLAYER_OFFSET_FROM_WALL = 1e-8
MAX_STAMINA = 100


class Player(PersistentRender):
    def __init__(self, pos=None, health=100):
        if pos is None:
            pos = Vec2(100, 100)

        self.pos = pos
        self.health = health
        self.stamina = MAX_STAMINA

    def move(self, app, vec):
        vec *= PLAYER_MOVE_SPEED  # * dt

        self.make_move_safe(app, vec)

        self.pos += vec
        app.camera.follow_player(app, vec)

        if getRowColFromCoordinate(app, self.pos) == (app.rows-1, app.cols-1):
            setActiveScreen("win")

    def make_move_safe(self, app, vec):
        current_row, current_col = getRowColFromCoordinate(app, self.pos)
        next_pos = self.pos + vec

        # really spaghetti way of handling all this but it works.
        # TODO fix collisions with corners.
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
        elif next_pos.y >= app.rows*app.cell_size - PLAYER_COLLIDER_RADIUS:
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

        if vec.is_zero():
            # prevents a nasty NaN bug
            return

        self.look_for_diagonal_collisions(app, vec)

    def look_for_diagonal_collisions(self, app, vec):
        for delta in [Vec2(1, 1), Vec2(-1, 1), Vec2(1, -1), Vec2(-1, -1)]:
            next_pos = self.pos + vec + delta*PLAYER_COLLIDER_RADIUS
            next_cell = next_pos // app.cell_size

            if next_cell == self.pos // app.cell_size:
                continue

            self.check_corner_collisions(app, vec, next_cell)

    def check_corner_collisions(self, app, vec, next_cell):
        corners = getCornersOfCell(app, next_cell.y, next_cell.x)
        for corner in corners:
            if (self.pos - corner).distanceSquared() < PLAYER_COLLIDER_RADIUS ** 2:
                self.fix_corner_collision(app, vec, corner)
                return

    def fix_corner_collision(self, app, vec, corner):
        # direction from the corner to the player
        corner_relative_direction = (self.pos - corner).normalize()

        # get the point closest to the corner without
        # touching that is along the player's movement axis

        # for some reason without the extra boost, the move
        # doesn't guarantee to put the player a full 50 units away,
        # causing them to be constantly locked in position. I assume
        # it's because normalization magnitude is 0.9... instead of 1
        # due to floating point precision.
        # the bump looks bad and buggy but I can't see a fix to this problem,
        # I'd rather have it look buggy than have a chance of softlocking the
        # player whenever they hit a corner.
        target_pos = corner + corner_relative_direction * \
            (PLAYER_COLLIDER_RADIUS + PLAYER_OFFSET_FROM_WALL + 1.15)

        ideal_move = (target_pos - self.pos)

        # TODO probably some sort of mutating
        # function for this stuff
        vec.x = ideal_move.x
        vec.y = ideal_move.y

    def render(self, app):
        screen_pos = app.camera.get_screen_coords(app, self.pos)

        drawCircle(screen_pos.x.item(), screen_pos.y.item(),
                   PLAYER_COLLIDER_RADIUS)


def getCornersOfCell(app, row, col):
    return [Vec2(col, row)*app.cell_size, Vec2(col+1, row)*app.cell_size, Vec2(col, row+1)*app.cell_size, Vec2(col+1, row+1)*app.cell_size]
