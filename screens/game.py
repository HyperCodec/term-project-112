from cmu_graphics import *
from player import Player, MAX_STAMINA
from engine.camera import Camera
from maze import generateMaze, renderMazeImage
from engine.time import TimeManager
from engine.vector import Vec2
from engine.animation import AnimationTicker
from engine.ui import *
from enemy import spawnEnemyRandomly

NUM_ENEMIES = 1
DEBUG_SPECTATE_ENEMY = False


def resetGame(app):
    print("Generating maze")
    generateMaze(app)
    print("Finished generating maze")
    renderMazeImage(app)

    app.player = Player()
    app.stamina_bar = PercentageBar(
        Vec2(app.width-160, app.height-50), 150, 25, {'fill': 'skyBlue'},
        {'border': 'dodgerBlue'}, 1)

    stamina_label = PersistentLabel(
        "Stamina", Vec2(app.width-95, app.height-60), fill='skyBlue')

    app.camera = Camera()

    app.camera.prm.register_render(app.player)
    app.camera.prm.register_render(app.stamina_bar)
    app.camera.prm.register_render(stamina_label)

    app.time = TimeManager()
    app.animations = AnimationTicker()

    registerAnimations(app)

    app.loss = False
    app.steps = 0
    app.was_sprinting = False

    app.enemies = []

    for _ in range(NUM_ENEMIES):
        spawnEnemyRandomly(app)


def registerAnimations(app):
    pass


def game_onScreenActivate(app):
    # app.stepsPerSecond = 60

    app.rows = 25
    app.cols = 25
    app.cell_size = 200
    app.background = 'black'

    resetGame(app)


def game_onStep(app):
    dt = app.time.delta_seconds()
    # print(f"frametime: {dt}")

    app.steps += 1

    if not app.was_sprinting and app.steps % 3 == 0:
        app.player.stamina = min(app.player.stamina + 1, MAX_STAMINA)

    app.stamina_bar.percentage = app.player.stamina / MAX_STAMINA

    # animations and such
    app.animations.tick(dt)

    if app.loss:
        # don't keep changing things about the game on a loss
        return

    for enemy in app.enemies:
        enemy.move(app)

    app.time.mark_step_end()
    app.was_sprinting = False

    if DEBUG_SPECTATE_ENEMY:
        app.camera.pos = app.enemies[0].pos


def game_onKeyPress(app, key):
    # death screen keybinds
    if not app.loss:
        return

    if key == 'r':
        resetGame(app)
        return


def game_onKeyHold(app, keys):
    # idk why cmu graphics ever thought it was a
    # good idea to make keys a list, just pressing
    # too many keys can make it really laggy.
    keys = set(keys)

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

    if 'z' in keys:
        app.was_sprinting = True
        if app.player.stamina >= 2:
            movement *= 2
            app.player.stamina -= 2

    app.player.move(app, movement)


def game_redrawAll(app):
    # takes a long time to render a frame.
    # not sure exactly why other than maybe maze
    # or CMU renderer itself when objects are drawn.
    app.camera.render_frame(app)
