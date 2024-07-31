from cmu_graphics import *
from engine.camera import Camera
from engine.ui import *
from engine.vector import Vec2


class TitleButton(SingleRectButton):
    def on_click(self, _app):
        setActiveScreen("title")


def win_onScreenActivate(app):
    app.camera = Camera()

    app.ui_click_manager = ClickableElementManager()
    app.ui_hover_manager = HoverableElementManager()

    you_win = PersistentLabel(
        "You Win!",
        Vec2(app.width/2, app.height/2 - 100),
        size=50,
        fill='blue'
    )

    app.camera.prm.register_render(you_win)

    title_label = PersistentLabel(
        "Back to title",
        Vec2(app.width/2, app.height/2),
        size=16,
        fill='white'
    )

    title_rect_size = Vec2(100, 50)
    title_rect = PersistentRect(
        Vec2(app.width/2, app.height/2)-title_rect_size/2,
        title_rect_size,
    )

    title_button = TitleButton(
        title_label,
        title_rect,
        'black',
        'green'
    )

    registerButton(app, title_button)

    app.background = 'white'


def win_onMouseMove(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_hover_manager.on_mouse_move(app, mouse_pos)


def win_onMousePress(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_click_manager.on_mouse_press(app, mouse_pos)


def win_redrawAll(app):
    app.camera.render_persistent(app)
