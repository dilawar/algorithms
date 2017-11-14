"""plot_roh.py: 

Plot ROH.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import pandas as pd
import numpy as np
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use( 'bmh' )
mpl.rcParams['axes.linewidth'] = 0.2
mpl.rcParams['lines.linewidth'] = 1.0

cols = [ 'Chromosome', 'Position', 'State', 'Quality' ]

def plotROH( files, ax ):
    """Each file is plotted
    """
    img = [ ]
    chromosomes = { }
    maxlength = 0
    for  i, f in enumerate( files ):
        print( '[INFO] Processing %s' % f )
        data = pd.read_csv( f, comment = '#', sep = '\t', names = cols  )
        allchoromosomes = set( data[ 'Chromosome' ] )
        for chromo in allchoromosomes:
            cdata = data[ data[ 'Chromosome' ] == chromo ]
            chromosomes[ chromo ] = cdata 
            if max( cdata[ 'Position' ] ) > maxlength:
                maxlength = max( cdata[ 'Position' ] )

    print( 'INFO: Max row size %d' % maxlength )
    img = np.zeros( shape = (len(chromosomes), maxlength ) )
    for i, chromo in enumerate( chromosomes ):
        cdata = chromosomes[ chromo ]
        ax.imshow( img )

def main( ):
    datadir = sys.argv[1]
    files = glob.glob( "%s/*" % datadir )
    ax = plt.subplot( 111 )
    plotROH( files, ax )
    plt.show( )

if __name__ == '__main__':
    main()

