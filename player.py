from engine.vector import Vec2
from engine.camera import PersistentRender
from cmu_graphics import drawCircle

PLAYER_MOVE_SPEED = 50


class Player(PersistentRender):
    def __init__(self, pos=None, health=100):
        if pos is None:
            pos = Vec2(0, 0)

        self.pos = pos
        self.health = health

    def move(self, app, vec, dt):
        self.pos += vec * PLAYER_MOVE_SPEED * dt
        # app.camera.follow_player(app)

    def render(self, app):
        screen_pos = app.camera.get_screen_coords(self.pos)

        drawCircle(screen_pos.x, screen_pos.y, 60)
