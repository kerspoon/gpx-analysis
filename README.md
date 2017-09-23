
# Data Analysis for Anquet (outdoor map navigator) GPX files

run `main.py` and you will see a load of data and graphs will be saved as `png` files.

# To Do

- Read options from command line
  + select level of smoothing for graphs
  + process an entire folder not just one file
- Research how to do least squares fitting on the speed/slope scatterplot. We probably need three variables to fit: the midpoint (x,y) and the slope. OR we can look at fitting against X km/h + Y for every 10m elevation gain - which will be similar, but simpler.

# Notes

## Non-linear regression

- http://www.stat.colostate.edu/regression_book/chapter9.pdf
- https://en.wikipedia.org/wiki/Non-linear_least_squares
- https://en.wikipedia.org/wiki/Segmented_regression
