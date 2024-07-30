from maze import findNeighbors, getRowColFromCoordinate
from engine.vector import Vec2

# idea kind of credit to the guest lecture,
# was planning on implementing this exact
# algorithm beforehand anyways though


def BFS(app, source, target):
    directional_mappings = {}
    frontier = [source]

    while frontier != []:
        next_frontier = []

        for cell in frontier:
            if cell == target:
                return directional_mappings

            for neighbor in findNeighbors(app, cell[0], cell[1]):
                if not app.grid[int(cell[0]), int(cell[1])] or neighbor in directional_mappings:
                    continue

                next_frontier.append(neighbor)
                directional_mappings[neighbor] = directional_mappings.get(
                    neighbor, cell)

            frontier = next_frontier

    return None


def getPathFromMappings(directional_mappings, source, target):
    path = []

    cur_cell = target
    while cur_cell != source:
        path.insert(0, cur_cell)

        cur_cell = directional_mappings[cur_cell]

    return path


class PathTweener:
    def __init__(self, path):
        self.path = path
        self.target_cell = path.pop(0)

    def select_next_cell(self):
        self.target_cell = self.path.pop(0)

    def calculate_direction_to_target(self, app, current_pos):
        target_center = Vec2(self.target_cell[1]*app.cell_size + (
            app.cell_size/2), self.target_cell[0]*app.cell_size + (app.cell_size/2))
        direction_raw = (target_center - current_pos).normalize()

        return direction_raw.y, direction_raw.x

    def move_toward_target(self, app, speed, parent):
        drow, dcol = self.calculate_direction_to_target(app, parent.pos)
        movement = Vec2(dcol, drow) * speed

        parent.pos += movement

        if parent.is_fully_in_cell(app, *self.target_cell):
            if self.path == []:
                return True, (drow, dcol)
            self.select_next_cell()

        return False, (drow, dcol)


def calculateBLineMovement(source, target, speed):
    direction = (target - source).normalize()
    return direction * speed


class PathfindingEntity:
    def is_fully_in_cell(self, app, row, col):
        pass
