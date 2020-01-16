import numpy as np
from scipy import interpolate
import Object
import Utils as util


def distance(x1, y1, x2, y2):
    return np.hypot(x2 - x1, y2 - y1)


def getYNew(xSet, ySet, xNew):
    tck = interpolate.splrep(xSet, ySet, s=0)
    return interpolate.splev(xNew, tck, der=0)


def extentObjects(object):
    newObject = object.copy()
    newX = []
    newY = []
    newXY = []

    newXY.append([object.x[0], object.y[0]])
    newX.append(object.x[0])
    newY.append(object.y[0])

    xCurrent = object.x[0]
    yCurrent = object.y[0]

    for i, _ in enumerate(object.x):
        if i < len(object.x)-1:
            print 'level', i
            xNew = object.x[i+1]
            yNew = object.y[i+1]

            while distance(xCurrent, yCurrent, xNew, yNew) > 50:
                xNew = (xNew + xCurrent) / 2
                yNew = getYNew(object.x, object.y, xNew)

                yNew = np.array([yNew])[0]

                print (xNew, yNew)

                newXY.append([xNew, yNew])
                newX.append(xNew)
                newY.append(yNew)

                xCurrent = xNew
                yCurrent = yNew

                xNew = object.x[i+1]
                yNew = object.y[i+1]

            newXY.append([xNew, yNew])
            newX.append(xNew)
            newY.append(yNew)

            xCurrent = xNew
            yCurrent = yNew

    newObject.xy = util.merge(newX, newY)
    newObject.x = newX
    newObject.y = newY
    # OPTIONAL: conversion to lon/lat

    return newObject

def main():

    x = [1, 10, 50, 140, 300]
    y = [1, 20, 89, 450, 10]

    object = Object.Object(1, 045)
    object.xy = util.merge(x, y)
    object.x = x
    object.y = y

    newObject = extentObjects(object)
    print 'done'

if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")