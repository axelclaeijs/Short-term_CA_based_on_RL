import numpy as np
import Sources.configs.potentialFieldConfig as pfConfig


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
def potential_field_planning(sx, sy, gx, gy, pmap, minx, miny):

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
        xp = ix * pfConfig.grid_size
        yp = iy * pfConfig.grid_size

        d = np.hypot(gx - xp, gy - yp)

        rx.append(xp)
        ry.append(yp)

    return rx, ry