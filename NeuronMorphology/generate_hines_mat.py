"""generate_hines_mat.py: 

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
import random

def generate_hines_mat( N ):
    mat = np.zeros( N*N )
    randI = [0, 1]
    for i in range(1, N-1):
        randI += [ i*N+(i-1), i*N+i, i*N+(i+1) ]
    randI += [ N**2-2, N**2-1 ]
    for x in randI:
        mat[x] = random.uniform(1, 10)

    mat = mat.reshape( N, N)
    for i in range( N//4 ):
        i = random.randint(i, N-1)
        if i+1 >= N-1:
            continue
        j = random.randint(i+1, N-1)
        mat[i, j] = random.uniform(1, 10)
        mat[j, i] = random.uniform(1, 10)

    plt.figure( figsize=(8,3) )
    plt.subplot( 121 )
    plt.imshow( mat, interpolation = 'none', aspect='auto' )
    plt.title( 'H' )
    plt.colorbar()
    plt.subplot( 122 )
    plt.imshow( mat ** -1, interpolation = 'none', aspect='auto' )
    plt.colorbar()
    plt.title( 'invH' )
    plt.savefig( 'test.png' )


def main():
    N = int(sys.argv[1])
    generate_hines_mat( N )

if __name__ == '__main__':
    main()
