from enum import Enum

class Area(Enum):
    waterway = 0
    boundary = 1
    trajectory = 2

class Maptype(Enum):
    waterways = 0
    boundaries = 1
    all = 2

class FieldType(Enum):
    repulsive = 0
    attractive = 1
