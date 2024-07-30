import random
from engine.pathfinding import BFS, getPathFromMappings, PathTweener, calculateBLineMovement, PathfindingEntity
from engine.camera import PersistentRender
from engine.animation import SpriteSheet, AnimationSelection
from maze import getRowColFromCoordinate
from engine.vector import Vec2
from cmu_graphics import drawCircle
from player import PLAYER_COLLIDER_RADIUS

ENEMY_AGGRO_SPEED = 6
ENEMY_WANDER_SPEED = 2
ENEMY_COLLIDER_RADIUS = 30


class BasicEnemy(PersistentRender, PathfindingEntity):
    def __init__(self, pos):
        self.pos = pos
        self.aggro = False
        self.path_tweener = None

        wander_right = SpriteSheet("./assets/enemy-wander.png", 1, 8, 0.1)
        wander_left = SpriteSheet(
            "./assets/enemy-wander.png", 1, 8, 0.1, h_flip=True)

        self.animations = AnimationSelection({
            "wander_right": wander_right,
            "wander_left": wander_left,
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

        self.pos += movement

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

    def has_line_of_sight(self, app):
        # TODO check whether it can directly see the player
        return False

    def move(self, app):
        if self.has_line_of_sight(app):
            self.aggro = True
            self.aggro_chase(app)
            return

        if self.aggro:
            # was previously aggro, TODO set destination to
            # a point past the player.
            pass

        # is not aggro, pathfind to destination
        self.move_toward_destination(app)

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
    while not app.grid[row, col] or (Vec2(row, col) - Vec2(prow, pcol)).distanceSquared() <= 10:
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
