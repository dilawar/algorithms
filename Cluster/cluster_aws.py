#!/usr/bin/env python
    
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
import numpy as np
import re

def head_and_tail( vec ):
    head = list(itertools.takewhile(lambda x: x[0] == vec[0][0], vec))
    return head, vec[len(head):]

def find_elem_in_vec( vec, pivot ):
    for i, v in enumerate( vec ):
        if v[2] == pivot:
            return i
    return None

def cluster_data( vec, result ):
    if len( vec ) < 1:
        return result

    cluster, vec = head_and_tail( vec )
    specs = [ x[2] for x in cluster ]
    pivotSpec, pivotSpecCount = Counter( specs ).most_common( 1 )[0]
    newcluster = [ None ] * len(cluster)
    for i, e in enumerate(cluster):
        if e[2] == pivotSpec:
            newcluster[i] = e
            continue

        fromI = find_elem_in_vec( vec, pivotSpec )
        if fromI is None:
            continue

        newcluster[ i ] = vec[ fromI ]
        vec.insert( fromI, e )
        del vec[ fromI ]

    result.append( newcluster )
    return cluster_data( vec, result )


def test( ):
    data = []
    with open( sys.argv[1], 'r' ) as f:
        for line in f:
            data.append( tuple(line.strip().split( ',' )) )

    result = [ ]
    cluster_data( data, result )
    for l in result:
        print( l )

if __name__ == '__main__':
    test( )

