#!/usr/bin/env python

"""test_pysox.py: 

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
import sox

def main():
    infile = sys.argv[1]
    print( "[INFO ] Processing %s" % infile )
    

if __name__ == '__main__':
    main()
