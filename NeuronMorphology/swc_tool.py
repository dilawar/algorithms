#!/usr/bin/env python
"""swc_tool.py: 

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
from collections import defaultdict
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use( 'ggplot' )
from mpl_toolkits.mplot3d import Axes3D

args_ = None
soma_ = 0

def parse_swc( swctxt ):
    global args_
    S = defaultdict( list )
    for i, l in enumerate(swctxt.split('\n')):
        if not l.strip():
            continue
        if l[0] == '#':
            continue
        fs = [ float(x) for x in l.split()]
        if not len(fs) == 7:
            print( "[WARN ] Bad line: Ignored %d: %s" % (i,l) )
            continue
        S[ int(fs[1]) ].append( fs )
    return S

def add_node( s, g ):
    x, y, z = s[2:5]
    g.add_node( int(s[0]), x=x, y=y, z=z, type=int(s[1]) )
    if int(s[-1]) > 0:
        g.add_edge( int(s[-1]), int(s[0]), radius = s[5] )

def to_graphviz( S ):
    global soma_
    g = nx.DiGraph( )
    # First add soma.
    somas = S[1]
    for s in somas:
        print( 'Soma ', s )
        if soma_ == 0:
            soma_ = int(s[0])
            add_node( s, g )

    for k in S.keys():
        if k == 1:
            # already added.
            continue
        [ add_node(n, g) for n in S[k] ]
    return g

def plot_neuron( g, scale = 2, ax = None ):
    global args_
    if ax is None:
        ax = fig.add_subplot(111, projection='3d')

    ax.grid( False )
    for k in g:
        X, Y, Z = [], [], []
        alpha, m =  0.5, "."
        if k == 1:
            m = 'H'
            alpha = 1.0
        pts = [ x[2:5] for x in g[k] ]
        X, Y, Z = zip(*pts)
        ax.scatter( X, Y, Z, marker=m, alpha = alpha )

def show_incidence_matrix( g, ax ):
    global args_
    im = nx.incidence_matrix( g )
    img = im.todense()
    ax.grid( False )
    ax.imshow( img, aspect = 'auto', interpolation = 'none' )
    np.savetxt( '%s_incidence_matrix.csv' % args_.swc, img, fmt='%d' )
    print( 'Saved matrix to csv file' )

def main( args ):
    global args_
    args_ = args
    print( "[INFO ] Morphology file %s" % args.swc )
    with open( args_.swc, 'r' ) as f:
        txt = f.read()
    S = parse_swc( txt )
    g = to_graphviz( S )
    plt.figure( figsize=(10, 5) )
    ax1 = plt.subplot( 121, projection='3d')
    ax2 = plt.subplot( 122 )
    if args_.plot:
        plot_neuron( S, scale = 2, ax = ax1 )
    if args_.incidence_matrix:
        show_incidence_matrix( g, ax2 )

    plt.tight_layout( )
    outfile = '%s.output.png' % args_.swc
    plt.savefig( outfile )
    print( "[INFO ] Saved to %s" % outfile )
    plt.close()
    

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''SWC (NeuroMorpho) tools.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--swc', '-i'
        , required = True
        , help = 'Input file'
        )
    parser.add_argument('--plot', '-p'
        , required = False, action = 'store_true'
        , help = 'Plot morphology using matplotlib (only rough morphology is '
                ' plotted for quick overview.)'
        )
    parser.add_argument('--incidence-matrix', '-im'
        , required = False, action = 'store_true'
        , help = 'Show incidence matrix.'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )

