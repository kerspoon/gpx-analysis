
from datetime import timedelta
import statistics
import numpy
from parse import parse_gpx_file
from diff import calcluate_waypoint_deltas
import plot
import argparse
import os
import csv
from scipy.optimize import curve_fit
import math


# ---------------------------------------------------------------------------- #
# Argument Parsing
# ---------------------------------------------------------------------------- #

parser = argparse.ArgumentParser(description='Process GPX files.')

parser.add_argument('filepath', help='the GPX filename')
parser.add_argument('-d','--datapath', help='where to store the results')
parser.add_argument('-s','--smoothing', type=int, default=20, help='how much smoothing to apply to path drawings')
parser.add_argument('-k','--killends', type=int, default=2, help='ignore the first and last `k` waypoints (they are often errors)')
parser.add_argument('-c','--csv', action='store_true', help='save the stats to a csv file')



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

                if len(waypoints) <= args.killends*2:
                    print("skipping, not enough data points after killing ends.", len(waypoints), "datapoints")
                    print("skipping, not enough data points after killing ends.", len(waypoints), "datapoints", file=outfile)
                    continue

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
                print_stats("speed (km/h)", [diff.speed*3.6 for diff in diffs], outfile)
                print_stats("climb (metres)", [diff.climb for diff in diffs], outfile)

                # why on earth is this different?!
                print("average speed", total_distance/total_time.total_seconds()*3.6, "km/h", file=outfile)


                t = smooth([diff.steepness for diff in diffs], args.smoothing)
                plt = plot.route(waypoints, t, "steepness of climb")
                plt.savefig(datapath + '-route-steepness.png')
                plt.close()

                plt = plot.route(waypoints, None, "altitude of route")
                plt.savefig(datapath + '-route-altitude.png')
                plt.close()

                plt = plot.scatter_dist_time(diffs)
                plt.savefig(datapath + '-scatter_dist_time.png')
                plt.close()


                t = smooth([diff.speed for diff in diffs], args.smoothing)
                plt = plot.route(waypoints, t, "speed of route")
                plt.savefig(datapath + '-route-speed.png')
                plt.close()


                def generic_naismith(slope, p1, p2):
                    """slope is the x coordinate that this uses to predict the
                    y value (speed), which is returned. p1 and p2 are the
                    parameters. They are usually a = 12 min/km, b = 100
                    min/km-elevation"""
                    return 60.0/(p1 + p2*numpy.tan(numpy.deg2rad(slope)))

                xdata = [math.degrees(math.atan(diff.steepness)) for diff in diffs if diff.steepness >= 0]
                ydata = [diff.speed*3.6 for diff in diffs if diff.steepness >= 0]
                popt, pcov = curve_fit(generic_naismith, xdata, ydata, p0=(12.0,100))

                plt = plot.scatter_climb_speed(diffs, popt)
                plt.savefig(datapath + '-scatter_climb_speed.png')
                plt.close()

                print("generic_naismith curve fitting, min/km distance then for elevation", popt, file=outfile)

                if args.csv:
                    args.csv.writerow([
                      '', filepath, len(waypoints),
                      int(total_distance), total_time,
                      sum(diff.climb for diff in diffs if diff.climb > 0),
                      total_distance/total_time.total_seconds()*3.6,
                      statistics.mean(diff.speed*3.6 for diff in diffs),
                      popt[0],
                      popt[1]
                    ])

if args.csv:
    csvfile = open('data.csv', 'w')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Date', 'description', '# waypoints', 'distance', 'time', 'elevation gain', 'speed'])
    args.csv = csvwriter

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
