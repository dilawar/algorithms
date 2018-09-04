"""test_sym_mat.py: 

Inverse of symmetrical matrix. Diagonal entries are zero.

https://www.jstor.org/stable/2690437?seq=1#page_scan_tab_contents

And,
https://www.jstor.org/stable/2690437?seq=1#page_scan_tab_contents

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
import random

random.seed( 1 )

def main( ):
    N = 3
    G = np.eye( N, dtype=float )
    H = np.zeros( (N,N) )
    for i in range( 1 ):
        i = random.choice( range(N) )
        j = random.choice( range(N) )
        while j == i:
            j = random.choice( range(N) )
        print( i, j )
        H[i, j] = random.random()
        #  a[j, i] = random.random()
    invG = np.linalg.inv( G)
    tr = np.trace( H * invG )
    res1 = invG - (1/(1+tr)) * np.dot(np.dot(invG, H), invG)
    expected = np.linalg.inv( G + H )
    assert np.isclose(res1, expected).all(), res1
    print( res1 )

if __name__ == '__main__':
    main()

