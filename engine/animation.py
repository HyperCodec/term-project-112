from PIL import Image
from engine.camera import CameraRenderable
from cmu_graphics import drawImage, CMUImage


class Animation(CameraRenderable):
    def __init__(self, frames, frametime, start=0):
        self.frames = frames
        self.cur_frame = start
        self.frametime = frametime
        self.remaining_frametime = frametime

    def _step_frame(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)

    def tick(self, dt):
        self.remaining_frametime -= dt

        if self.remaining_frametime <= 0:
            self._step_frame()
            self.remaining_frametime = self.frametime

    def render(self, app, screen_pos):
        frame = self.frames[self.cur_frame]

        drawImage(frame, screen_pos.x, screen_pos.y, align='center')


class Gif(Animation):
    def __init__(self, path, frametime, start=0):
        frames = []

        gif_raw = Image.open(path)

        for frame in range(gif_raw.n_frames):
            gif_raw.seek(frame)

            frames.append(CMUImage(gif_raw))

        super().__init__(frames, frametime, start)


class SpriteSheet(Animation):
    def __init__(self, path, rows, cols, frametime, start=0):
        frames = []

        sheet_raw = Image.open(path)

        frame_width = sheet_raw.shape[0] // cols
        frame_height = sheet_raw.shape[1] // rows

        for x in range(0, sheet_raw.shape[0], frame_width):
            for y in range(0, sheet_raw.shape[1], frame_height):
                frame = sheet_raw.crop((
                    x, y, x+frame_width, y+frame_height))
                frames.append(CMUImage(frame))

        super().__init__(frames, frametime, start)


# can really make this either CameraRenderable or Animation because
# of the `tick` override, but I'm using CameraRenderable since the
# super().__init__() of Animation is completely different and
# CameraRenderable doesn't define one at all.
class AnimationSelection(CameraRenderable):
    def __init__(self, animations, starter):
        self.animations = animations
        self.current_animation = self.animations[starter]

    def select_animation(self, id):
        self.current_animation = self.animations[id]

    def tick(self, dt):
        self.current_animation.tick(dt)

    def render(self, app, screen_pos):
        self.current_animation.render(app, screen_pos)


# stores aliases to animations that are contained in other objects
# and updates them during onStep
class AnimationTicker:
    def __init__(self):
        self.animations = []

    def register_animation(self, animation):
        self.animations.append(animation)

    def tick(self, dt):
        for animation in self.animations:
            animation.tick(dt)
