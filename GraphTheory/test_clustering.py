"""test_max_clique.py: 

This file test if finding cliques can be used to partition a graph

"""

from __future__ import print_function
    
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

random.seed( 10 )
np.random.seed( 10 )

colors_ = []

def filter_graph( g, min_weight = 1.0 ):
    toRemove = [ ]
    for s, t in g.edges( ):
        if g[s][t][ 'weight' ] < min_weight:
            print( 'D', end = '' )
            toRemove.append( (s, t) )

    g.remove_edges_from( toRemove )
    print( 'Total edges after filtering %s' % g.number_of_edges( ) )
    return g

def cluster_graph( g, colors, current_color = 0 ):
    # Initialize colors
    degrees = []
    for n in g.nodes( ):
        degrees.append( (nx.degree(g, n ), n))

    nodeWithMaxDegree = sorted( degrees, reverse = True )[0][1]

    # Start with node with maximum degree
    current_color  += 1
    colors[ nodeWithMaxDegree ] = current_color

    numIteration = 0
    pN = nodeWithMaxDegree
    stack = [ nodeWithMaxDegree ]
    while stack:
        neighbours = nx.neighbors( g, stack.pop( ) )
        numIteration += 1
        for n in neighbours:
            if colors[n] > 0:
                continue
            # If most neightbours of n are as close to pN as the value current
            # iteration, then accept this node.
            potentialCandidates = filter(lambda x: colors[x] == 0, nx.neighbors( g, n ))
            # print( "Potential neighbours ", potentialCandidates )
            distance2pN = [ nx.shortest_path_length( g, x, pN) for x in potentialCandidates ]
            goodDist2pN = filter( lambda x: x <= numIteration, distance2pN )
            accepted = False
            if len( goodDist2pN ) > 0:
                accepted = True
                colors[ n ] = current_color 
                stack.append( n )
            # print n, ' -> ', distance2pN, ',', goodDist2pN, 'Accepted', accepted
        # print stack
    return g

def main( g = None ):
    if g is None:
        print( 'Generating complete graph' )
        g = nx.complete_graph( 20 )
        for s, t in g.edges( ):
            g[s][t]['weight'] = (0.15 + random.random( )) ** 2

    plt.subplot( 211 )
    g = filter_graph( g, 0.5 )

    width = []
    for s, t in g.edges( ):
        width.append( g[s][t]['weight'] ** 2.0 )
    nx.draw_networkx( g, width = width )

    plt.subplot( 212 )
    # Now do the thingy
    for n in g.nodes( ):
        colors_.append( 0 )
    g = cluster_graph( g, colors_, 0 )
    nx.draw_networkx( g, node_color = colors_ )
    # print( cluster )
    plt.savefig( 'test_graph.png' )

if __name__ == '__main__':
    g = None
    if len( sys.argv ) > 1:
        graphfile = sys.argv[1]
        print( '[INFO] Got graph file %s' % graphfile )
        g = nx.read_gpickle( graphfile )
        assert g.number_of_edges( ) > 10
    main( g )
