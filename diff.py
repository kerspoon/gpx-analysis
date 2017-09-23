import math
from datetime import timedelta

class Diff(object):
    def __init__(self, distance, duration, climb, w1, w2):
        self.distance = distance # in meters
        self.duration = duration # in timedelta format
        self.climb = climb # in meters
        self.speed = distance/duration.total_seconds() # in metres / second
        self.w1 = w1
        self.w2 = w2
    def __repr__(self):
        return "D(%s, %s, %s, %s)" % (self.distance, self.duration, self.climb, self.speed)


# One degree in meters:
ONE_DEGREE = 1000. * 10000.8 / 90.

EARTH_RADIUS = 6371 * 1000


def to_rad(x):
    return x / 180. * math.pi


def haversine_distance(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    Haversine distance between two points, expressed in meters.

    Implemented from http://www.movable-type.co.uk/scripts/latlong.html
    """
    d_lat = to_rad(latitude_1 - latitude_2)
    d_lon = to_rad(longitude_1 - longitude_2)
    lat1 = to_rad(latitude_1)
    lat2 = to_rad(latitude_2)

    a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
        math.sin(d_lon/2) * math.sin(d_lon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = EARTH_RADIUS * c

    return d


def wpdiff(point, last):
    distance = haversine_distance(point.lat, point.lon, last.lat, last.lon)
    duration = last.time - point.time
    climb = (last.ele - point.ele)/distance
    if duration == timedelta(minutes=0):
        print('zero duration', point, last)
        raise Exception("baad")
    return Diff(distance, duration, climb, point, last)


def calcluate_waypoint_deltas(waypoints):
    return [wpdiff(point,last) for point,last in zip(waypoints, waypoints[1:])]
