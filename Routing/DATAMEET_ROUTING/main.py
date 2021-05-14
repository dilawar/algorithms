__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import sys
from pathlib import Path
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

g_ = nx.Graph()

def distance(p1, p2):
    x0, y0 = p1
    x1, y1 = p2
    return ((x0-x1)**2 + (y0-y1)**2) ** 0.5

def add_line(line):
    global g_
    pts = list(zip(*line.xy))
    for p1, p2 in zip(pts, pts[1:]):
        g_.add_node(p1, pos=p1, size=1)
        g_.add_node(p2, pos=p2, size=1)
        g_.add_edge(p1, p2, weight=distance(p1, p2))

def main():
    infile = Path(sys.argv[1])
    data = gpd.read_file(infile)
    lines = data['geometry']
    for line in lines:
        add_line(line)

    plt.figure(figsize=(10,10))
    plt.subplot(221)
    pos = nx.get_node_attributes(g_, 'pos')
    nx.draw_networkx(g_, with_labels=False, pos=pos, node_size=0.5)
    plt.title(f'{infile}')


    plt.savefig(f'{infile}.png')


if __name__ == '__main__':
    main()
