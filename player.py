from engine.vector import Vec2
from engine.camera import PersistentRender
from cmu_graphics import drawCircle

PLAYER_MOVE_SPEED = 3


class Player(PersistentRender):
    def __init__(self, pos=None, health=100):
        if pos is None:
            pos = Vec2(0, 0)

        self.pos = pos
        self.health = health

    def move(self, app, vec):
        vec = vec * PLAYER_MOVE_SPEED  # * dt
        self.pos += vec
        app.camera.follow_player(app)

    def render(self, app):
        screen_pos = app.camera.get_screen_coords(self.pos)

        drawCircle(screen_pos.x.item(), screen_pos.y.item(), 60)
