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
    for ps in PS:
        a = np.eye( R.shape[0] )
        for c, r, s in ps:
            a[r,c] = s
        collect.append(a)

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
        ps = []
        p = A[i, i]
        for j in range( N ):
            if i == j:
                continue
            s = - A[i,j] / p
            # do the column operations.
            A[:,j] += s * A[:,i]
            ps.append( (j, i, s) )
        PS.append( ps )
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

def test_random( ):
    """docstring for test_random"""
    for i in range(100):
        a = np.random.rand( 10, 10 )
        ainv1 = np.linalg.inv( a )
        ainv2 = invert( a )
        #  print( 'Numpy solution' )
        #  print( ainv1)
        #  print( 'Our solution' )
        #  print( ainv2 )
        assert np.isclose( ainv1, ainv2 ).all()

def benchmark( ):
    import time
    for i in range(10, 100, 10):
        t = time.time()
        invert( np.random.rand(i, i) )
        s = time.time() - t
        print( "Size is %d. Time %g" % (i,s) )

if __name__ == '__main__':
    test()
    benchmark( )
    #  test_random()
