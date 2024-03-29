__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import sys
import pickle
from pathlib import Path
import geopandas as gpd
import networkx as nx

import matplotlib.pyplot as plt


def distance(p1, p2):
    x0, y0 = p1
    x1, y1 = p2
    return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5


def add_line(g, line):
    pts = list(zip(*line.xy))
    for p1, p2 in zip(pts, pts[1:]):
        g.add_node(p1, pos=p1, size=1)
        g.add_node(p2, pos=p2, size=1)
        d = distance(p1, p2)
        g.add_edge(p1, p2, weight=distance(p1, p2), capacity=1)
    return g


def generate_graph(infile, outfile):
    g = nx.Graph()
    data = gpd.read_file(infile)
    lines = data["geometry"]
    for line in lines:
        add_line(g, line)

    nx.write_gpickle(g, outfile)
    return outfile


def main():

    plt.figure(figsize=(10, 5))
    infile = Path(sys.argv[1])
    k = int(sys.argv[2])
    print('[INFO] Partitioning {infile} in {k} partitions')

    pklfile = Path(f"{infile}.g.pkl")
    if pklfile.exists():
        g = nx.read_gpickle(pklfile)
    else:
        print(f"[INFO] Loading pickle {pklfile}")
        g = generate_graph(infile, pklfile)

    plt.subplot(121)
    pos = nx.get_node_attributes(g, "pos")
    nx.draw_networkx(g, with_labels=False, pos=pos, node_size=0.5)
    plt.title(f"{infile}")

    #
    # Gomori Hu
    #
    pklfile = Path(f"{infile}.ghu.pkl")
    if pklfile.exists():
        print(f"[INFO] Loading pickle {pklfile}")
        T = nx.read_gpickle(pklfile)
    else:
        T = nx.gomory_hu_tree(g)
        nx.write_gpickle(T, pklfile)

    # plt.subplot(222)
    # gg = g.subgraph(list(T.nodes))
    # nx.draw_networkx(gg, with_labels=False, pos=pos, node_size=0.5)

    #
    # Aync fluidc
    #
    plt.subplot(122)

    cc = max(nx.connected_components(g), key=len)
    lG = g.subgraph(list(cc))

    assert nx.is_connected(lG), "Required connected graph"
    C = nx.algorithms.community.asyn_fluid.asyn_fluidc(lG, k=k, max_iter=3000)
    C = list(C)

    pos = nx.get_node_attributes(lG, 'pos')
    colors = 'bgkrcmy'
    for i, c in zip(range(k), colors):
        n1 = list(C[i])
        ggg = lG.subgraph(n1)
        nx.draw_networkx(ggg, pos=pos, with_labels=False, node_size=0.1,
                edge_color=c)
    plt.title(f'{k} partitions')

    plt.savefig(f"{infile}.png")


if __name__ == "__main__":
    main()
