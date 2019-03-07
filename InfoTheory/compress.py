#!/usr/bin/env python

from __future__ import print_function, division

"""encode.py: 

Encode a data file.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import pickle
from collections import Counter
import math

py = sys.version_info.major

try:
    import huffman      # pip install huffman
    import bitarray     # pip install bitarray
except ImportError as e:
    import subprocess
    subprocess.call( [ 'pip%d' % py, 'install', 'huffman', '--user' ] )
    subprocess.call( [ 'pip%d' % py, 'install', 'bitarray', '--user' ] )

import huffman     
import bitarray   

delim_ = b'__####__'

def entropy( freq ):
    """Compute entropy of given frequencies.
    Compute in one-pass.
    """
    N = 0.0
    entropy = 0.0
    for x, v in freq.items( ):
        N += v
        entropy -= v * math.log( v, 2 )
    return (N * math.log( N, 2 ) + entropy) / N

def compress( txt, args ):
    print( 'Generating codebook', end = '')
    sys.stdout.flush( )
    freq = Counter( txt )
    codebook = huffman.codebook( freq.items( ) )
    avgCode = 0.0
    print( '.. done.' )

    print( 'Compressing files', end = '' )
    sys.stdout.flush( )

    enc_ = bitarray.bitarray( )
    for i, a in enumerate( txt ):
        code = codebook[a]
        avgCode = (avgCode * i + len(code) ) / (i+1)
        enc_.extend( code )
    print( '      .. done.' )

    # Write to compressed file. Add the codebook as well. This does not change
    # the compression ration very much.
    outfile = '%s.dx' % args.file 
    with open( outfile, 'wb' ) as fo:
        revCodeBook = dict((v, k) for k, v in codebook.items())
        codebookStr = ('%s' % revCodeBook).replace( ' ', '' )
        fo.write( codebookStr.encode( ) )
        fo.write( delim_ )
        fo.write( enc_.tobytes( ) )

    bestCode = entropy( freq )
    print( 'Average codeword length      : %f' % avgCode )
    print( '| Optimal average code length: %f' % bestCode )

    print( 'Compressed files is written to %s' % outfile )

    s1, s2 = map( os.path.getsize, [ args.file, outfile ] )
    print( '| Original   file size : %d' % s1 )
    print( '| Compressed file size : %d' % s2 )
    print( '| Compression ratio    : %f' % (s1 / float( s2 ) ) )

def decompress( txt, args ):
    """Decompress given file 
    """
    codebook, txt = txt.split( delim_ )
    codebook = eval( codebook )
    print( 'Decompressing %s' % args.file, end = '' )
    sys.stdout.flush( )
    res = ''
    N = len( txt )
    code = ''
    for i, x in enumerate(txt):
        # Convert to binary string and remove prefix of 0b.
        cb = bitarray.bitarray( )
        cb.frombytes( x )
        for c in cb.to01( ):
            code += c
            if code in codebook:
                res += codebook[code]
                code = ''

    print( '.. done.' )

    # remove extensition
    outfile = args.file.replace( '.dx', '', 1 )
    with open( outfile, 'w' ) as f:
        f.write( res )
    print( 'Decompressed to %s' % outfile )


def process( args ):
    filename = args.file
    print( 'Reading %s (%d MB)' % (filename, os.path.getsize(filename)/(1024**2))
            , end = '' )
    sys.stdout.flush( )
    with open( filename, 'r' ) as f:
        txt = '%s' % f.read( )
    print( '.. done.' )

    if args.compress:
        compress( txt, args )

    if args.decompress:
        decompress( txt, args )


def main( args ):
    process( args )

if __name__ == '__main__':
    
    import argparse
    # Argument parser.
    description = '''Compress/Decompress a file using Huffman codes.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--compress', '-c'
        , action = 'store_true'
        , help = 'Compress file'
        )
    parser.add_argument('--decompress', '-d'
        , action = 'store_true'
        , help = 'Decompress file'
        )
    parser.add_argument('file'
        , action = 'store'
        , help = 'File to compress/decompress.'
        )

    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )
