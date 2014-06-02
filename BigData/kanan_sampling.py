#!/usr/bin/env python3

import numpy as np

array = np.random.random_integers(0, 1e7, 1e6)
prob_factor = 5e-7

def choose(num, p):
    """Choose this element with probablity p """
    if p >= random.random():
        return True
    return False
    

def sampleOnFly():
    runningSum = 0
    samples = []
    for i, a in enumerate(array):
        p = prob_factor * a

        


def main():
    print("Calling main function:")
    sampleOnFly()

if __name__ == '__main__':
    main()
