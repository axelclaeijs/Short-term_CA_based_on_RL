import OSM_parser_v2 as parser
import Potential_field as PF
import Util.Transform as transform
import Sources.configs.potentialFieldConfig as pfConfig
import numpy as np
import matplotlib.pyplot as plt
import Object
import Util.Utils as util
import Util.Interpolation as interpolation

# MapType: 0 (all), 1 (waterways), 2 (areas)
mapType = 1

if __name__ == '__main__':
    if len(parser.sys.argv) != 3:
        print("> Usage: python main3.py <infile> <outfile>")
        parser.sys.exit(-1)

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

    # x- and y- width
    xw = transform.distanceXY(xmin, ymin, xmax, ymin)
    yw = transform.distanceXY(xmin, ymin, xmin, ymax)

    # gridSize
    xStep = (xmax - xmin) / xw
    yStep = (ymax - ymin) / yw

    # ref x and y
    x, y = transform.coordsToMeters(ref_lonmin, ref_latmin, xmin, ymin)
    sx, sy = transform.coordsToMeters(pfConfig.slon, pfConfig.slat, xmin, ymin)

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

    # summarize objects
    for coord in nodes.coords:
        olat.append(coord[1])
        olon.append(coord[0])
        allCoords.append([coord[0], coord[1]])

    print 'xmax - xmin= ', (xmax-xmin)
    print 'ymax - ymin= ', (ymax-ymin)

    print 'xw: ', xw
    print 'yw: ', yw

    print 'xStep: ', xStep
    print 'yStep: ', yStep

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
                if ref == n[2]:
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
            object = Object.Object(1, id)

        else:
            cntRiver += 1
            object = Object.Object(0, id)

        id += 1

        object.ref = nodeRef
        object.lon = pltLon
        object.lat = pltLat

        newObject = interpolation.extentObjects(object)

        objects.append(newObject)

    print '#river: ', cntRiver
    print '#areas: ', cntArea

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Calculate (X,Y)-coordinates")
    print("-----------------------------------------------------------------------------------------------------------")

    for object in objects:
        ox = []
        oy = []

        for i in range(len(object.lon)):
            x, y = transform.coordsToMeters(object.lon[i], object.lat[i], xmin, ymin)

            #CONVERSION X Y (UTM coords?))

            ox.append(x)
            oy.append(y)

            allX.append(x)
            allY.append(y)

        object.x = ox
        object.y = oy

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

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Producing Potential Field map")
    print("-----------------------------------------------------------------------------------------------------------")

    pmap, xw, yw = PF.calc_potential_field(min(allX), max(allX), min(allY), max(allY), sx, sy, pfConfig.gx, pfConfig.gy,
                                               pfConfig.grid_size, pfConfig.robot_radius, objects, mapType)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start potential field drawing")
    print("-----------------------------------------------------------------------------------------------------------")

    if PF.show_animation:
        PF.draw_heatmap(pmap, xw, yw)
        #PF.draw_slice_heatmap(pmap, yw)

    plt.show()
