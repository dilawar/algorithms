from __future__ import division, print_function
import tinynumpy.tinynumpy as tnp
import itertools
import random

def rand( *size ):
    A = tnp.zeros( size )
    for s in itertools.product( *map(range, size) ):
        A[s] = random.random()
    return A

def test( ):
    a = rand(4,4,4)

if __name__ == '__main__':
    test()

