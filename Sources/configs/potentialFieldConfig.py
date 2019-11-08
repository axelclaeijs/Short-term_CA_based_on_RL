#!/usr/bin/env python

mysql = {'host': 'localhost',
         'user': 'root',
         'passwd': 'my secret password',
         'db': 'write-math'}

# PF's parameters
Gatt = 5.0  # attractive potential gain
Grep = 100.0  # repulsive potential gain
AREA_WIDTH = 100.0  # potential area width [m]
grid_size = 1  # potential grid size [m]

# ships parameters
slon = 3.7408  # start lon position
slat = 51.1064  # start lat positon
robot_radius = 1000  # robot radius [m]

# Viewrange ship
front = 800
back = 200
left = 500
right = 500

# goals parameters
gx = 30.0  # goal x position [m]
gy = 30.0  # goal y position [m]
