#!/usr/bin/env python3
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
from collections import Counter
import math
import huffman      # pip install huffman
import bitarray     # pip install bitarray

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

def compress(filename, args ):
    print( 'Generating codebook', end = '')
    with open(filename, 'r') as f: txt = f.read()
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

def decompress(filename, args ):
    """Decompress given file 
    """
    with open(filename, 'rb') as f:
        txt = f.read()
    codebook, txt = txt.split( delim_ )
    codebook = eval( codebook )
    print(codebook)
    print( 'Decompressing %s' % args.file)
    res = ''
    code = ''
    for i, x in enumerate(txt):
        # Convert to binary string and remove prefix of 0b.
        cb = bitarray.bitarray(x)
        for c in cb.to01( ):
            code += c
            if code in codebook:
                res += codebook[code]
                code = ''

    print( '.. done.' )
    # remove extensition
    #  outfile = args.file.replace( '.dx', '', 1 )
    sys.stdout.write( res )


def process( args ):
    filename = args.file
    if args.compress:
        compress(filename, args )

    if args.decompress:
        decompress(filename, args )


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
