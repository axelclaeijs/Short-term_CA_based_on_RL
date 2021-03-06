import Sources.configs.potentialFieldConfig as pfConfig

# Inset waterways and areas into DB
def insertObject(dbClient, object):

    client = dbClient
    db = client.map.objects
    lonlats = []
    xy = []

    for index in range(len(object.lon)):
        lonlats.append([object.lon[index], object.lat[index]])
        xy.append([object.x[index], object.y[index]])

    document = {
        'geometry': {
            'type': "Polygon",
            'coordinates': lonlats,
            'xy': xy,
            'refs': object.ref
        },
        'id': object.id,
        'area': object.area
    }

    result = db.insert_one(document)


# Insert global repulsive potentialfield of certain map
def insertRepG(dbClient, mapNumber, map, description):

    client = dbClient
    db = client.map.pf

    repmap = map[0]
    xw = map[1]
    yw = map[2]

    document = {
        'description': description,
        'mapNumber': mapNumber,
        'repmap': repmap,
        'xw': xw,
        'yw': yw
    }

    result = db.insert_one(document)


# Insert a ship with its timeseries of repulsive fields and global navigation route
def insertShip(dbClient, ship, number):

    client = dbClient
    db = client.map

    xw = ship[0]
    yw = ship[1]
    attrmap = ship[2]
    repmap = ship[3]
    route = ship[4]
    shipNumber = number

    document = {
        'shipNumber': shipNumber,
        'xw': xw,
        'yw': yw,
        'attrmap': attrmap,
        'repmap': repmap,
        'route': route
    }

    result = db.ships.insert_one(document)

# Request amount of objects
def amountObjects(dbClient):

    client = dbClient
    db = client.map.objects

    amount = db.find({}).count()

    return amount

# Request object by ID
def getObject(dbClient, objectID):

    client = dbClient
    db = client.map.objects

    object = db.find_one({"id": objectID})

    xy = object[u'geometry'][u'xy']
    lonlat = object[u'geometry'][u'coordinates']
    area = object[u'area']
    id = objectID
    refs = object[u'geometry'][u'refs']

    return xy, lonlat, area, id, refs


# Request global repulsive map
def getRepMap(dbClient, mapNumer):

    client = dbClient
    db = client.map.pf

    pfMap = db.find_one({"mapNumber": mapNumer})

    repmap = pfMap[u'repmap']
    xw = pfMap[u'xw']
    yw = pfMap[u'yw']

    return repmap, xw, yw


# Request global repulsive map
def getShip(dbClient, shipNumber):

    client = dbClient
    db = client.map.ships

    pfMap = db.find_one({"shipNumber": shipNumber})

    xw = pfMap[u'xw']
    yw = pfMap[u'yw']
    attrmap = pfMap[u'attrmap']
    repmap = pfMap[u'repmap']
    route = pfMap[u'route']

    return repmap, attrmap, xw, yw, route

