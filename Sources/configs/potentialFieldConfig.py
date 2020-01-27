#!/usr/bin/env python

mysql = {'host': 'localhost',
         'user': 'root',
         'passwd': 'my secret password',
         'db': 'write-math'}

# PF's parameters
Gatt = 5.0  # attractive potential gain
Grep = 1.0  # repulsive potential gain
AREA_WIDTH = 0.0  # potential area width [m]
grid_size = 1  # potential grid size [m]

# ships parameters
slon = 3.7455  # start lon position
slat = 51.1118  # start lat positon
robot_radius = float("inf") #50.0  # robot radius [m]

# Viewrange ship
front = 800
back = 200
left = 500
right = 500

# goals parameters
glon = 3.7359  # goal lon position
glat = 51.0808 # goal lat position
