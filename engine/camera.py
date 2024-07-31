from engine.vector import Vec2
from cmu_graphics import drawRect, drawImage, drawPolygon

PLAYER_FOLLOW_MARGIN = 200


class Camera:
    def __init__(self, pos=None):
        if pos is None:
            pos = Vec2(100, 100)

        self.pos = pos
        self.prm = PersistentRenderManager()

    def get_screen_coords(self, app, pos):
        return pos - self.pos + Vec2(app.width, app.height)/2

    def get_full_coords_from_screen(self, app, screen_pos):
        return screen_pos + self.pos - Vec2(app.width, app.height)/2

    def follow_player(self, app, moved):
        player_screen_pos = self.get_screen_coords(app, app.player.pos)

        if (player_screen_pos.x <= PLAYER_FOLLOW_MARGIN or
                player_screen_pos.x >= app.width - PLAYER_FOLLOW_MARGIN):
            self.pos.x += moved.x

        if (player_screen_pos.y <= PLAYER_FOLLOW_MARGIN or
                player_screen_pos.y >= app.height - PLAYER_FOLLOW_MARGIN):
            self.pos.y += moved.y

    def render_object(self, app, obj, absolute_pos):
        screen_pos = self.get_screen_coords(app, absolute_pos)
        obj.render(app, screen_pos)

        return screen_pos

    # draws a black polygon to obscure the maze where it
    # would not be visible if it were first-person.
    def trace_polygon_view_boundaries(self, app):
        pass

    def draw_view_boundary(self, app, corner):
        player_screen_pos = self.get_screen_coords(app, app.player.pos)
        screen_edge = 0 if corner.x < player_screen_pos.x else app.width
        remaining_screen_width = screen_edge - player_screen_pos.x

        direction = (corner - player_screen_pos).normalize()

        # make a vector of width `remaining_screen_width` with the same slope
        # as the vector from player to corner. this is then added to the
        # player's location to get the endpoint of the vector, which is the
        # next point of the triangle that is being drawn.
        multiplier = remaining_screen_width / direction.x
        edge_translation = direction * multiplier

        second_point = player_screen_pos + edge_translation

        # third point will essentially make it a right triangle by being
        # either at the top or bottom of the screen at the corner's x position.
        third_point_y = 0 if corner.y < player_screen_pos.y else app.height
        third_point = Vec2(corner.x, third_point_y)

        drawPolygon(corner.x.item(), corner.y.item(),
                    second_point.x.item(), second_point.y.item(),
                    third_point.x.item(), third_point.y.item())

    def render_grid_around_player(self, app):
        screen_pos = self.get_screen_coords(app, Vec2(0, 0))

        app.maze_render.render(app, screen_pos)

    def render_persistent(self, app):
        self.prm.render(app)

    def render_frame(self, app):
        # renders the actual maze
        self.render_grid_around_player(app)

        # view obstruction polygons
        self.trace_polygon_view_boundaries(app)

        # persistent entities (such as UI) drawn on top.
        self.render_persistent(app)


class CameraRenderable:
    def render(self, app, screen_pos):
        pass


# probably doesn't belong here,
# should change to a separate file
# that makes these rendereable classes.
class RenderableImage(CameraRenderable):
    def __init__(self, image, **kwargs):
        self.image = image
        self.kwargs = kwargs

    def render(self, app, screen_pos):
        drawImage(self.image, screen_pos.x.item(),
                  screen_pos.y.item(), **self.kwargs)


# a renderable object that retains its position
# and doesn't care what the surrounding conditions
# are (such as camera position). not all of them
# need to be in `PersistentRenderManager`, such as
# ones that compose larger persistent renders.
class PersistentRender:
    def __init__(self, pos, renderable):
        self.pos = pos
        self.renderable = renderable

    def render(self, app):
        self.renderable.render(app, self.pos)


class PersistentRenderManager:
    def __init__(self):
        self.persistent_renders = []

    def register_render(self, obj):
        self.persistent_renders.append(obj)

    def render(self, app):
        for prend in self.persistent_renders:
            prend.render(app)
