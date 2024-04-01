import json
import math
import random
from ds import Rectangle
import json
import random

def initialize_positions(rectangles):
    for rectangle in rectangles:
        rectangle.x = random.uniform(0, 100)
        rectangle.y = random.uniform(0, 100)

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Rectangle(**_) for _ in data]


def write_to_json(file_path, rectangles):
    # Convert rectangles and points into dictionaries
    data = [
        {
            'id': rectangle.id,
            'x': rectangle.x,
            'y': rectangle.y,
            'width': rectangle.width,
            'height': rectangle.height,
            'points': [
                {
                    'id': point.id,
                    'x': point.x,
                    'y': point.y,
                    'connection': point.connection
                }
                for point in rectangle.points
            ]
        }
        for rectangle in rectangles
    ]

    # Write the data to a JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file)

def check_overlap(rectangles):
    for i, rect1 in enumerate(rectangles):
        for rect2 in rectangles[i+1:]:
            if not (rect1.x >= rect2.x + rect2.width
                    or rect1.x + rect1.width <= rect2.x
                    or rect1.y >= rect2.y + rect2.height
                    or rect1.y + rect1.height <= rect2.y):
                print(f"Rectangles {rect1.id} and {rect2.id} overlap.")
                return False
    return True

def check_within_bounds(rectangles, width_limit, height_limit):
    for rectangle in rectangles:
        if not (0 <= rectangle.x <= width_limit - rectangle.width and 0 <= rectangle.y <= height_limit - rectangle.height):
            print(f"Rectangle {rectangle.id} is out of bounds.")
            return False
    return True


def rotate_matrix(matrix):
    return list(reversed(list(zip(*matrix))))

def rotate_matrix_left(matrix):
    return [row[::-1] for row in zip(*matrix)]

def rotate_180(matrix):
    return [row[::-1] for row in matrix[::-1]]

def rotate_90_clockwise(matrix):
    return [list(reversed(i)) for i in zip(*matrix)]


def generate_rectangle_data(number_of_rectangles, number_of_points, space_width, space_height):
    rectangles = []
    all_points = []

    for i in range(number_of_rectangles):
        x = random.uniform(0, space_width - 20)  # Deduct the max possible rectangle width
        y = random.uniform(0, space_height - 30)  # Deduct the max possible rectangle height
        # width = random.uniform(0, 20)
        # height = random.uniform(0, 30)
        width = 10
        height = 10

        points = []
        for j in range(number_of_points):
            rel_x = random.choice([0, 1])  # Relative x is on the side of the rectangle
            rel_y = random.choice([0, 1])  # Relative y is on the side of the rectangle
            point_id = j + 1 + i * number_of_points

            # calculate absolute x and y using the relative co-ordinates
            abs_x = x + rel_x * width
            abs_y = y + rel_y * height

            points.append({"id": point_id, "x": rel_x, "y": rel_y, "connection": None})
            all_points.append({"id": point_id, "x": abs_x, "y": abs_y})  # Absolute coordinates for connections

        rectangles.append({
            "id": "r" + str(i + 1),
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "points": points
        })

    # Assign connections ensuring that a point is not connected to another point from the same rectangle
    for rectangle in rectangles:
        for point in rectangle['points']:
            distinct_points = [p for p in all_points if
                               p['id'] != point['id'] and p['id'] not in [pt['id'] for pt in rectangle['points']]]
            connection = random.choice(distinct_points)['id']
            point['connection'] = connection

    # Generate JSON data
    json_data = json.dumps(rectangles, indent=2)

    # Save JSON data to the file
    with open('rectangle_data.json', 'w') as json_file:
        json_file.write(json_data)

