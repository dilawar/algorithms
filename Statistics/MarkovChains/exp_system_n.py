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

size_ = 2
pUp_ = 0.01
pDown_ = 0.01

try:
    plt.style.use( 'poster' )
except Exception as e:
    pass

def main( ):
    effect = []
    xvec = []
    for c in range(100):
        delUp = 0.005 * c
        xvec.append( delUp )
        ef = markov_chains.main(
                size = size_, pUp = pUp_, pDown = pDown_, excitation = delUp
                )
        effect.append( ef )

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
