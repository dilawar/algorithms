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
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    mpl.style.use( 'seaborn-talk' )
except Exception as e:
    pass
mpl.rcParams['axes.linewidth'] = 0.1
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def sync_index( a, b ):
    signA = np.sign( np.diff( a ) )
    signB = np.sign( np.diff( b ) )
    return np.sum( signA * signB ) / len( signA )


def main( ):
    N = 10**3
    time = np.linspace( 0, 30, 10**3 )
    a = np.sin( time )
    N = 2 * 2
    bs = [ time, a, np.cos(time), a + np.random.uniform( N ) ]
    for i, b in enumerate( bs ):
        plt.subplot( len(bs) / 2, 2, i % 2 + 1)
        plt.plot( a )
        plt.plot( b )
        plt.title( sync_index( a, b ) )
    outfile = 'sync_index.png' 
    plt.savefig( outfile )
    print( 'All done. Wrote to %s' % outfile )


if __name__ == '__main__':
    main()
