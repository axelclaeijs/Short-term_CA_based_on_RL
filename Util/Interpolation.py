import math
import Object
import Utils as util
import matplotlib.pyplot as plt
from pyproj import Geod
from Util import Transform
import Sources.configs.potentialFieldConfig as pfConfig


# Return new points between start end end point
def interpolate(x1, y1, x2, y2, n):
    geoid = Geod(ellps="WGS84")
    return geoid.npts(x1, y1, x2, y2, n)


# Create new points in object where distance between two sequent points < ds
def extentObjects(object):
    cnt = 0
    newObject = object.copy()
    newObject.copyXY(object)
    newLon = []
    newLat = []

    for index in range(len(object.lon)):
        if index != len(object.lon)-1:

            lonCurrent = object.lon[index]
            latCurrent = object.lat[index]

            lonNext = object.lon[index + 1]
            latNext = object.lat[index + 1]

            l = Transform.distance(lonCurrent, latCurrent, lonNext, latNext)
            n = int(math.ceil(l / pfConfig.ds))
            lonlat = interpolate(lonCurrent, latCurrent, lonNext, latNext, n)
            cnt += n
            lon, lat = util.unpack(lonlat)

            newLon.append(object.lon[index])
            newLat.append(object.lat[index])

            newLon.extend(lon)
            newLat.extend(lat)

    newLon.append(object.lon[-1])
    newLat.append(object.lat[-1])

    newObject.lon = newLon
    newObject.lat = newLat

    return newObject


# Cut points from object which are out of region
def boundObject(object, lonmin, lonmax, latmin, latmax):

    lons = []
    lats = []

    for n in range(len(object.lon)):
        if (lonmin <= object.lon[n] <= lonmax) and (latmin <= object.lat[n] <= latmax):
            lons.append(object.lon[n])
            lats.append(object.lat[n])

    object.lon = lons
    object.lat = lats

    return object


# Testcases
def main():

    lon1 = [3.7462253, 3.749938, 3.7539657, 3.7545463, 3.7535907, 3.7547027, 3.7543556, 3.7536614, 3.7536998, 3.7503072, 3.7472361, 3.7438261, 3.7417986, 3.7407546, 3.738608, 3.7405009, 3.7427835, 3.7426739, 3.7432193, 3.7462253]
    lat1 = [51.1027785, 51.0977146, 51.0922055, 51.0914167, 51.0871377, 51.0857686, 51.0844009, 51.0844736, 51.0861361, 51.0907719, 51.0949729, 51.0996352, 51.1023994, 51.1038138, 51.1051764, 51.1065571, 51.1082221, 51.1076259, 51.1068765, 51.1027785]

    lonlat = util.merge(lon1, lat1)

    # print len(lonlat)
    #
    for index in range(len(lonlat)):
        if index != len(lonlat)-1:
            print Transform.distance(lonlat[index][0], lonlat[index][1], lonlat[index+1][0], lonlat[index+1][1])
        print index

    object = Object.Object(1, 045)
    object.lonlat = lonlat
    object.lon = lon1
    object.lat = lat1

    newObject = extentObjects(object)

    for lon, lat in lonlat:
        plt.plot(lon, lat, 'o')
        plt.plot(newObject.lon, newObject.lat, 'x')

    plt.show()

    print 'done'

if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")