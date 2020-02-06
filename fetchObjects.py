from Util import OSM_parser as parser
import Util.Transform as transform
import Object
import Util.Interpolation as interpolation
import Util.Utils as util
from Sources.database import dbConnection
from Util.Enums import Maptype, Area, FieldType


# Parse new OSM-file
def fetchNewObjects(dbClient):

    nodes = parser.WaterwayCollector2()
    nodes.apply_file(parser.sys.argv[2])

    boundFinder = parser.BoundsFinder(parser.sys.argv[1])
    boundFinder.find()

    ref_lonmin = boundFinder.minlon
    ref_lonmax = boundFinder.maxlon
    ref_latmin = boundFinder.minlat
    ref_latmax = boundFinder.maxlat

    # objects (lon,lat)
    allLon = []
    allLat = []

    # objects all inclusive
    objects = []

    # list of different coords (lon,lat)
    allCoords = []
    waterwayCoords = []
    areaCoords = []

    # list of different coords (X,Y)
    allX = []
    allY = []

    print ("> Number of nodes: ", len(nodes.coords))
    print ("> Number of areas: ", len(nodes.areas))

    print("-----------------------------------------------------------------------------------------------------------")
    print(" Start analyzing objects")
    print("-----------------------------------------------------------------------------------------------------------")

    # summarize objects
    for coord in nodes.coords:
        if (ref_latmin <= coord[1] <= ref_latmax) and (ref_lonmin <= coord[0] <= ref_lonmax):
            allLat.append(coord[1])
            allLon.append(coord[0])
            allCoords.append([coord[0], coord[1]])

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

        dbConnection.insertObject(dbClient, object)  # INSERT DATABASE

    return objects, allX, allY, allLon, allLat, ref_lonmin, ref_lonmax, ref_latmin, ref_latmax

# Get nodes from DB
def fetchDBObjects(client):

    objects = []

    # list of different coords (X,Y)
    allX = []
    allY = []

    # objects (lon,lat)
    allLon = []
    allLat = []

    amount = dbConnection.amountObjects(client)

    for i in range(amount):
        dbObject = dbConnection.getObject(client, i)

        object = Object.Object(dbObject[2], dbObject[3])
        object.ref = dbObject[4]
        object.x, object.y = util.unpack(dbObject[0])
        object.lon, object.lat = util.unpack(dbObject[1])
        objects.append(object)

        for x in object.x:
            allX.append(x)
        for y in object.y:
            allY.append(y)
        for lon in object.lon:
            allLon.append(lon)
        for lat in object.lat:
            allLat.append(lat)

    ref_lonmin = min(allLon)
    ref_lonmax = max(allLon)
    ref_latmin = min(allLat)
    ref_latmax = max(allLat)

    return objects, allX, allY, allLon, allLat, ref_lonmin, ref_lonmax, ref_latmin, ref_latmax
