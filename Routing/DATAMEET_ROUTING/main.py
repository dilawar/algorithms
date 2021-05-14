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
    return ((x0-x1)**2 + (y0-y1)**2) ** 0.5

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
    lines = data['geometry']
    for line in lines:
        add_line(g, line)

    nx.write_gpickle(g, outfile)
    return outfile

def main():

    infile = Path(sys.argv[1])
    pklfile = Path(f'{infile}.g.pkl')
    if pklfile.exists():
        g = nx.read_gpickle(pklfile)
    else:
        print(f'[INFO] Loading pickle {pklfile}')
        g = generate_graph(infile, pklfile)

    pklfile = Path(f'{infile}.ghu.pkl')
    if pklfile.exists():
        print(f'[INFO] Loading pickle {pklfile}')
        T = nx.read_gpickle(pklfile)
    else:
        T = nx.gomory_hu_tree(g)
        nx.write_gpickle(T, pklfile)

    for n1, n2 in T.edges():
        print(n1, n2, T[n1][n2])

    plt.figure(figsize=(10,10))
    plt.subplot(221)
    pos = nx.get_node_attributes(g, 'pos')
    nx.draw_networkx(g, with_labels=False, pos=pos, node_size=0.5)
    plt.title(f'{infile}')

    plt.subplot(222)
    gg = g.subgraph(list(T.nodes))
    pos = nx.get_node_attributes(gg, 'pos')
    nx.draw_networkx(gg, with_labels=False, pos=pos, node_size=0.5)


    plt.savefig(f'{infile}.png')


if __name__ == '__main__':
    main()
