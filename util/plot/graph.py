import random

import matplotlib.pyplot as plt
import networkx as nx
import networkx.drawing as nx_draw


def draw_graph(g: nx.Graph, file_name: str, with_labels: bool = False):
    random.seed(1)
    pos = nx.circular_layout(g)
    pos = nx.spring_layout(g, dim=2, pos=pos, iterations = 10000) # positions for all nodes
    labels = nx.get_node_attributes(g, 'hexes') 
    nx_draw.draw(g, labels=labels, pos=pos, with_labels = with_labels, node_size=100)
    # TODO: Add a bunch of fucntionality here for drawing houses, etc.
    plt.savefig(file_name + ".png")