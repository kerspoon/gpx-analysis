
import matplotlib.pyplot as plt
import pylab
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


def create_line_collection(x, y, t=None):
    if t is None:
        t = np.linspace(0, 100, len(x))
    t = np.asarray(t)
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=plt.get_cmap('Greens'),
                        norm=plt.Normalize(min(t), max(t)))
    lc.set_array(t)
    lc.set_linewidth(3)
    return lc

def route(waypoints, t=None, title=None):
    x = [w.lon for w in waypoints]
    y = [w.lat for w in waypoints]

    # by default show the elevation as the colour
    if t is None:
        t = [w.ele for w in waypoints]

    lcc = create_line_collection(x, y, t)
    fig = plt.figure(facecolor = '0.05')

    # don't fuck up the aspect ratio while plotting
    # don't bother showing the axis either, they mean nothing
    ax = plt.Axes(fig, [0., 0., 1., .9], )
    ax.set_aspect('equal')
    ax.set_axis_off()
    fig.add_axes(ax)

    if title is not None:
        plt.title(title, color="green")

    # but do show all the data on the viewport, not some random other segment of
    # the graph. And give it a bit of room on either size (currently 20% of the
    # total width of the data for each axis)
    xsize = max(x)-min(x)
    ysize = max(y)-min(y)
    plt.xlim(min(x)-xsize/20, max(x)+(2*xsize/20))
    plt.ylim(min(y)-ysize/20, max(y)+(2*ysize/20))

    plt.gca().add_collection(lcc)

    return plt


def scatter_dist_time(diffs):
    fig = plt.figure()
    plt.title('correlation between distance and duration')
    plt.scatter([diff.distance for diff in diffs],[diff.duration.total_seconds() for diff in diffs])
    plt.xlabel('distance')
    plt.ylabel('time')
    return plt

def scatter_climb_speed(diffs):
    fig = plt.figure()
    plt.title('correlation between speed and steepness of climb')
    plt.scatter([diff.climb for diff in diffs],[diff.speed for diff in diffs])
    plt.xlabel('climb')
    plt.ylabel('speed')
    return plt

def show():
    plt.show()
