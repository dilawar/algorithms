import scipy
import scipy.linalg
import numpy as np
import random
import sympy

def sparse_matrix( m, n, k = 0.05 ):
    a = np.random.choice( [0,1], size=(m,n), p = [1-k, k] )
    return sympy.Matrix( a )

def main( ):
    a = sparse_matrix( 10, 50 )
    print( a )
    sympy.pprint( a.rref( )[0] )

if __name__ == '__main__':
    main()
