import matplotlib.pyplot as plt
import matplotlib.patches as patches
from routing import *

def visualize_rectangles_and_wires(rectangles, routing_algorithm, space_width, space_height):
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
            path = routing_algorithm(rectangles, rectangle, point, space_width, space_height)
            print('1')
            for node_1, node_2 in zip(path[:-1], path[1:]):
                ax.plot([node_1[0], node_2[0]], [node_1[1], node_2[1]], 'b-')

    ax.set_xlim([0, max([r.x + r.width for r in rectangles]) + 10])
    ax.set_ylim([0, max([r.y + r.height for r in rectangles]) + 10])
    plt.axis('equal')
    plt.show()

def visualize_rectangles(rectangles):
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
                (rectangle.x, rectangle.y),   # (x,y)
                rectangle.width,              # width
                rectangle.height,             # height
                fill=True,
                alpha=0.3,
                edgecolor='black',  # Outline color
                linewidth=0.5  # Outline thickness
            )
        )
        # Adding rectangle id
        ax.text(rectangle.x, rectangle.y - 2, rectangle.id)
        for point in rectangle.points:
            point_coords = (rectangle.x + point.x * rectangle.width, rectangle.y + point.y * rectangle.height)
            ax.plot(*point_coords, 'ro')
            # Adding point id
            ax.text(point_coords[0], point_coords[1], f'id: {point.id}')

    # Add wires
    for rectangle in rectangles:
        for point in rectangle.points:
            if point.connection in point_dict:
                connected_point_coords = point_dict[point.connection]
                ax.plot([rectangle.x + point.x * rectangle.width, connected_point_coords['x']],
                        [rectangle.y + point.y * rectangle.height, connected_point_coords['y']], 'b-')

    ax.set_xlim([0, max([r.x + r.width for r in rectangles]) + 10])
    ax.set_ylim([0, max([r.y + r.height for r in rectangles]) + 10])
    plt.show()


def visualize_rectangles_and_wires2(rectangles, space_width, space_height):
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
                fill=True, alpha=0.3, edgecolor='black', linewidth=1  # Added border to rectangle
            )
        )

        # Adding rectangle id
        ax.text(rectangle.x, rectangle.y - 2, rectangle.id, fontsize=8)

        for point in rectangle.points:
            point_coords = (rectangle.x + point.x * rectangle.width, rectangle.y + point.y * rectangle.height)
            ax.plot(*point_coords, 'ro')

            # Adding point id
            ax.text(point_coords[0], point_coords[1], f'id: {point.id}', fontsize=8)

            path = route_wire_a_star2(rectangles, rectangle, point, space_width, space_height)  # draw path between points
            for node_1, node_2 in zip(path[:-1], path[1:]):
                ax.plot([node_1[0], node_2[0]], [node_1[1], node_2[1]], 'b-')

    ax.set_xlim([0, max([r.x + r.width for r in rectangles]) + 10])
    ax.set_ylim([0, max([r.y + r.height for r in rectangles]) + 10])

    plt.axis('equal')
    plt.show()