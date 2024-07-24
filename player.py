from engine.vector import Vec2


class Player:
    def __init__(self, pos=None, health=100):
        if pos is None:
            pos = Vec2(0, 0)

        self.pos = pos
        self.health = health

    def move(self, app, vec):
        self.pos += vec
        app.camera.follow_player(app)
