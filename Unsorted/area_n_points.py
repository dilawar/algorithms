"""area_n_points.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import numpy as np

def triangularization( pts ):
    return []

def area(pts, plot = True):
    if plot:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        x, y = zip(*pts)
        mpl.style.use( ['bmh', 'fivethirtyeight'] )
        plt.plot( x, y, 'o' )
        plt.savefig( 'test.png' )

    a = 0.0
    tris = triangularization(pts)
    if plot:
        for tri in tris:
            print(tri)

    return a

def main():
    n = 6
    xs = np.random.randint( 0, 100, n)
    ys = np.random.randint( 0, 100, n)
    pts = list(zip(xs, ys))
    print( pts )
    a = area(pts)
    print( '[INFO] Area bouded by points %f' % a)

if __name__ == '__main__':
    main()

