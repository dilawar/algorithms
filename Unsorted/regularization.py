"""regularization.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def xs( ts, eps = 1e-10 ):
    return 0.1 * ts + np.sin( ts / eps / eps ) * eps

def main( ):
    ts = np.linspace( 0, 1e-1, 10000 )
    pos = xs( ts )
    plt.subplot( 212 )
    vs = np.diff( pos )
    plt.plot( ts[1:], vs )

    # Now recompute xs and plot
    plt.subplot( 211 )
    plt.plot( ts, pos )
    plt.plot( ts[1:], np.cumsum( vs ), alpha = 0.5 )

    plt.savefig( '%s.png' % sys.argv[0] )

if __name__ == '__main__':
    main()
