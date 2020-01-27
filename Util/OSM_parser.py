"""
OSM_parser is used to filter all non relevant objects.
In first run we go through the file to remember all relevant objects
In second run we go again through the file to write these relevant remembered objects to a new file
"""

import osmium as o
import sys
from xml.etree.cElementTree import parse


## References of relevant objects are stored
class WaterwayFilter(o.SimpleHandler):

    def __init__(self):
        super(WaterwayFilter, self).__init__()
        self.nodes = set()

    def filter(self, tags):
        if tags['waterway'] == 'river':
            return 1
        else:
            return 0

    def way(self, w):
        if 'waterway' in w.tags \
                and (w.tags['waterway'] == 'riverbank' \
                or w.tags['waterway'] == 'river' \
                or w.tags['waterway'] == 'dock' \
                or w.tags['waterway'] == 'canal'):
            print w.tags
            print '--'
            for n in w.nodes:
                self.nodes.add(n.ref)


## All related objects with reminded objects are written to new file
class WaterwayWriter(o.SimpleHandler):

    def __init__(self, writer, nodes):
        super(WaterwayWriter, self).__init__()
        self.writer = writer
        self.nodes = nodes

    def node(self, n):
        if n.id in self.nodes:
            self.writer.add_node(n)

    def way(self, w):
        if 'waterway' in w.tags \
                and (w.tags['waterway'] == 'riverbank' \
                or w.tags['waterway'] == 'river' \
                or w.tags['waterway'] == 'dock' \
                or w.tags['waterway'] == 'canal'):
            self.writer.add_way(w)


## Get coordinates of every object in new file comparing with old file
class WaterwayCollector(o.SimpleHandler):

    def __init__(self, nodes):
        super(WaterwayCollector, self).__init__()
        self.nodes = nodes
        self.coords = set()

    def node(self, n):
        if n.id in self.nodes:
            self.coords.add((n.location.lon, n.location.lat))


## Get coordinates of every object in new file
class WaterwayCollector2(o.SimpleHandler):

    def __init__(self):
        super(WaterwayCollector2, self).__init__()
        self.coords = set()
        self.areas = []

    def node(self, n):
        self.coords.add((n.location.lon, n.location.lat, n.id ))

    def way(self, w):
        way = []
        for n in w.nodes:
            way.append(n.ref)
        self.areas.append(way)

class BoundsFinder():

    def __init__(self, file):
        self.file = file
        self.minlon = 0
        self.minlat = 0
        self.maxlon = 0
        self.maxlat = 0

    def find(self):
        root = parse(self.file).getroot()

        # Load bounds element.
        attrib = root.find('bounds').attrib
        self.minlon = float(attrib['minlon'])
        self.minlat = float(attrib['minlat'])
        self.maxlon = float(attrib['maxlon'])
        self.maxlat = float(attrib['maxlat'])

def main():
    if len(sys.argv) != 3:
        print("Usage: python OSM_parser.py <infile> <outfile>")
        sys.exit(-1)

    # go through the ways to find all relevant nodes
    ways = WaterwayFilter()
    ways.apply_file(sys.argv[1])

    # go through the file again and write out the data
    writer = o.SimpleWriter(sys.argv[2])
    WaterwayWriter(writer, ways.nodes).apply_file(sys.argv[1])

    writer.close()

    nodes = WaterwayCollector(ways.nodes)
    nodes.apply_file(sys.argv[2])

    boundFinder = BoundsFinder(sys.argv[1])
    boundFinder.find()

if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
    print(__file__ + " Done!!")