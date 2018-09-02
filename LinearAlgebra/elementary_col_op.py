"""
Elementary column operations.
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

def perm_to_mat( p, N):
    # c1 <- c1 * s*c2
    m = np.eye( N )
    c1, c2, s = p
    m[c2,c1] = s
    return m

def apply_permutation( a, p):
    # c1 <- c1 + s*c2
    b = a.copy()
    c1, c2, s = p
    b[:,c1] += s*b[:,c2]
    return b

def _multiply_perm( mat, p ):
    T = mat.copy()
    q, p, s = p
    for i in range(T.shape[0]):
        T[i,q] += T[i,p]*s
    return T

def test_a( ):
    # Test multiplication by elementary column op.
    t = np.matrix( '1 2 3 4 0; 0 1 0 0 0; 0 0 1 0 0; 0 0 0 1 0; 0 0 0 0 1', dtype=np.float )
    p = (2, 1, -1.5 )
    print( t )
    t1 = _multiply_perm( t, p )
    pm = perm_to_mat( p, t.shape[0] )
    expected = np.dot(t, pm)
    print( p )
    print( 'ElColOp Mat ' )
    print( pm )
    print( 'Got' )
    print( t1 )
    print( 'Expected ' )
    print( expected )


def gen_permutations_mat( PS, N ):
    # generate permuation matrix combining all permuatations given in the list
    # of PS.
    print( "[INFO ] Generating permuation matrix out of %s" % PS ) 
    T = np.eye( N )
    for p in PS:
        T = _multiply_perm(T, p)
        print( T )
    return T

def test_perm_to_mat( a ):
    p1 = (1,2,-1)
    p2 = (2,1,-2)

    for p in [p1, p2]:
        pm = perm_to_mat( p, 3 )
        a1 = np.dot(a, pm )
        a2 = apply_permutation(a, p)
        print( 'permutation', p )
        assert np.isclose( a1, a2).all(), "Test failed"
        print( 'Test passed' )

def test_fast_perm_mult( A ):
    print( '===== Test multiplication of permutations matrices' )
    a = A.copy()
    p1 = (1,2,-1)
    p2 = (2,1,-2)
    p3 = (2,1,-0.5)
    pS = []
    for p in [p1, p2, p3]:
        print( a )
        pm = perm_to_mat(p, 3)
        pS.append( pm )
        a = np.dot(a, pm)

    # multiply as pS
    t = np.eye(A.shape[0])
    for p in pS:
        t = np.dot(t, p)
    a1 = np.dot(A, t)
    assert np.isclose(a, a1).all()
    print( 'Final answer after all application of permutations' )
    print( a )
    # Now generate permutation matrix
    P = gen_permutations_mat( [p1, p2, p3], 3 )
    assert np.isclose( P, t ).all(), P

def test( ):
    a = np.matrix( '1 2 3; 1 1 3; 9 2 4' )
    test_perm_to_mat( a )
    test_fast_perm_mult( a )

if __name__ == '__main__':
    test_a( )
    #  test()

