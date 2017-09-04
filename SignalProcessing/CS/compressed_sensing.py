import sys
import os
import numpy as np
from pyCSalgos.BP.l1eq_pd import l1eq_pd
import matplotlib as mpl
import matplotlib.pyplot as plt
try:
    mpl.style.use( 'seaborn-talk' )
except Exception as e:
    pass
mpl.rcParams['axes.linewidth'] = 0.1
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

import pypgfplots


N = 500
s = 0.05


# Theoretically K > 2sN, in practice K >= 4sN (gurenteed); >= 3sN also works
# sometime.
K = int( 5 * s * N )

title_ = 'N=%d, samples=%d ' % (N, K )

def sparse_signal( n, sparsity ):
    x = np.zeros( n )
    xi = np.random.randint(0, n+1, int( sparsity * n) )
    x[ xi ] = 1
    np.savetxt( "_signal.dat", x )
    return x

def obtain_random_measurements( x, k, err = 0):
    global title_
    # Make boolean matrix for measurement. It represents the Mask used in
    # imaging.
    # A = np.random.randn( k, N )
    A = np.random.randint(0, 2, (k, N) )
    np.savetxt( "_measurement_matrix.dat", A )
    x1 = x + err
    y = np.dot( A, x1 )
    np.savetxt( "_measurements.dat", y )
    pypgfplots.standalone( (np.arange(0,len(y),1), y)
            , outfile = 'figure_measurements.tex' 
            , title = 'Measured signal'
            , every = 10
            , label = r'\bf a.'
            , axis_attribs = 'smooth,no marks'
            , width = '8cm', height = '4cm'
            )
    return A, y

def main( ):
    global title_
    gridSize = (2, 2)

    ax1 = plt.subplot2grid( gridSize, (0,0), colspan = 1 )
    ax2 = plt.subplot2grid( gridSize, (0,1), colspan = 1 )
    ax3 = plt.subplot2grid( gridSize, (1,0), colspan = 1 )
    ax4 = plt.subplot2grid( gridSize, (1,1), colspan = 1 )

    # Make a sparse singal.
    x = sparse_signal( N, s )
    ax1.plot( x )
    ax1.set_title( 'x' )

    mean, var = 1e-2, 1e-3
    title_ += 'Error=normal(%.3f,%.3f)' % (mean,var )
    err = np.abs( np.random.normal( mean, var ) )
    A, y = obtain_random_measurements( x, K, err = err )
    fig = ax2.imshow( A, aspect = 'auto', interpolation = 'none' )
    ax2.set_title( 'A (measurement matrix)' )
    plt.colorbar( fig, ax = ax2 )

    ax3.plot( y )
    ax3.set_title( 'measurements' )
    ax3.legend(loc='best', framealpha=0.4)

    # compressed recovery.
    x0 = np.dot( A.T,  y )
    pypgfplots.standalone( matrix = A
            , every = 10
            , title = 'Measurement matrix'
            , xlabel = 'index', ylabel = 'index'
            , outfile = 'figure_measurements.tex' 
            )

    res = l1eq_pd( x0, A, [ ], y )
    np.savetxt( '_result.dat', res )
    print( 'Error:', np.linalg.norm( res - x0 ) )
    ax4.plot( x, label = 'original' )
    ax4.plot( res, label = 'recovered' )
    ax3.legend( )
    ax4.set_title( 'reconstructed' )
    ax4.legend(loc='best', framealpha=0.4)

    plt.suptitle( title_ )
    plt.tight_layout( pad = 1, rect = (0,0,1,0.9) )
    plt.savefig( 'compressed_sensing.png' )

if __name__ == '__main__':
    main()
