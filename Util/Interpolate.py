import numpy as np
from scipy import interpolate


def distance(x1, y1, x2, y2):
    return np.hypot(x2 - x1, y2 - y1)


def getYNew(xSet, ySet, xNew):
    tck = interpolate.splrep(xSet, ySet, s=0)
    return interpolate.splev(xNew, tck, der=0)


def extentObjects(object):
    newObject = []

    for i,_ in enumerate(object.xy[0]):
        if i == 0:
            newObject.append([object.xy[0][0], object.xy[1][0]])
            xNew = object.xy[0][0]
            yNew = object.xy[1][0]

        d = distance(newObject[i][0], newObject[i][1], xNew, yNew)
        while d > 50:
            xNew = (object.xy[0][i+1] - object.xy[0][i]) / 2
            yNew = getYNew(object.xy[0], object.xy[1], xNew)
            newObject.append([xNew, yNew])
        if distance(object.xy[0][i], object.xy[1][i], xNew, yNew) > 50:
            xNew = (xNew - object.xy[0][i]) / 2
            yNew = getYNew(object.xy[0], object.xy[1], xNew)
            newObject.append([xNew, yNew])
        if distance(object.xy[0][i], object.xy[1][i], xNew, yNew) > 50:
            xNew = (xNew - object.xy[0][i]) / 2
            yNew = getYNew(object.xy[0], object.xy[1], xNew)
            newObject.append([xNew, yNew])



        newObject.append([object.xy[0][i], object.xy[1][i]])

    return newObject