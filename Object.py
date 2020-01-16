
## This object is a collection of coordinates.
## The obect can either be an area or waterway
class Object():

    def __init__(self, type, id):
        self.area = type
        self.xy = []
        self.lonlat = []
        self.id = id
        self.x = []
        self.y = []
        self.ref = []

    def copy(self):
        newObject = Object(self.area, self.id)
        newObject.ref = self.ref
        return newObject
