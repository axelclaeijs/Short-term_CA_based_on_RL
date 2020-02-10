import numpy as np
import Sources.configs.potentialFieldConfig as pfConfig
import matplotlib.pyplot as plt
import Util.Transform as transform
import Util.Utils as util

# Possible movements of the ship
def get_motion_model():

    motion = [[1, 0],
              [0, 1],
              [-1, 0],
              [0, -1],
              [-1, -1],
              [-1, 1],
              [1, -1],
              [1, 1]]

    return motion


# Calculate ideal path from start to goal
def potential_field_planning(sx, sy, gx, gy, pmap, minx, miny, maxx, maxy, objects):

    gain = 1
    xp = 0
    yp = 0
    xpprev = -1
    ypprev = -1
    xpprevprev = -2
    ypprevprev = -2

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round(sx / pfConfig.grid_size)
    iy = round(sy / pfConfig.grid_size)
    gix = round(gx / pfConfig.grid_size)
    giy = round(gy / pfConfig.grid_size)

    rx, ry = [sx], [sy]
    motion = get_motion_model()
    while d >= pfConfig.grid_size:
        minp = float("inf")
        minix, miniy = -1, -1
        for i, _ in enumerate(motion):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            if inx >= len(pmap) or iny >= len(pmap[0]):
                p = float("inf")  # outside area
            else:
                p = pmap[inx][iny]
            if minp > p:
                minp = p
                minix = inx
                miniy = iny
        ix = minix
        iy = miniy

        xpprevprev = xpprev
        ypprevprev = ypprev
        xpprev = xp
        ypprev = yp
        xp = ix * pfConfig.grid_size
        yp = iy * pfConfig.grid_size

        d = np.hypot(gx - xp, gy - yp)
        print d
        print (xp, yp)

        if (xp == xpprev and yp == ypprev) or (xp == xpprevprev and yp == ypprevprev):
            gain += 10
        else:
            gain = 1
            rx.append(xp)
            ry.append(yp)

        motion = np.array(get_motion_model()) * gain

    return rx, ry


def calcDistanceTrajectory(x,y):
    """
    Return list with distances between trajectory-coords
    :param x: x-coords of trajectory
    :param y: y-coords of trajectory
    :return: list of distances
    """
    distanceTrajectory = []

    for i in range(len(x) - 1):
        distanceTrajectory.append(transform.distanceXY(x[i], y[i], x[i+1], y[i+1]))

    return distanceTrajectory


def calcPositionOnTrajectory(ship, time):
    """
    Given a speed and time, return the position of the ship on its trajectory
    speed [m/h]
    x, y trajectory [m]
    time from start [hh:mm:ss]
    """
    splitTime = time.split(":")
    hours = float(splitTime[0]) + (float(splitTime[1]) * 1/60) + (float(splitTime[2]) * 1/3600)

    distance = util.knotsToMperh(ship.knots) * hours

    d = float("inf")
    d_temp = 0
    index = 0

    for i in range(len(ship.distanceTrajectory)):
        dev = d_temp - distance
        if abs(dev) <= d:
            d = abs(dev)
            index = i
        d_temp += ship.distanceTrajectory[i]



    return ship.x[index], ship.y[index]

def calcTimeForTrajectory(ship):
    """
    Calculate the time done over the trajectory
    :param ship: with speed and trajectory distances
    :return: time [h]
    """

    distance = sum(ship.distanceTrajectory)
    time = distance / util.knotsToMperh(ship.knots)

    return time
