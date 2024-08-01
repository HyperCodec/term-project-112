import os
import pathlib
from cmu_graphics import Sound


# fuction taken from sounds example
def loadSound(relativePath):
    # Convert to absolute path (because pathlib.Path only takes absolute paths)
    absolutePath = os.path.abspath(relativePath)
    # Get local file URL
    url = pathlib.Path(absolutePath).as_uri()
    # Load Sound file from local URL
    return Sound(url)


DEFAULT_VOLUME = 10


def findVolumeDistanceModifier(app, absolute_pos):
    screen_pos = app.camera.get_screen_coords(app, absolute_pos)

    return DEFAULT_VOLUME / screen_pos.distance()
