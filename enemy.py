import random
import copy
from engine.pathfinding import BFS, getPathFromMappings, PathTweener, calculateBLineMovement, PathfindingEntity
from engine.camera import PersistentRender
from engine.animation import SpriteSheet, AnimationSelection
from maze import getRowColFromCoordinate
from engine.vector import Vec2
from cmu_graphics import drawCircle
from player import PLAYER_COLLIDER_RADIUS, PLAYER_OFFSET_FROM_WALL

ENEMY_AGGRO_SPEED = 5
ENEMY_WANDER_SPEED = 2
ENEMY_COLLIDER_RADIUS = 20
ENEMY_AGGRO_RANGE = 300


class BasicEnemy(PersistentRender, PathfindingEntity):
    def __init__(self, pos):
        self.pos = pos
        self.aggro = False
        self.path_tweener = None

        wander_right = SpriteSheet("./assets/enemy-wander.png", 1, 8, 0.1)
        wander_left = SpriteSheet(
            "./assets/enemy-wander.png", 1, 8, 0.1, h_flip=True)

        chase_right = copy.deepcopy(wander_right)
        chase_right.frametime = 0.01

        chase_left = copy.deepcopy(wander_left)
        chase_left.frametime = 0.01

        self.animations = AnimationSelection({
            "wander_right": wander_right,
            "wander_left": wander_left,
            "chase_right": chase_right,
            "chase_left": chase_left
        }, "wander_right")

    def select_new_wandering_point(self, app):
        source = getRowColFromCoordinate(app, self.pos)
        target = (random.randrange(app.rows), random.randrange(app.cols))

        while not app.grid[target[0], target[1]] or target == source:
            target = (random.randrange(app.rows), random.randrange(app.cols))

        direction_mappings = BFS(
            app, source, target)

        path = getPathFromMappings(
            direction_mappings, source, target)

        self.path_tweener = PathTweener(path)

    def aggro_chase(self, app):
        target = app.player.pos

        movement = calculateBLineMovement(self.pos, target, ENEMY_AGGRO_SPEED)

        self.aggro_avoid_walls(app, movement)
        self.pos += movement

        if movement.x > 0:
            self.animations.select_animation("chase_right")
        elif movement.x < 0:
            self.animations.select_animation("chase_left")

    def aggro_avoid_walls(self, app, vec):
        self.wallbump(app, vec)

        # TODO probably some continuous space pathfinding

    def wallbump(self, app, vec):
        next_pos = self.pos + vec

        cur_row, cur_col = getRowColFromCoordinate(app, self.pos)

        erow, ecol = getRowColFromCoordinate(
            app, Vec2(next_pos.x + ENEMY_COLLIDER_RADIUS, next_pos.y))
        wrow, wcol = getRowColFromCoordinate(
            app, Vec2(next_pos.x - ENEMY_COLLIDER_RADIUS, next_pos.y))

        if not app.grid[int(erow), int(ecol)]:
            target = cur_col*app.cell_size + app.cell_size - \
                ENEMY_COLLIDER_RADIUS - PLAYER_OFFSET_FROM_WALL
            ideal_move = target - self.pos.x
            vec.x = ideal_move

        elif not app.grid[int(wrow), int(wcol)]:
            target = cur_col*app.cell_size + ENEMY_COLLIDER_RADIUS + PLAYER_OFFSET_FROM_WALL
            ideal_move = target - self.pos.x
            vec.x = ideal_move

        nrow, ncol = getRowColFromCoordinate(
            app, Vec2(next_pos.x, next_pos.y - ENEMY_COLLIDER_RADIUS))
        srow, scol = getRowColFromCoordinate(
            app, Vec2(next_pos.x, next_pos.y + ENEMY_COLLIDER_RADIUS))

        if not app.grid[int(nrow), int(ncol)]:
            target = cur_row*app.cell_size + ENEMY_COLLIDER_RADIUS + PLAYER_OFFSET_FROM_WALL
            ideal_move = target - self.pos.y
            vec.y = ideal_move

        elif not app.grid[int(srow), int(scol)]:
            target = cur_row*app.cell_size + app.cell_size - \
                ENEMY_COLLIDER_RADIUS - PLAYER_OFFSET_FROM_WALL
            ideal_move = target - self.pos.y
            vec.y = ideal_move

    def move_toward_destination(self, app):
        completed, (drow, dcol) = self.path_tweener.move_toward_target(
            app, ENEMY_WANDER_SPEED, self)

        if dcol > 0:
            self.animations.select_animation("wander_right")
        elif dcol < 0:
            self.animations.select_animation("wander_left")

        if completed:
            # destination reached, wander to another random point.
            self.select_new_wandering_point(app)

    def move(self, app):
        if hasLineOfSight(app, self.pos, app.player.pos):
            self.aggro = True
            self.aggro_chase(app)

            if not self.aggro:
                # TODO play some angry noise
                pass
        else:
            # is not aggro, pathfind to destination
            self.move_toward_destination(app)

            if self.aggro:
                self.aggro = False

                # was going to make it just run past
                # the hiding spot but this works fine anyways.
                self.select_new_wandering_point(app)

        if (app.player.pos - self.pos).distanceSquared() <= \
                (ENEMY_COLLIDER_RADIUS + PLAYER_COLLIDER_RADIUS) ** 2:
            loseGame(app)

    def is_fully_in_cell(self, app, row, col):
        center_rowcol = getRowColFromCoordinate(app, self.pos)

        if center_rowcol != (row, col):
            return False

        for delta in [Vec2(1, 0), Vec2(0, 1), Vec2(-1, 0), Vec2(0, -1)]:
            offset_pos = self.pos + delta*ENEMY_COLLIDER_RADIUS
            offset_rowcol = getRowColFromCoordinate(app, offset_pos)

            if offset_rowcol != (row, col):
                return False

        return True

    def render(self, app):
        screen_pos = app.camera.get_screen_coords(app, self.pos)

        self.animations.render(app, screen_pos)


def spawnEnemyRandomly(app):
    row, col = random.randrange(app.rows), random.randrange(app.cols)

    prow, pcol = getRowColFromCoordinate(app, app.player.pos)

    # cannot spawn on an empty cell or within 10 cells of the player.
    while not app.grid[row, col] or (Vec2(row, col) - Vec2(prow, pcol)).distanceSquared() <= 5:
        row, col = random.randrange(app.rows), random.randrange(app.cols)

    actual_pos = Vec2(col*app.cell_size + (app.cell_size/2),
                      row*app.cell_size + (app.cell_size/2))

    enemy = BasicEnemy(actual_pos)
    enemy.select_new_wandering_point(app)

    app.enemies.append(enemy)
    app.camera.prm.register_render(enemy)
    app.animations.register_animation(enemy.animations)


def loseGame(app):
    app.loss = True
    app.loss_menu.visible = True


# based on Bresenham's algorithm
def hasLineOfSight(app, source, target):
    if app.player_hiding or (target - source).distanceSquared() > ENEMY_AGGRO_RANGE ** 2:
        return False

    direction = (target - source).normalize()
    step = direction * app.cell_size

    current_pos = source

    while (target - current_pos).distanceSquared() > app.cell_size ** 2:
        row, col = getRowColFromCoordinate(app, current_pos)

        # no idea why sometimes it doesn't return an int,
        # floor division is weird.
        if not app.grid[int(row), int(col)]:
            return False

        current_pos += step

    return True
