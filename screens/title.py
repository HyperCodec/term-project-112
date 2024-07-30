from cmu_graphics import *
from engine.ui import *
from engine.camera import Camera
from engine.vector import Vec2
from PIL import Image


class StartButton(SingleRectButton):
    def on_click(self, _app):
        setActiveScreen("game")


def title_onScreenActivate(app):
    app.background = 'gray'
    app.ui_click_manager = ClickableElementManager()
    app.ui_hover_manager = HoverableElementManager()
    app.camera = Camera()

    title_center = Vec2(app.width/2, app.height/2 - 100)
    title_size = Vec2(392, 68)  # taken from image properties
    title_top_left = title_center - title_size/2

    image = Image.open("./assets/title.png")

    title_image = PersistentImage(
        CMUImage(image),
        title_top_left
    )

    app.camera.prm.register_render(title_image)

    start_size = Vec2(200, 50)
    start_top_left = Vec2(title_center.x - start_size.x/2,
                          title_center.y + title_size.y/2 + 35)
    start_center = start_top_left + start_size/2

    start_label = PersistentLabel(
        "Start game",
        start_center,
        size=16,
        fill='white'
    )

    start_rect = PersistentRect(
        start_top_left,
        start_size,
        fill='black'
    )

    start_btn = StartButton(
        start_label,
        start_rect,
        'black',
        'green'
    )

    registerButton(app, start_btn)


def title_onKeyPress(app, key):
    if key == 'enter' or key == 'space':
        setActiveScreen("game")


def title_onMouseMove(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_hover_manager.on_mouse_move(app, mouse_pos)


def title_onMousePress(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_click_manager.on_mouse_press(app, mouse_pos)


def title_redrawAll(app):
    app.camera.render_persistent(app)
