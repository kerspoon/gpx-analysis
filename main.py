
from datetime import timedelta
import statistics
import numpy
from parse import parse_gpx_file
from diff import calcluate_waypoint_deltas
import plot
import argparse
import os
from decode import decode

# ---------------------------------------------------------------------------- #
# Argument Parsing
# ---------------------------------------------------------------------------- #

parser = argparse.ArgumentParser(description='Process GPX files.')

parser.add_argument('filepath', help='the GPX filename')
parser.add_argument('-d','--datapath', help='where to store the results')

args = parser.parse_args()

if None is args.datapath:
    args.datapath = os.path.splitext(args.filepath)[0]

print("parsing", args.filepath)
print("datapath", args.datapath)

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


def print_stats(name, data):
    stats = basic_stats(data)
    print(name)
    print("  %.2f < %.2f < %.2f" % (stats['min'], stats['med'], stats['max']))
    print("  mu = %.2f, stdev = %.2f" % (stats['avg'], stats['dev']))


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

def main(filepath, datapath):

    with open(filepath, 'rb') as file:

        routes = parse_gpx_file(file)

        for waypoints in routes:
            # the first few are often crap
            waypoints = waypoints[2:-2]

            diffs = calcluate_waypoint_deltas(waypoints)

            total_distance = sum(diff.distance for diff in diffs) # in metres
            total_time = sum((diff.duration for diff in diffs), timedelta(minutes=0))

            print("number of waypoints", len(waypoints))
            print("total distance", int(total_distance), "m")
            print("total time", total_time)
            print("total elevation gain", sum(diff.climb for diff in diffs if diff.climb > 0), "m")
            print_stats("distance (metres)", [diff.distance for diff in diffs])
            print_stats("time (seconds)", [diff.duration.total_seconds() for diff in diffs])
            print_stats("speed (m/s)", [diff.speed for diff in diffs])
            print_stats("climb (metres)", [diff.climb for diff in diffs])

            # why on earth is this different?!
            print("average speed", total_distance/total_time.total_seconds(), "m/s")

            t = smooth([diff.climb for diff in diffs], int(len(waypoints)/10))
            plt = plot.route(waypoints, t, "steepness of climb")
            plt.savefig(datapath + '-route-steepness.png')

            plt = plot.route(waypoints, None, "altitude of route")
            plt.savefig(datapath + '-route-altitude.png')

            plt = plot.scatter_dist_time(diffs)
            plt.savefig(datapath + '-scatter_dist_time.png')

            plt = plot.scatter_climb_speed(diffs)
            plt.savefig(datapath + '-scatter_climb_speed.png')

            t = smooth([diff.speed for diff in diffs], 20)
            plt = plot.route(waypoints, t, "speed of route")
            plt.savefig(datapath + '-route-speed.png')


main(args.filepath, args.datapath)
