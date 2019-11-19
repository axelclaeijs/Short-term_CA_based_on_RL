import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import Sources.configs.potentialFieldConfig as pfConfig
import math
import sys

show_animation = True


def calc_potential_field(xmin, xmax, ymin, ymax, sx, sy, gx, gy, ox, oy, reso, rr):
    countx = 0
    county = 0

    minx = min(ox) - pfConfig.AREA_WIDTH / 2.0
    miny = min(oy) - pfConfig.AREA_WIDTH / 2.0
    maxx = max(ox) + pfConfig.AREA_WIDTH / 2.0
    maxy = max(oy) + pfConfig.AREA_WIDTH / 2.0
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))

    # calc each potential
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in range(xw):
        countx += 1
        x = ix * reso + minx

        for iy in range(yw):
            county += 1
            y = iy * reso + miny
            ug = 0#calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            uf = ug + uo
            pmap[ix][iy] = uf

        print countx, ' ', county

    return pmap, xw, yw


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * pfConfig.Gatt * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, ox, oy, rr):

    # search nearest obstacle
    minid = -1
    dmin = float("inf")
    for i, _ in enumerate(ox):
        d = np.hypot(x - ox[i], y - oy[i])
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential
    dq = np.hypot(x - ox[minid], y - oy[minid])

    if dq <= rr:
        if dq <= 0.1:
            dq = 0.1

        value = 0.5 * pfConfig.Grep * (1.0 / dq - 1.0 / rr) ** 2
        return value
    else:
        return 0.0


def draw_heatmap(data, xw, yw):
    # make data
    data = np.array(data).T
    x = np.linspace(0, xw, xw)
    y = np.linspace(0, yw, yw)
    X, Y = np.meshgrid(x, y)

    # plot surface
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, data, cmap=cm.coolwarm)
    fig.colorbar(surf)
    plt.show()


def main():
    print("potential_field_planning start")

    sx = 0.0  # start x position [m]
    sy = 10.0  # start y positon [m]
    gx = 30.0  # goal x position [m]
    gy = 30.0  # goal y position [m]
    grid_size = 1  # potential grid size [m]
    robot_radius = 10.0  # robot radius [m]

    ox = [15.0, 5.0, 20.0, 25.0]  # obstacle x position list [m]
    oy = [25.0, 15.0, 26.0, 25.0]  # obstacle y position list [m]

    # calc potential field
    pmap, xw, yw = calc_potential_field(0,0,0,0,sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    if show_animation:
        draw_heatmap(pmap, xw, yw)


if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
