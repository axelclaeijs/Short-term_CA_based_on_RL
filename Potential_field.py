import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import Sources.configs.potentialFieldConfig as pfConfig
import math
import sys
import Util.Transform as transform

show_animation = True
beta = 1

def calc_potential_field(xmin, xmax, ymin, ymax, sx, sy, gx, gy, nodes, reso, rr, objects):
    count = 0

    # scale
    minx = xmin - pfConfig.AREA_WIDTH
    miny = ymin - pfConfig.AREA_WIDTH
    maxx = xmax + pfConfig.AREA_WIDTH
    maxy = ymax + pfConfig.AREA_WIDTH
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))

    # calc each potential
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in range(xw):
        x = ix * reso + minx

        for iy in range(yw):
            count += 1
            y = iy * reso + miny
            ug = 0  # calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential_3(x, y, nodes, rr)
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap, xw, yw


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * pfConfig.Gatt * np.hypot(x - gx, y - gy)


def calc_repulsive_potential_3(x, y, nodes, rr):
    freptot = 0
    for node in nodes:
        dq = np.hypot(x - node[0], y - node[1])
        value = 0.5 * pfConfig.Grep * (1.0 / dq - 1.0 / rr) ** 2
        freptot += value

    return -math.log(freptot)


def calc_repulsive_potential_2(x, y, objects, rr):
    freptot = 0
    cntObj = 0
    usedNodeList = []
    for object in objects:
        if (object.area):
            for i,_ in enumerate(object.xy[0]):
                dq = np.hypot(x - object.xy[0][i], y - object.xy[1][i])
                if not([object.xy[0][i], object.xy[1][i]] in usedNodeList):
                    value = 0.5 * pfConfig.Grep * (1.0 / dq - 1.0 / rr) ** 2
                    freptot += value
                    usedNodeList.append([object.xy[0][i], object.xy[1][i]])

            cntObj += 1

    return -math.log(freptot)


def calc_repulsive_potential(x, y, objects, rr):

    # search nearest obstacle
    minid = [-1, -1]    # [id of node, id of object]
    dmin = float("inf")
    for object in objects:
        for i,_ in enumerate(object.xy[0]):
            d = np.hypot(x - object.xy[0][i], y - object.xy[1][i])
            if dmin >= d:
                dmin = d
                minid = [i, object.id]

    if not(minid == [0, 0]):# and not(x == objects[minid[1]].xy[0][minid[0]]) and not(y == objects[minid[1]].xy[1][minid[0]]):
        # calc repulsive potential
        dq = np.hypot(x - objects[minid[1]].xy[0][minid[0]], y - objects[minid[1]].xy[1][minid[0]])

        if dq <= rr:
            if dq <= 0.1:
                dq = 0.1

            value = 0.5 * pfConfig.Grep * (1.0 / dq - 1.0 / rr) ** 2

            if (objects[minid[1]].area):
                return math.log(value)
            else:
                return 0
        else:
            return 0.0
    else:
        return 0.0


def draw_slice_heatmap(data, xw):
    xcnt = 0

    plt.figure()
    plt.ion()
    plt.show()

    while 1:

        # make data
        y = np.array(data[xcnt]).T
        x = np.linspace(0, xw, xw)

        plt.plot(x, y)
        plt.draw()
        plt.pause(0.001)

        input = raw_input("type in enter")
        if input == "":
            xcnt += 1
            plt.clf()
        if input == "0":
            break
        if xcnt == 791:
            break


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
