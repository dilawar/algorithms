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
import sys
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

def welford(data):
    mean = data[0]
    var = 0.0
    j = 1.0
    for x in data[1:]:
        newmean = (j*mean + x)/(j+1)
        newvar = ((x - mean)*(x - newmean) + j*var)/(j+1)
        var, mean = newvar, newmean
        j += 1
    return var

def compare(data):
    wikivar = online_estimate(data)
    numpyvar = np.var(data)
    welfordvar = welford(data)
    return wikivar, numpyvar, welfordvar

def main():
    mean = 1e-10
    wiki_ = []
    numpy_ = []
    welford_ = []
    variance_ = []

    for x in np.linspace(-10, 2, 20):
        std = 10**x
        variance_.append(std*std)
        data = np.random.normal(mean, std, 1e6)
        wikivar, numpyvar, welfordvar = compare(data)
        print("Wiki: %s, numpy: %s, welford: %s" % (wikivar, numpyvar,
            welfordvar))
        wiki_.append(wikivar)
        numpy_.append(numpyvar)
        welford_.append(welfordvar)

    pylab.title("Mean: %s" % std)
    pylab.semilogx(variance_, wiki_,  label="Wiki")
    pylab.semilogx(variance_, numpy_, label="Numpy")
    pylab.semilogx(variance_, welford_, label="Welford")
    pylab.xlabel("Variance")
    pylab.legend(loc='best', framealpha=0.4);
    pylab.show()
    
if __name__ == '__main__':
    main()
