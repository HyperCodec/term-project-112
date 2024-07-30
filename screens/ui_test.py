from cmu_graphics import *
from engine.ui import *
from engine.camera import Camera
from engine.vector import Vec2


def ui_test_onAppStart(app):
    app.camera = Camera()
    app.ui_click_manager = ClickableElementManager()
    app.ui_hover_manager = HoverableElementManager()

    text = PersistentLabel("click me!", Vec2(200, 200))
    background = PersistentRect(Vec2(100, 100), Vec2(200, 200), fill='red')
    button = SingleRectButton(text, background, 'red', 'green')

    # bad way of doing stuff but too lazy to write class rn
    setattr(button, "on_click", on_click)

    registerButton(app, button)


def ui_test_onMousePress(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_click_manager.on_mouse_press(app, mouse_pos)


def ui_test_onMouseMove(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_hover_manager.on_mouse_move(app, mouse_pos)


def ui_test_redrawAll(app):
    app.camera.render_frame(app)


def on_click(_):
    print("hello world")
