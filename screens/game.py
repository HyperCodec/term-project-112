from cmu_graphics import *
from player import Player, MAX_STAMINA, PLAYER_COLLIDER_RADIUS
from engine.camera import Camera
from maze import generateMaze, renderMazeImage, HIDING_SPOT_COLLIDER_RADIUS
from engine.time import TimeManager
from engine.vector import Vec2
from engine.animation import AnimationTicker
from engine.ui import *
from enemy import spawnEnemyRandomly, loseGame

NUM_ENEMIES = 10
DEBUG_SPECTATE_ENEMY = False


class LossMenu(UIElement):
    def __init__(self, app):
        self.is_visible = False
        self.center = Vec2(app.width/2, app.height/2)

        self.size = Vec2(300, 200)

        # probably should make some sort of components API instead
        # of hardcoding each individual component.
        top_left = self.center - self.size/2
        self.background = PersistentRect(
            top_left,
            self.size,
            opacity=50
        )

        self.you_died = PersistentLabel(
            "You died",
            Vec2(self.center.x, self.center.y - self.size.y/3),
            size=22,
            fill='red'
        )

        # back to title button
        btt_size = Vec2(self.size.x * 2/3, self.size.y/4)
        btt_top_left = Vec2(self.center.x - btt_size.x/2,
                            self.center.y + self.size.y/4 - btt_size.y/2)
        btt_rect = PersistentRect(
            btt_top_left,
            btt_size,
        )

        btt_center = btt_top_left + btt_size/2

        btt_label = PersistentLabel(
            "Back to title",
            btt_center,
            size=16,
            fill='white'
        )

        self.back_to_title_btn = BackToTitle(
            btt_label,
            btt_rect,
            'black',
            'crimson'
        )

        # restart game button
        # restart button size is equal to btt_size.
        restart_top_left = Vec2(
            btt_top_left.x, btt_top_left.y - btt_size.y - 20)
        restart_rect = PersistentRect(
            restart_top_left,
            btt_size,
        )

        restart_center = restart_top_left + btt_size/2

        restart_label = PersistentLabel(
            "Restart game",
            restart_center,
            fill='white',
            size=16
        )

        self.restart_btn = RestartGame(
            restart_label,
            restart_rect,
            'black',
            'crimson'
        )

        app.ui_click_manager.register_clickable(self.back_to_title_btn)
        app.ui_click_manager.register_clickable(self.restart_btn)

        app.ui_hover_manager.register_hoverable(self.back_to_title_btn)
        app.ui_hover_manager.register_hoverable(self.restart_btn)

    @property
    def visible(self):
        return self.is_visible

    @visible.setter
    def visible(self, v):
        self.back_to_title_btn.visible = v
        self.restart_btn.visible = v
        self.is_visible = v

    def render(self, app):
        if not self.is_visible:
            return

        self.background.render(app)
        self.you_died.render(app)
        self.restart_btn.render(app)
        self.back_to_title_btn.render(app)


class BackToTitle(SingleRectButton):
    def on_click(self, app):
        setActiveScreen("title")


class RestartGame(SingleRectButton):
    def on_click(self, app):
        resetGame(app)


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

    app.animations.register_animation(app.player.animations)

    app.loss = False
    app.steps = 0
    app.was_sprinting = False
    app.was_moving = False

    app.enemies = []

    for _ in range(NUM_ENEMIES):
        spawnEnemyRandomly(app)

    app.ui_click_manager = ClickableElementManager()
    app.ui_hover_manager = HoverableElementManager()

    app.loss_menu = LossMenu(app)
    app.camera.prm.register_render(app.loss_menu)

    app.player_hiding = False


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

    if app.loss:
        # don't keep changing things about the game on a loss
        return

    app.animations.tick(dt)

    if not app.was_moving:
        if app.player.facing_direction:
            app.player.animations.select_animation("idle_right")
        else:
            app.player.animations.select_animation("idle_left")

    for enemy in app.enemies:
        enemy.move(app)

    app.time.mark_step_end()
    app.was_sprinting = False
    app.was_moving = False

    if DEBUG_SPECTATE_ENEMY:
        app.camera.pos = app.enemies[0].pos


def game_onKeyPress(app, key):
    # testing
    if key == 'm':
        loseGame(app)

    if key == 'f':
        if app.player_hiding:
            app.player_hiding = False
        else:
            for hiding_spot in app.hiding_spots:
                if (hiding_spot - app.player.pos).distanceSquared() <=  \
                        (PLAYER_COLLIDER_RADIUS + HIDING_SPOT_COLLIDER_RADIUS) ** 2:
                    app.player_hiding = True
                    break

    # death screen keybinds
    if not app.loss:
        return

    if key == 'r' or key == 'space':
        resetGame(app)
        return

    if key == 't':
        setActiveScreen('title')


def game_onMouseMove(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_hover_manager.on_mouse_move(app, mouse_pos)


def game_onMousePress(app, mouseX, mouseY):
    mouse_pos = Vec2(mouseX, mouseY)

    app.ui_click_manager.on_mouse_press(app, mouse_pos)


def game_onKeyHold(app, keys):
    if app.loss or app.player_hiding:
        return

    # idk why cmu graphics ever thought it was a
    # good idea to make keys a list, just pressing
    # too many keys can make it really laggy.
    keys = set(keys)

    movement = Vec2(0, 0)

    # idk why, but sometimes holding up prevents
    # counter strafing. there is nothing in the code that could
    # suggest that happening, might just be cmu graphics
    # doing its thing.
    if 'right' in keys:
        app.was_moving = True
        movement.x += 1

    if 'left' in keys:
        app.was_moving = True
        movement.x -= 1

    if 'up' in keys:
        app.was_moving = True
        movement.y -= 1

    if 'down' in keys:
        app.was_moving = True
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
