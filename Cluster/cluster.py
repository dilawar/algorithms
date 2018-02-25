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

class Elem( ):

    def __init__( self, id, pos ):
        self.id = id
        self.pos = pos 

    def __eq__( self, x ):
        return self.id == x.id 

    def __lt__( self, x ):
        return self.id < x.id 

    def __ge__( self, x ):
        return self.id > x.id 

    def __repr__( self ):
        return self.id 

    def __hash__( self ):
        return hash( '%s.%d' % (self.id, self.pos) )

def print_chunks( chunks ):
    strc = [ ''.join(map(str,x)) for x in chunks ]
    print( ' '.join( strc ) )

def find_replacement( char, vec ):
    for i, v in enumerate( vec ):
        if v == char:
            return i
    return None

def fix_chunk( chunk, vec, k, result ):
    if len( vec ) < k or len(chunk) < k:
        return result + chunk + vec

    chars = chunk[:]
    counts = [ (chunk.count(x),x) for x in set(chars) ]
    sorted( counts )
    charCount, baseChar = counts[0]
    for i, c in enumerate( chars ):
        if c == baseChar:
            continue

        try:
            frmI = vec.index( baseChar )
            cc = vec[ frmI ]
            vec[ frmI ] = c
            chunk[i] = cc
        except ValueError as e:
            # We have run out of elements. Result the current result.
            continue
            #return result + chunk

    result += chunk
    chunk, vec = vec[:k], vec[k:]
    print_chunks( [ result, chunk, vec ] )
    return fix_chunk( chunk, vec, k, result )

def dynamic_programming( vec, k ):
    res = [ ]

    chunk, rest = vec[:k], vec[k:]
    result = [ ]

    result = fix_chunk( chunk, rest, k, result )
    print( result )


def cluster_data( vec, k, save = True ):
    dynamic_programming( vec, k )

def test( ):
    np.random.seed( 0 )
    data = np.random.choice( list( 'ABCDE' ), 90, p = [0.2,0.2,0.2,0.1,0.3] )
    data = list( zip( data, range(0,len(data) )))
    data = [ Elem(c,i) for c, i in data ]
    cluster_data( data, 3 )

if __name__ == '__main__':
    test( )

