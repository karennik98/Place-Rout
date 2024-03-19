from utilities import *
from utilities import initialize_positions

from visual import *
from placement import *
from routing import *

rectangles = read_json('changed.json')

# initialize_positions(rectangles)
visualize_rectangles(rectangles)

# Check if placement is valid
if not check_within_bounds(rectangles, 200, 200) or not check_overlap(rectangles):
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

# visualize_rectangles_and_wires(rectangles, route_wire_a_star2)
visualize_rectangles_and_wires2(rectangles)