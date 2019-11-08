import OSM_parser_v2 as parser
import Potential_field as PF
import Util.Transform as transform
import Sources.configs.potentialFieldConfig as pfConfig
import math

if __name__ == '__main__':
    if len(parser.sys.argv) != 3:
        print("> Usage: python main.py <infile> <outfile>")
        parser.sys.exit(-1)

    print("-----------------")
    print(" Start parsing OSM file")
    print("-----------------")

    # go through the ways to find all relevant nodes
    ways = parser.WaterwayFilter()
    ways.apply_file(parser.sys.argv[1])

    print "> Number of nodes in file: ", len(ways.nodes)

    # go through the file again and write out the data
    writer = parser.o.SimpleWriter(parser.sys.argv[2])
    parser.WaterwayWriter(writer, ways.nodes).apply_file(parser.sys.argv[1])

    writer.close()

    nodes = parser.WaterwayCollector(ways.nodes)
    nodes.apply_file(parser.sys.argv[2])

    boundFinder = parser.BoundsFinder(parser.sys.argv[1])
    boundFinder.find()

    print("-----------------")
    print(" Start potential field generator")
    print("-----------------")

    # ref lon and lat to more usable variables
    ref_lonmin = boundFinder.minlon
    ref_lonmax = boundFinder.maxlon
    ref_latmin = boundFinder.minlat
    ref_latmax = boundFinder.maxlat

    # ref x and y
    ref_xmin = transform.lonToX(ref_lonmin - ref_lonmin, 0)
    ref_xmax = transform.lonToX(ref_lonmax - ref_lonmin, 0)
    ref_ymin = transform.latToY(ref_latmin - ref_latmin, 0)
    ref_ymax = transform.latToY(ref_latmax - ref_latmin, 0)

    # total PF mapsize
    mapSizeX, mapSizeY = transform.coordsToMeters(boundFinder.maxlon, boundFinder.maxlat, boundFinder.minlon, boundFinder.minlat)

    # list of all obstacles
    ox = []
    oy = []

    # ship x and y
    sx, sy = transform.coordsToMeters(pfConfig.slon - ref_lonmin, pfConfig.slat - ref_latmin, ref_lonmin - ref_lonmin, ref_latmin - ref_latmin)

    # obstacles x and y
    for coord in nodes.coords:
        x, y = transform.coordsToMeters(coord[0] - ref_lonmin, coord[1] - ref_latmin, ref_lonmin - ref_lonmin, ref_latmin - ref_latmin)
        ox.append(x)
        oy.append(y)

    print("> Producing map...")

    # list of interesting obstacles
    map_ox = []
    map_oy = []

    # extracting interesting obstacles
    for i, _ in enumerate(ox):
        if ox[i] <= sx + pfConfig.right and ox[i] >= sx - pfConfig.left and oy[i] <= sy + pfConfig.front and oy[i] >= sy - pfConfig.back:
            map_ox.append(ox[i])
            map_oy.append(oy[i])

    # calc potential field
    pmap, xw, yw = PF.calc_potential_field(ref_xmin, ref_xmax, ref_ymin, ref_ymax, sx, sy, pfConfig.gx, pfConfig.gy, map_ox, map_oy, pfConfig.grid_size, pfConfig.robot_radius)

    print("-----------------")
    print(" Start potential field drawing")
    print("-----------------")

    if PF.show_animation:
        PF.draw_heatmap(pmap, xw, yw)
