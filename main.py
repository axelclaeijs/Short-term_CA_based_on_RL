from Util import OSM_parser as parser
import Potential_field as PF
import Util.Transform as transform
import Sources.configs.potentialFieldConfig as pfConfig
import matplotlib.pyplot as plt
import Object
import Util.Interpolation as interpolation
from pymongo import MongoClient
from Sources.database import dbConnection
from Util.Enums import Maptype, Area, FieldType
import Navigation as nav
import numpy as np
import fetchObjects

mapType = Maptype.all
newPFMap = 0
newOSMMap = 0
insertDB = 0
mapNumber = 8
plotCoords = 1
plot2DHeatmap = 1
plot3DHeatmap = 1
plotSlice = 0
description = 'old_rep500_attr2_rr10'

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
    print(" FetchObjects")
    print("-----------------------------------------------------------------------------------------------------------")

    if newOSMMap:
        objects, allX, allY, allLon, allLat, minlon, maxlon, minlat, maxlat = fetchObjects.fetchNewObjects(client)

    else:
        objects, allX, allY, allLon, allLat, minlon, maxlon, minlat, maxlat = fetchObjects.fetchDBObjects(client)

    # ref lon and lat to more usable variables
    ref_lonmin = minlon
    ref_lonmax = maxlon
    ref_latmin = minlat
    ref_latmax = maxlat

    # absolute (lon,lat) to (x,y) conversion
    xmin = transform.lonToX(ref_lonmin, ref_latmin)
    xmax = transform.lonToX(ref_lonmax, ref_latmin)
    ymin = transform.latToY(ref_lonmin, ref_latmin)
    ymax = transform.latToY(ref_lonmin, ref_latmax)

    lonw = transform.distance(ref_lonmin, ref_latmin, ref_lonmax, ref_latmin)
    latw = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, ref_latmax)

    # source and goals coords
    sx = transform.distance(ref_lonmin, ref_latmin, pfConfig.slon, ref_latmin)
    sy = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, pfConfig.slat)

    gx = transform.distance(ref_lonmin, ref_latmin, pfConfig.glon, ref_latmin)
    gy = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, pfConfig.glat)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Plot (x,y) and (lon,lat) graph")
    print("-----------------------------------------------------------------------------------------------------------")

    if plotCoords:
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

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Producing Global Repulsive Potential Field map")
    print("-----------------------------------------------------------------------------------------------------------")

    if newPFMap:
        repmapG, xw, yw = PF.calc_potential_field(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
                                           pfConfig.robot_radius, objects, gx, gy, mapType, FieldType.repulsive)

        attrmap, xw, yw = PF.calc_potential_field(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
                                                  pfConfig.robot_radius, objects, gx, gy, mapType, FieldType.attractive)

        if insertDB:
            dbConnection.insertRepG(client, mapNumber, [repmapG.tolist(), xw, yw], description)   # INSERT DATABASE

    else:

        repmapG, attrmap, xw, yw = dbConnection.getRepMap(client, mapNumber)   # CALL DATABASE

    repmap = np.array(repmapG)
    attrmap = np.array(attrmap)
    pmap = repmap + attrmap

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Navigation planning")
    print("-----------------------------------------------------------------------------------------------------------")

    routeX, routeY = nav.potential_field_planning(sx, sy, gx, gy, pmap, xmin, ymin)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Producing Local Repulsive Potential Field map")
    print("-----------------------------------------------------------------------------------------------------------")

    # shipPath = Object.Object(Area.trajectory, 'null')
    # shipPath.x, shipPath.y = [sx, sy]
    #
    # repmapL, xw, yw = PF.calc_potential_field(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
    #                                           pfConfig.robot_radius, shipPath, gx, gy, mapType, FieldType.repulsive)
    #
    # ship = [xw, yw, attrmap, repmapL, [routeX, routeY]]
    # dbConnection.insertShip(client, ship, pfConfig.shipID)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start potential field drawing")
    print("-----------------------------------------------------------------------------------------------------------")

    if PF.show_animation:
        print
        if plot3DHeatmap:
            PF.draw_3d_heatmap(repmap, xw, yw)
            PF.draw_3d_heatmap(attrmap, xw, yw)
            PF.draw_3d_heatmap(pmap, xw, yw)

        if plot2DHeatmap:
            #PF.draw_2d_heatmap(pmap, 0, 0, xw, yw)
            PF.draw_2d_heatmap(pmap, np.array(routeX)/pfConfig.grid_size, np.array(routeY)/pfConfig.grid_size, xw, yw)

        if plotSlice:
            PF.draw_slice_heatmap(repmap, yw)

    plt.show()
