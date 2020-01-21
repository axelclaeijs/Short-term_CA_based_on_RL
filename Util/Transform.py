
from geopy.distance import lonlat, geodesic
import math

# Constants
R = 6371    # Earth's Radius [km]


def coordsToMeters(lon, lat, xmin, ymin):
    x = (R * math.cos(lat) * math.cos(lon) ) - xmin
    y = (R * math.cos(lat) * math.sin(lon) ) - ymin

    return x, y


def coordsToMeters2(lon, lat, ref_lon, ref_lat):
    x = distance(ref_lon, ref_lat, lon, ref_lat)
    y = distance(ref_lon, ref_lat, ref_lon, lat)

    return x, y


def lonToX(lon, lat):
    return R * math.cos(lat) * math.cos(lon)


def latToY(lon, lat):
    return R * math.cos(lat) * math.sin(lon)


def distance(lon1, lat1, lon2, lat2):
    loc1 = (lon1, lat1)
    loc2 = (lon2, lat2)
    return geodesic(lonlat(*loc1), lonlat(*loc2)).m

def distanceXY(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

