
## This object is a collection of coordinates.
## The obect can either be an area or waterway
class Object():

    def __init__(self, type, id):
        self.area = type
        self.xy = []
        self.lonlat = []
        self.id = id

    def addNodes(self, xy, lonlat):
        self.xy = xy
        self.lonlat = lonlat
