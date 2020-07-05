"""Global variables for the app

Variables:
	RANDOM_LEVEL {bool} -- If the level is generated randomly
	GAME_SPEED {number} -- The game speed in MS
	NUMBER_SIMULATION {number} -- Number of simulation
	CASE_SIZE {number} -- Size of tile in pixel
	WIDTH {number} -- Tile width
	HEIGHT {number} -- Tile height
	FRAME_LIST {dict} -- List of frame for the app
	FRAME_ACTIVE {number} -- The active frame
"""

RANDOM_LEVEL = True
GAME_SPEED = 50
NUMBER_SIMULATION = 2000
CASE_SIZE = 50
WIDTH = 20
HEIGHT = 20

FRAME = None
CANVAS = None

FRAME_LIST = {}
FRAME_ACTIVE = 0
