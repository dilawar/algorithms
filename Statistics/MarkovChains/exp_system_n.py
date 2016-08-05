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

size_ = 5
pUp_ = 0.01
pDown_ = 0.01

try:
    plt.style.use( 'ggplot' )
except Exception as e:
    pass

def get_indices( i ):
    """For a given size of network, what indices have the effect i.
    For example 00, 01, 10, 11 has effect of 0, 1, 1, 2.
    """
    global size_
    states = itertools.product( [0, 1], repeat = size_)
    indices = []
    for x, st in enumerate(states):
        if i == sum( st ):
            indices.append( x )
    return np.array( indices )

def get_effects( state ):
    activity = np.zeros( size_ + 1)
    for i, act in enumerate( activity ):
        idx = get_indices( i )
        activity[i] = np.sum( state[idx] )
    return activity

def main( ):
    effect = []
    xvec = []
    for c in range(100):
        delUp = 0.005 * c
        xvec.append( delUp )
        sol = markov_chains.main(
                size = size_, pUp = pUp_, pDown = pDown_, excitation = delUp
                )
        effect.append(  get_effects(sol) )

    effect = np.vstack( effect )
    for i, row in enumerate( effect.T ):
        plt.plot( xvec,  row, label = 'Effect=%d' % i )
    plt.legend( framealpha = 0.4 )
    title_ = 'System %d : pUp=%s, pDown=%s' % ( size_, pUp_, pDown_ )
    plt.title( title_ )
    plt.xlabel( 'delta pUp (interaction)' )
    plt.legend( )
    outfile = title_.replace( ' ', '_' ) + '.png'
    plt.savefig( outfile )
    print( '[INFO] Saved it to %s' % outfile )

if __name__ == '__main__':
    main()
