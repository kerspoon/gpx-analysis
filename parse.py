from lxml import etree
from datetime import datetime

etree.register_namespace('gpx', 'http://www.topografix.com/GPX/1/1')

namespaces = {
  'xmlns': "http://www.topografix.com/GPX/1/1",
  'gpxx': "http://www.anquet.com/schemas/v1"
}

# get the first waypoint to play with
# wp = root.xpath('xmlns:rte', namespaces=namespaces)[0].xpath('xmlns:rtept', namespaces=namespaces)[0]

class Waypoint(object):
    def __init__(self, lat, lon, ele, time):
        self.lat = float(lat)
        self.lon = float(lon)
        self.ele = float(ele)
        self.time = datetime.strptime(time, '%d/%m/%Y %H:%M:%S') # '27/08/2017 13:46:46'
    def __str__(self):
        return "W(%s, %s, %s, %s)" % (self.lat, self.lon, self.ele, self.time)


# currently just parses the format from "outdoor map navagator"
def parse_gpx_file(file):
    tree = etree.parse(file)
    root = tree.getroot()
    routes = []
    for route in root.xpath('xmlns:rte', namespaces=namespaces):
        waypoints = []
        for waypoint in route.xpath('xmlns:rtept', namespaces=namespaces):
            time = waypoint.xpath('.//gpxx:RtfNotes[1]', namespaces=namespaces)[0].text
            ele = waypoint.xpath('xmlns:ele[1]', namespaces=namespaces)[0].text
            waypoints.append(Waypoint(waypoint.get("lat"), waypoint.get("lon"), ele, time))
            # print(waypoint.get("lat"), waypoint.get("lon"), ele, time)
        routes.append(waypoints)
    return routes
