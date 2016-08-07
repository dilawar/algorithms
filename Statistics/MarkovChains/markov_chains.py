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
import time
import markov

up_ = 'U'
down_ = 'D'
same_ = '.'

def get_indices( i, size_ ):
    """For a given size of network, what indices have the effect i.
    For example 00, 01, 10, 11 has effect of 0, 1, 1, 2.
    """
    states = itertools.product( [0, 1], repeat = size_)
    indices = []
    for x, st in enumerate(states):
        if i == sum( st ):
            indices.append( x )
    return np.array( indices )

def get_effects( state, size_ ):
    activity = np.zeros( size_ + 1)
    for i, act in enumerate( activity ):
        idx = get_indices( i, size_ )
        activity[i] = np.sum( state[idx] )
    return activity

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

def create_transition_graph( size ):
    # print( '[INFO] Creating transition network of size %d' % size )
    # print( '\t States of each element = %d' % num_states )
    allStates = itertools.product( [0, 1], repeat = size )
    network = nx.DiGraph( )
    network.graph['graph'] = { 
            'overlap' : 'false'
            , 'rankdir' : 'LR' 
            , 'splines' : 'true'
            }

    for i, ss in enumerate(allStates):
        network.add_node( ss, label = label(ss), order=i  )

    assert network.number_of_nodes( ) == 2 ** size
    # print( '[INFO] Total states %d' % network.number_of_nodes( ) )

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

def add_interaction( network, pup, pdown, exc, inh ):
    for s, t in network.edges( ):
        trans = transition( s, t )
        p = []
        # pxpr = []
        for x, tr in zip(s, trans):
            if tr == up_:
                p.append( pup + exc )  
                # pxpr.append( p )
            elif tr == down_:
                p.append(pdown + inh)
                # pxpr.append( p )
            else:
                if x == 0:
                    p.append( 1.0 - pup )
                else:
                    p.append( 1.0 - pdown )
                # pxpr.append( p )
        # Multiply them all
        p = reduce( lambda x, y : x*y, p )
        assert p <= 1.0, "P must be less than 1.0, got %s" % p
        network[s][t]['weight'] = p

    # Notice. Make sure nodelist is passed in correct sorted order.
    matT = nx.to_numpy_matrix( network, nodelist=sorted(network.nodes()) )
    # Make sure that diagonal entries are 1.0 - sum of rest.
    for i, row in enumerate(matT):
        row[0,i] = 1.0 - np.sum( row )
    return matT


def main( size,  **args ):
    network = create_transition_graph( size )
    # Add interaction and return the matrix
    assert args['pUp'] > 0.0
    assert args['pDown'] > 0.0
    T = add_interaction( network
            , args['pUp']
            , args['pDown']
            , args.get('excitation', 0.0) 
            , args.get('inhibition', 0.0) 
            )
    print( "Running with parameters : %s" % args )
    if args.get('plot', False):
        transitionMatFile = 'transition_matrix_%d.csv' % size 
        np.savetxt( transitionMatFile, T )
        matImgFile = 'transition_mat_%04d.png' % size
        plt.figure()
        # create a binary image out of T.
        tImg = np.copy(T)
        tImg[ np.where( tImg != 0 ) ] = 1.0
        plt.figure( )
        plt.imshow( tImg, interpolation = 'none' )
        plt.title( 'Transition matrix. Zero and non-zero entries' )
        # plt.colorbar( )
        plt.savefig( matImgFile )
        plt.close( )
        dotFile = 'network_%d.dot' % size 
        nx.write_dot( network, dotFile )
        print( '[INFO] Graph is written to dot file %s' % dotFile )
        # subprocess.call( [ "neato", "-Tpng", dotFile,  "-O"  ] )

    # Once I have the transition matrix, I now use markov module to solve it.
    s = markov.MarkovChain( T )
    ss = s.find_steady_state( method = args['method'] )
    return get_effects( ss, size )

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
        , default = 0.001
        , type = float
        , help = 'Down to Up transition probabilities'
        )
    parser.add_argument('--pDown', '-d'
        , required = False
        , default = 0.001
        , type = float
        , help = 'Up to Down transition probabilities'
        )
    parser.add_argument('--excitation', '-e'
        , required = False
        , default = 0.0
        , type = float
        , help = 'Excitation. Increases pUp of \delta pOn'
        )
    parser.add_argument('--inhibition', '-i'
        , required = False
        , default = 0.0
        , type = float
        , help = 'Inhibition. Decreases pDown of \delta pDown'
        )
    parser.add_argument('--plot', '-p'
        , action = 'store_true'
        , help = 'If given produce plots.'
        )
    parser.add_argument('--method', '-m'
        , required = False
        , default = 'analytic'
        , type = str
        , help = 'Which method (default analytic)'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    t1 = time.time()
    steadyState = main( args.system_size, **vars(args) )
    t2 = time.time( )
    print( '[INFO] Time taken %f' % ( t2 - t1 ) )
    print( '[INFO] Steady state' )
    print( steadyState )
    with open( 'run_time.csv', 'a' ) as f:
        f.write( '%d,%s\n' % ( args.system_size, t2 - t1 ) )
