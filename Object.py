
## This object is a collection of coordinates.
## The obect can either be an area or waterway
class Object():

    def __init__(self, type, id):
        self.id = id    # Identification of object
        self.ref = []   # Identification of nodes in object
        self.area = type    # Waterway or area

        self.xy = []
        self.x = []
        self.y = []

        self.lonlat = []
        self.lon = []
        self.lat = []


    def copy(self):
        newObject = Object(self.area, self.id)
        newObject.ref = self.ref
        return newObject

    def copyLonLat(self, objectB):
        self.lonlat = objectB.lonlat
        self.lon = objectB.lon
        self.lat = objectB.lat

    def copyXY(self, objectB):
        self.xy = objectB.xy
        self.x = objectB.x
        self.y = objectB.y