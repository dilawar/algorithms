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
    # Positive d means postponing AWS or moving to right.
    return d+d if d > 0 else d**2 + abs(d)

def cost_of_moving_elem( v, newpos ):
    return cost_of_moving( newpos - v[1] )

def print_result( res, indent = 2 ):
    prefix = ''.join([ ' ' for i in range( indent ) ] )
    s = ''.join( [ x[0] for x in res ] )
    ks = ''.join( [ '%s' % x[2]['k'] for x in res ] )
    print( prefix + s + "\n" + prefix + ks )

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

def find_move_min_cost( cid, pos, N, vec ):
    # First char in right.
    moves = [ ]
    print( 'Cluster %s, pos %d, size %d' % (cid,pos,N) )
    for i, v in enumerate(vec[pos+N+1:]):
        if v[0] == cid:
            moves.append( (pos+N+i+2, (pos+N)) )
            break
    for i, v in enumerate( reversed(vec[:pos-1]) ):
        if v[0] == cid:
            moves.append( (pos-i-1, pos)  )
            break

    res = [ (cost_of_moving_elem( vec[x[1]], x[0] ), *x) for x in moves ]
    print( 'Cost', res )
    return sorted(res)[0]

def make_move( move, vec ):
    cost, frm, to = move
    print( '[DBEUG] Moving %d -> %d' % (frm,to) )
    if frm < to:
        vec.insert( to, vec[frm] )
        del vec[frm]
    else:
        vec.insert( to, vec[frm])
        del vec[frm+1]

def find_cluster_with_max_len( vec ):
    maxLen = max( [ x[2]['k'] for x in vec ] )
    clusters, cluster, cid = [ ], [0,0], ''
    clusterStart = False

    for i, v in enumerate( vec ):
        if not clusterStart and v[2]['k'] == maxLen:
            clusterStart = True
            cluster[0] = i
        elif clusterStart and v[2]['k'] != maxLen:
            cluster[1] = i
            clusters.append( (v[0], cluster) )
            cluster = [0,0]
            clusterStart = False

    for x,c in clusters:
        assert vec[c[0]][0] == vec[c[1]][0], [vec[i] for i in c]
    return maxLen, clusters

def remove_cluster( vec, clusters ):
    notId = [ ]
    print( '[INFO] Removing %s' % str( clusters ) )
    for cid, cluster in clusters:
        notId += list( range( cluster[0], cluster[1] ) )
    return [ x for i, x in enumerate(vec) if i not in notId ]

def cluster_recurse( vec, k, res, num_call ):
    if num_call == 5:
        return res

    # Find the strongest cluster.
    recompute( vec, k )
    maxLen, clusters = find_cluster_with_max_len( vec )
    if (maxLen + 1) % k == 0:
        # This is a good cluster. Remove it and keep it in res
        res.append( clusters )
        vec = remove_cluster( vec, clusters )
        recompute( vec, k )
        print_result( vec )
        return cluster_recurse( vec, k, res, num_call + 1 )

    # Move a char to this cluster.
    print( 'CLUSTERS:', clusters )
    print_result( vec, 3 )
    for clusterId, cluster in clusters:
        maxLen = cluster[1] - cluster[0]
        fI = find_move_min_cost( clusterId, cluster[0], maxLen, vec )
        if fI:
            make_move( fI, vec )
            recompute( vec, k )
            print_result( vec )

    return cluster_recurse( vec, k, res, num_call + 1 )

def recompute( values, k ):
    for i, (c, l, attrib) in enumerate(values):
        alreadySeen = [ ]
        samec = find_same_neighbour(i, c, values)
        attrib['k'] = len(samec) 

def dynamic_programming( vec, k ):
    res = [ ]
    for i, (c,l) in enumerate( vec ):
        res.append( (c, l, dict(k=0,cid=0)) )

    recompute( res, k )
    print_result( res )

    res = cluster_recurse( res, k, [ ], 0 )


def cluster_data( vec, k, save = True ):
    dynamic_programming( vec, k )

def test( ):
    np.random.seed( 0 )
    data = np.random.choice( list( 'ABCDE' ), 120, p = [0.2,0.2,0.2,0.1,0.3] )
    data = list( zip( data, range(0,len(data) )))
    cluster_data( data, 3 )

if __name__ == '__main__':
    test( )

