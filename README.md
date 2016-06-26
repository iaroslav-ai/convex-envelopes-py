#Convexification of Learning from Constraints

This code demonstrates techniques to obtain a convex optimization problem whose solution are equivalent to solution of optimization of the form min_{w \in W,y \in Y} l(w,y) + r(w), where it is assumed that l(w, y) is convex for fixed y and r is convex.

This python code implements the convex extension of the user defined function. For some of the functions, their optimized convex extensions are available. 

You need python 2.7 to use this repository, together with standard python scientific computing routines like numpy, scipy. The easiest way to install those is to use [Anaconda distribution.](https://www.continuum.io/downloads)

This code should work on Windows, Mac OS and Linux. If not, please let us know in the issues.

###Contents:

**general_envelope.py**: implements convex extension of arbitrary function f(w,y), if f is convex for fixed y. See example usage in the file itself or run it to see it in action.
