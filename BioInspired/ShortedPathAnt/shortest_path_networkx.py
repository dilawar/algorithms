"""shortest_path_networkx.py: 

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
import networkx as nx
import cv2

N = 300
arena_ = nx.grid_graph( dim=(N,N) )

#for n1 in arena_.nodes( ):
#    arena_.node[n1][ 'weight' ] = 0.0

def show_graph( ):
    global arena_
    img = nx.to_numpy_matrix( arena_ )
    print( img )


def main( ):
    show_graph( )
    pass

if __name__ == '__main__':
    main()
