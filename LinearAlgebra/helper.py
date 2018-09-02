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

def apply_elementary_col_operation( mat, p ):
    T = mat.copy()
    q, p, s = p
    for i in range(T.shape[0]):
        T[i,q] += T[i,p]*s
    return T

def apply_elementary_col_operations( mat, ps ):
    T = mat.copy()
    for p in ps:
        T = apply_elementary_col_operation(T, p)
    return T

def test_apply_elementary_col_operation( ):
    # Test multiplication by elementary column op.
    for i in range(10):
        t = np.random.rand(4, 4)
        p1 = (2, 1, -1.5 )
        p2 = (1, 3, 0.5)
        t1 = apply_elementary_col_operation( t, p1 )
        t2 = apply_elementary_col_operation( t1, p2)
        pm1 = perm_to_mat( p1, t.shape[0] )
        pm2 = perm_to_mat( p2, t.shape[0] )
        expected1 = np.dot( t, pm1 )
        expected2 = np.dot(t1, pm2 )
        assert np.isclose( t1, expected1 ).all()
        assert np.isclose( t2, expected2 ).all()
    fname = sys._getframe(  ).f_code.co_name
    print( '[INFO] %s ' % fname + '%30s' % 'PASSED' )


def gen_permutations_mat( PS, N ):
    # generate permuation matrix combining all permuatations given in the list
    # of PS.
    print( "[INFO ] Generating permuation matrix out of %s" % PS ) 
    T = np.eye( N )
    for p in PS:
        T = apply_elementary_col_operation(T, p)
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
    p1 = (1,2,-1)
    p2 = (2,1,-2)
    p3 = (2,1,-0.5)
    ps = [p1, p2, p3]
    mats = [ perm_to_mat(p, A.shape[0]) for p in ps ]
    r1 = apply_elementary_col_operations(A, ps)
    r2 = A.copy()
    for m in mats:
        r2 = np.dot(r2, m)
    assert np.isclose( r1, r2 ).all()

def test_other( ):
    a = np.matrix( '1.0 2.0 3.0; 1 1 3; 9 2 4' )
    test_perm_to_mat( a )
    test_fast_perm_mult( a )

if __name__ == '__main__':
    test_apply_elementary_col_operation( )
    test_other()

