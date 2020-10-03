"""
Dense associative memory. 
Krotov & Hopfield 2016

https://arxiv.org/pdf/1606.01164.pdf
"""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

from dataclasses import dataclass, field
import random
import math
import typing as T

STATES = [-1, 1]


@dataclass
class Pattern:
    """
    True -> +1
    False -> -1
    """

    vec: T.List
    vals: T.List = field(init=False)

    def __post_init__(self):
        self.vals = [1 if x else -1 for x in self.vec]

    def __repr__(self):
        return "".join([f"{x:2d}" for x in self.vec])

    def __len__(self):
        return len(self.vec)

    def __getitem__(self, i):
        return self.vals[i]


@dataclass
class Neuron:
    """Neuron in the net"""

    v: int

    def __repr__(self):
        return f"{self.v:2d}"


class DenseMemoryNetwork:
    """Network of neurons."""

    def __init__(self, nrns, patterns):
        self.nrns = nrns
        self.N = len(self.nrns)
        self.patterns = patterns
        self.E = self.compute_energy(power=3)

    @property
    def σ(self, i):
        return self.nrns[i].v

    def F(self, x, power: int = 3):
        return x ** power

    def compute_energy(self, power: int):
        assert self.patterns
        E = 0.0
        for μ, ξμ in enumerate(self.patterns):
            E -= self.F(sum([ξμ[i] * self.nrns[i].v for i in range(self.N)]), 3)
        return E

    def update(self, i: int, power: int=3) -> int:
        assert self.patterns
        E = 0
        for μ, ξμ in enumerate(self.patterns):
            #  print(f'\t{i=} {μ=} {ξμ=}')
            ai = ξμ[i]
            bi = -ξμ[i]
            for j in range(self.N):
                if i == j:
                    continue
                dE = ξμ[j] * self.nrns[j].v
                ai += dE
                bi += dE
            E += self.F(ai) - self.F(bi)
        self.nrns[i].v = int(math.copysign(1, E))

    def __repr__(self):
        msg = "NEURONS: "
        msg += " " + str(self.nrns)
        msg += "\nPATTERNS:\n\t"
        msg += "\n\t".join([str(x) for x in self.patterns])
        msg += f"\nEnergy={self.E}\n"
        return msg

    @property
    def sigma(self):
        return [x.v for x in self.nrns]


def main():
    # generate xor patterns.
    xors = [
        Pattern([0, 0, 0]),
        Pattern([0, 1, 1]),
        Pattern([1, 0, 1]),
        Pattern([1, 1, 0]),
    ]
    nrns = [Neuron(random.choice(STATES)) for i in range(len(xors[0]))]
    n = DenseMemoryNetwork(nrns, xors)
    print(n.sigma)
    n.update(2)
    print(n.sigma)


if __name__ == "__main__":
    main()
