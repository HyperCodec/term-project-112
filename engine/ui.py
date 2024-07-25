from cmu_graphics import drawRect, drawLabel
from engine.camera import CameraRenderable, PersistentRender
from engine.collider import Collider, RectCollider


class UIElement:
    def __init__(self, pos, renderable, visible=True):
        self.pos = pos
        self.renderable = renderable
        self.visible = visible

    def render(self, app):
        if not self.visible:
            return

        screen_pos = app.camera.get_screen_coords(self.pos)

        self.renderable.render(app, screen_pos)


class ClickableElementManager:
    def __init__(self):
        self.clickables = []

    def register_clickable(self, clickable):
        self.clickables.append(clickable)

    def on_mouse_press(self, mouse_pos):
        for clickable in self.clickables:
            if clickable.collider.is_point_colliding(mouse_pos):
                clickable.on_click()


class HoverableElementManager:
    def __init__(self):
        self.hoverables = []

    def register_hoverable(self, hoverable):
        self.hoverables.append(hoverable)

    def on_mouse_move(self, mouse_pos):
        for hoverable in self.hoverables:
            if hoverable.collider.is_point_colliding(mouse_pos):
                hoverable.on_hover()

                if not hoverable.is_hovered:
                    hoverable.on_start_hover()

                hoverable.is_hovered = True
                continue

            if hoverable.is_hovered:
                hoverable.on_stop_hover()

            hoverable.is_hovered = False


class Clickable:
    def __init__(self, collider):
        self.collider = collider

    def on_click(self):
        pass


class Hoverable:
    def __init__(self, collider):
        self.collider = collider
        self.is_hovered = False

    def on_hover(self):
        pass

    def on_start_hover(self):
        pass

    def on_stop_hover(self):
        pass


class PersistentRect(RectCollider, PersistentRender):
    def __init__(self, top_left, shape, **kwargs):
        # collider init
        super().__init__(top_left, shape)

        self.kwargs = kwargs

    def render(self, app):
        drawRect(self.top_left.x, self.top_left.y,
                 self.shape.x, self.shape.y, **self.kwargs)


class PersistentLabel(PersistentRender):
    def __init__(self, text, pos, **kwargs):
        super().__init__(pos)

        self.text = text
        self.kwargs = kwargs

    def render(self, app):
        drawLabel(self.text, self.pos.x, self.pos.y, **self.kwargs)


# TODO probably rename these because they would
# work with non-rect persistents too.
class SingleRectButton(Hoverable, Clickable, PersistentRender):
    def __init__(self, label, prect, normal_fill, hovered_fill):
        super().__init__(prect)
        self.normal_fill = normal_fill
        self.hovered_fill = hovered_fill
        self.label = label

    def on_start_hover(self):
        self.collider.kwargs["fill"] = self.hovered_fill

    def on_stop_hover(self):
        self.collider.kwargs["fill"] = self.normal_fill

    def render(self, app):
        self.collider.render(app)
        self.label.render(app)


class DoubleRectButton(Hoverable, Clickable, PersistentRender):
    def __init__(self, label, normal_prect, hovered_prect):
        super().__init__(normal_prect)
        self.normal_prect = normal_prect
        self.hovered_prect = hovered_prect
        self.label = label

    def on_start_hover(self):
        self.collider = self.hovered_prect

    def on_stop_hover(self):
        self.collider = self.normal_prect

    def render(self, app):
        self.collider.render(app)
        self.label.render(app)
