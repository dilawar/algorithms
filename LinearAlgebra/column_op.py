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
import helper
import numpy as np

def _generate_inverse_fast(R, PS):
    S = R.copy()
    T = np.eye( S.shape[0] )
    for ps in PS:
        for p in ps:
            T = helper._multiply_perm(T, p)
    print( T )
    return T


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
        assert np.isclose( ainv1, ainv2 ).all()

def benchmark( ):
    import time
    import matplotlib.pyplot as plt
    print( 'Size, Time' )
    X, Y, Ynumpy = [], [], []
    for i in np.linspace(10, 400, 10):
        ts, ts2 = [], []
        t = time.time()
        invert( np.random.rand(int(i),int(i)) )
        s = time.time() - t
        ts.append( s )

        t = time.time()
        np.linalg.inv( np.random.rand(int(i),int(i)) )
        s = time.time() - t
        ts2.append( s )

        print( "%s,%g,%g" % (i, np.mean(ts), np.std(ts)) )
        X.append( i )
        Y.append( ts )
        Ynumpy.append( ts2 )

    ax = plt.subplot( 111 )
    ax1 = ax.twinx()
    ax.plot( X, Y, '-o', color = 'blue' )
    ax.set_ylabel( 'ColOp (blue)' )
    ax1.plot( X, Ynumpy, '-x', color = 'red' )
    ax1.set_ylabel( 'numpy (red)' )
    plt.xlabel( 'Size' )
    plt.savefig( 'benchmark.png' )


if __name__ == '__main__':
    test()
    test_random()
    benchmark( )
