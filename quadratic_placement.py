import random
import math
import matplotlib.pyplot as plt
import json
import numpy as np

class Block:
    def __init__(self, height, width, uid, x=None, y=None, pins=None):
        self.height = height
        self.width = width
        self.uid = uid
        self.x = x
        self.y = y
        self.pins = pins if pins else []


def generate_input_json(min_width, max_width, min_height, max_height, min_pins_count, max_pins_count, num_blocks,
                        obstacles_count, min_obstacle_width, max_obstacle_width, min_obstacle_height,
                        max_obstacle_height, filename):
    blocks = [
        {
            'uid': f'Block{i}',
            'width': random.randint(min_width, max_width),
            'height': random.randint(min_height, max_height),
            'pins': [{'uid': f'p{j}', 'x': random.uniform(0, 1), 'y': random.choice([0, 1])} for j in
                     range(random.randint(min_pins_count, max_pins_count))]
        }
        for i in range(num_blocks)
    ]

    # Add netlist
    nets = []
    for i in range(num_blocks - 1):
        start_block = blocks[i]
        end_block = blocks[i + 1]

        nets.append({
            'uid': f'Net{i}',
            'start_pin': {'block_uid': start_block['uid'], 'pin_uid': start_block['pins'][0]['uid']},
            'end_pin': {'block_uid': end_block['uid'], 'pin_uid': end_block['pins'][0]['uid']}
        })

    obstacles = [
        {
            'uid': f'Obstacle{i}',
            'width': random.randint(min_obstacle_width, max_obstacle_width),
            'height': random.randint(min_obstacle_height, max_obstacle_height),
            'x': random.randint(0, boundary_width - max_obstacle_width),
            # x position now can't exceed the grid boundary
            'y': random.randint(0, boundary_height - max_obstacle_height)
            # y position now can't exceed the grid boundary
        } for i in range(obstacles_count)
    ]

    data = {'sram_blocks': blocks, 'nets': nets, 'obstacles': obstacles}

    with open(filename, 'w') as f:
        json.dump(data, f)


def load_blocks_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    sram_blocks = [Block(block['height'], block['width'], block['uid'], pins=block['pins']) for block in
                   data['sram_blocks']]
    nets = data['nets']
    obstacles = [Block(obstacle['height'], obstacle['width'], obstacle['uid'], x=obstacle['x'], y=obstacle['y']) for obstacle in data['obstacles']]

    return sram_blocks, nets, obstacles

def save_blocks_to_json(sram_blocks, filename):
    blocks = [
        {
            'uid': block.uid,
            'width': block.width,
            'height': block.height,
            'x': block.x,
            'y': block.y,
            'pins': block.pins
        }
        for block in sram_blocks
    ]

    data = {'sram_blocks': blocks}

    with open(filename, 'w') as f:
        json.dump(data, f)


def visualize_initial_placement(sram_blocks, nets, obstacles, boundary_height, boundary_width):
    fig, ax = plt.subplots()
    ax.set_xlim([0, boundary_width])
    ax.set_ylim([0, boundary_height])

    # Draw blocks in blue
    for block in sram_blocks:
        ax.add_patch(plt.Rectangle((block.x, block.y), block.width, block.height, color='blue', alpha=0.3))
        ax.text(block.x, block.y, block.uid, fontsize=6, ha='center')  # Draw block uid
        for pin in block.pins:
            pin_plot_x = block.x + pin['x'] * block.width
            pin_plot_y = block.y + pin['y'] * block.height
            ax.plot(pin_plot_x, pin_plot_y, 'ro')
            ax.text(pin_plot_x, pin_plot_y, pin['uid'], fontsize=6, ha='center')  # Draw pin uid

    # Draw obstacles in black
    for obstacle in obstacles:
        ax.add_patch(plt.Rectangle((obstacle.x, obstacle.y), obstacle.width, obstacle.height, color='black'))
        # ax.text(obstacle.x, obstacle.y, obstacle.uid, fontsize=6, ha='center', color='')  # Draw obstacle uid

    # Visualize nets
    for net in nets:
        start_block_uid = net['start_pin']['block_uid']
        end_block_uid = net['end_pin']['block_uid']
        start_pin_uid = net['start_pin']['pin_uid']
        end_pin_uid = net['end_pin']['pin_uid']

        start_block = next(block for block in sram_blocks if block.uid == start_block_uid)
        end_block = next(block for block in sram_blocks if block.uid == end_block_uid)

        start_pin = next(pin for pin in start_block.pins if pin['uid'] == start_pin_uid)
        end_pin = next(pin for pin in end_block.pins if pin['uid'] == end_pin_uid)

        start_pin_plot_x = start_block.x + start_pin['x'] * start_block.width
        start_pin_plot_y = start_block.y + start_pin['y'] * start_block.height

        end_pin_plot_x = end_block.x + end_pin['x'] * end_block.width
        end_pin_plot_y = end_block.y + end_pin['y'] * end_block.height

        ax.plot([start_pin_plot_x, end_pin_plot_x], [start_pin_plot_y, end_pin_plot_y], 'r-')
        ax.text((start_pin_plot_x + end_pin_plot_x) / 2, (start_pin_plot_y + end_pin_plot_y) / 2, net['uid'], fontsize=6, ha='center')  # Draw net uid

    plt.show()



def create_horizontal_grid(boundary_height, boundary_width, grid_spacing):
    num_lines = boundary_height // (grid_spacing + 5)
    lines = []
    for i in range(num_lines):
        y = i * (grid_spacing + 5)
        lines.append((0, y, boundary_width, y))

    return lines


def random_placement(sram_blocks, obstacles, boundary_height, boundary_width, min_spacing):
    for block in sram_blocks:
        while True:  # keep trying until we break out of loop when an empty placement is found
            block.x = random.randint(min_spacing, boundary_width - block.width - min_spacing)
            block.y = random.randint(min_spacing, boundary_height - block.height - min_spacing)

            # Check if the new position clashes with any existing obstacles.
            no_clashes = True
            for obstacle in obstacles:
                if (block.x < obstacle.x + obstacle.width and block.x + block.width > obstacle.x and
                        block.y < obstacle.y + obstacle.height and block.y + block.height > obstacle.y):
                    no_clashes = False
                    break

            # Check if new position clashes with existing blocks
            for existing_block in [b for b in sram_blocks if b.x is not None and b.y is not None]:
                if existing_block == block:
                    continue
                if (block.x < existing_block.x + existing_block.width and block.x + block.width > existing_block.x and
                        block.y < existing_block.y + existing_block.height and block.y + block.height > existing_block.y):
                    no_clashes = False
                    break

            if no_clashes:
                break  # found an empty spot, break infinite loop
    return sram_blocks


def quadratic_placement(blocks, boundary_height, boundary_width, min_spacing):
    total_blocks = len(blocks)
    num_blocks_side = math.ceil(math.sqrt(total_blocks))
    block_width = blocks[0].width
    block_height = blocks[0].height

    rect_width = num_blocks_side * block_width + (num_blocks_side - 1) * min_spacing
    rect_height = num_blocks_side * block_height + (num_blocks_side - 1) * min_spacing

    start_x = (boundary_width - rect_width) // 2
    start_y = (boundary_height - rect_height) // 2

    current_x = start_x
    current_y = start_y

    for i, block in enumerate(blocks):
        block.x = current_x
        block.y = current_y

        current_x += block_width + min_spacing

        if (i + 1) % num_blocks_side == 0:
            current_x = start_x
            current_y += block_height + min_spacing

    return blocks


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def Astar(grid, start, end):
    # Create start and end node
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialize open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until the end node is reached
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0

        # Get the node with the lowest f cost
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        # Remove the current node from the open list and add it to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Check if the goal has been reached, if so return the path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        children = []
        # Generate children from the adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Check within boundaries
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) -1) or node_position[1] < 0:
                continue

            # Ensure walkable terrain
            if grid[node_position[0]][node_position[1]] == 1:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            # Child is in the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list:
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

            # Add the child to the open list
            open_list.append(child)

import itertools

def visualize_placement_and_routing(sram_blocks, nets, grid, obstacles, boundary_height, boundary_width):
    fig, ax = plt.subplots()
    ax.set_xlim([0, boundary_width])
    ax.set_ylim([0, boundary_height])

    for obstacle in obstacles:
        ax.add_patch(plt.Rectangle((obstacle.x, obstacle.y), obstacle.width, obstacle.height, color='black'))

    # Define a color cycle iterator for different paths
    colors = itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y', 'k'])

    for block in sram_blocks:
        ax.add_patch(plt.Rectangle((block.x, block.y), block.width, block.height, color='blue', alpha=0.3))
        ax.text(block.x, block.y, block.uid, fontsize=6, ha='center')

    for block in sram_blocks:
        for pin in block.pins:
            pin_plot_x = block.x + pin['x'] * block.width
            pin_plot_y = block.y + pin['y'] * block.height
            ax.plot(pin_plot_x, pin_plot_y, 'ro')
            ax.text(pin_plot_x, pin_plot_y, pin['uid'], fontsize=6, ha='center')

    for net in nets:
        start_block = next(block for block in sram_blocks if block.uid == net['start_pin']['block_uid'])
        start_pin = next(pin for pin in start_block.pins if pin['uid'] == net['start_pin']['pin_uid'])
        start_pin_coordinates = (int(start_block.y + start_pin['y']*start_block.height), int(start_block.x + start_pin['x']*start_block.width))

        end_block = next(block for block in sram_blocks if block.uid == net['end_pin']['block_uid'])
        end_pin = next(pin for pin in end_block.pins if pin['uid'] == net['end_pin']['pin_uid'])
        end_pin_coordinates = (int(end_block.y + end_pin['y']*end_block.height), int(end_block.x + end_pin['x']*end_block.width))

        path = Astar(grid, start_pin_coordinates, end_pin_coordinates)
        for coordinates in path:
            grid[coordinates[0], coordinates[1]] = 1

        for coordinates in path:
            grid[coordinates[0], coordinates[1]] = 3    # Mark path on the grid

        color = next(colors)  # Cycle to next color
        for index in range(len(path) - 1):
            ax.plot([path[index][1], path[index + 1][1]], [path[index][0], path[index + 1][0]], color=color, linewidth=1)  # Drawing the path with the color
        ax.text((path[0][1] + path[-1][1]) / 2, (path[0][0] + path[-1][0]) / 2, net['uid'], fontsize=6, ha='center')  # Draw net uid in the middle of the net

    plt.show()

if __name__ == "__main__":
    boundary_height = 500
    boundary_width = 500

    min_width = 20
    max_width = 20
    min_height = 20
    max_height = 20
    num_blocks = 90
    min_pins_count = 1
    max_pins_count = 2

    obstacles_count = 4
    min_obstacle_width = 10
    max_obstacle_width = 20
    min_obstacle_height = 10
    max_obstacle_height = 20

    generate_input_json(min_width, max_width, min_height, max_height, min_pins_count, max_pins_count, num_blocks,
                        obstacles_count, min_obstacle_width, max_obstacle_width, min_obstacle_height, max_obstacle_height, "input.json")

    sram_blocks, nets, obstacles = load_blocks_from_json("input.json")
    min_spacing = 30
    grip_spacing = 15

    random_placement(sram_blocks, obstacles, boundary_height, boundary_width, min_spacing)
    visualize_initial_placement(sram_blocks, nets, obstacles, boundary_height, boundary_width)

    quadratic_placement(sram_blocks, boundary_height, boundary_width, min_spacing)
    visualize_initial_placement(sram_blocks, nets, obstacles, boundary_height, boundary_width)

    # Generate a 2D grid with the boundaries defined.
    grid = np.zeros((boundary_height, boundary_width))

    for obstacle in obstacles:
        grid[obstacle.y:obstacle.y + obstacle.height, obstacle.x:obstacle.x + obstacle.width] = 1

    # Mark all cells within a block as 1.
    for block in sram_blocks:
        xlim = min(int(block.x + block.width), boundary_width)
        ylim = min(int(block.y + block.height), boundary_height)
        grid[int(block.y):ylim, int(block.x):xlim] = 1

    # Mark all pins as 2.
    for block in sram_blocks:
        for pin in block.pins:
            pin_x = int(block.x + pin['x'] * block.width)
            pin_y = int(block.y + pin['y'] * block.height)
            grid[pin_y, pin_x] = 2

    # For every two pins in nets, calculate and print the shortest path.
    for net in nets:
        # Look for the start and end pins, and mark them as A and B.
        start_pin = next((block, pin) for block in sram_blocks for pin in block.pins if pin['uid'] == net['start_pin']['pin_uid'])
        end_pin = next((block, pin) for block in sram_blocks for pin in block.pins if pin['uid'] == net['end_pin']['pin_uid'])

        A = (int(start_pin[0].y + start_pin[1]['y'] * start_pin[0].height), int(start_pin[0].x + start_pin[1]['x'] * start_pin[0].width))
        B = (int(end_pin[0].y + end_pin[1]['y'] * end_pin[0].height), int(end_pin[0].x + end_pin[1]['x'] * end_pin[0].width))

        # Call A* and capture the result.
        path = Astar(grid, A, B)

        # Print the path.
        print(path)

    # within your main function
    for net in nets:
        start_block = next(block for block in sram_blocks if block.uid == net['start_pin']['block_uid'])
        start_pin = next(pin for pin in start_block.pins if pin['uid'] == net['start_pin']['pin_uid'])
        start_pin_coordinates = (int(start_block.y + start_pin['y'] * start_block.height),
                                 int(start_block.x + start_pin['x'] * start_block.width))

        end_block = next(block for block in sram_blocks if block.uid == net['end_pin']['block_uid'])
        end_pin = next(pin for pin in end_block.pins if pin['uid'] == net['end_pin']['pin_uid'])
        end_pin_coordinates = (
        int(end_block.y + end_pin['y'] * end_block.height), int(end_block.x + end_pin['x'] * end_block.width))

        path = Astar(grid, start_pin_coordinates, end_pin_coordinates)
        for coordinates in path:
            print(1)
            grid[coordinates[0], coordinates[1]] = 3

    print(2)
    visualize_placement_and_routing(sram_blocks, nets, grid, obstacles, boundary_height, boundary_width)
    print(3)
    # visualize_initial_placement(sram_blocks, nets, boundary_height, boundary_width)
    save_blocks_to_json(sram_blocks, 'output.json')

# This solution assumes that the coordinates (0,0) are at the bottom left of the boundary which is common mathematical convention.
# This solution also works perfectly if pins are at the center of grid cells.
# Whether (0,0) is at the top left or bottom left depends on your actual environment setup.