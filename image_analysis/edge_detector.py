#!/usr/bin/env python

"""edge_detector.py: 

Detect edges in an image.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import cv2 
import numpy as np
import helper 

debug_level_ = 0

def debug__( msg, level = 1 ):
    # Print debug message depending on level
    global debug_level_ 
    if type(msg) == list: msg = '\n|- '.join(msg)
    if level < debug_level_: print( msg )

def all_edges( img, **kwargs ):
    global debug_level_
    debug_level_ = kwargs.get( 'debug', 0)
    mean_, std_ = img.mean(), img.std()
    high = kwargs.get('threshold_high', min(mean_ + 2 * std_, img.max()) )
    low = kwargs.get('threshold_low',  max(mean_ , 10) )
    l2grad = kwargs.get('L2gradient', True)
    debug__( [ 'Canny edges: low: %s, high = %s' % (low, high) ], 0)
    edges = cv2.Canny( img, low, high, L2gradient = l2grad )
    return edges

def detect_edges( filename, **kwargs ):
    debug__('[INFO] Detecting edges in %s' % filename)
    orignal = cv2.imread( filename )
    img = cv2.imread(filename, 0)
    edges = all_edges(img, **kwargs )
    outfile = kwargs.get('outfile', '%s_edges.png' % filename)
    debug__('Wrote edges to %s' % outfile )
    helper.plot_images( { 'original' : orignal, 'edges' : edges }
            , outfile = outfile
            )
    return edges

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Detect edges in an image'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', '-i'
        , required = True
        , help = 'Input file'
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
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    detect_edges( args.input, **vars(args) )

