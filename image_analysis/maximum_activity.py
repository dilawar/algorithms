"""maximum_activity.py: 

Contains function to detect maximum change in activity at pixals.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import numpy as np
import pylab

import frame_reader as fr
import logging 
logger = logging.getLogger('')

pixal_of_interest_ = {}

class Pixal( ):

    def __init__(self, activity, loc):
        self.mean = activity.mean()
        self.min = activity.min()
        self.max = activity.max()
        self.std = activity.std()
        self.loc = loc
        self.index = 0.0
        self.init()

    def init(self ):
        if self.max > self.mean + 2 * self.std:
            self.index = (self.max - self.mean) / self.max

def add_pixal( pixal ):
    global pixal_of_interest_ 
    pixal_of_interest_[pixal.loc] = pixal

def main( inputfile, **kwargs):
    logger.info('Processing %s ' % inputfile)
    frames = fr.read_frames( inputfile, 10 )
    fShape = frames[0].shape
    logger.info('Got total %s frames' % len(frames))
    print("Done reading frames")
    data = np.dstack( frames )
    rows, cols = data.shape[0], data.shape[1]
    pixals = []
    for r in range(rows):
        for c in range(cols):
            vec = data[r, c, :]
            pixals.append( Pixal(vec, (r,c)) )
    
    for p in pixals:
        add_pixal( p )

    print("Total nice pixals: %s" % len(pixal_of_interest_))
    img = np.zeros( shape = fShape )
    for loc in pixal_of_interest_:
        img[loc] = pixal_of_interest_[loc].max
    
    pylab.imshow( img )
    pylab.show()


if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Locate pixals with maximum activity'''
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
    main( args.input, **vars(args) )
