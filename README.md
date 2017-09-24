
# Data Analysis for Anquet (outdoor map navigator) GPX files

run `main.py` and you will see a load of data and graphs will be saved as `png` files. Note that you need to use Anquet GPX files (annoyingly they use a non standard way of saving the timestamp)

Usage: `python main.py filepath` (uses python 3)

where `filepath` is either a gpx file or a folder containing them.

It will print out various stats:

- number of waypoints
- distance (total, median, mean, stdev)
- time (total, median, mean, stdev)
- speed (min, max, median, mean, stdev)
- climb (min, max, median, mean, stdev)
- total elevation gain

And also graph:

- a drawing of the path coloured by:
 + altitude
 + speed
 + steepness
- a scatter plot of
 + speed vs. steepness of climb
 + distance and duration

# To Do

- Read options from command line
  + select level of smoothing for graphs
- Research how to do least squares fitting on the speed/slope scatterplot. We probably need three variables to fit: the midpoint (x,y) and the slope. OR we can look at fitting against X km/h + Y for every 10m elevation gain - which will be similar, but simpler.

# Notes

## Non-linear regression

- http://www.stat.colostate.edu/regression_book/chapter9.pdf
- https://en.wikipedia.org/wiki/Non-linear_least_squares
- https://en.wikipedia.org/wiki/Segmented_regression
