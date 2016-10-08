"""synchronization.py: 

Tell if two signals are synchronized.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import math
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    # mpl.style.use( 'seaborn-talk' )
    mpl.style.use( 'ggplot' )
except Exception as e:
    pass
mpl.rcParams['axes.linewidth'] = 0.1
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def sync_index( a, b ):
    # Must smooth out the high frequency components.
    assert min(len( a ), len( b )) > 30, "Singal too small"
    kernal = np.ones( 31 ) / 31.0
    a = np.convolve( a, kernal, 'same' )
    b = np.convolve( b, kernal, 'same' )
    signA = np.sign( np.diff( a ) )
    signB = np.sign( np.diff( b ) )
    s1 = np.sum( signA * signB ) / len( signA )
    s2 = np.convolve(signA, signB).max() / len( signA )
    return (s1, s2)

def sync_index_correlate( a, b ):
    same = np.correlate( a, a )[0]
    other = np.correlate( a, b)[0]
    return other / same


def main( ):
    N = 10**3
    time = np.linspace( 0, 50, N )
    a = 1.2 +  np.sin( time )

    bs = [ np.random.uniform( -0.1, 0.1, N ), np.random.normal( 0.1, 0.2, N )
            , a, a * 0.2
            , np.cos(time) , a + np.random.uniform(-0.2,0.1,N) 
            , a + np.random.normal( 0, 0.2, N ), np.sin( 3.0 * time / 7.0 )
            ]

    numRows = math.ceil( len(bs) / 2.0 )
    plt.figure( figsize=(8,1.5 * numRows ) )
    for i, b in enumerate( bs ):
        plt.subplot( numRows, 2, i + 1)
        plt.plot( a, alpha = 0.5 )
        plt.plot( b, alpha = 0.5 )
        plt.xticks( [] )
        s = sync_index( a, b )
        p = sync_index_correlate( a, b )
        t = '$S=(%.3f,%.3f)$, $c=%.3f$' % (s[0], s[1], p )
        plt.title( t, loc = 'center', fontsize = 10 )
        plt.xlabel( 'Plot %1d' % i )
    outfile = 'sync_index.png' 
    plt.tight_layout( )
    plt.savefig( outfile )
    print( 'All done. Wrote to %s' % outfile )


if __name__ == '__main__':
    main()
