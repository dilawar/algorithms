"""
System of bistable switches with interaction.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import markov_chains
import math
from collections import defaultdict
import itertools

size_ = 4
pUp_ = 0.01
pDown_ = 0.01

try:
    # plt.style.use( 'ggplot' )
    pass
except Exception as e:
    pass

def accumulate_all_effect( effect ):
    res = 0.0
    # Multiply the effect by the probability of occuring of the effect.
    for i, x in enumerate( effect ):
        res += i * x
    return res

def states_vs_interaction( pUp_, pDown_, plot = True ):
    effect = []
    xvec = []
    for c in range(100):
        delUp = 0.001 * c
        xvec.append( delUp )
        ef = markov_chains.main(
                size = size_, pUp = pUp_, pDown = pDown_, excitation = delUp
                )
        effect.append( ef )
    effect = np.vstack( effect )

    if plot:
        for i, row in enumerate( effect.T ):
            plt.plot( xvec,  row, label = 'Effect=%d' % i )
        plt.legend( framealpha = 0.4 )
        title_ = 'System %d : pUp=%s, pDown=%s' % ( size_, pUp_, pDown_ )
        plt.title( title_ )
        plt.xlabel( 'delta pUp (interaction)' )
        plt.legend( framealpha = 0.4 )
        outfile = title_.replace( ' ', '_' ) + '.png'
        plt.savefig( outfile )
        print( '[INFO] Saved it to %s' % outfile )

    return effect

def phase_space( size ):
    global size_ 
    size_ = size
    pUpSpace = np.linspace(0.0001, 0.01, 50 )
    pDownSpace = np.linspace(0.0001, 0.01, 50 )
    for c in range( 20 ):
        c *= 0.001
        plt.figure()
        outfile = 'phase_space_%0.5f.png' % c
        img = np.zeros( shape=(len(pUpSpace), len(pDownSpace) ) )
        for i, pUp in enumerate( pUpSpace ):
            for j, pDown in enumerate( pDownSpace ):
                ef = markov_chains.main( 
                        size = 4, pUp = pUp, pDown = pDown, excitation = c 
                        )
                img[i, j] = accumulate_all_effect( ef )

        cs =plt.contour(pUpSpace, pDownSpace, img , size, colors = 'black',
                linewidth = .5 )
        plt.clabel( cs, inline = 1, fontsize = 10 )
        plt.pcolormesh( pUpSpace, pDownSpace, img, cmap = 'seismic' 
                , vmin = 0, vmax = size
                )
        plt.xlabel( '$p(\downarrow)$' )
        plt.ylabel( '$p(\uparrow)$' )
        plt.title( '$\Delta p(\uparrow) = %0.5f$' % c )
        plt.colorbar( )
        plt.savefig( outfile )
        print( '[INFO] Wrote phase space to %s' % outfile )


def main( size ):
    print( '[INFO] System with size %d' % size )
    phase_space( size )

if __name__ == '__main__':
    system_size = int(sys.argv[1])
    main( system_size )
