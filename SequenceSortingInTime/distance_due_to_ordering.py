"""distance_due_to_ordering.py: 

A procedure suggested my Malav.

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
import matplotlib.pyplot as plt
import numpy as np
import itertools

def main( ):
    N = 4
    yvec = [ ]
    reference = range( N )
    for x in itertools.permutations( reference ):
        for loc, i in enumerate( x ):
            diff = abs( loc - reference.index( i ) )
            weight = ( 1.0 / ( 1 + loc) ) ** diff 
            yvec.append( weight )
            # print( diff )
    plt.plot(yvec )
    plt.plot( sorted (yvec), label = 'sorted' )
    plt.legend(loc='best', framealpha=0.4)
    plt.savefig( '%s.png' % sys.argv[0] )
    plt.show( )

if __name__ == '__main__':
    main()
