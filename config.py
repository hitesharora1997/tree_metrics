"""
Configuration parameters for the tree metrics calculation project.
"""
# DBH (Diameter at Breast Height) measurement parameters
DBH_HEIGHT = 1.3  # meters above ground
DBH_TOLERANCE = 0.05  # ±5cm around the DBH height
DBH_MIN_POINTS = 5  # Minimum number of points needed for reliable DBH calculation

# Classification values
GROUND_CLASS = 0
TRUNK_CLASS = 1
BRANCH_CLASS = 2
CANOPY_CLASS = 3

# Output parameters
DEFAULT_OUTPUT_FILE = "outputs/tree_metrics.csv"

# Visualization parameters
POINT_SIZE = 3
COLOR_MAP = "jet"