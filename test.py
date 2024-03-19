import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
# class Point:
#     def __init__(self, id, x, y, connection):
#         self.id = id
#         self.x = x
#         self.y = y
#         self.connection = connection  # List of Points that this point is connected to
#
#     def __lt__(self, other):
#         return self.id < other.id
#
#
# class Rectangle:
#     def __init__(self, id, width, height, points):
#         self.id = id
#         self.width = width
#         self.height = height
#         self.points = points  # List of Points for this rectangle
#         self.x = 0  # The x-coordinate of this rectangle in the plane
#         self.y = 0  # The y-coordinate of this rectangle in the plane
#         self.vx = 0  # The current x-velocity of this rectangle (for the Force-Directed method)
#         self.vy = 0  # The current y-velocity of this rectangle (for the Force-Directed method)
#
#
# def initialize_positions(rectangles):
#     for rectangle in rectangles:
#         rectangle.x = random.uniform(0, 100)
#         rectangle.y = random.uniform(0, 100)
#
# def parse_input(file_path):
#     # Read the JSON file
#     with open(file_path, 'r') as file:
#         data = json.load(file)
#
#     # Parse the data into rectangle objects
#     rectangles = []
#     for rectangle_data in data:
#         points = [
#             Point(
#                 id=point_data['id'],
#                 x=point_data['x'],
#                 y=point_data['y'],
#                 # We're assuming connections are just a list of point ids for simplicity
#                 connection=point_data['connection']
#             )
#             for point_data in rectangle_data['points']
#         ]
#
#         rectangle = Rectangle(
#             id=rectangle_data['id'],
#             width=rectangle_data['width'],
#             height=rectangle_data['height'],
#             points=points
#         )
#         rectangles.append(rectangle)
#
#     # Link the points objects across different rectangles based on the connection IDs
#     point_id_to_point = {point.id: point for rectangle in rectangles for point in rectangle.points}
#     for rectangle in rectangles:
#         for point in rectangle.points:
#             point.connection = [point_id_to_point[connected_id] for connected_id in point.connection]
#
#     return rectangles
#
def visualize_rectangles(rectangles):
    fig, ax = plt.subplots()

    for rectangle in rectangles:
        ax.add_patch(
            patches.Rectangle(
                (rectangle.x, rectangle.y),  # (x,y)
                rectangle.width,  # width
                rectangle.height,  # height
                fill=True
            )
        )
        for point in rectangle.points:
            ax.plot(rectangle.x + point.x * rectangle.width, rectangle.y + point.y * rectangle.height, 'ro')

    ax.set_xlim([0, max([r.x + r.width for r in rectangles]) + 10])
    ax.set_ylim([0, max([r.y + r.height for r in rectangles]) + 10])

    plt.show()
#
#
# def draw_rectangle(rect, ax):
#     ax.add_patch(
#         patches.Rectangle(
#             (rect.x, rect.y),
#             rect.width,
#             rect.height,
#             edgecolor = 'black',
#             fill=False
#         )
#     )
#
# def visualize_layout(rectangles):
#     fig, ax = plt.subplots()
#
#     all_points = {point: rect for rect in rectangles for point in rect.points}
#
#     for rect in rectangles:
#         draw_rectangle(rect, ax)
#         for point in rect.points:
#             for connection in point.connection:
#                 connecting_rect = all_points[connection]
#                 ax.plot([rect.x + point.x, connecting_rect.x + connection.x],
#                         [rect.y + point.y, connecting_rect.y + connection.y],'r-')
#
#     plt.xlim([0, 200])
#     plt.ylim([0, 200])
#     plt.gca().set_aspect('equal', adjustable='box')  # Maintain aspect ratio
#     plt.show()
#
# rectangles = parse_input('input.json')
# initialize_positions(rectangles)
# visualize_layout(rectangles)
# # visualize_rectangles(rectangles)



import json
import random

def visualize_rectangles2(rectangles):
    fig, ax = plt.subplots()

    point_dict = {}
    for rectangle in rectangles:
        # Save all points in a dictionary to reference later
        for point in rectangle.points:
            point_dict[point.id] = {'x': rectangle.x + point.x * rectangle.width,
                                     'y': rectangle.y + point.y * rectangle.height}

    # Add rectangles and points to plot
    for rectangle in rectangles:
        ax.add_patch(
            patches.Rectangle(
                (rectangle.x, rectangle.y),  # (x,y)
                rectangle.width,  # width
                rectangle.height,  # height
                fill=True, alpha=0.3
            )
        )
        for point in rectangle.points:
            ax.plot(rectangle.x + point.x * rectangle.width, rectangle.y + point.y * rectangle.height, 'ro')

    # Add wires
    for rectangle in rectangles:
        for point in rectangle.points:
            if point.connection in point_dict:  # Check if the connection actually exists
                connected_point_coords = point_dict[point.connection]
                ax.plot([rectangle.x + point.x * rectangle.width, connected_point_coords['x']],
                        [rectangle.y + point.y * rectangle.height, connected_point_coords['y']], 'b-')

    ax.set_xlim([0, max([r.x + r.width for r in rectangles]) + 10])
    ax.set_ylim([0, max([r.y + r.height for r in rectangles]) + 10])
    plt.show()

def visualize_rectangles_and_wires(rectangles):
    fig, ax = plt.subplots()

    for rectangle in rectangles:
        ax.add_patch(
            patches.Rectangle(
                (rectangle.x, rectangle.y),   # (x,y)
                rectangle.width,              # width
                rectangle.height,             # height
                fill=True, alpha=0.3
            )
        )
        for point in rectangle.points:
            point_coordinates = (rectangle.x + point.x * rectangle.width, rectangle.y + point.y * rectangle.height)
            ax.plot(*point_coordinates, 'ro')
            path = route_wire_a_star(rectangles, rectangle, point)
            for node_1, node_2 in zip(path[:-1], path[1:]):
                ax.plot([node_1[0], node_2[0]], [node_1[1], node_2[1]], 'b-')

    ax.set_xlim([0, max([r.x + r.width for r in rectangles]) + 10])
    ax.set_ylim([0, max([r.y + r.height for r in rectangles]) + 10])
    plt.axis('equal')
    plt.show()
class Point:
    def __init__(self, id, x, y, connection):
        self.id = id
        self.x = x
        self.y = y
        self.connection = connection

class Rectangle:
    def __init__(self, id, width, height, points):
        self.id = id
        self.width = width
        self.height = height
        self.points = [Point(**p) for p in points]
        self.x = None  # Initialize as None, will be updated in `initialize_positions`
        self.y = None  # Initialize as None, will be updated in `initialize_positions`
def initialize_positions(rectangles):
    for rectangle in rectangles:
        rectangle.x = random.uniform(0, 100)
        rectangle.y = random.uniform(0, 100)

def route_wire_a_star(rectangles, rectangle, source_point):
    matrix = [[0 for _ in range(100)] for __ in range(100)]
    for rect in rectangles:
        if rect.id_ != rectangle.id_:
            for i in range(int(rect.x), int(rect.x + rect.width)):
                for j in range(int(rect.y), int(rect.y + rect.height)):
                    matrix[j][i] = 1

    grid = Grid(matrix=matrix)
    source = grid.node(int(source_point.x*rectangle.width + rectangle.x), int(source_point.y*rectangle.height + rectangle.y))
    dest_id = source_point.connection
    for point in rectangle.points:
        if point.id_ == dest_id:
            dest_point = point
            break
    dest = grid.node(int(dest_point.x*rectangle.width + rectangle.x), int(dest_point.y*rectangle.height + rectangle.y))
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(source, dest, grid)
    return path
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Rectangle(**r) for r in data]


rectangles = read_json('input.json')
initialize_positions(rectangles)
visualize_rectangles2(rectangles)