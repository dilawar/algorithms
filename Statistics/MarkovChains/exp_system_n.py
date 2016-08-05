"""exp_system_n.py: 

In this experiment, we generate transition matrix for a system of N bistable
switches.

NOTE: Only atomic transitions are allowed.

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
import subprocess
import itertools
import markov

up_ = 'U'
down_ = 'D'
same_ = '.'

def transition( nodeA, nodeB ):
    transitions = []
    for x, y in zip( nodeA, nodeB):
        if y - x == 0:
            transitions.append( same_ )
        elif y - x == 1:
            transitions.append( up_ )
        elif y - x == -1:
            transitions.append( down_ )
    return transitions

def label( node ):
    label = [ str(x) for x in node ] 
    return ''.join( label )

def up_and_down_transitions( nodeA, nodeB ):
    # number of non-zero up and down transitions. Only one step transitions are
    # legal.
    trans = transition( nodeA, nodeB )
    return ( trans.count( up_ ), trans.count( down_ ) )

def create_transition_graph( size, num_states = 2 ):
    print( '[INFO] Creating transition network of size %d' % size )
    print( '\t States of each element = %d' % num_states )
    allStates = itertools.product( range(num_states), repeat = size )
    network = nx.DiGraph( )
    network.graph['graph'] = { 
            'overlap' : 'false'
            , 'rankdir' : 'LR' 
            , 'splines' : 'true'
            }

    for ss in allStates:
        network.add_node( ss, label = label(ss)  )

    assert network.number_of_nodes( ) == num_states ** size
    print( '[INFO] Total states %d' % network.number_of_nodes( ) )

    # Only connect nodes which are one distance away.
    for n in network.nodes():
        for nn in network.nodes():
            up, down = up_and_down_transitions( n, nn )
            # Probability of transition.
            if up + down != 1:
                pass
            elif up == 1:
                network.add_edge( n, nn, transition = str( up_ ) )
            elif down == 1:
                network.add_edge( n, nn, transition = str( down_ ) )

    components = 0
    for c in nx.strongly_connected_components( network ):
        components += 1
    if components != 1:
        print( "[WARN] We must have a strongly connected network" )
        print( "\tFound %d" % components )

    return network

def add_interaction( network, pup, pdown, interaction ):
    delpUp, delpDown = interaction
    for s, t in network.edges( ):
        trans = transition( s, t )
        p = 1.0
        # pxpr = []
        for x, tr in zip(s, trans):
            if tr == up_:
                p *= ( pup + delpUp )  
                # pxpr.append( p )
            elif tr == down_:
                p *= (pdown + delpDown)
                # pxpr.append( p )
            else:
                if x == 0:
                    p *= ( 1.0 - pup )
                else:
                    p *= ( 1.0 - pdown )
                # pxpr.append( p )
        # print pxpr
        assert p <= 1.0
        network[s][t]['weight'] = p
    matT = nx.to_numpy_matrix( network )
    # Make sure that diagonal entries are 1.0 - sum of rest.
    for i, row in enumerate(matT):
        row[0,i] = 1.0 - np.sum( row )
    return matT


def main( args ):
    size = args.system_size
    network = create_transition_graph( size )
    # Add interaction and return the matrix
    T = add_interaction( network , args.pUp, args.pDown, (args.interaction, 0.0) )
    transitionMatFile = 'transition_matrix_%d.csv' % size 

    matImgFile = 'transition_mat_%d.png' % size
    plt.figure()
    plt.imshow( T, interpolation = 'none' )
    plt.colorbar( )
    plt.savefig( matImgFile )
    plt.close( )

    np.savetxt( transitionMatFile, T )
    dotFile = 'network_%d.dot' % size 
    nx.write_dot( network, dotFile )
    print( '[INFO] Graph is written to dot file %s' % dotFile )
    subprocess.call( [ "neato", "-Tpng", dotFile,  "-O"  ] )

    # Once I have the transition matrix, I now use markov module to solve it.
    s = markov.MarkovChain( T )
    print s.find_steady_state( )


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
    parser.add_argument('--pUp', '-u'
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
        , default = 0.0
        , type = float
        , help = 'Interaction of \delta pOn'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
