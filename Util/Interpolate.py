import numpy as np
import Object
from scipy import interpolate


def distance(x1, y1, x2, y2):
    return np.hypot(x2 - x1, y2 - y1)


def getYNew(xSet, ySet, xNew):
    tck = interpolate.splrep(xSet, ySet, s=0)
    return interpolate.splev(xNew, tck, der=0)


def extentObjects(object):
    newObject = Object.Object(object.area, id)

    newObject.xy.append([object.xy[0][0], object.xy[1][0]])
    xCurrent = object.xy[0][0]
    yCurrent = object.xy[1][0]

    for i,_ in enumerate(object.xy[0]):

        xNew = object.xy[0][i]
        yNew = object.xy[1][i]

        while distance(xCurrent, yCurrent, xNew, yNew) > 50:
            xNew = (object.xy[0][i+1] - object.xy[0][i]) / 2
            yNew = getYNew(object.xy[0], object.xy[1], xNew)


        newObject.append([xNew, yNew])

        xCurrent = xNew
        yCurrent = yNew

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