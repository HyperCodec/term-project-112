from cmu_graphics import drawRect, drawLabel, drawImage
from engine.camera import CameraRenderable, PersistentRender
from engine.collider import Collider, RectCollider


class UIElement(PersistentRender):
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

    def on_mouse_press(self, app, mouse_pos):
        for clickable in self.clickables:
            if clickable.collider.is_point_colliding(mouse_pos):
                clickable.on_click(app)


class HoverableElementManager:
    def __init__(self):
        self.hoverables = []

    def register_hoverable(self, hoverable):
        self.hoverables.append(hoverable)

    def on_mouse_move(self, app, mouse_pos):
        for hoverable in self.hoverables:
            if hoverable.collider.is_point_colliding(mouse_pos):
                hoverable.on_hover(app)

                if not hoverable.is_hovered:
                    hoverable.on_start_hover(app)

                hoverable.is_hovered = True
                continue

            if hoverable.is_hovered:
                hoverable.on_stop_hover(app)

            hoverable.is_hovered = False


class Clickable:
    def __init__(self, collider):
        self.collider = collider

    def on_click(self, app):
        pass


class Hoverable:
    def __init__(self, collider):
        self.collider = collider
        self.is_hovered = False

    def on_hover(self, app):
        pass

    def on_start_hover(self, app):
        pass

    def on_stop_hover(self, app):
        pass


class PersistentRect(RectCollider, PersistentRender):
    def __init__(self, top_left, shape, **kwargs):
        # collider init
        super().__init__(top_left, shape)

        self.kwargs = kwargs

    def render(self, app):
        drawRect(self.top_left.x.item(), self.top_left.y.item(),
                 self.shape.x.item(), self.shape.y.item(), **self.kwargs)


class PersistentLabel(PersistentRender):
    def __init__(self, text, pos, **kwargs):
        self.pos = pos

        self.text = text
        self.kwargs = kwargs

    def render(self, app):
        drawLabel(self.text, self.pos.x.item(),
                  self.pos.y.item(), **self.kwargs)


class PersistentImage(PersistentRender):
    def __init__(self, image, pos, **kwargs):
        self.pos = pos

        self.image = image
        self.kwargs = kwargs

    def render(self, app):
        drawImage(self.pos.x.item(), self.pos.y.item(), **self.kwargs)


# TODO probably rename these because they would
# work with non-rect persistents too.
class SingleRectButton(Hoverable, Clickable, UIElement):
    def __init__(self, label, prect, normal_fill, hovered_fill):
        super().__init__(prect)
        self.normal_fill = normal_fill
        self.hovered_fill = hovered_fill
        self.label = label
        self.visible = True

    def on_start_hover(self, _app):
        self.collider.kwargs["fill"] = self.hovered_fill

    def on_stop_hover(self, _app):
        self.collider.kwargs["fill"] = self.normal_fill

    def render(self, app):
        if not self.visible:
            return

        self.collider.render(app)
        self.label.render(app)


class DoubleRectButton(Hoverable, Clickable, UIElement):
    def __init__(self, label, normal_prect, hovered_prect):
        super().__init__(normal_prect)
        self.normal_prect = normal_prect
        self.hovered_prect = hovered_prect
        self.label = label
        self.visible = True

    def on_start_hover(self, _app):
        self.collider = self.hovered_prect

    def on_stop_hover(self, _app):
        self.collider = self.normal_prect

    def render(self, app):
        if not self.visible:
            return

        self.collider.render(app)
        self.label.render(app)


class PercentageBar(UIElement):
    def __init__(self, pos, max_width, height, inner_kwargs, outer_kwargs, starting_percentage=0):
        self.percentage = starting_percentage
        self.max_width = max_width
        self.height = height
        self.pos = pos
        self.inner_kwargs = inner_kwargs
        self.outer_kwargs = outer_kwargs
        self.outer_kwargs['border'] = self.outer_kwargs.get('border', 'black')

    def render(self, app):
        # inner
        drawRect(self.pos.x.item(), self.pos.y.item(), max(
            self.percentage * self.max_width, 1), self.height, **self.inner_kwargs)

        # outer
        drawRect(self.pos.x.item(), self.pos.y.item(), self.max_width,
                 self.height, fill=None, **self.outer_kwargs)


def registerButton(app, button):
    app.ui_click_manager.register_clickable(button)
    app.ui_hover_manager.register_hoverable(button)
    app.camera.prm.register_render(button)
