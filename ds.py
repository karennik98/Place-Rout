class Point:
    def __init__(self, id, x, y, connection):
        self.id = id
        self.x = x
        self.y = y
        self.connection = connection

class Rectangle:
    def __init__(self, id, x, y, width, height, points):
        self.id = id
        self.width = width
        self.height = height
        self.points = [Point(**_) for _ in points]
        self.x = x  # Initialize as None, will be updated in `initialize_positions`
        self.y = y  # Initialize as None, will be updated in `initialize_positions`
