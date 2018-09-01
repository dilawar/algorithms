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

def _generate_inverse( R, PS ):
    collect = [ ]
    S = R.copy()
    for c, r, s in PS:
        a = np.eye( R.shape[0] )
        a[r,c] = s
        collect.append(a)
        #  print( 'a' )
        #  print( a )
        #  print( 'S' )
        #  S = np.dot(S,a )
        #  print( S )

    res = np.eye( R.shape[0] )
    for a in reversed(collect):
        res = np.dot( a, res )

    # Scale the columns.
    for i in range(R.shape[0]):
        res[:,i] = res[:,i] / R[i,i]
    return res

def invert( mat ):
    A = mat.copy()
    N, M = A.shape 
    assert N == M
    PS = [ ]
    cost = 0
    for i in range( N ):
        p = A[i, i]
        for j in range( N ):
            if i == j:
                continue
            s = - A[i,j] / p
            # do the column operations.
            A[:,j] += s * A[:,i]
            PS.append( (j, i, s) )
    invA = _generate_inverse( A, PS )
    return invA

def test():
    a = np.matrix( '1 2 1; 3 4.0 9;1 1 2.0' )
    #  a = np.matrix( '1 2; 3 4.0' )
    b = invert( a )
    print( 'Our result == ' )
    print( b )
    print( 'Numpy result == ' )
    print( a )
    ainv = np.linalg.inv( a )
    print( 'inverse' )
    print( ainv )

if __name__ == '__main__':
    test()
