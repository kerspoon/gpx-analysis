
from datetime import timedelta
import statistics
import numpy
from parse import parse_gpx_file
from diff import calcluate_waypoint_deltas
import plot
import argparse
import os

# ---------------------------------------------------------------------------- #
# Argument Parsing
# ---------------------------------------------------------------------------- #

parser = argparse.ArgumentParser(description='Process GPX files.')

parser.add_argument('filepath', help='the GPX filename')
parser.add_argument('-d','--datapath', help='where to store the results')
parser.add_argument('-s','--smoothing', default=20, help='how much smoothing to apply to path drawings')
parser.add_argument('-k','--killends', default=2, help='ignore the first and last `k` waypoints (they are often errors)')

args = parser.parse_args()

print("gpx-analysis on", args.filepath)

# ---------------------------------------------------------------------------- #
# Utility Functions
# ---------------------------------------------------------------------------- #

def basic_stats(data):
    return {
      'min': min(data),
      'max': max(data),
      'avg': statistics.mean(data),
      'med': statistics.median(data),
      'dev': statistics.stdev(data)
    }


def print_stats(name, data, outfile):
    stats = basic_stats(data)
    print(name, file=outfile)
    print("  %.2f < %.2f < %.2f" % (stats['min'], stats['med'], stats['max']), file=outfile)
    print("  mu = %.2f, stdev = %.2f" % (stats['avg'], stats['dev']), file=outfile)


def smooth(x,window_len=11,window='hanning'):
    # http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
    s=numpy.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='valid')
    return y

# ---------------------------------------------------------------------------- #
# Main
# ---------------------------------------------------------------------------- #



def main(filepath, datapath, args):
    with open(datapath + "-info.txt", 'w') as outfile:

        print("processing", args.killends, args.smoothing, filepath, datapath)
        print("processing", args.killends, args.smoothing, filepath, datapath, file=outfile)

        with open(filepath, 'rb') as infile:

            routes = parse_gpx_file(infile)

            for waypoints in routes:
                # the first few are often crap
                waypoints = waypoints[args.killends:-args.killends]

                diffs = calcluate_waypoint_deltas(waypoints)

                total_distance = sum(diff.distance for diff in diffs) # in metres
                total_time = sum((diff.duration for diff in diffs), timedelta(minutes=0))

                print("number of waypoints", len(waypoints), file=outfile)
                print("total distance", int(total_distance), "m", file=outfile)
                print("total time", total_time, file=outfile)
                print("total elevation gain", sum(diff.climb for diff in diffs if diff.climb > 0), "m", file=outfile)
                print_stats("distance (metres)", [diff.distance for diff in diffs], outfile)
                print_stats("time (seconds)", [diff.duration.total_seconds() for diff in diffs], outfile)
                print_stats("speed (m/s)", [diff.speed for diff in diffs], outfile)
                print_stats("climb (metres)", [diff.climb for diff in diffs], outfile)

                # why on earth is this different?!
                print("average speed", total_distance/total_time.total_seconds(), "m/s", file=outfile)

                t = smooth([diff.climb for diff in diffs], args.smoothing)
                plt = plot.route(waypoints, t, "steepness of climb")
                plt.savefig(datapath + '-route-steepness.png')

                plt = plot.route(waypoints, None, "altitude of route")
                plt.savefig(datapath + '-route-altitude.png')

                plt = plot.scatter_dist_time(diffs)
                plt.savefig(datapath + '-scatter_dist_time.png')

                plt = plot.scatter_climb_speed(diffs)
                plt.savefig(datapath + '-scatter_climb_speed.png')

                t = smooth([diff.speed for diff in diffs], args.smoothing)
                plt = plot.route(waypoints, t, "speed of route")
                plt.savefig(datapath + '-route-speed.png')


if os.path.isdir(args.filepath):
        for root, dirs, files in os.walk(args.filepath):
            for filename in files:
                if filename.endswith(".gpx"):
                    filepath = os.path.join(root, filename)
                    datapath = os.path.splitext(filepath)[0]
                    main(filepath, datapath, args)
else:
    if None is args.datapath:
        args.datapath = os.path.splitext(args.filepath)[0]
    main(args.filepath, args.datapath, args)
