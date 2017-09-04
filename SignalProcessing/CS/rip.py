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
import matplotlib.pyplot as plt
import numpy as np

def norm2( x ):
    return sum( x ** 2.0 ) ** 0.5

def sparse_vector( length, k = 0.1 ):
    return np.random.choice( [0,1], length, p = [ 1 - k, k ] )

def main( ):
    A = np.random.random_integers( 0, 1, (100, 100) )
    print( A )
    x = sparse_vector( 100 )
    delta = [ ]
    for i in range( 100 ):
        x = sparse_vector( 100 )
        y = A.dot( x.T )
        d = norm2( x ) - norm2( y )
        delta.append( d )
        print(  x )
        print( y )

    print( delta )

if __name__ == '__main__':
    main()
