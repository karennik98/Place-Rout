from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import matplotlib.pyplot as plt
from utilities import *

def route_wire_lees(rectangles, rectangle, source_point, space_width, space_height):
    gridw = space_width
    gridh = space_height
    # Similar logic to generate matrix and grid as in A* function
    matrix = [[0 for _ in range(gridw)] for __ in range(gridh)]

    for rect in rectangles:
        if rect.id != rectangle.id:
            for i in range(int(rect.x), int(rect.x + rect.width)):
                for j in range(int(rect.y), int(rect.y + rect.height)):
                    matrix[j][i] = 1

    grid = Grid(matrix=matrix)

    # Initialize a wave propagation grid with -2 in open spaces and -1 in blocked spaces
    wave_propagation_grid = [[-2 for _ in range(gridw)] for __ in range(gridh)]
    for i in range(gridw):
        for j in range(gridh):
            if grid.node(i, j).walkable is False:
                wave_propagation_grid[j][i] = -1

                # Initialize `src` and `dest_point` as in the A* function
    src = grid.node(round(source_point.x * rectangle.width + rectangle.x),
                    round(source_point.y * rectangle.height + rectangle.y))
    dest_id = source_point.connection
    dest_point = None
    dest_rect = None

    # Search for destination point in all rectangles
    for rect in rectangles:
        for point in rect.points:
            if point.id == dest_id:
                dest_point = point
                dest_rect = rect
                break
    # If no destination point was found
    if dest_point is None:
        return []

    dest = grid.node(round(dest_point.x * dest_rect.width + dest_rect.x),
                     round(dest_point.y * dest_rect.height + dest_rect.y))

    dx = [0, 1, 0, -1]  # possible movements in x direction
    dy = [1, 0, -1, 0]  # possible movements in y direction

    # Wave propagation
    queue = [src]
    while len(queue) > 0:
        cur_node = queue.pop(0)
        for direction in range(4):  # Try each direction
            next_x = cur_node.x + dx[direction]
            next_y = cur_node.y + dy[direction]
            # Check if the coordinates are within the grid and it is not blocked
            if next_x >= 0 and next_y >= 0 and next_x < gridw and next_y < gridh and wave_propagation_grid[next_y][
                next_x] == -2:
                queue.append(grid.node(next_x, next_y))
                wave_propagation_grid[next_y][next_x] = wave_propagation_grid[cur_node.y][
                                                            cur_node.x] + 1  # Increment the wave propagation number

    # Traceback
    cur_node = dest
    path = [dest]
    while cur_node != src:
        for direction in range(4):  # Check each direction
            next_x = cur_node.x + dx[direction]
            next_y = cur_node.y + dy[direction]
            # Check if the coordinates are within the grid
            if next_x >= 0 and next_y >= 0 and next_x < gridw and next_y < gridh and wave_propagation_grid[next_y][
                next_x] == wave_propagation_grid[cur_node.y][cur_node.x] - 1:
                cur_node = grid.node(next_x, next_y)
                path.append(cur_node)
                break
    return path[::-1]  # The path is traced from `dest` to `src`, so reverse it before returning

count = 0
def route_wire_a_star(rectangles, rectangle, source_point, space_width, space_height):
    matrix = [[0 for _ in range(space_width)] for __ in range(space_height)]

    for rect in rectangles:
        if rect.id != rectangle.id:
            for j in range(int(rect.y), int(rect.y + rect.height)):
                for i in range(int(rect.x), int(rect.x + rect.width)):
                    matrix[j][i] = 1
    # matrix = rotate_180(matrix)

    # Invert matrix vertically
    # matrix = matrix[::-1]
    # matrx_plt = matrix

    # global count
    # if count == 0:
    #     plt.imshow(matrx_plt, cmap='binary_r')
    #     plt.show()
    #     # count += 1

    grid = Grid(matrix=matrix)

    source = grid.node(round(source_point.x * rectangle.width + rectangle.x),
                       round(source_point.y * rectangle.height + rectangle.y))

    dest_id = source_point.connection
    dest_point = None
    dest_rect = None

    # Search for destination point in all rectangles
    for rect in rectangles:
        for point in rect.points:
            if point.id == dest_id:
                dest_point = point
                dest_rect = rect
                break

    # If no destination point was found
    if dest_point is None:
        return []

    dest = grid.node(round(dest_point.x * dest_rect.width + dest_rect.x),
                     round(dest_point.y * dest_rect.height + dest_rect.y))

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(source, dest, grid)
    return path


from queue import PriorityQueue


def heuristic(start, target):
    """
    Compute the Manhattan distance from start to target
    """
    return abs(start[0] - target[0]) + abs(start[1] - target[1])


def route_wire_a_star2(rectangles, rectangle, source_point, space_width, space_height):
    # Initialize grid
    grid = [[0 for _ in range(space_width)] for __ in range(space_height)]
    for rect in rectangles:
        if rect.id != rectangle.id:
            for i in range(int(rect.x), int(rect.x + rect.width)):
                for j in range(int(rect.y), int(rect.y + rect.height)):
                    grid[i][j] = -1

    start = (round(rectangle.x + source_point.x * rectangle.width),
             round(rectangle.y + source_point.y * rectangle.height))

    dest_id = source_point.connection
    goal = None
    for rect in rectangles:
        for point in rect.points:
            if point.id == dest_id:
                goal = (round(rect.x + point.x * rect.width),
                        round(rect.y + point.y * rect.height))
                break

    if goal is None:
        return []

    # A* algorithm
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                next = (current[0] + dx, current[1] + dy)
                new_cost = cost_so_far[current] + 1
                if 0 <= next[0] < space_width and 0 <= next[1] < space_height and grid[next[0]][next[1]] != -1 and (
                        next not in cost_so_far or new_cost < cost_so_far[next]):
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

    # Reconstruct path
    current = goal
    path = []
    while current != start:
        if current in came_from:
            path.append(current)
            current = came_from[current]
        else:
            print(f"No valid path could be found for source_point: {source_point.id} in rectangle: {rectangle.id}")
            return []
    path.append(start)
    path.reverse()

    return path