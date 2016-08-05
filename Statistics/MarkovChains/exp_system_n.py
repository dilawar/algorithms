"""exp_system_n.py: 

In this experiment, we generate transition matrix for a system of N bistable
switches.

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
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import itertools

def transition( nodeA, nodeB ):
    transitions = []
    for x, y in zip( nodeA, nodeB):
        transitions.append( y - x )
    return transitions

def up_and_down_transitions( nodeA, nodeB ):
    # number of non-zero up and down transitions. Only one step transitions are
    # legal.
    trans = transition( nodeA, nodeB )
    return ( trans.count(1), trans.count(-1) )

def create_transition_graph( size, num_states = 2 ):
    print( '[INFO] Creating transition graph of size %d' % size )
    print( '\t States of each element = %d' % num_states )
    allStates = itertools.product( range(num_states), repeat = size )
    graph = nx.MultiDiGraph( )
    for ss in allStates:
        graph.add_node( ss )

    assert graph.number_of_nodes( ) == num_states ** size
    print( '[INFO] Total states %d' % graph.number_of_nodes( ) )

    # Only connect nodes which are one distance away.
    for n in graph.nodes():
        for nn in graph.nodes():
            up, down = up_and_down_transitions( n, nn )
            if up + down != 1:
                pass
            elif up == 1:
                graph.add_edge( n, nn, transtion = 'up' )
            elif down == 1:
                graph.add_edge( n, nn, transtion = 'down' )

    components = 0
    for c in nx.strongly_connected_components( graph ):
        components += 1
    if components != 1:
        print( "[WARN] We must have a strongly connected graph" )
        print( "\tFound %d" % components )

    nx.write_dot( graph, sys.stdout )
    return graph

def main( args ):
    graph = create_transition_graph( args.system_size )
    nx.draw_graphviz( graph, 'neato' )
    plt.savefig( 'graph.png' )


if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Experiment 2'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--system-size', '-s'
        , required = True
        , type = int
        , help = 'Size of system'
        )
    parser.add_argument('--pOn', '-u'
        , required = False
        , default = 0.1
        , type = float
        , help = 'Down to Up transition probabilities'
        )
    parser.add_argument('--pDown', '-d'
        , required = False
        , default = 0.1
        , type = float
        , help = 'Up to Down transition probabilities'
        )
    parser.add_argument('--interaction', '-i'
        , required = False
        , default = 0.01
        , type = float
        , help = 'Interaction of \delta pOn'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
