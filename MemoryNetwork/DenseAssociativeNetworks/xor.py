"""
Dense associative netowork from Krotov and Hopfield 2016 

XOR example.
"""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import math
import random
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
import itertools

init_printing(unicode=True)

STATES = [-1, 1]    # -1 => False, 1 => True

x, y, z = var('x y z')
n = Symbol('n')

def xor(in1, in2):
    return -1 if in1 == in2 else 1

def func_energy(sigmas):
    global x, y, z, n
    E = 0.0
    for (a, b, c) in sigmas:
        e = - (x * a + y * b + z * c) ** n
        E += e
    return E


def F(x, n:int=3):
    return x**n


def find_minima(σ, XIs):
    σo = σ[:]
    for i in range(3):
        innerSum = 0
        for μ, ξμ in enumerate(XIs):
            # first F(ξμi + Σ ξμj σj)
            a = ξμ[i]
            for j in range(len(σ)):
                if i == j:
                    continue
                a += ξμ[j] * σ[j]
            a = F(a)
            # second F(-ξμi + Σ ξμj σj)
            b = - ξμ[i]
            for j in range(len(σ)):
                if i == j:
                    continue
                b += ξμ[j] * σ[j]
            b = F(b)
            x = a - b
            innerSum += x
        σo[i] = int(math.copysign(1, innerSum))
    return σo

def to_str(ls):
    return ''.join([f'{x:2d}' for x in ls])


def compute_z(σ, XIs):
    """Only z needs to be computed.
    """
    x, y, z = σ 




def ex_xor():
    """XOR example
    """
    # All patterns created by xor function.
    XIs = [(a, b, xor(a, b)) for a, b in itertools.product(STATES, repeat=2)]
    """
    #for i, xi in enumerate(XIs):
    #    print(f'[INFO] σ{i} {xi}')

    ## sybolic energy function.
    #  energy = func_energy(XIs)

    ## minimization of energy
    #  E3 = energy.subs('n', 3).simplify()

    #  E3a = E3.subs('z', -1)
    #  E3b = E3.subs('z', 1)
    #  z = sign(E3a - E3b).expand().simplify()
    """

    # apply a random pattern and retrieve it.
    for i in range(20):
        σ = [random.choice(STATES), random.choice(STATES), random.choice(STATES)]
        σo = find_minima(σ, XIs)
        print(f' {to_str(σ)} → {to_str(σo)}')
        assert σo[2] == xor(σo[0], σo[1]), f"xor is violated in {σo=}"


    # find z.
    for i in range(20):
        σ = [random.choice(STATES), random.choice(STATES), random.choice(STATES)]
        σo = compute_z(σ, XIs)
        print(f' {to_str(σ)} → {to_str(σo)}')
        assert σo[2] == xor(σo[0], σo[1]), f"xor is violated in {σo=}"


def main():
    ex_xor()


if __name__ == "__main__":
    main()
