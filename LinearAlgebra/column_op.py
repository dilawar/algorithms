"""column_op.py: 

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

def invert( a ):
    N, M = a.shape 
    print( a )

def test():
    a = np.matrix( '1 2; 3 4' )
    b = invert( a )
    print( b )

if __name__ == '__main__':
    test()
