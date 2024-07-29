import random
from engine.pathfinding import BFS, getPathFromMappings, PathTweener, calculateBLineMovement
from engine.camera import PersistentRender
from maze import getRowColFromCoordinate

ENEMY_AGGRO_SPEED = 6
ENEMY_WANDER_SPEED = 2


class BasicEnemy(PersistentRender):
    def __init__(self, pos):
        self.pos = pos
        self.aggro = False
        self.path_tweener = None
        self.animation = None  # TODO

    def select_new_wandering_point(self, app):
        target = (random.randrange(app.rows), random.randrange(app.cols))

        direction_mappings, distance_mappings = BFS(
            app, getRowColFromCoordinate(app, self.pos), target)

        path = getPathFromMappings(
            direction_mappings, distance_mappings, target)

        self.path_tweener = PathTweener(path)

    def aggro_chase(self, app):
        target = app.player.pos

        movement = calculateBLineMovement(self.pos, target, ENEMY_AGGRO_SPEED)

        self.pos += movement

    def move_toward_destination(self, app):
        completed = self.path_tweener.move_toward_target(
            app, ENEMY_WANDER_SPEED, self)

        if completed:
            # destination reached, wander to another random point.
            self.select_new_wandering_point(app)

    def has_line_of_sight(self, app):
        # TODO check whether it can directly see the player
        pass

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
