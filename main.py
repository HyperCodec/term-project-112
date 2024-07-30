from maze import generateMaze
from player import Player
from engine.camera import Camera
from cmu_graphics import *
# from screens.maze_algo_debug import *
from screens.game import *
# from screens.ui_test import *


def main():
    runAppWithScreens(initialScreen='game', width=1100, height=800)


if __name__ == "__main__":
    main()
