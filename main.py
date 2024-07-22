from maze import generateMaze
from cmu_graphics import *


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


def onKeyPress(app, key):
    if key == 'r':
        resetGame(app)


def redrawAll(app):
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


def main():
    runApp(width=1100, height=800)


if __name__ == "__main__":
    main()
