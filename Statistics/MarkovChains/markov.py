"""markov.py: 

Class for Markov Process

"""
import __future__
    
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
import networkx as nx
import matplotlib.pyplot as plt
import scipy
import numpy as np


class MarkovChain():
    """Markov chains"""

    def __init__(self, mat_or_string, **kwargs):
        self.T = None
        self.init_transition_matrix( mat_or_string )
        # size of the system
        self.N = self.T.shape[0]
        self.G = None

    def init_transition_matrix( self, mat_or_string ):
        if isinstance( mat_or_string, str ):
            rows = filter(None, mat_or_string.split(';'))
            self.N = len(rows)
            self.T = np.zeros( shape=( self.N, self.N) )
            for i, r in enumerate(rows):
                # Trick to avoid 1/3 evaluated to 0
                r = [ eval( compile(
                    x, '<string>', 'eval', __future__.division.compiler_flag
                    )) for x in r.split( ) ]
                if( np.sum( r ) > 1.0):
                    print( "[ERR] A row can not add up to more than 1.0" )
                    print( "\tRow was %s" % r )
                    quit( )
                r.insert( i, 1.0 - np.sum( r ) )
                self.T[i] = r 
        else:
            self.T = mat_or_string
            self.N = self.T.shape[0]

        if abs( np.sum( self.T ) - self.N) >= 1e-7:
            print( '[ERR] Invalid transition matrix' )
            print( '\tExpect sum %f, got %f' % (self.N, np.sum( self.T ) ) )
            print( self.T )
            quit( )

        if not np.allclose( np.sum( self.T , axis = 1), np.ones( self.N )):
            print( '[ERR] Invalid transition matrix. Each row must add up to 1' )
            print( '\t I constructed: %s' % self.T )

    def find_steady_state( self, **kwargs):
        # There are two ways in which one can do that. 
        if kwargs.get('method', 'analytic') == 'numeric':
            print( '[INFO] Running numeric algorithm' )
            max_iterations = kwargs.get( 'max_iterations', 100 )
            oldT = self.T
            newT = np.dot(oldT,  self.T)
            i = 0
            while not np.allclose( newT, oldT ):
                oldT = newT
                newT = np.dot(oldT,  self.T)
                i += 0
                assert i < max_iterations, 'Increase the max_iterations'
            diag = np.ravel( newT.diagonal( ) )
            return diag

        # Other method is to use the steady state argument that 
        #    finalDist = finalDist * self.T
        #    self.T' * finalDist' = finalDist' (A' = transpose A)
        a = self.T.T - np.identity( self.T.shape[0] )
        b = np.zeros( self.T.shape[0] )

        a[self.N-1,:] = np.ones( self.N )
        b[self.N-1] = 1
        
        # Up to now, this system is lineary dependant. Use that fact all
        # probabilities sums up to 1.
        return np.linalg.solve( a, b )

    def to_graph( self ):
        # TODO: Add label on edges as well.
        self.G = nx.DiGraph( self.T )
        outfile = 'transition_graph.dot'
        for s, t  in self.G.edges():
            self.G[s][t]['label'] = self.G[s][t]['weight']

        outA = 'network_topology_%03d.dot' % self.G.number_of_nodes( )
        nx.write_dot( self.G, outA )
        print( '[INFO] Wrote network file to %s' % outA )
        return 0

    def simulate( self, steps = 1000 ):
        allStates = range( self.N )
        states = [ np.random.choice( range( self.N ) ) ]
        rands = np.random.uniform( 0.0, 1.0, steps )
        for r in rands:
            currS = states[-1]
            otherStates = allStates.remove( currS )
            if r <= self.T[currS,currS]:
                # Remain here
                states.append( currS )
            else:
                # move to other state
                probs = self.T[currS,:currS] + self.T[currS,currS:]
                probs = probs / np.linalg.norm( probs, 1 )
                nextS = np.random.choice( otherStates, p = probs )

def main( args, method = 'analytic' ):
    mc = MarkovChain( args.transitions )
    print( '[INFO] Transition matrix ' )
    print( mc.T )
    stationary = mc.find_steady_state( method = method )
    print( '[RESULT] Stationary distribution' )
    print( stationary )
    mc.to_graph( )
    if args.simulate > 0:
        mc.simulate( args.simulate )

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Markov Chain'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--transitions', '-t'
        , required = True
        , type = str
        , help = 'Transitions. It has N-1 entries for each state.'
                 ' States are separated by character ;'
        )
    parser.add_argument('--output', '-o'
        , required = False
        , help = 'Output file'
        )
    parser.add_argument( '--debug', '-d'
        , required = False
        , default = 0
        , type = int
        , help = 'Enable debug mode. Default 0, debug level'
        )
    parser.add_argument('--simulate', '-s'
        , required = False
        , type = int
        , default = 0
        , help = 'Number of steps to simulate (default 0)'
        )

    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
