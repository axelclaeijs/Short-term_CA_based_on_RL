from imposm.parser import OSMParser
import osmapi as osm

# instantiate OSM API
api = osm.OsmApi()

# simple class that handles the parsed OSM data.
class WaterwayCounter(object):
    waterwaysCnt = 0
    waterwaysObj = []
    waterwayCoords = []

    def ways(self, ways):
        # callback method for ways
        for osmid, tags, refs in ways:
            if 'waterway' in tags:
                self.waterwaysObj.append(refs)
                self.waterwaysCnt += 1
                for value in refs:
                    self.waterwayCoords.append((api.NodeGet(value)['lat'], api.NodeGet(value)['lon']))

def main():
    # instantiate counter and parser and start parsing
    counter = WaterwayCounter()
    p = OSMParser(concurrency=4, ways_callback=counter.ways)
    p.parse('Sources/osm_maps/map.osm')

    # done
    print counter.waterwaysCnt
    print counter.waterwayCoords[1]

if __name__ == '__main__':
    print(__file__ + " start parsing")
    main()
    print(__file__ + " done parsing")