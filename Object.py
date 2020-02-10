
## This object is a collection of coordinates.
## The obect can either be an area or waterway
class Object():

    def __init__(self, type, id):
        self.id = id    # Identification of object
        self.ref = []   # Identification of nodes in object
        self.area = type    # Waterway or boundary

        self.x = []
        self.y = []

        self.lon = []
        self.lat = []


    def copy(self):
        newObject = Object(self.area, self.id)
        newObject.ref = self.ref
        return newObject

    def copyLonLat(self, objectB):
        self.lon = objectB.lon
        self.lat = objectB.lat

    def copyXY(self, objectB):
        self.x = objectB.x
        self.y = objectB.y

    def insertXY(self, x, y):
        self.x.append(x)
        self.y.append(y)

    def setSingleXY(self, x, y):
        self.x = [x]
        self.y = [y]