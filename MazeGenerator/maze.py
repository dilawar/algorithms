__author__ = "Dilawar Singh"
__email__ = "dilawar.s.rajput@gmail.com"

import itertools
import math
import random
from pathlib import Path
import typing as T

import networkx as nx
import matplotlib.pyplot as plt


def _possible_neighbours(node: T.Tuple[int, int], shape: T.Tuple[int, int]):
    m, n = shape
    _x, _y = node
    res = []
    # only horzontal or veritical paths are allowed.
    for theta in [0, math.pi / 2, math.pi, -math.pi / 2]:
        a, b = (_x + math.cos(theta), _y + math.sin(theta))
        if a < 0 or a >= m or b < 0 or b >= n:
            continue
        res.append((int(a), int(b)))
    return res


def _perpendicular_line(p0, p1, length=1.0):
    """Perpendicular line to (x, y)"""
    (x0, y0), (x1, y1) = p0, p1
    midx, midy = (x0 + x1) / 2, (y0 + y1) / 2
    theta = math.atan2(y1 - y0, x1 - x0) + math.pi / 2.0
    r = length / 2.0
    q0 = midx - r * math.cos(theta), midy - r * math.sin(theta)
    q1 = midx + r * math.cos(theta), midy + r * math.sin(theta)
    return q0, q1


def gen_seed_graph(m: int, n: int, is_perfect: bool = False):
    """
    Seed graph to generate the maze.
    """
    g = nx.Graph(shape=(m, n))
    nodes = []
    for i, j in itertools.product(range(m), range(n)):
        g.add_node((i, j), pos=(i + 1, j + 1))
        nodes.append((i, j))

    source, target = (0, 0), (m - 1, n - 1)
    g.nodes[source]["color"] = "red"
    g.nodes[target]["color"] = "red"
    while not nx.has_path(g, source, target):
        # add a random edge from a node to one of its nearest neighbour
        a = random.choice(nodes)
        b = random.choice(_possible_neighbours(a, g.graph["shape"]))
        g.add_edge(a, b)
    return g


def _draw_gragh(g, with_labels: bool = False, ax=None, **kwargs):
    if ax is None:
        return
    pos = nx.get_node_attributes(g, "pos")
    nx.draw(g, ax=ax, node_size=5, pos=pos, **kwargs)


def _draw_lines(lines, ax=None):
    if ax is None:
        return
    import matplotlib.pyplot as plt

    for p0, p1 in lines:
        xs, ys = zip(p0, p1)
        ax.plot(xs, ys, lw=2, color="k")
    ax.axis(False)


def _to_maze(g):
    """Now draw a maze from the graph.

    Draw a line between two disconnected nodes. Thats it.
    """
    nrow, ncol = g.graph["shape"]
    m, n = nrow - 1, ncol - 1
    r = 0.5
    lines = [
        ((m + r, 0 - r), (0, 0 - r)),  # entry notch
        ((m + r, n + r), (m + r, 0 - r)),
        ((0 - r, m + r), (m, n + r)),  # exit notch
        ((0 - r, 0 - r), (0 - r, m + r)),
    ]
    for a in g.nodes():
        bs = _possible_neighbours(a, g.graph["shape"])
        cs = list(g.neighbors(a))
        nopath = set(bs) - set(cs)
        for na in nopath:
            lines.append(_perpendicular_line(a, na))
    return lines


def create_maze(shape: T.Tuple[int, int] = (10, 10), is_perfect: bool = False):
    """Create maze of given shape."""
    g = gen_seed_graph(*shape, is_perfect)
    lines = _to_maze(g)
    return g, lines


def _find_all_solutions(g):
    m, n = g.graph["shape"]
    src, tgt = (0, 0), (m - 1, n - 1)
    return list(nx.all_shortest_paths(g, src, tgt))


def _find_a_solution(g):
    m, n = g.graph["shape"]
    src, tgt = (0, 0), (m - 1, n - 1)
    return nx.shortest_path(g, src, tgt)


def _draw_path(path, ax):
    xs, ys = zip(*path)
    ax.plot(xs, ys, alpha=0.5, color="blue")


def main(args):
    args.shape = (
        (int(x) for x in args.shape.split(","))
        if isinstance(args.shape, str)
        else args.shape
    )
    g, lines = create_maze(args.shape, is_perfect=args.perfect)
    ax = plt.subplot(111)
    _draw_lines(lines, ax=ax)

    if args.show_solution:
        # add solutions
        _draw_path(_find_a_solution(g), ax=ax)

    lines = [f"{l[0][0]} {l[0][1]} {l[1][0]} {l[1][1]}" for l in lines]
    if args.output is not None:
        with open(args.output, "w") as f:
            for l in lines:
                f.write(l)
            print(f'[+] maze is saved to {args.output}')

    if args.plot is not None:
        print(f"[+] Maze is saved to {args.plot}")
        plt.savefig(str(args.plot))
    else:
        plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create maze")
    parser.add_argument(
        "-s",
        "--shape",
        default=(10, 10),
        help="Gridsize of the maze as csv e.g. -s 20,20 or -s 10,10",
    )
    parser.add_argument("--perfect", action="store_false", help="Perfect maze?")
    parser.add_argument(
        "-o", "--output", type=Path, help="Save maze (as lines) to this path."
    )
    parser.add_argument(
        "-p", "--plot", type=Path, help="Save maze (as image) to this path."
    )
    parser.add_argument(
        "-X",
        "--show-solution",
        action="store_true",
        help="If true, draw solution as well. Requires --plot to be set.",
    )
    args = parser.parse_args()
    main(args)
