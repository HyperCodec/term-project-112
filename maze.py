import random
import numpy as np
from PIL import Image, ImageDraw
from cmu_graphics import CMUImage
from engine.camera import RenderableImage
from engine.vector import Vec2

HIDING_SPOT_SIZE = 50
NUM_HIDING_SPOTS = 20


# custom grid-based DFS algorithm. doing it this way instead of
# the graph way for efficiency when calculating things like collisions.
# also just easier to render something in grid format.
def generateMaze(app):
    app.grid = np.zeros((app.rows, app.cols))

    # starting at (0, 0), I don't think starting
    # randomly really affects anything.
    work = [(0, 0)]

    # I think this is a bit faster than len(work) == 0 bc the latter has
    # to loop through the whole list no matter what.
    while work != []:
        next_row, next_col = work.pop()

        if not isNodeValid(app, next_row, next_col):
            continue

        # cell is valid, make it white.
        app.grid[next_row, next_col] = 1

        # insert neighbors in random order.
        # because this is basically a stack, it chooses
        # a next neighbor and then investigates the whole
        # route before returning to other neighbor options.
        neighbors = findNeighbors(app, next_row, next_col)

        random.shuffle(neighbors)

        work += neighbors

    app.hiding_spots = []

    while len(app.hiding_spots) < NUM_HIDING_SPOTS:
        row, col = random.randrange(app.rows), random.randrange(app.cols)

        existing_locs = set(
            map(lambda v: getRowColFromCoordinate(app, v), app.hiding_spots))

        if not app.grid[row, col] or (row, col) in existing_locs:
            continue

        center = Vec2(col*app.cell_size, row*app.cell_size) + app.cell_size/2

        offset = Vec2(
            random.randrange(app.cell_size/2 - HIDING_SPOT_SIZE),
            random.randrange(app.cell_size/2 - HIDING_SPOT_SIZE)
        )

        hiding_spot = center + offset

        app.hiding_spots.append(hiding_spot)


def findNeighbors(app, row, col):
    neighbors = []

    for drow, dcol in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nrow, ncol = row+drow, col+dcol

        if not isCellInBounds(app, nrow, ncol):
            continue

        neighbors.append((nrow, ncol))

    return neighbors


# kind of similar to conway's game of life algo now that I think of it.
def isNodeValid(app, row, col):
    # immediately not valid if it's already filled
    if app.grid[row, col]:
        return False

    # counts the filled neighbors
    ncount = 0

    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            nrow, ncol = row+drow, col+dcol

            # make sure it isn't the start (because iterating through square
            # instead of just checking all 8 sides)
            if nrow == row and ncol == col:
                continue

            if not isCellInBounds(app, nrow, ncol):
                continue

            # only count if full
            if not app.grid[nrow, ncol]:
                continue

            ncount += 1

    return ncount < 3


def isCellInBounds(app, row, col):
    return (row >= 0 and row < app.rows and
            col >= 0 and col < app.cols)


def getRowColFromCoordinate(app, pos):
    return pos.y // app.cell_size, pos.x // app.cell_size


# optimized maze rendering due to how slow CMU graphics is.
def renderMazeImage(app):
    image = Image.new(mode="RGB", size=(
        app.rows*app.cell_size, app.cols*app.cell_size))
    draw = ImageDraw.Draw(image)

    for row in range(app.rows):
        for col in range(app.cols):
            cell = app.grid[row, col]
            fill = 'white' if cell else 'black'

            if (row, col) == (app.rows-1, app.cols-1):
                # goal cell
                fill = 'blue'

            top, left = row*app.cell_size, col*app.cell_size
            bottom, right = top+app.cell_size, left+app.cell_size
            draw.rectangle([(left, top), (right, bottom)], fill)

    for hiding_spot in app.hiding_spots:
        # render hiding spot.
        cx, cy = hiding_spot.x.item(), hiding_spot.y.item()
        draw.ellipse(
            [(cx-HIDING_SPOT_SIZE, cy-HIDING_SPOT_SIZE),
             (cx+HIDING_SPOT_SIZE, cy+HIDING_SPOT_SIZE)],
            'brown')

    image = CMUImage(image)
    app.maze_render = RenderableImage(image)
