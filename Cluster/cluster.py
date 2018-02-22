"""cluster.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
from collections import Counter
import itertools
import networkx as nx
import numpy as np

def build_flow_graph( vec, n ):
    g = nx.DiGraph( )
    g.add_node( 'source' )
    g.add_node( 'sink' )

    leaf = [ ]
    for i in range( 0, int(len(vec)/n)):
        g.add_node( 'chunk.%d' % i )
        g.add_edge( 'source', 'chunk.%d'%i, weight = 0, capacity = 1 )
        xs = vec[i*n:(i+1)*n]

        added = [ ]
        for ii, x in enumerate(xs):
            if x in added:
                continue
            else:
                added.append( x )

            name = '%d.%s' % (i*n+ii,x)
            g.add_node( name )
            g.add_edge( 'chunk.%d' % i, name, capacity=n, weight = 0 )
            leaf.append( name )

    # each leaf connect to same x 
    for l in leaf:
        index, val = l.split( '.' )
        index = int( index )
        for j, y in enumerate( vec ):
            if j == index:
                continue
            if val != y:
                continue
            ln = 'L.%d.%s' % (j,y)
            g.add_edge( l, ln, capacity = 1, weight = abs(index-j) )
            g.add_edge( ln, 'sink', capacity = 1, weight = 0 )

    return g

def compute_solution( g ):
    flowG = nx.DiGraph( )
    flowDict = nx.max_flow_min_cost( g, 'source', 'sink' )
    for n in flowDict:
        for m in flowDict[n]:
            flow = flowDict[n][m]
            if flow == 1:
                print(n, m, flow )
                flowG.add_edge( n, m )

    write_graph( flowG, 'flow.dot' )

def write_graph( g, outfile ):
    from networkx.drawing.nx_agraph import write_dot
    write_dot( g, outfile )
    print( 'Wrote graph to %s' % outfile )

def swap( vec, x, y):
    t = vec[y]
    vec[y] = vec[x]
    vec[x] = t
    return vec

def cost( veca, vecb ):
    return sum( abs(a[1]-b[1]) for a, b in zip( veca, vecb) )

def dynamic_programming( vec, n ):
    orig = vec[:]
    alphas = [ x[0] for x in vec ]
    freqs = Counter( alphas )
    groups = { k : max(1,int(v/n)) for k, v in freqs.items() }

    vecb = swap( vec, 2, 5 )
    a = cost( orig, vecb )


def cluster_data( vec, n, save = True ):
    # Cluster the vector for size of chunk n.
    # First we build the flow graph.
    #g = build_flow_graph( vec, n )
    #sol = compute_solution( g )
    #if save:
    #    write_graph( g, 'network.dot' )
    dynamic_programming( vec, n )

def test( ):
    np.random.seed( 0 )
    data = np.random.choice( list( 'ABCDE' ), 30, p = [0.2,0.2,0.2,0.1,0.3] )
    data = list( zip( data, range(0,len(data) )))
    cluster_data( data, 3 )

if __name__ == '__main__':
    test( )

