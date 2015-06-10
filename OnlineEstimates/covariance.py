"""covariance.py: 

    Estimating variance online.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2015, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import random
import pylab 
import numpy as np

def online_estimate(data):
    n = 0
    mean = 0.0
    M2 = 0
    for x in data:
        n = n + 1
        delta = x - mean
        mean = mean + delta/n
        M2 = M2 + delta*(x - mean)
    if n < 2:
        return 0
    variance = M2/(n - 1)
    return variance

def main():
    #data = np.random.sample(1e6)
    data = np.random.random_integers(0, 1000, 1e6)
    variance = online_estimate(data)
    print("Online estimate is: %s" % variance)
    variance = data.var()
    print("Variance is: %s" % variance)


if __name__ == '__main__':
    main()
