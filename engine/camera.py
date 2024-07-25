from engine.vector import Vec2

FOLLOW_MARGIN = 50


class Camera:
    def __init__(self, pos=None):
        if pos is None:
            pos = Vec2(0, 0)

        self.pos = pos

    def get_screen_coords(self, pos):
        return pos - self.pos

    def follow_player(self, app):
        player_screen_pos = self.get_screen_coords(app.player.pos)

        if not (player_screen_pos.x <= FOLLOW_MARGIN or player_screen_pos.y <= FOLLOW_MARGIN
                or player_screen_pos.x >= app.width - FOLLOW_MARGIN or player_screen_pos.y >= app.height - FOLLOW_MARGIN):
            return

        amount_to_move = player_screen_pos - Vec2(app.width, app.height)
        self.pos += amount_to_move

    def render_object(self, obj, app, absolute_pos):
        screen_pos = self.get_screen_coords(absolute_pos)
        obj.render(app, screen_pos)

        return screen_pos


class CameraRenderable:
    def render(self, app, screen_pos):
        pass
