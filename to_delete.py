import numpy as np
import json
import random
from queue import PriorityQueue
import matplotlib.pyplot as plt

def visualize_placement_and_routing(grid, blocks, nets):
    fig, ax = plt.subplots()

    # First visualize the blocks and pins
    for block in blocks:
        y, x = block.location
        ax.add_patch(plt.Rectangle((x, y), 1, 1, color='blue'))
        for pin in block.pins:
            py, px = pin.location
            ax.plot(px + 0.5, py + 0.5, 'go', markersize=5)

    # Then visualize the nets (routes)
    for net in nets:
        if 'route' in net:
            route = net['route']
            route_y, route_x = zip(*route)
            ax.plot(np.array(route_x) + 0.5, np.array(route_y) + 0.5, 'r-')

    ax.set_xlim(0, grid.shape[1])
    ax.set_ylim(0, grid.shape[0])
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()  # Match the array representation on grid
    plt.grid(color='gray', linewidth=0.4)
    plt.show()


class Block:
    def __init__(self, uid, location=None, pins=None):
        self.uid = uid
        self.location = location  # (row, col) on the grid
        self.pins = pins if pins else []


class Pin:
    def __init__(self, uid, location=None):
        self.uid = uid
        self.location = location  # (row, col) on the grid


def load_data_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    blocks = [Block(block['uid'], tuple(block['location']),
                    [Pin(pin['uid'], tuple(pin['location'])) for pin in block['pins']]) for block in data['blocks']]
    nets = data['nets']
    size = data['size']

    return size, blocks, nets


def save_data_to_json(size, blocks, nets, filename):
    blocks_data = [
        {
            'uid': block.uid,
            'location': block.location,
            'pins': [{'uid': pin.uid, 'location': pin.location} for pin in block.pins]
        }
        for block in blocks
    ]

    data = {'size': size, 'blocks': blocks_data, 'nets': nets}

    with open(filename, 'w') as f:
        json.dump(data, f)


def create_grid(size):
    height, width = size
    return np.zeros((height, width))


def manhattan_distance(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])


def astar(grid, start, end):
    height, width = grid.shape
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up
    open_queue = PriorityQueue()
    open_queue.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not open_queue.empty():
        _, current = open_queue.get()

        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in moves:
            next_move = (current[0] + dx, current[1] + dy)
            if 0 <= next_move[0] < height and 0 <= next_move[1] < width and grid[
                next_move] == 0:  # Checking if next_move is within grid and not an obstacle
                new_cost = cost_so_far[current] + 1
                if next_move not in cost_so_far or new_cost < cost_so_far[next_move]:
                    cost_so_far[next_move] = new_cost
                    priority = new_cost + manhattan_distance(end, next_move)
                    open_queue.put((priority, next_move))
                    came_from[next_move] = current

    return []


def add_block(grid, block):
    # Add block to the grid
    grid[block.location] = 1

    # Add block's pins to the grid
    for pin in block.pins:
        grid[pin.location] = 2  # or some other value than 0 and 1. 2 is used for simplicity here


def route_net(blocks, grid, net):
    start_block = next(block for block in blocks if block.uid == net['start_pin']['block_uid'])
    start_pin = next(pin for pin in start_block.pins if pin.uid == net['start_pin']['pin_uid'])

    end_block = next(block for block in blocks if block.uid == net['end_pin']['block_uid'])
    end_pin = next(pin for pin in end_block.pins if pin.uid == net['end_pin']['pin_uid'])

    start_pin_location = start_pin.location
    end_pin_location = end_pin.location

    route = astar(grid, start_pin_location, end_pin_location)

    return route


def run_placement_and_routing(input_filename, output_filename):
    # Load blocks and nets from JSON file
    size, blocks, nets = load_data_from_json(input_filename)

    # Create grid
    grid = create_grid(size)
    # Add blocks to grid
    for block in blocks:
        add_block(grid, block)

    # Route nets and add them to the result
    result = []

    for net in nets:
        route = route_net(blocks, grid, net)

        # Add net route to result
        if route:
            net['route'] = route
            result.append(net)

    # Save the final placement and routing to a JSON file
    save_data_to_json(size, blocks, result, output_filename)
    visualize_placement_and_routing(grid, blocks, nets)

def generate_input_json(height, width, num_blocks, min_pins, max_pins, filename):
    # Generate random blocks with random pins
    blocks = []
    used_locations = set()

    for i in range(num_blocks):
        block_location = (random.randint(0, height - 1), random.randint(0, width - 1))
        while block_location in used_locations:
            block_location = (random.randint(0, height - 1), random.randint(0, width - 1))

        used_locations.add(block_location)

        pins = []
        for j in range(random.randint(min_pins, max_pins)):
            pin_location = (random.randint(0, height - 1), random.randint(0, width - 1))
            while pin_location in used_locations:
                pin_location = (random.randint(0, height - 1), random.randint(0, width - 1))

            used_locations.add(pin_location)

            pins.append({"uid": f"p{j}", "location": list(pin_location)})

        block = {
            "uid": f"Block{i}",
            "location": list(block_location),
            "pins": pins
        }
        blocks.append(block)

    # Generate random nets
    nets = []
    all_pins = [(block['uid'], pin['uid']) for block in blocks for pin in block['pins']]
    random.shuffle(all_pins)

    for k in range(0, len(all_pins), 2):
        if k + 1 < len(all_pins):
            start_pin_uid = all_pins[k]
            end_pin_uid = all_pins[k + 1]

            net = {
                "uid": f"Net{k//2}",
                "start_pin": {"block_uid": start_pin_uid[0], "pin_uid": start_pin_uid[1]},
                "end_pin": {"block_uid": end_pin_uid[0], "pin_uid": end_pin_uid[1]}
            }
            nets.append(net)

    data = {"blocks": blocks, "nets": nets, "size": [height, width]}

    with open(filename, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    # Parameters for input.json
    height = 10
    width = 20
    num_blocks = 20
    min_pins = 1
    max_pins = 4

    # Generate input.json
    generate_input_json(height, width, num_blocks, min_pins, max_pins, 'input2.json')
    # Parameters for input.json and output.json
    input_filename = 'input2.json'
    output_filename = 'output2.json'

    run_placement_and_routing(input_filename, output_filename)

