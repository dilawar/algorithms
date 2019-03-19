#!/usr/bin/env python

"""contour_detection.py: 

Detect contours in an image

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
import edge_detector

def get_contours( filename, **kwargs ):
    print('[INFO] Detecting contours in %s' % filename)
    img = cv2.imread(filename, 0)
    return contours(img, **kwargs)

def contours(img, **kwargs):
    debugLevel = kwargs.get('debug', -1)
    edges = edge_detector.all_edges( img, debug = 0, **kwargs )
    cnts, heir = cv2.findContours(edges, cv2.RETR_EXTERNAL
            , cv2.CHAIN_APPROX_TC89_KCOS)
    if debugLevel > 0:
        cntImg = np.zeros( img.shape )
        cv2.drawContours( cntImg, cnts, -1, 255 )
        helper.plot_images( { 'original' : img, 'contours' : cntImg } )
    return cnts

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Detect contours in an image'''
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
    contours( args.input, **vars(args) )
