"""main.py: 
Send an image over noisy channel.
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

class Channel():
    
    def __init__(self):
        pass


def main():
    msg = plt.imread( './data.png' )
    print( msg )
    pass

if __name__ == '__main__':
    main()
