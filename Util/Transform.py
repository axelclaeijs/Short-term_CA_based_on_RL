
from geopy.distance import lonlat, geodesic
import math

# Constants
R = 6371    # Earth's Radius [km]


def coordsToMeters(lon, lat):
    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)

    return x, y


def lonToX(lon, lat):
    return R * math.cos(lat) * math.cos(lon)


def latToY(lon, lat):
    return R * math.cos(lat) * math.sin(lon)


def distance(lon1, lat1, lon2, lat2):
    loc1 = (lon1, lat1)
    loc2 = (lon2, lat2)
    return geodesic(lonlat(*loc1), lonlat(*loc2)).m

