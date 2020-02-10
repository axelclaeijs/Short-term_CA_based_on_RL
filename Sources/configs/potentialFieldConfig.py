#!/usr/bin/env python

# PF's parameters
Gatt = 5.0  # attractive potential gain
GrepG = 500  # repulsive potential gain
GrepL = 100  # repulsive potential gain for trajectories
AREA_WIDTH = 0.0  # potential area width [m]
grid_size = 10  # potential grid size [m]

# ships parameters
shipID = 0
slon = 3.7455  # start lon position
slat = 51.1118  # start lat positon
robot_radius = float("inf") #50.0  # robot radius [m]

# Viewrange ship
front = 100
back = 100
left = 100
right = 100

# goals parameters
glon = 3.7359  # goal lon position
glat = 51.0808 # goal lat position

# DB parameters
database = 'map'

# Start and stop coords
shipCoords = [[[3.757,51.113],[3.736,51.111]],[[3.72696,51.1032],[3.7255,51.0877]]]#,[[3.7455,51.1118],[3.7359,51.0808]],[[3.759,51.123],[3.72673,51.077]]]
# Ships speed in knots
shipSpeeds = [7, 8, 9]

# Interpolation
ds = 50     # Space between nodes for interpolation