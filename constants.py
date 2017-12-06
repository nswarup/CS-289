# note: width/height are always from the perspective of the screen

# directions
UP = 0
DOWN = 1

# car dimensions
CAR_WIDTH = 15
CAR_HEIGHT = 7
CAR_DIMENSIONS = (CAR_WIDTH, CAR_HEIGHT)
CAR_COLOR = (230, 0, 0) # dark red

# lane dimensions
LANES = 4
LANE_HEIGHT = CAR_HEIGHT + 15
LANE_HASH_WIDTH = 10
LANE_HASH_HEIGHT = 2
LANE_HASH_DIMENSIONS = (LANE_HASH_WIDTH, LANE_HASH_HEIGHT)
LANE_HASH_SPACING = 5
LANE_COLOR = (255, 255, 255)

# screen attributes (based on number of lanes)
VERTICAL_MARGIN = 40
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = LANES * LANE_HEIGHT + 2 * VERTICAL_MARGIN
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 10

# if `False`, will not display visualization or sleep at each loop iteration
VISUALIZING = True

# if `False`, will not check for collisions at each time step
CHECKING_COLLISIONS = True

# macro to handle screen wraparounds
def handle_laps(car):
    if car.pos >= SCREEN_WIDTH:
        car.pos -= SCREEN_WIDTH
        car.lap += 1

# names of simulator classes
SIMULATION_NAMES = [
    'TestSim',
    'SingleLaneIDM',
    'MultiLaneIDM',
    'LaneSwitchIDM'
]
