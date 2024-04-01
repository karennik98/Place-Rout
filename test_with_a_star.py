from utilities import *
from utilities import initialize_positions

from visual import *
from placement import *
from routing import *

space_width = 200
space_height = 200

generate_rectangle_data(20, 2, space_width, space_height)
rectangles = read_json('rectangle_data.json')
visualize_rectangles(rectangles)

rectangles = quadratic_placement(rectangles)
rectangles = rectangular_placement(rectangles)  # Avoids overlaps and keeps rectangles in bounds
visualize_rectangles(rectangles)


# rectangles = place_groups(rectangles)
# visualize_rectangles(rectangles)

# Check if placement is valid
if not check_within_bounds(rectangles, space_width, space_height) or not check_overlap(rectangles):
    print("Invalid placement of rectangles.")

# place_rectangles(rectangles, 200, 200)  # Define the width and height limits according to your design area
# visualize_rectangles(rectangles)
# Save the rectangles to JSON after placement
# write_to_json('changed.json', rectangles)


# rectangle = quadratic_placement(rectangles)
# visualize_rectangles(rectangles)
#
# rectangle = force_directed_placement(rectangles)
# visualize_rectangles(rectangles)
#
# rectangles = simulated_annealing_placement(rectangles)
# visualize_rectangles(rectangles)

# visualize_rectangles_and_wires(rectangles, route_wire_a_star, space_width=space_width, space_height=space_height)
visualize_rectangles_and_wires2(rectangles, space_width=space_width, space_height=space_height)