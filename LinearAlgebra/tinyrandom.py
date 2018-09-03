# -*- coding: utf-8 -*-
"""tinyrandom.py: 
"""

from __future__ import division
from __future__ import absolute_import
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2018-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawar.s.rajput@gmail.com"
__status__           = "Development"

import itertools
import random

def seed( seed ):
    random.seed(seed)

def rand( *size ):
    # Generate an array of given size. All elements are sampled between 0 and 1
    A = tnp.zeros( size )
    for s in itertools.product( *map(range, size) ):
        A[s] = random.random()
    return A

def randn( *size ):
    # Generate an array of given size. All elements are sampled between 0 and 1
    A = tnp.zeros( size )
    for s in itertools.product( *map(range, size) ):
        A[s] = random.gauss()
    return A

def randint( low, high = None, size=None ):
    # Generate an array of given size. All elements are sampled between 0 and 1
    if high is None:
        high = low
        low = 0
    if size is None:
        size = 1
    A = tnp.zeros( size )
    for s in itertools.product( *map(range, size) ):
        A[s] = random.randint(low, high)
    return A

def random( size = None ):
    if size is None:
        size = 1
    A = tnp.zeros( size )
    for s in itertools.product( *map(range, size) ):
        A[s] = random.random( )
    return A

