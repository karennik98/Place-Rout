import math
import random
import copy
import networkx as nx
from networkx.algorithms import community
import numpy as np
from scipy.optimize import minimize

#####################################################################
def cost(rectangles):
    # The cost function calculating total Manhattan distances between each pair of connected points
    total_cost = 0
    for rectangle in rectangles:
        for point in rectangle.points:
            source_coords = (rectangle.x + point.x * rectangle.width, rectangle.y + point.y * rectangle.height)
            for rect in rectangles:
                for p in rect.points:
                    if p.id == point.connection:
                        dest_coords = (rect.x + p.x * rect.width, rect.y + p.y * rect.height)
                        total_cost += abs(dest_coords[0] - source_coords[0]) + abs(dest_coords[1] - source_coords[1])
                        break
    return total_cost
def simulated_annealing_placement(rectangles):
    # The temperature parameter
    T = 100
    Tmin = 0.01

    # Decrease rate of the temperature
    alpha = 0.9

    while T > Tmin:
        # Create a new solution for comparison
        new_rectangles = rectangles

        selected = random.choice(new_rectangles)
        selected.x += random.uniform(0, 20)
        selected.y += random.uniform(0, 20)

        # Original cost and new cost
        old_cost = cost(rectangles)
        new_cost = cost(new_rectangles)

        # Accept the new solution if it is better, or with a certain probability if it is worse
        if new_cost < old_cost or random.uniform(0, 1) < math.exp((old_cost - new_cost) / T):
            rectangles = new_rectangles

        T = T * alpha

    return rectangles
#####################################################################

#####################################################################
def F_repulsion(q, k=100):
    return k / (q*q)
def F_attraction(x, k=0.1):
    return k * x
def force_directed_placement(rectangles):
    for _ in range(200):  # Number of iterations
        for rec1 in rectangles:
            F_total = [0, 0]  # Total force on rec1
            for rec2 in rectangles:
                if rec1 != rec2:
                    # Compute Euclidean distance between rec1 and rec2
                    dx = rec1.x - rec2.x
                    dy = rec1.y - rec2.y
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance < 1:  # To avoid division by zero
                        distance = 1

                    # Compute unit vector direction of the force
                    direction = [dx/distance, dy/distance]

                    # Compute force and update total force
                    F = F_repulsion(distance)
                    F_total[0] += F * direction[0]
                    F_total[1] += F * direction[1]

            # Add attractive forces
            for point in rec1.points:
                for rec2 in rectangles:
                    for point2 in rec2.points:
                        if point.connection == point2.id:
                            dx = rec1.x - rec2.x
                            dy = rec1.y - rec2.y
                            distance = math.sqrt(dx*dx + dy*dy)

                            direction = [dx/distance, dy/distance]

                            F = F_attraction(distance)
                            F_total[0] -= F * direction[0]
                            F_total[1] -= F * direction[1]

            # Update the position of the rectangle according to the total force on it
            rec1.x += F_total[0]
            rec1.y += F_total[1]
#####################################################################

#####################################################################
def total_wirelength(rectangles):
    total = 0
    for rectangle in rectangles:
        for point in rectangle.points:
            for rect2 in rectangles:
                for point2 in rect2.points:
                    if point.connection == point2.id:
                        dx = (rectangle.x + point.x * rectangle.width) - (rect2.x + point2.x * rect2.width)
                        dy = (rectangle.y + point.y * rectangle.height) - (rect2.y + point2.y * rect2.height)
                        total += dx*dx + dy*dy  # squared euclidean distance
    return total
# def quadratic_placement(rectangles):
#     # Initial solution
#     pos = [coordinate for rectangle in rectangles for coordinate in [rectangle.x, rectangle.y]]
#
#     # Define optimization function
#     def func(flattened_pos):
#         for i, rectangle in enumerate(rectangles):
#             rectangle.x, rectangle.y = flattened_pos[i*2], flattened_pos[i*2 + 1]
#         return total_wirelength(rectangles)
#
#     # Run optimization
#     result = minimize(func, pos, method='Powell')
#
#     # Update rectangles with optimized positions
#     for i, rectangle in enumerate(rectangles):
#         rectangle.x, rectangle.y = result.x[i*2], result.x[i*2 + 1]
#
#     return rectangles
#####################################################################

#####################################################################
# def place_rectangles(rectangles, width_limit, height_limit):
#     # Randomly place rectangles in distinct positions
#     positions = [(i, j) for i in range(width_limit) for j in range(height_limit)]
#     random.shuffle(positions)
#     for rectangle in rectangles:
#         rectangle.x, rectangle.y = positions.pop(0)
#
#     # Continue adjusting positions until no overlaps
#     while True:
#         has_overlap = False
#         for rect1 in rectangles:
#             for rect2 in rectangles:
#                 if rect1 != rect2 and is_overlap(rect1, rect2):
#                     has_overlap = True
#                     # Calculate direction of repulsive force
#                     dir_x, dir_y = 0, 0
#                     if rect1.x < rect2.x: dir_x = -1
#                     elif rect1.x > rect2.x: dir_x = 1
#                     if rect1.y < rect2.y: dir_y = -1
#                     elif rect1.y > rect2.y: dir_y = 1
#                     # Apply repulsive force to rect1 (move away from rect2)
#                     rect1.x += dir_x
#                     rect1.y += dir_y
#         if not has_overlap:
#             break
def is_overlap(rect1, rect2):
    return not (rect1.x >= rect2.x + rect2.width or rect1.x + rect1.width <= rect2.x or rect1.y >= rect2.y + rect2.height or rect1.y + rect1.height <= rect2.y)
#####################################################################

#####################################################################
def min_cut_partition(rectangles):
    # Build graph
    G = nx.Graph()

    # Include a node for each rectangle
    for rectangle in rectangles:
        G.add_node(rectangle.id)

    # Include an edge for each rectangle that has a point of connection with another rectangle
    for rectangle in rectangles:
        for point in rectangle.points:
            for rect in rectangles:
                if point.connection in [p.id for p in rect.points]:
                    G.add_edge(rectangle.id, rect.id)

    # Apply Kernighan–Lin bipartition to divide into two groups
    partition = community.kernighan_lin.kernighan_lin_bisection(G)

    return partition

def place_groups(rectangles):
    # Step 1: Partitioning
    partition = min_cut_partition(rectangles)

    # Prepare two lists to store the positions of the rectangles in each partition
    placed_rectangles = [[], []]

    # Step 2: Placement
    for i, group in enumerate(partition):
        # Use deep copy to create a new independent list of rectangles
        group_rects = copy.deepcopy([rect for rect in rectangles if rect.id in group])

        # Use either simulated annealing or force-directed to place the rectangles
        placed_group = simulated_annealing_placement(group_rects)  # Or use force_directed_placement()
        placed_rectangles[i] = placed_group

    # Adjust position of the second group so that it is placed next to the first one
    x_adjust = max(
        rect.x + rect.width for rect in placed_rectangles[0]) + 2  # Plus 2 for a small gap between the groups
    for rect in placed_rectangles[1]:
        rect.x += x_adjust

    # Combine the rectangles from both groups
    return placed_rectangles[0] + placed_rectangles[1]
#####################################################################


def quadratic_placement(rectangles):
    # Number of rectangles
    n = len(rectangles)

    # Compute the total wirelength for a placement
    def total_wirelength(pos):
        pos = pos.reshape((n, 2))
        # Assign new positions to rectangles
        for rect, p in zip(rectangles, pos):
            rect.x, rect.y = p
        # Compute total wirelength
        total = 0
        for rectangle in rectangles:
            for point in rectangle.points:
                source_coords = (rectangle.x + point.x * rectangle.width, rectangle.y + point.y * rectangle.height)
                for rect2 in rectangles:
                    for point2 in rect2.points:
                        if point.connection == point2.id:
                            dest_coords = (rect2.x + point2.x * rect2.width, rect2.y + point2.y * rect2.height)
                            total += abs(dest_coords[0] - source_coords[0]) + abs(dest_coords[1] - source_coords[1])
        return total

    # random initial positions
    x0 = np.random.rand(n, 2).flatten()

    # Execute optimizer
    result = minimize(total_wirelength, x0)

    # Return the rectangles with the new placement
    return rectangles


def rectangular_placement(rectangles):
    # # Random initial placement
    # for rectangle in rectangles:
    #     rectangle.x = random.uniform(0, 100)
    #     rectangle.y = random.uniform(0, 100)

    # Legalization: Shift overlapping rectangles to the right
    sorted_rectangles = sorted(rectangles, key=lambda rectangle: rectangle.x)
    current_x = 0

    for rectangle in sorted_rectangles:
        if rectangle.x < current_x:  # Check if rectangle overlaps with the previous one
            rectangle.x = current_x  # If overlap, move it to the right of the previous one
        current_x = rectangle.x + rectangle.width
    return rectangles
