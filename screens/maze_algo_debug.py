from cmu_graphics import *
from maze import generateMaze


def maze_algo_debug_onAppStart(app):
    app.cell_size = 50
    app.rows = app.height // app.cell_size
    app.cols = app.width // app.cell_size

    resetMaze(app)


def resetMaze(app):
    print("Generating maze")
    generateMaze(app)
    print("Finished generating maze")


def maze_algo_debug_onKeyPress(app, key):
    if key == 'r':
        resetMaze(app)


def maze_algo_debug_redrawAll(app):
    drawGrid(app)


def drawGrid(app):
    for row in range(len(app.grid)):
        for col in range(len(app.grid[row])):
            left, top = getCellLeftTop(app, row, col)

            fill = 'white' if app.grid[row, col] else 'black'

            drawRect(left, top, app.cell_size, app.cell_size,
                     fill=fill)


def getCellLeftTop(app, row, col):
    return col * app.cell_size, row * app.cell_size
