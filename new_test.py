# import json
# import random
# import numpy as np
# from scipy.optimize import minimize
# import json
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import json
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
#
#
# def generate_data(max_height, max_width, blocks_count, nets_count, matrix_width, matrix_height):
#     blocks = []
#     occupied = [[0] * matrix_width for _ in range(matrix_height)]
#     max_height = min(max_height, matrix_height)
#     max_width = min(max_width, matrix_width)
#
#     def is_place_free(x, y, width, height):
#         if x + width > matrix_width or y + height > matrix_height:
#             return False
#         for i in range(y, y + height):
#             for j in range(x, x + width):
#                 if occupied[i][j] == 1:
#                     return False
#         return True
#
#     def mark_as_occupied(x, y, width, height):
#         for i in range(y, y + height):
#             for j in range(x, x + width):
#                 occupied[i][j] = 1
#
#     def generate_pins(x, y, width, height):
#         return [(x, y), (x + width - 1, y), (x, y + height - 1), (x + width - 1, y + height - 1)]
#
#     for i in range(1, blocks_count + 1):
#         for _ in range(10000):
#             width = random.randint(1, max_width)
#             height = random.randint(1, max_height)
#             x = random.randint(0, matrix_width - 1)
#             y = random.randint(0, matrix_height - 1)
#             if is_place_free(x, y, width, height):
#                 pins = generate_pins(x, y, width, height)
#                 blocks.append({
#                     "id": "B" + str(i),
#                     "width": width,
#                     "height": height,
#                     "x": x,
#                     "y": y,
#                     "pins": pins
#                 })
#                 mark_as_occupied(x, y, width, height)
#                 break
#
#     nets = []
#     for i in range(1, nets_count + 1):
#         conn_blocks = random.sample(blocks, min(blocks_count, random.randint(2, 4)))
#         # randomly connect to block's pins
#         conns = [(block, random.choice(block['pins'])) for block in conn_blocks]
#         converted_conns = ["%s:P%s" % (block['id'], block['pins'].index(conn)) for block, conn in conns]
#         nets.append({
#             "id": "N" + str(i),
#             "connections": converted_conns
#         })
#
#     data = {
#         "blocks": blocks,
#         "nets": nets
#     }
#
#     with open('data.json', 'w') as f:
#         json.dump(data, f, indent=4)
#
#
#
#
# def visualize_data(filename):
#     with open(filename, 'r') as f:
#         data = json.load(f)
#
#     fig, ax = plt.subplots()
#
#     blocks = data['blocks']
#     nets = data['nets']
#
#     for block in blocks:
#         x = block['x']
#         y = block['y']
#         width = block['width']
#         height = block['height']
#         pins = block['pins']
#         rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
#         ax.add_patch(rect)
#         for pin in pins:
#             plt.plot(*pin, marker='o', markersize=3, color='blue')
#
#     for net in nets:
#         conns_for_net = []
#         for connection in net['connections']:
#             block_id, _, pin_index = connection.partition(':')
#             pin_index = int(pin_index[1:])
#             pin = next(block['pins'][pin_index] for block in blocks if block['id'] == block_id)
#             # add to list of connections for this net
#             conns_for_net.append(pin)
#             # draw pin for connection
#             plt.plot(*pin, marker='o', markersize=5, color='green')
#         # draw line connecting all pins for this net
#         plt.plot(*zip(*conns_for_net), linewidth=1, linestyle='-.')
#
#     plt.grid(True)
#     plt.show()
#
# def visualize_placement2(blocks):
#     fig, ax = plt.subplots()
#     for block in blocks:
#         x = block['x']
#         y = block['y']
#         width = block['width']
#         height = block['height']
#         rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
#         ax.add_patch(rect)
#     plt.grid(True)
#     plt.show()
#
# def quadratic_placement(blocks, nets):
#     block_positions = {block['id']: np.array([block['x'], block['y']], dtype=float) for block in blocks}
#
#     def objective(X):
#         cost = 0
#         X = X.reshape(-1, 2)
#         for net in nets:
#             for connection in net['connections']:
#                 block_id, _, pin_index = connection.partition(':')
#                 pin_index = int(pin_index[1:])
#                 block_index = int(block_id[1:]) - 1
#                 pin = blocks[block_index]['pins'][pin_index]
#                 cost += np.sum((X[block_index, :] - pin) ** 2)
#         return cost
#
#     X0 = np.array([pos for pos in block_positions.values()])
#     X0 = X0.flatten()
#     bounds = [(0, 1) for _ in blocks for _ in range(2)]
#     result = minimize(objective, X0, bounds=bounds, method='L-BFGS-B')
#
#     print("Optimization result: ", result)  # Adde print statement here.
#
#     for i, block in enumerate(blocks):
#         block['x'] = result.x[i*2]
#         block['y'] = result.x[i*2 + 1]
#
#     return blocks
#
# def read_and_optimize(filename):
#     with open(filename, 'r') as f:
#         data = json.load(f)
#
#     blocks = data['blocks']
#     nets = data['nets']
#
#     optimized_blocks = quadratic_placement(blocks, nets)
#     visualize_placement2(optimized_blocks)
#
#
# # Save the data to a file
# generate_data(5, 5, 10, 5, 20, 20)
# # Visualize the data
# visualize_data('data.json')
#
# # Optimize and visualize the layout
# read_and_optimize('data.json')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def parse_file(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        blocks = {}
        nets = {}
        rows = []
        block_x = 0
        block_y = 0
        while line:
            if line.startswith('.NumBlocks'):
                num_blocks = int(line.split(':')[1].strip())

            elif line.startswith('.NumNets'):
                num_nets = int(line.split(':')[1].strip())

            elif line.startswith('.NumRows'):
                num_rows = int(line.split(':')[1].strip())

            elif line.startswith('U'):
                split_line = line.split()
                # width = int(split_line[1])
                # # If the block can't fit into current row, move it to the next one
                # if block_x + width > len(rows[block_y]):
                #     block_y += 1
                #     block_x = 0
                blocks[split_line[0]] = (int(split_line[1]), int(split_line[2]))
                # block_x += width

            elif line.startswith('N'):
                nets[line.split(':')[0].strip()] = line.split(':')[1].strip().split()

            elif line.startswith('ROW'):
                row_width = int(line.split(':')[1].strip())
                row_info = np.zeros(row_width)
                rows.append(row_info)

            line = f.readline()

    return blocks, nets, rows


def plot_design(blocks, nets, rows):
    # Create figure and axes
    fig, ax = plt.subplots(1)

    # Display the Rows
    for i, row in enumerate(rows):
        ax.add_patch(patches.Rectangle((0, i), len(row), 1, edgecolor='blue', facecolor='none'))

    # Display the Blocks and Nets
    for block, value in blocks.items():
        ax.add_patch(patches.Rectangle((value[2], value[3]), value[0], value[1], edgecolor='black', facecolor='grey'))

    for net, net_blocks in nets.items():
        for i in range(len(net_blocks) - 1):
            x1 = blocks[net_blocks[i]][2] + blocks[net_blocks[i]][0] / 2  # center x of the first block
            y1 = blocks[net_blocks[i]][3] + blocks[net_blocks[i]][1] / 2  # center y of the first block
            x2 = blocks[net_blocks[i + 1]][2] + blocks[net_blocks[i + 1]][0] / 2  # center x of the next block
            y2 = blocks[net_blocks[i + 1]][3] + blocks[net_blocks[i + 1]][1] / 2  # center y of the next block
            ax.plot([x1, x2], [y1, y2], 'r-')

    plt.grid(True)
    plt.show()


# Call the functions
blocks, nets, rows = parse_file("input_file.txt")
plot_design(blocks, nets, rows)

