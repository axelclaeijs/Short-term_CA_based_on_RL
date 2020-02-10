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
import Ship

mapType = Maptype.all
newPFMap = 0
newOSMMap = 0
insertDB = 0
mapNumber = 8
plotCoords = 1
plot2DHeatmap = 1
plot3DHeatmap = 1
plotSlice = 0
shipInput = 0
description = 'rep500_attr2_rr10_seriesPF'

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
                    axes = plt.gca()
                    axes.set_xlim([min(allX), max(allX)])
                    axes.set_ylim([min(allY), max(allY)])

                    plt.figure(2)
                    plt.plot(object.lon, object.lat)
                    plt.scatter(object.lon, object.lat)
                    axes = plt.gca()
                    axes.set_xlim([min(allLon), max(allLon)])
                    axes.set_ylim([min(allLat), max(allLat)])


    print("-----------------------------------------------------------------------------------------------------------")
    print(" Producing Global Repulsive Potential Field map")
    print("-----------------------------------------------------------------------------------------------------------")

    if newPFMap:
        repmapG, xw, yw = PF.calc_potential_field(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
                                           pfConfig.robot_radius, objects, 0, 0, mapType, FieldType.repulsive)

        if insertDB:
            dbConnection.insertRepG(client, mapNumber, [repmapG.tolist(), xw, yw], description)   # INSERT DATABASE

    else:

        repmapG, xw, yw = dbConnection.getRepMap(client, mapNumber)   # CALL DATABASE

    repmap = np.array(repmapG)
    pmap = repmap

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Input foreign ships")
    print("-----------------------------------------------------------------------------------------------------------")

    shipCoords = []

    if shipInput:
        i = 1

        print "Start of ship nr" + str(i) + "    (enter like this: lon, lat) \n"
        inp = raw_input()  # Get the input
        inp_list = inp.split(",")
        startCoord = [float(a) for a in inp_list]

        print "Stop of ship nr" + str(i) + "    (enter like this: lon, lat) \n"
        inp = raw_input()  # Get the input
        inp_list = inp.split(",")
        stopCoord = [float(a) for a in inp_list]

        shipCoords.append([startCoord, stopCoord])

        print "Would you like to add more ships? (Enter or 'Q' for stop)"
        inp = raw_input()

        while inp != "Q":  # Loop until it is a blank line
            i += 1
            print "Start of ship nr" + str(i) + "    (enter like this: lon, lat)\n "
            inp = raw_input()  # Get the input
            inp_list = inp.split(",")
            startCoord = [float(a) for a in inp_list]

            print "Stop of ship nr" + str(i) + "    (enter like this: lon, lat)\n "
            inp = raw_input()  # Get the input
            inp_list = inp.split(",")
            stopCoord = [float(a) for a in inp_list]

            shipCoords.append([startCoord, stopCoord])

            print "Would you like to add more ships? (Enter or 'Q' for stop)"
            inp = raw_input()
    else:

        shipCoords = pfConfig.shipCoords

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Navigation planning per ship")
    print("-----------------------------------------------------------------------------------------------------------")

    shipPaths = []
    ships = []
    i = 0

    for ship in shipCoords:

        repmapLs = []
        shipObject = Ship.Ship(i, pfConfig.shipSpeeds[i])

        startLonLat = ship[0]
        stopLonLat = ship[1]
        sx = transform.distance(ref_lonmin, ref_latmin, startLonLat[0], ref_latmin)
        sy = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, startLonLat[1])
        gx = transform.distance(ref_lonmin, ref_latmin, stopLonLat[0], ref_latmin)
        gy = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, stopLonLat[1])

        attrmap, xw, yw = PF.calc_potential_field(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
                                                  pfConfig.robot_radius, [], gx, gy, mapType, FieldType.attractive)

        shipObject.attr = attrmap

        shipPF = np.array(repmapG) + np.array(attrmap)

        shipObject.x, shipObject.y = nav.potential_field_planning(sx, sy, gx, gy, shipPF, xmin, ymin, xmax, ymax, objects)

        shipObject.distanceTrajectory = nav.calcDistanceTrajectory(shipObject.x, shipObject.y)

        repmapL, xw, yw = PF.calc_repulsive_potential_on_timestamp(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
                                                  pfConfig.robot_radius, shipObject, 0, 0, Maptype.trajectories, FieldType.repulsive, "00:10:00")

        repmapL1, xw, yw = PF.calc_repulsive_potential_on_timestamp(min(allX), max(allX), min(allY), max(allY), pfConfig.grid_size,
                                                  pfConfig.robot_radius, shipObject, 0, 0, Maptype.trajectories, FieldType.repulsive, "00:30:00")

        repmapLs.append(repmapL.tolist())
        repmapLs.append(repmapL1.tolist())

        shipObject.rep = repmapL.tolist()
        shipObject.xw = xw
        shipObject.yw = yw

        ships.append(shipObject)
        dbConnection.insertShip(client, shipObject)

        i += 1

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start potential field drawing")
    print("-----------------------------------------------------------------------------------------------------------")

    if PF.show_animation:
        print
        if plot3DHeatmap:
            # PF.draw_3d_heatmap(repmap, xw, yw)
            # PF.draw_3d_heatmap(attrmap, xw, yw)
            # PF.draw_3d_heatmap(pmap, xw, yw)
            for ship in ships:
                pmap = np.array(ship.attr) + np.array(ship.rep[0]) + np.array(repmapG)
                PF.draw_3d_heatmap(pmap, xw, yw)

        if plot2DHeatmap:
            #PF.draw_2d_heatmap(pmap, 0, 0, xw, yw)
            for ship in ships:
                pmap = np.array(ship[2]) + np.array(ship[3]) + np.array(repmapG)
                PF.draw_2d_heatmap(pmap, np.array(ship[4][0])/pfConfig.grid_size, np.array(ship[4][1])/pfConfig.grid_size, xw, yw)

        if plotSlice:
            PF.draw_slice_heatmap(repmap, yw)

    plt.show()
