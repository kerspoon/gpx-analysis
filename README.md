
# Data Analysis for Anquet (outdoor map navigator) GPX files

run `main.py` and you will see a load of data and graphs will be saved as `png` files. Note that you need to use Anquet GPX files (annoyingly they use a non standard way of saving the timestamp). You files will be stored in `C:\program data\outdoor map navigator\7578577567240\Anquet Connect\User Data Files\`

Oh crappy programme - Anquet exports GPX file three different ways. In the folder above it uses the standard (with `trkseg`). If you do `user data -> manage -> export all` it leaves off the timestamps making them worthless for analysis. If you `user data -> open` then `user data -> Export to GPX` it uses utf-16 with BOM and a non standard GPX extension to save the timestamp, it also uses route rather than tracklog (`rtep` not `trkseg`). This one is made for either copying from the folder above or `Export to GPX`. It would be fairly easy to change this for other types of GPX file.

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
 + speed vs. steepness of climb (\*)
 + distance and duration

\* the speed steepness scatterplot also shows Naismith's Rule and a least squares fit of the same formula as Naismith's Rule with the optimal 2 parameters. You can see the fitted values in the stats file.

# To Do

- Research how to do least squares fitting on the speed/slope scatterplot. We probably need three variables to fit: the midpoint (x,y) and the slope. OR we can look at fitting against X km/h + Y for every 10m elevation gain - which will be similar, but simpler.

# Notes

## Naismith's Rule

- https://en.wikipedia.org/wiki/Naismith%27s_rule
- https://www.wolframalpha.com/input/?i=60%2F(12+%2B+(+tan(40+deg)+*100))

## Non-linear regression & Curve fitting

- http://www.walkingrandomly.com/?p=5215
- http://www.stat.colostate.edu/regression_book/chapter9.pdf
- https://en.wikipedia.org/wiki/Non-linear_least_squares
- https://en.wikipedia.org/wiki/Segmented_regression
