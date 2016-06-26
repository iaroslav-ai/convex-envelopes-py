"""
This script demonstrates a general approach on how to
obtain a convex extension of some function of the form
            f: W x Y -> R
Where W is typically subset of R^n, and Y is a subset
of {0,1}^m. f needs to be convex for fixed Y.

This code is meant for educational purposes only, and
therefore it is *very* slow.
"""

import numpy as np
from scipy.optimize import minimize
from itertools import combinations


# convex envelope of f at point w in W, y in conv(Y)
def cvx_env(w, y, W, Y, f):
    """

    :param w: continuous point w in W at which to compute the envelope
    :param y: continuous value y in conv(Y) at which to compute the envelope
    :param W: box constraints that define feasible w
    :param Y: set of all feasible y
    :param f: python function f: W x Y -> R whose convex envelope is computed.
              this function needs to be convex for fixed y.
    :return: the value of convex envelope of f at point w, y.
    """

    S = len(Y[0]) # dimensions of Y
    Csz = min(S+1, len(Y)) # size of combination
    Yc = [] # all simplices of Y containing y

    # below is used in further computations
    Ce = np.ones((Csz, S+1))
    ye = np.concatenate([y, [1]])

    # find all simplices of Y where y belong to
    for C in combinations(Y, Csz):
        # check if y in conv(C)
        Ce[:-1, :] = np.array(C).T
        a, res, rank, s = np.linalg.lstsq(Ce, ye)

        if np.all(a >= 0.0):
            Yc.append((np.array(C), a))

    # candidate values for the convex envelope
    candidate_values = []

    # compute inner optimization problem
    for C, a in Yc:

        # initialization for optimization
        th0 = np.array([w for y in C])
        shp = th0.shape

        # define inner objective
        def fc(theta):
            result = 0.0
            rtheta = np.reshape(theta, shp)
            for thv, yv, av in zip(rtheta, C, a):
                result += f(thv, yv) * av
            return result

        # linear constraint
        def ct(theta):
            rtheta = np.reshape(theta, shp)
            return np.dot(rtheta.T, a) - np.array(w)

        # solve inner minimization problem
        fmin = minimize(fc, th0, bounds=W*len(C), constraints={'type':'eq', 'fun': ct}).fun
        candidate_values.append(fmin)

    # result is minimum of candidate values
    return min(candidate_values)


if __name__ == "__main__":
    # below is a simple example for convex envelope
    # with single value as w and single value as y

    # set of all feasible y in Y
    Y = [[0], [1]]

    # set of all feasible values of W;
    # Defined as box set
    W = [[-3,3],]


    # some abstract function convex for fixed Y
    def f(w, y):
        x = 1.0
        return np.maximum(1 - x * w * (y*2-1), 0.0) + np.sum(np.abs(w))

    print cvx_env([0.1], [0.5], W, Y, f)

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    Xp, Yp, Zp = [], [], []

    for w in np.linspace(-2, 2):
        for y in np.linspace(0.001, 0.999):
            Xp.append(w)
            Yp.append(y)
            z = cvx_env([w], [y], W, Y, f)
            Zp.append(z)

    ax.scatter(Xp, Yp, Zp)

    ax.set_xlabel('w')
    ax.set_ylabel('y')
    ax.set_zlabel('env(f)(w,y)')

    plt.show()