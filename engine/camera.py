from engine.vector import Vec2

FOLLOW_MARGIN = 50


class Camera:
    def __init__(self, pos=None):
        if pos is None:
            pos = Vec2(0, 0)

        self.pos = pos

    def get_screen_coords(self, pos):
        return pos - self.pos

    def get_full_coords_from_screen(self, screen_pos):
        return screen_pos + self.pos

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

    # draws a vector from the near grid corners
    # to the edge of the screen, then draws a black
    # polygon to obscure that part of the maze.
    def trace_polygon_view_boundaries(self, app):
        pass

    def render_grid_around_player(self, app):
        pass

    def render_player(self, app):
        pass

    def render_enemies(self, app):
        pass

    def render_frame(self, app):
        self.render_player(app)
        self.render_enemies(app)

        self.render_grid_around_player(app)

        self.trace_polygon_view_boundaries(app)


class CameraRenderable:
    def render(self, app, screen_pos):
        pass
