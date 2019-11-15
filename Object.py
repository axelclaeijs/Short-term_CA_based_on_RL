
## This object is a collection of coordinates.
## The obect can either be an area or waterway
class Object():

    def __init__(self, type):
        self.area = type
        self.nodes = []

    def addNodes(self, nodes):
        self.nodes = nodes
