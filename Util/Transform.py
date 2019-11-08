import geopy.distance


def coordsToMeters(lon, lat, ref_lon, ref_lat):
    x = geopy.distance.vincenty((ref_lon, 0), (lon, 0)).m
    y = geopy.distance.vincenty((0, ref_lat), (0, lat)).m

    return x, y


def lonToX(lon, ref_lon):
    return geopy.distance.vincenty((ref_lon, 0), (lon, 0)).m


def latToY(lat, ref_lat):
    return geopy.distance.vincenty((0, ref_lat), (0, lat)).m


def distance(lon1, lat1, lon2, lat2):
    return geopy.distance.vincenty((lon1, lat1), (lon2, lat2)).m