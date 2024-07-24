from cmu_graphics import *
from player import Player
from engine.camera import Camera
from maze import generateMaze
from engine.time import TimeManager


def resetGame(app):
    print("Generating maze")
    generateMaze(app)
    print("Finished generating maze")

    app.player = Player()
    app.camera = Camera()
    app.time = TimeManager()


def game_onAppStart(app):
    app.stepsPerSecond = 60


def game_onStep(app):
    pass


def game_onKeyPress(app, key):
    pass
