from engine.vector import Vec2

PLAYER_MOVE_SPEED = 10


class Player:
    def __init__(self, pos=None, health=100):
        if pos is None:
            pos = Vec2(0, 0)

        self.pos = pos
        self.health = health

    def move(self, app, vec, dt):
        self.pos += vec * PLAYER_MOVE_SPEED * dt
        app.camera.follow_player(app)
