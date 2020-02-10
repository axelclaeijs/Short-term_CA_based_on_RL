"""
ships object consists of
- speed (knots)
- attractive PF
- trajectory (x,y)-coords
- distance between trajectory (x,y)-coords
- series of rep PF linked to speed (HOW??) 
"""""
class Ship():

    def __init__(self, id, speed):
        self.id = id    # Identification of object

        self.knots = speed
        self.attr = []
        self.x = []
        self.y = []
        self.distanceTrajectory = []
        self.xw = 0
        self.yw = 0

        self.rep = []

