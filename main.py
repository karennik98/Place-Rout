class Point:
    def __init__(self, id, x, y, connections):
        self.id = id
        self.x = x
        self.y = y
        self.connections = connections  # List of Points that this point is connected to

    def __lt__(self, other):
        return self.id < other.id


class Rectangle:
    def __init__(self, id, width, height, points):
        self.id = id
        self.width = width
        self.height = height
        self.points = points  # List of Points for this rectangle
        self.x = 0  # The x-coordinate of this rectangle in the plane
        self.y = 0  # The y-coordinate of this rectangle in the plane
        self.vx = 0  # The current x-velocity of this rectangle (for the Force-Directed method)
        self.vy = 0  # The current y-velocity of this rectangle (for the Force-Directed method)

import math
import random

def calculate_force(rectangle1, rectangle2):
    # Calculate a force between two rectangles
    dx = rectangle1.x - rectangle2.x
    dy = rectangle1.y - rectangle2.y

    # Adding a small constant to similar efforts to avoid division by zero
    distance = math.sqrt(dx * dx + dy * dy) + 1.0
    force = 1.0 / (distance * distance)
    return dx * force, dy * force


# Initialization of the coordinates of rectangles
def initialize_positions(rectangles):
    for rectangle in rectangles:
        rectangle.x = random.uniform(0, 100)
        rectangle.y = random.uniform(0, 100)


def force_directed_placement(rectangles):
    for _ in range(100):  # Number of iterations, can be adjusted accordingly
        for rectangle1 in rectangles:
            force_x = 0
            force_y = 0

            for rectangle2 in rectangles:
                if rectangle1 != rectangle2:
                    fx, fy = calculate_force(rectangle1, rectangle2)
                    force_x += fx
                    force_y += fy

            # Update rectangle's velocity and position
            rectangle1.vx += force_x
            rectangle1.vy += force_y
            rectangle1.x += rectangle1.vx
            rectangle1.y += rectangle1.vy

            rectangle1.x = min(max(rectangle1.x, 0), 100)
            rectangle1.y = min(max(rectangle1.y, 0), 100)

from queue import PriorityQueue


def heuristic(a, b):
  # Calculate heuristic (in this case, Manhattan distance)
  return abs(b.x - a.x) + abs(b.y - a.y)


def a_star_search(start, goal):
    # The set of discovered nodes that may need to be (re-)expanded.
    open_set = PriorityQueue()
    open_set.put((0, start))

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start to n currently known.
    came_from = {start: None}

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known
    g_score = {start: 0}

    while not open_set.empty():
        # Current node in the path
        current = open_set.get()[1]

        if current == goal:
            break

        for connection in current.connections:  # iterate over connections rather than neighbors
            temp_g_score = g_score[current] + heuristic(current, connection)

            if connection not in g_score or temp_g_score < g_score[connection]:
                g_score[connection] = temp_g_score
                f_score = temp_g_score + heuristic(goal, connection)
                open_set.put((f_score, connection))
                came_from[connection] = current

    # now we need to retrace our steps from the goal to the start along the best path
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path = path[::-1]  # reverse the list

    return path


import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_rectangle(rect, ax):
    ax.add_patch(
        patches.Rectangle(
            (rect.x, rect.y),
            rect.width,
            rect.height,
            edgecolor = 'black',
            fill=False
        )
    )

def visualize_layout(rectangles):
    fig, ax = plt.subplots()

    all_points = {point: rect for rect in rectangles for point in rect.points}

    for rect in rectangles:
        draw_rectangle(rect, ax)
        for point in rect.points:
            for connection in point.connections:
                connecting_rect = all_points[connection]
                ax.plot([rect.x + point.x, connecting_rect.x + connection.x],
                        [rect.y + point.y, connecting_rect.y + connection.y],'r-')

    plt.xlim([0, 500])
    plt.ylim([0, 500])
    plt.gca().set_aspect('equal', adjustable='box')  # Maintain aspect ratio
    plt.show()


import json

def parse_input(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Parse the data into rectangle objects
    rectangles = []
    for rectangle_data in data:
        points = [
            Point(
                id=point_data['id'],
                x=point_data['x'],
                y=point_data['y'],
                # We're assuming connections are just a list of point ids for simplicity
                connections=point_data['connections']
            )
            for point_data in rectangle_data['points']
        ]

        rectangle = Rectangle(
            id=rectangle_data['id'],
            width=rectangle_data['width'],
            height=rectangle_data['height'],
            points=points
        )
        rectangles.append(rectangle)

    # Link the points objects across different rectangles based on the connection IDs
    point_id_to_point = {point.id: point for rectangle in rectangles for point in rectangle.points}
    for rectangle in rectangles:
        for point in rectangle.points:
            point.connections = [point_id_to_point[connected_id] for connected_id in point.connections]

    return rectangles

def main(input_data):
    # Step 1: Parse the input data and create the rectangles
    rectangles = parse_input(input_data)

    # Initialize the x and y positions of the rectangles
    initialize_positions(rectangles)

    visualize_layout(rectangles)

    # Step 2: Perform placement using the Force-Directed Placement method
    force_directed_placement(rectangles)

    visualize_layout(rectangles)

    # Step 3: After performing placement, go through each Rectangle and perform routing
    for rectangle in rectangles:
      for point in rectangle.points:
        for connected_point in point.connections:
          print(a_star_search(point, connected_point))

    # Graphical visualization:
    visualize_layout(rectangles)

main('input.json')


