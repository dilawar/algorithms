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
import PyGnuplot as gp
import shutil

dataDir = '_temp_data'
if os.path.exists( dataDir ):
    shutil.rmtree( dataDir )

os.makedirs( dataDir )

mpl.style.use( 'bmh' )
mpl.rcParams['axes.linewidth'] = 0.2
mpl.rcParams['lines.linewidth'] = 1.0

cols = [ 'Chromosome', 'Position', 'State', 'Quality' ]

def find_connected_segments( data ):
    # find indices where data is 1 
    where1 = data[ data[ 'State' ] == 1 ]['Position'] 
    wherediff = np.diff( where1.values )



def plotROH( files, ax = None ):
    """Each file is plotted
    """
    img = [ ]
    chromosomes = { }
    for  i, f in enumerate( files ):
        print( '[INFO] Processing %s' % f )
        data = pd.read_csv( f, comment = '#', sep = '\t', names = cols  )
        allchoromosomes = set( data[ 'Chromosome' ] )
        for chromo in allchoromosomes:
            cdata = data[ data[ 'Chromosome' ] == chromo ]
            chromosomes[ chromo ] = cdata 

    # img = np.zeros( shape = (len(chromosomes), maxlength ) )
    for i, chromo in enumerate( chromosomes ):
        cdata = chromosomes[ chromo ]
        whereOne = cdata[ cdata[ 'State' ] == 1 ]
        x, y = whereOne[ 'Position' ], whereOne[ 'State' ]
        outfile = os.path.join( dataDir, '%s.dat' % chromo )
        df = pd.DataFrame( )
        df[ 'x' ] = x
        df[ 'y' ] = y + 2*i
        df.to_csv( outfile, sep = ' ', header=False, index = False )
        if i > 5:
            break

    for i, f in enumerate( glob.glob( '%s/*.dat' % dataDir ) ):
        print( 'Plotting %s' % f )
        cmd = 'plot "%s" u 1:2 w p pointtype 5 notitle ' % f
        if i > 0:
            cmd = 're' + cmd  
        gp.c( cmd )

    gp.pdf('results.pdf' )
    print( 'Saved' )


def main( ):
    datadir = sys.argv[1]
    files = glob.glob( "%s/*" % datadir )
    #ax = plt.subplot( 111 )
    plotROH( files )
    #plt.show( )

if __name__ == '__main__':
    main()

