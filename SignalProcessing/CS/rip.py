"""rip.py: 

Restricted isometric property.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    mpl.style.use( 'seaborn-talk' )
except Exception as e:
    pass
mpl.rcParams['axes.linewidth'] = 0.1
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
import numpy as np
import pypgfplots

N_ = 1000

def norm2( x ):
    return sum( x ** 2.0 ) ** 0.5

def sparse_vector( length, k = 0.05 ):
    return np.random.choice( [0,1], length, p = [ 1 - k, k ] )

def construct_RIP( n ):
    """Only a very sparse matrix shows RIP
    """
    a = np.eye( n )
    a = np.zeros( shape = (n,n) )
    rands = np.random.normal( 0, 0.1, n*n)
    for (i,j), v in np.ndenumerate( a ):
        if rands[n*i+j] > 0.36:
            a[i,j] = 1
    return a

def main( ):
    A = construct_RIP( N_ )
    delta = [ ]
    for i in range( 1000 ):
        x = sparse_vector( N_ )
        y = A.dot( x.T )
        xn, yn = map(norm2, (x,y))
        # ds must be less than 1.
        ds = yn / xn
        delta.append( ds )

    plt.subplot( 211 )
    plt.imshow( A, aspect = 'auto', interpolation = 'none' )
    plt.colorbar( )
    plt.subplot( 212 )
    plt.plot( delta )
    plt.ylabel( '$\\frac{||Ax||}{||x||}$' )
    plt.savefig( '%s.png' % sys.argv[0] )

    #pypgfplots.standalone( matrix = A
    #        , title = 'RIP matrix?' 
    #        , every = 10
    #        , outfile = 'figure_rip.tex' 
    #        )

if __name__ == '__main__':
    main()
