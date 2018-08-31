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

def data_for_cylinder_along_z(center_x,center_y,radius,height_z):
    z = np.linspace(0, height_z, 50)
    theta = np.linspace(0, 2*np.pi, 50)
    theta_grid, z_grid=np.meshgrid(theta, z)
    x_grid = radius*np.cos(theta_grid) + center_x
    y_grid = radius*np.sin(theta_grid) + center_y
    return x_grid,y_grid,z_grid

def plot_cylinder( p0, p1, R, ax ):
    # This is from https://stackoverflow.com/a/32383775/1805129
    v = p1 - p0
    mag = np.linalg.norm(v)
    v = v / mag
    not_v = np.array([1, 0, 0])
    if (v == not_v).all():
        not_v = np.array([0, 1, 0])
    n1 = np.cross(v, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v, n1)
    t = np.linspace(0, mag, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    t, theta = np.meshgrid(t, theta)
    X, Y, Z = [p0[i] + v[i] * t + R * np.sin(theta) * n1[i] + R * np.cos(theta) * n2[i] for i in [0, 1, 2]]
    ax.plot_surface(X, Y, Z)

def parse_swc( swctxt ):
    global args_
    g = nx.DiGraph()
    for i, l in enumerate(swctxt.split('\n')):
        if not l.strip():
            continue
        if l[0] == '#':
            continue
        fs = [ float(x) for x in l.split()]
        if not len(fs) == 7:
            print( "[WARN ] Bad line: Ignored %d: %s" % (i,l) )
            continue

        # id, type, x, y, z, radius, parent
        pos = fs[2:5]
        g.add_node( fs[0], pos=pos, type=fs[1], x=fs[2], y=fs[3], z=fs[4], radius=fs[5] 
                , size = 10 * fs[5]
                )
        if fs[6] > 0:
            g.add_edge( fs[6], fs[0] )
    return g

def find_soma( g ):
    somas = []
    for n in g.nodes():
        if int(g.node[n]['type']) == 1:
            somas.append( n )
    print( '[INFO] Found %d somas' % len(somas) )
    return somas

def plot_graph( g ):
    global args_
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    mpl.style.use( 'ggplot' )
    #  mpl.rcParams['axes.linewidth'] = 0.2
    #  mpl.rcParams['lines.linewidth'] = 1.0
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.grid( False )
    #  ax.axis( 'off' )
    pos = nx.get_node_attributes( g, 'pos' ).values()
    X, Y, Z = zip(*pos)
    size = list(nx.get_node_attributes( g, 'size' ).values())
    ax.scatter( X, Y, Z, s = size, alpha = 0.7 )

    # plot somas.
    somas = find_soma( g )
    if len(somas) > 0:
        a = g.node[somas[0]]
        ax.scatter( a['x'], a['y'], a['z'], s=100)

    outfile = '%s.graph.png' % args_.swc
    plt.suptitle( args_.swc )
    plt.savefig( outfile )
    plt.close()
    print( 'Morphology is saved to %s' % outfile )

def show_incidence_matrix( g ):
    global args_
    import matplotlib.pyplot as plt
    #  assert int(g.node[1]['type']) == 1, 'Got %s' % g.node[1]['type']
    im = nx.incidence_matrix( g )
    img = np.uint8(im.todense())
    plt.grid( False )
    plt.imshow( img, aspect = 'auto' )
    plt.savefig( '%s_incidence_matrix.png' % args_.swc )  
    np.savetxt( '%s_incidence_matrix.csv' % args_.swc, img, fmt='%d' )
    print( 'Saved matrix to image and csv file' )
    plt.close()

def main( args ):
    global args_
    args_ = args
    print( "[INFO ] Morphology file %s" % args.swc )
    with open( args_.swc, 'r' ) as f:
        txt = f.read()
    g = parse_swc( txt )
    if args_.plot:
        plot_graph( g )

    if args_.incidence_matrix:
        show_incidence_matrix( g )

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

