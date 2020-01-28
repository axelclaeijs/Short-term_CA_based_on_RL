import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib import cm
import Sources.configs.potentialFieldConfig as pfConfig
import math
from tqdm import tqdm
from Util.Utils import merge, unpack
from Util.Enums import Maptype, Area, FieldType
from scipy import interpolate
import Util.Utils as util
import scipy as sp
import scipy.ndimage

show_animation = True
beta = 1


def calc_potential_field(xmin, xmax, ymin, ymax, reso, rr, objects, gx, gy, mapType, fieldType):

    # scale
    minx = xmin - pfConfig.AREA_WIDTH
    miny = ymin - pfConfig.AREA_WIDTH
    maxx = xmax + pfConfig.AREA_WIDTH
    maxy = ymax + pfConfig.AREA_WIDTH
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))

    # Extract all coordinates
    coords = []
    for object in objects:
        if mapType == Maptype.waterways and object.area == Area.waterway:
            coords.extend(merge(object.x, object.y))
        if mapType == Maptype.boundaries and object.area == Area.boundary:
            coords.extend(merge(object.x, object.y))
        if mapType == Maptype.all:
            coords.extend(merge(object.x, object.y))


    # calc each potential
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in tqdm(range(xw)):
        x = ix * reso + minx

        for iy in range(yw):
            y = iy * reso + miny

            if fieldType == FieldType.attractive:
                p = calc_attractive_potential(x, y, gx, gy)
            if fieldType == FieldType.repulsive:
                p = calc_repulsive_potential_1(x, y, coords, rr)
                if p > 10:
                    p = 10
                p = -p

            pmap[ix][iy] = p

    return pmap, xw, yw


def filter(pmap, xw, yw):

    sigma_y = 5
    sigma_x = 5

    # Apply gaussian filter
    sigma = [sigma_y, sigma_x]
    return sp.ndimage.filters.gaussian_filter(pmap, sigma, mode='constant')


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * pfConfig.Gatt * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, nodes, rr):
    freptot = 0
    for node in nodes:
        dq = np.hypot(x - node[0], y - node[1])
        value = 0.5 * pfConfig.Grep * (1.0 / dq - 1.0 / rr) ** 2
        freptot += value

    return -math.log(freptot)


def calc_repulsive_potential_1(x, y, nodes, rr):
    ox, oy = unpack(nodes)

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

        return 0.5 * pfConfig.Grep * (1.0 / dq - 1.0 / rr) ** 2
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
        if xcnt == xw:
            break


def draw_3d_heatmap(data, xw, yw):

    #mean = 5
    #newData = np.clip(data, mean, max(map(max, data)))

    #newData = 10**np.array(data)

    # newData= util.scale(newData, 0, 1)

    # make data
    newData = np.array(data).T
    x = np.linspace(0, xw, xw)
    y = np.linspace(0, yw, yw)
    X, Y = np.meshgrid(x, y)

    # plot surface
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, newData, cmap=cm.Greys, linewidths=0)
    fig.colorbar(surf)

def draw_3d_heatmap_interpol(data, xw, yw):

    X, Y = np.mgrid[0:xw/2, 0:yw/2]
    X2, Y2 = np.mgrid[xw/2:xw, yw/2:yw]
    xnew, ynew = np.mgrid[0:xw, 0:yw]
    tck = interpolate.bisplrep(X, Y, data, s=0)
    tck2 = interpolate.bisplrep(X2, Y2, data, s=0)
    znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)

    fig = plt.figure(figsize=(12, 12))
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, data, cmap='summer', rstride=1, cstride=1, alpha=None)


    fig = plt.figure(figsize=(12, 12))
    ax = fig.gca(projection='3d')
    ax.plot_surface(xnew, ynew, znew, cmap='summer', rstride=1, cstride=1, alpha=None, antialiased=True)


def draw_2d_heatmap(data, routeX, routeY, xw, yw):

    data = np.array(data)
    x, y = np.mgrid[0:xw, 0:yw]

    plt.figure()
    plt.pcolor(x, y, data, cmap=cm.Greys)
    plt.plot(routeX, routeY)
    plt.colorbar()

def draw_2d(data, xw, yw):

    x, y = np.mgrid[0:xw, 0:yw]
    sigma_y = 5
    sigma_x = 5

    plt.figure()
    plt.imshow(data, interpolation='nearest')
    plt.xlabel("$x$")
    plt.ylabel("$y$")

    # Apply gaussian filter
    sigma = [sigma_y, sigma_x]
    y = sp.ndimage.filters.gaussian_filter(data, sigma, mode='constant')

    # Display filtered array
    plt.imshow(y, cmap='Blues', interpolation='nearest')
    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$\sigma_x = " + str(sigma_x) + "\quad \sigma_y = " + str(sigma_y) + "$")


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
        draw_3d_heatmap(pmap, xw, yw)


if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")
