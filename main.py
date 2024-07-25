from maze import generateMaze
from player import Player
from engine.camera import Camera
from cmu_graphics import *
from screens.maze_algo_debug import *

"""
def onAppStart(app):
    print("App started")
    app.setMaxShapeCount(10000)
    app.cell_size = 50
    app.rows = app.height // app.cell_size
    app.cols = app.width // app.cell_size
    resetGame(app)


def resetGame(app):
    print("Generating maze")
    generateMaze(app)
    print("Finished generating maze")

    app.player = Player()
    app.camera = Camera()


def redrawAll(app):
    app.camera.render_frame(app)
"""


def main():
    runAppWithScreens(initialScreen='maze_algo_debug', width=1100, height=800)


if __name__ == "__main__":
    main()
