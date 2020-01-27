from Util import OSM_parser as parser
import Potential_field as PF
import Util.Transform as transform
import Sources.configs.potentialFieldConfig as pfConfig
import matplotlib.pyplot as plt
import Object
import Util.Interpolation as interpolation
import Util.Utils as util
from pymongo import MongoClient
from Sources.database import dbConnection
from Util.Enums import Maptype, Area
import Navigation as nav
import numpy as np

mapType = Maptype.all
newMap = 'false'
mapNumber = 4

if __name__ == '__main__':
    if len(parser.sys.argv) != 3:
        print("> Usage: python main3.py <infile> <outfile>")
        parser.sys.exit(-1)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Connection to MongoDB client")
    print("-----------------------------------------------------------------------------------------------------------")

    client = MongoClient("localhost:27017")
    db = client.admin
    serverStatusResult = db.command("serverStatus")
    # pprint(serverStatusResult)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start parsing OSM file")
    print("-----------------------------------------------------------------------------------------------------------")

    # go through the ways to find all relevant nodes
    # ways = parser.WaterwayFilter()
    # ways.apply_file(parser.sys.argv[1])

    # go through the file again and write out the data
    # writer = parser.o.SimpleWriter(parser.sys.argv[2])
    # parser.WaterwayWriter(writer, ways.nodes).apply_file(parser.sys.argv[1])
    #
    # writer.close()

    nodes = parser.WaterwayCollector2()
    nodes.apply_file(parser.sys.argv[2])

    boundFinder = parser.BoundsFinder(parser.sys.argv[1])
    boundFinder.find()

    print ("> Number of nodes: ", len(nodes.coords))
    print ("> Number of areas: ", len(nodes.areas))

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start analyzing objects")
    print("-----------------------------------------------------------------------------------------------------------")

    # lat1 = 51.28463
    # lon1 = 4.389471
    #
    # x1 = transform.lonToX(lon1, lat1)
    # y1 = transform.latToY(lon1, lat1)
    #
    # x11, y11 = transform.coordsToMeters(lon1, lat1, 0, 0)
    #
    # lat2 = 51.284642
    # lon2 = 4.403773
    #
    # x2 = transform.lonToX(lon2, lat2)
    # y2 = transform.latToY(lon2, lat2)
    #
    # x22, y22 = transform.coordsToMeters(lon2, lat2, 0, 0)
    # yw = transform.distanceXY(x11, y11, x22, y22)
    # xw = transform.distanceXY(x1, y1, x2, y2)
    #
    #
    # lonw = transform.distance(lon1, lat1, lon2, lat2)

    # ref lon and lat to more usable variables
    ref_lonmin = boundFinder.minlon
    ref_lonmax = boundFinder.maxlon
    ref_latmin = boundFinder.minlat
    ref_latmax = boundFinder.maxlat

    # absolute (lon,lat) to (x,y) conversion
    xmin = transform.lonToX(ref_lonmin, ref_latmin)
    xmax = transform.lonToX(ref_lonmax, ref_latmin)
    ymin = transform.latToY(ref_lonmin, ref_latmin)
    ymax = transform.latToY(ref_lonmin, ref_latmax)

    lonw = transform.distance(ref_lonmin, ref_latmin, ref_lonmax, ref_latmin)
    latw = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, ref_latmax)

    # objects (lon,lat)
    allLon = []
    allLat = []

    # objects all inclusive
    objects = []

    # list of different coords (lon,lat)
    allCoords = []
    waterwayCoords = []
    areaCoords = []

    #list of different coords (X,Y)
    allX = []
    allY = []

    # source and goals coords
    sx = transform.distance(ref_lonmin, ref_latmin, pfConfig.slon, ref_latmin)
    sy = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, pfConfig.slat)

    gx = transform.distance(ref_lonmin, ref_latmin, pfConfig.glon, ref_latmin)
    gy = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, pfConfig.glat)

    # summarize objects
    for coord in nodes.coords:
        if (ref_latmin <= coord[1] <= ref_latmax) and (ref_lonmin <= coord[0] <= ref_lonmax):
            allLat.append(coord[1])
            allLon.append(coord[0])
            allCoords.append([coord[0], coord[1]])

    print 'ref lon min: ', ref_lonmin
    print 'ref lat min: ', ref_latmin
    print 'ref lon max: ', ref_lonmax
    print 'ref lat max: ', ref_latmax

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Generate objects")
    print("-----------------------------------------------------------------------------------------------------------")
    cntRiver = 0
    cntArea = 0
    id = 0

    for area in nodes.areas:
        cntNodes = 0
        pltLon = []
        pltLat = []
        pltX = []
        pltY = []
        nodeRef = []
        for ref in area:
            for n in nodes.coords:
                if (ref == n[2]):
                    cntNodes += 1
                    nodeRef.append(ref)
                    lon, lat = n[0], n[1]
                    pltLon.append(lon)
                    pltLat.append(lat)
                    if area[0] == area[-1]:
                        if [lon, lat] not in areaCoords and [lon, lat] not in waterwayCoords:
                            areaCoords.append([lon, lat])
                    else:
                        if [lon, lat] not in waterwayCoords and [lon, lat] not in areaCoords:
                            waterwayCoords.append([lon, lat])
                    break

        if area[0] == area[-1]:
            cntArea += 1
            object = Object.Object(Area.boundary, id)

        else:
            cntRiver += 1
            object = Object.Object(Area.waterway, id)

        id += 1

        object.ref = nodeRef
        object.lon = pltLon
        object.lat = pltLat

        newObject = interpolation.extentObjects(object)
        boundObject = interpolation.boundObject(newObject, ref_lonmin, ref_lonmax, ref_latmin, ref_latmax)

        objects.append(boundObject)

    print '#river: ', cntRiver
    print '#areas: ', cntArea

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Calculate (X,Y)-coordinates")
    print("-----------------------------------------------------------------------------------------------------------")

    for object in objects:
        ox = []
        oy = []

        for i in range(len(object.lon)):

            x = transform.distance(ref_lonmin, ref_latmin, object.lon[i], ref_latmin)
            y = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, object.lat[i])

            ox.append(x)
            oy.append(y)

            allX.append(x)
            allY.append(y)

        object.x = ox
        object.y = oy

        dbConnection.insertObject(client, object)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Plot (x,y) and (lon,lat) graph")
    print("-----------------------------------------------------------------------------------------------------------")

    for object in objects:
            #if not(object.area):
                plt.figure(1)
                plt.plot(object.x, object.y)
                plt.scatter(object.x, object.y)
                plt.scatter(sx, sy, color='blue')
                axes = plt.gca()
                axes.set_xlim([min(allX), max(allX)])
                axes.set_ylim([min(allY), max(allY)])

                plt.figure(2)
                plt.plot(object.lon, object.lat)
                plt.scatter(object.lon, object.lat)
                plt.scatter(pfConfig.slon, pfConfig.slat, color='blue')
                axes = plt.gca()
                axes.set_xlim([min(allLon), max(allLon)])
                axes.set_ylim([min(allLat), max(allLat)])

    plt.show()
    print("-----------------------------------------------------------------------------------------------------------")
    print(" Producing Potential Field map")
    print("-----------------------------------------------------------------------------------------------------------")

    if newMap == 'true':
        pmap, xw, yw = PF.calc_potential_field(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
                                           pfConfig.robot_radius, objects, mapType)

        dbConnection.insertMap(client, mapNumber, [pmap, xw, yw])

    else:

        pmap, xw, yw = dbConnection.getMap(client, mapNumber)

    #pmap = np.array(pmap)

    #pmap = util.scale(pmap, 0, 1)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Navigation planning")
    print("-----------------------------------------------------------------------------------------------------------")

    #routeX, routeY = nav.potential_field_planning(sx, sy, gx, gy, pmap, xw, yw, xmin, ymin)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start potential field drawing")
    print("-----------------------------------------------------------------------------------------------------------")

    if PF.show_animation:
        print
        PF.draw_3d_heatmap(pmap, xw, yw)
        #PF.draw_3d_heatmap_interpol(pmap, xw, yw)
        #PF.draw_slice_heatmap(pmap, yw)
        #PF.draw_2d_heatmap(pmap, routeX, routeY, xw, yw)

    plt.show()
