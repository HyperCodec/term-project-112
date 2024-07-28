from cmu_graphics import *
from player import Player
from engine.camera import Camera
from maze import generateMaze, renderMazeImage
from engine.time import TimeManager
from engine.vector import Vec2
from engine.animation import AnimationTicker


def resetGame(app):
    print("Generating maze")
    generateMaze(app)
    print("Finished generating maze")
    renderMazeImage(app)

    app.player = Player()
    app.camera = Camera()

    app.camera.prm.register_render(app.player)

    app.time = TimeManager()
    app.animations = AnimationTicker()

    registerAnimations(app)

    app.loss = False


def registerAnimations(app):
    pass


def game_onAppStart(app):
    # app.stepsPerSecond = 60

    app.rows = 25
    app.cols = 25
    app.cell_size = 200
    app.background = 'black'

    resetGame(app)


def game_onStep(app):
    dt = app.time.delta_seconds()
    # print(f"frametime: {dt}")

    # animations and such
    app.animations.tick(dt)

    if app.loss:
        # don't keep changing things about the game on a loss
        return

    # TODO game logic (enemies and such)

    app.time.mark_step_end()


def game_onKeyPress(app, key):
    # death screen keybinds
    if not app.loss:
        return

    if key == 'r':
        resetGame(app)
        return


def game_onKeyHold(app, keys):
    movement = Vec2(0, 0)

    if 'right' in keys:
        movement.x += 1

    if 'left' in keys:
        movement.x -= 1

    if 'up' in keys:
        movement.y -= 1

    if 'down' in keys:
        movement.y += 1

    if movement.is_zero():
        return

    app.player.move(app, movement)


def game_redrawAll(app):
    # takes a long time to render a frame.
    # not sure exactly why other than maybe maze
    # or CMU renderer itself when objects are drawn.
    app.camera.render_frame(app)
