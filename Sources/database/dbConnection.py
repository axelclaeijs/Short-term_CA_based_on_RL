import numpy as np
from pymongo import MongoClient
from pprint import pprint
from Util import Utils as util



def insertObject(dbClient, object):
    client = dbClient
    db = client.map
    lonlats = []
    xy = []

    for index in range(len(object.lon)):
        lonlats.append([object.lon[index], object.lat[index]])
        xy.append([object.x[index], object.y[index]])

    document = {
        'geometry': {
            'type': "Polygon",
            'coordinates': lonlats,
            'xy': xy
        },
        'id': object.id,
        'area': object.area
    }

    result = db.objects.insert_one(document)


def insertMap(dbClient, mapNumber, map, description):
    client = dbClient
    db = client.map

    repmap = map[0]
    attrmap = map[1]
    xw = map[2]
    yw = map[3]

    document = {
        'description': description,
        'mapNumber': mapNumber,
        'repmap': repmap,
        'attrmap': attrmap,
        'xw': xw,
        'yw': yw
    }

    result = db.pf.insert_one(document)

def getMap(dbClient, mapNumer):
    client = dbClient
    db = client.map

    pfMap = db.pf.find_one({"mapNumber": mapNumer})

    repmap = pfMap[u'repmap']
    attrmap = pfMap[u'attrmap']
    xw = pfMap[u'xw']
    yw = pfMap[u'yw']

    return repmap, attrmap, xw, yw

