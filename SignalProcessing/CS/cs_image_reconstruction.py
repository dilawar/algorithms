"""cs_image_reconstruction.py: 

Construct image.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.misc

def main( ):
    nrn = scipy.misc.imread( './nrn.jpg' )
    print( nrn.shape )


if __name__ == '__main__':
    main()
