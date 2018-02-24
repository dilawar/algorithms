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
import re

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

def find_groups( string, alphas, n ):
    ptrns = r'%s' % '|'.join( [ '%s{%d}'%(x,n) for x in alphas] ) 
    pat = re.compile( r'%s' % ptrns )
    return pat.findall( string )

def cost_of_moving( d ):
    return d if d > 0 else d ** 2

def print_result( res ):
    s = ''.join( [ x[0] for x in res ] )
    ks = ''.join( [ '%s' % x[2]['k'] for x in res ] )
    print( s + "\n" + ks )

def find_same_neighbour( i, c, values ):
    res = [ ]
    for j, v in enumerate(values[i+1:]):
        if v[0] == c:
            res.append( i+j+1 )
        else:
            break
    for j, v in enumerate(reversed(values[:i])):
        if v[0] == c:
            res.append(i-j-1)
        else:
            break
    return res

def step( res ):
    return res

def recompute( values ):
    for i, (c, l, attrib) in enumerate(values):
        alreadySeen = [ ]
        samec = find_same_neighbour(i, c, values)
        attrib['k'] = len(samec)

def dynamic_programming( vec, k ):
    res = [ ]
    for i, (c,l) in enumerate( vec ):
        res.append( (c, l, dict(k=0)) )

    orig = res[:]
    recompute( res )
    print_result( res )

    step( res )
    print( cost( orig, res ) )
    # Now do the step.


def random_grouping( vec, n ):
    for i, (v,oi) in enumerate( vec ):
        xi = abs(i - oi)
        print( xi, v, oi )


def cluster_data( vec, k, save = True ):
    # Cluster the vector for size of chunk n.
    # First we build the flow graph.
    #g = build_flow_graph( vec, n )
    #sol = compute_solution( g )
    #if save:
    #    write_graph( g, 'network.dot' )
    dynamic_programming( vec, k )

def test( ):
    np.random.seed( 0 )
    data = np.random.choice( list( 'ABCDE' ), 100, p = [0.2,0.2,0.2,0.1,0.3] )
    data = list( zip( data, range(0,len(data) )))
    cluster_data( data, 3 )

if __name__ == '__main__':
    test( )

