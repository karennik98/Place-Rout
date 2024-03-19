import json
import math
import random
from ds import Rectangle

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
                print(f"Rectangles {rect1.id_} and {rect2.id_} overlap.")
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