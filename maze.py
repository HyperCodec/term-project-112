import random
import numpy as np


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

    # these loops might be the cause of those clump things.
    # TODO maybe try similar to `findNeighbors`
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
