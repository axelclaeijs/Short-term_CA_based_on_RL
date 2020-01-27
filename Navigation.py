import numpy as np
import Sources.configs.potentialFieldConfig as pfConfig
import Potential_field as pf
import matplotlib.pyplot as plt


def get_motion_model():
    # dx, dy
    motion = [[1, 0],
              [0, 1],
              [-1, 0],
              [0, -1],
              [-1, -1],
              [-1, 1],
              [1, -1],
              [1, 1]]

    return motion


def potential_field_planning(sx, sy, gx, gy, pmap, xw, yw, minx, miny):

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round((sx - minx) / pfConfig.grid_size)
    iy = round((sy - miny) / pfConfig.grid_size)
    gix = round((gx - minx) / pfConfig.grid_size)
    giy = round((gy - miny) / pfConfig.grid_size)

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
        xp = ix * pfConfig.grid_size + minx
        yp = iy * pfConfig.grid_size + miny
        print (xp, yp)
        d = np.hypot(gx - xp, gy - yp)
        rx.append(xp)
        ry.append(yp)

    return rx, ry