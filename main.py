from maze import generateMaze
from player import Player
from engine.camera import Camera
from cmu_graphics import *
from screens.title import *
from screens.game import *
from screens.win import *


def main():
    runAppWithScreens(initialScreen='title', width=1100, height=800)


if __name__ == "__main__":
    main()
