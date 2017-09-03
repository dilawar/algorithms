"""l2_min_norms.py: 

A very stupid way to solver under-determined system which minimized l2-norm.
"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    mpl.style.use( 'ggplot' )
except Exception as e:
    pass
mpl.rcParams['axes.linewidth'] = 0.2
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

import numpy as np

# Three numbers and their sum is N.
n = 5
S = 10
L = 3*S
prob = '$\sum_{i=%d}x_i = %d, \quad \\forall x_i \in \\left[ %d,%d \\right]$' % (n, S, -L, L)

def l2norm( xs ):
    return ( np.sum( xs ** 2.0 ) / len( xs )) ** 0.5

def l1norm( xs ): 
    return ( np.sum( np.abs( xs ) ) / len( xs )) ** 0.5

def l0norm( xs ):
    return len( xs[xs != 0] )

def main( ):
    N = 10000
    xs = np.random.randint( -L, L+1, N )
    ys = np.random.randint( -L, L+1, N )
    solutions = [ ]
    l0, l1, l2 = [ ], [ ], [ ]
    for x, y in zip( xs, ys ):
        z = S - x - y
        if (x,y,z) in solutions:
            continue 
        else:
           solutions.append( (x,y,z) )
        nums = np.array( [ x, y, z ] )
        l0.append( (l0norm(nums), nums ) )
        l1.append( (l1norm(nums), nums ) )
        l2.append( (l2norm(nums), nums ) )

    ls = [ l0, l1, l2 ]
    print( 'Plotting now..' )

    plt.figure( )
    for i, l in enumerate( ls ):
        plt.subplot( len(ls), 2, 2*i+1 )
        x, y = zip( *l )
        plt.hist( x, bins = 20, label = '$L_%d$ norm' % i )
        plt.legend(framealpha=0.4)
    plt.xlabel( 'Histogram of solutions' )

    for i, l in enumerate( ls ):
        plt.subplot( len(ls), 2, 2*i+2 )
        sortedL = sorted( l, key = lambda x: x[0] )[:10]
        x, y = zip( *sortedL )
        xlabels = [ ','.join(map(str,a)) for a in y ]
        plt.plot( x, '-o', label = '$L_%d$ norm' % i )
        plt.xticks( range( len(xlabels) ), xlabels, rotation = 'vertical' )
        plt.legend(framealpha=0.4)

    plt.xlabel( 'Sorted solutions ' )
    plt.suptitle( 'Solutions : %s' % prob )
    plt.tight_layout( pad = 2 )
    plt.savefig( '%s.png' % sys.argv[0] )


if __name__ == '__main__':
    main()
