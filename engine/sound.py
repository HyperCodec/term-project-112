from direct.showbase import Audio3DManager


class SoundManager:
    def __init__(self):
        self.panda_manager = Audio3DManager.Audio3DManager()

    def load_sfx(self, path):
        return self.panda_manager.loadSfx(path)
