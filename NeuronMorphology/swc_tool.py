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
import networkx as nx

args_ = None

def parse_swc( swctxt ):
    global args_
    g = nx.DiGraph()
    for i, l in enumerate(swctxt.split('\n')):
        if not l.strip():
            continue
        if l[0] == '#':
            continue
        fs = l.split()
        if not len(fs) == 7:
            print( "[WARN ] Bad line: Ignored %d: %s" % (i,l) )
            continue

        # id, type, x, y, z, radius, parent
        g.add_node( fs[0], type=fs[1], x=fs[2], y=fs[3], z=fs[4], radius=fs[5] )
        g.add_edge( fs[6], fs[0] )
    return g

def plot_graph( g ):
    global args_
    import matplotlib.pyplot as plt
    nx.draw_networkx( g )
    plt.savefig( '%s.graph.png' % args_.swc )

def main( args ):
    global args_
    args_ = args
    print( "[INFO ] Morphology file %s" % args.swc )
    with open( args_.swc, 'r' ) as f:
        txt = f.read()
    g = parse_swc( txt )
    plot_graph( g )
    

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''SWC (NeuroMorpho) tools.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--swc', '-i'
        , required = True
        , help = 'Input file'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )

