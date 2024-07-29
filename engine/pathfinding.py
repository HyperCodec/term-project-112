from maze import findNeighbors, getRowColFromCoordinate
from engine.vector import Vec2


def BFS(app, source, target):
    directional_mappings = {}
    distance_mappings = {}

    frontier = [source]

    cur_dist = 0
    while frontier != []:
        next_frontier = []

        for cell in frontier:
            distance_mappings[cell] = cur_dist

            if cell == target:
                return directional_mappings, distance_mappings

            for neighbor in findNeighbors(app, cell[0], cell[1]):
                if neighbor in distance_mappings:
                    continue

                next_frontier.append(neighbor)
                directional_mappings[neighbor] = directional_mappings.get(
                    neighbor, cell)

            frontier = next_frontier
        cur_dist += 1

    return None


def getPathFromMappings(directional_mappings, distance_mappings, target):
    path = []

    cur_cell = target
    while distance_mappings[cur_cell]:
        path.insert(0, cur_cell)

        cur_cell = directional_mappings[cur_cell]

    return path


class PathTweener:
    def __init__(self, path):
        self.path = path
        self.target_cell = path.popleft()

    def select_next_cell(self):
        self.target_cell = self.path.popleft()

    def calculate_direction_to_target(self, app, current_pos):
        cur_row, cur_col = getRowColFromCoordinate(app, current_pos)

        return self.target_cell[0] - cur_row, self.target_cell[1] - cur_col

    def move_toward_target(self, app, speed, parent):
        drow, dcol = self.calculate_direction_to_target(app, parent.pos)
        mrow, mcol = drow * speed, dcol * speed

        parent.pos += Vec2(mcol, mrow) * app.cell_size

        if getRowColFromCoordinate(app, parent.pos) == self.target_cell:
            if self.path == []:
                return True
            self.select_next_cell()

        return False


def calculateBLineMovement(source, target, speed):
    direction = (target - source).normalize()
    return direction * speed
