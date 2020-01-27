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


def insertMap(dbClient, mapNumber, map):
    client = dbClient
    db = client.map

    pmap = map[0]
    xw = map[1]
    yw = map[2]

    document = {
        'mapNumber': mapNumber,
        'pmap': pmap,
        'xw': xw,
        'yw': yw
    }

    result = db.pf.insert_one(document)

def getMap(dbClient, mapNumer):
    client = dbClient
    db = client.map

    pfMap = db.pf.find_one({"mapNumber": mapNumer})

    pmap = pfMap[u'pmap']
    xw = pfMap[u'xw']
    yw = pfMap[u'yw']

    return pmap, xw, yw

