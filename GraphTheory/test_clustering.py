"""test_max_clique.py: 

This file test if finding cliques can be used to partition a graph

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
import matplotlib
matplotlib.use( 'TkAgg' )
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random

def filter_graph( g, min_weight = 1.0 ):
    toRemove = [ ]
    for s, t in g.edges( ):
        if g[s][t][ 'weight' ] < min_weight:
            toRemove.append( (s, t) )

    g.remove_edges_from( toRemove )
    print( 'Total edges after filtering %s' % g.number_of_edges( ) )
    return g

def cluster_graph( g ):
    # Start with the node with maximum degree
    return g

def main( ):
    g = nx.complete_graph( 50 )
    for s, t in g.edges( ):
        g[s][t]['weight'] = (0.1 + random.random( )) ** 2

    plt.subplot( 121 )
    g = filter_graph( g )

    width = []
    for s, t in g.edges( ):
        width.append( g[s][t]['weight'] ** 2.0 )

    nx.draw_networkx( g, width = width )

    plt.subplot( 122 )
    # Now do the thingy
    # nx.draw( g )
    cluster_graph( g )
    # print( cluster )
    plt.savefig( 'test_graph.png' )

if __name__ == '__main__':
    main()
