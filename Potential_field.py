import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from matplotlib import cm
import Sources.configs.potentialFieldConfig as pfConfig
from tqdm import tqdm
from Util.Utils import merge, unpack
from Util.Enums import Maptype, Area, FieldType
import scipy as sp
import scipy.ndimage

show_animation = True
beta = 1

# Apply Gaussian filter to map
def filter(pmap, xw, yw):

    sigma_y = 5
    sigma_x = 5

    # Apply gaussian filter
    sigma = [sigma_y, sigma_x]
    return sp.ndimage.filters.gaussian_filter(pmap, sigma, mode='constant')

# Calculate the attractive or repulsive field
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
                p = calc_repulsive_potential(x, y, coords, rr)
                if p > 10:
                    p = 10
                p = -p

            pmap[ix][iy] = p

    pmap = np.array(pmap)

    if fieldType == FieldType.repulsive:
        pmap = filter(pmap, xw, yw)
        pmap[pmap < -0.5] = -0.5

    if fieldType == FieldType.attractive:
        pmap = np.array(pmap)
        pmap = np.interp(pmap, (min(map(min, pmap)), max(map(max, pmap))), (0, 1))

    return pmap, xw, yw


def calc_attractive_potential(x, y, gx, gy):
    return 0.5 * pfConfig.Gatt * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, nodes, rr):
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


# Draw slice of map in Y-direction
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


# Plot 3D heatmap of map
def draw_3d_heatmap(data, xw, yw):

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


# Plot 2D heatmap of map
def draw_2d_heatmap(data, routeX, routeY, xw, yw):

    data = np.array(data)
    x, y = np.mgrid[0:xw, 0:yw]

    plt.figure()
    plt.pcolor(x, y, data, cmap=cm.Greys)
    plt.plot(routeX, routeY)
    plt.colorbar()


# Testcases
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
