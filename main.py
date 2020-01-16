import OSM_parser_v2 as parser
import Potential_field as PF
import Util.Transform as transform
import Sources.configs.potentialFieldConfig as pfConfig
import numpy as np
import matplotlib.pyplot as plt
import Object
import Util.Utils as util
import Util.Interpolation_test as interpolation

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
    xw = transform.distance(ref_lonmin, ref_latmin, ref_lonmax, ref_latmin)
    yw = transform.distance(ref_lonmin, ref_latmin, ref_lonmin, ref_latmax)

    # gridSize
    xStep = (xmax - xmin) / xw
    yStep = (ymax - ymin) / yw

    # ref x and y
    x, y = transform.coordsToMeters(ref_lonmin, ref_latmin, xmin, ymin)
    sx, sy = transform.coordsToMeters(pfConfig.slon, pfConfig.slat, xmin, ymin)

    # objects (lon,lat)
    olon = []
    olat = []

    # objects (x,y)
    ox = []
    oy = []

    # objects all inclusive
    objects = []

    # list of different coords
    allCoords = []
    waterwayCoords = []
    areaCoords = []

    # summarize objects
    for coord in nodes.coords:
        olat.append(coord[1])
        olon.append(coord[0])
        x, y = transform.coordsToMeters(coord[0], coord[1], xmin, ymin)
        ox.append(x)
        oy.append(y)
        allCoords.append([x, y])

    print 'max ox: ', max(ox)
    print 'max oy: ', max(oy)
    print 'min ox: ', min(ox)
    print 'min oy: ', min(oy)

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
                    pltLon.append(n[0])
                    pltLat.append(n[1])
                    x, y = transform.coordsToMeters(n[0], n[1], xmin, ymin)
                    pltX.append(x)
                    pltY.append(y)
                    if area[0] == area[-1]:
                        if [x, y] not in areaCoords and [x, y] not in waterwayCoords:
                            areaCoords.append([x, y])
                    else:
                        if [x, y] not in waterwayCoords and [x, y] not in areaCoords:
                            waterwayCoords.append([x, y])
                    break

        if area[0] == area[-1]:
            cntArea += 1
            object = Object.Object(1, id)

        else:
            cntRiver += 1
            object = Object.Object(0, id)

        id += 1

        object.xy = util.merge(pltX, pltY)
        object.lonlat = [pltLon, pltLat]
        object.ref = nodeRef
        object.x = pltX
        object.y = pltY
        newObject = interpolation.extentObjects(object)
        objects.append(newObject)

    print '#river: ', cntRiver
    print '#areas: ', cntArea

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
                axes.set_xlim([min(ox), max(ox)])
                axes.set_ylim([min(oy), max(oy)])

                plt.figure(2)
                plt.plot(object.lonlat[0], object.lonlat[1])
                plt.scatter(object.lonlat[0], object.lonlat[1])
                plt.scatter(pfConfig.slon, pfConfig.slat, color='blue')
                axes = plt.gca()
                axes.set_xlim([min(olon), max(olon)])
                axes.set_ylim([min(olat), max(olat)])

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Cubic spline")
    print("-----------------------------------------------------------------------------------------------------------")



    print("-----------------------------------------------------------------------------------------------------------")
    print(" Producing Potential Field map")
    print("-----------------------------------------------------------------------------------------------------------")

    # # list of interesting obstacles
    # map_ox = []
    # map_oy = []
    #
    # # extracting interesting obstacles
    # for i, _ in enumerate(ox):
    #     if ox[i] <= sx + pfConfig.right and ox[i] >= sx - pfConfig.left and oy[i] <= sy + pfConfig.front and oy[i] >= sy - pfConfig.back:
    #         map_ox.append(ox[i])
    #         map_oy.append(oy[i])
    #
    # print "> Number of nodes in map: ", len(map_ox)

    # calc potential field
    if mapType == 0:
        pmap, xw, yw = PF.calc_potential_field(min(ox), max(ox), min(oy), max(oy), sx, sy, pfConfig.gx, pfConfig.gy,
                                               waterwayCoords, pfConfig.grid_size, pfConfig.robot_radius, objects)
    elif mapType == 1:
        pmap, xw, yw = PF.calc_potential_field(min(ox), max(ox), min(oy), max(oy), sx, sy, pfConfig.gx, pfConfig.gy,
                                               areaCoords, pfConfig.grid_size, pfConfig.robot_radius, objects)
    else:
        pmap, xw, yw = PF.calc_potential_field(min(ox), max(ox), min(oy), max(oy), sx, sy, pfConfig.gx, pfConfig.gy,
                                               allCoords, pfConfig.grid_size, pfConfig.robot_radius, objects)

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start potential field drawing")
    print("-----------------------------------------------------------------------------------------------------------")

    if PF.show_animation:
        PF.draw_heatmap(pmap, xw, yw)
        #PF.draw_slice_heatmap(pmap, yw)

    plt.show()
