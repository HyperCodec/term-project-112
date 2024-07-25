import time  # hopefully this isnt a cyclic import


class TimeManager:
    def __init__(self):
        self.last_frame = time.time()

    def delta_seconds(self):
        return time.time() - self.last_frame

    def mark_step_end(self):
        self.last_frame = time.time()
