import random
from typing import Callable, Dict, List

import matplotlib.pyplot as plt
import networkx as nx
import networkx.drawing as nx_draw
import numpy as np

from util.plot.color import generate_red_range

"""
    Colorings should be a list of (vertex, str) where each vertex is a vertex
    and color represents a color, a defulat color will be used as well
"""
def draw_graph(g: nx.Graph, colorings: Dict = {}, default_color="blue", iterations=10000):
    if len(g.nodes) == 0:
        nx_draw.draw(g, with_labels=False, node_size=50)
        return
    pos = nx.circular_layout(g)
    pos = nx.fruchterman_reingold_layout(g, dim=2, pos=pos, iterations=iterations)
    print(colorings)
    colors = [colorings[x] if x in colorings else default_color for x in g.nodes]
    nx_draw.draw(g, pos=pos, with_labels=False, node_size=30, node_color=colors)

def draw_gradient_graph(g: nx.Graph, get_color: Callable, get_label: Callable=None, iterations=10000):
    pos = nx.circular_layout(g)
    pos = nx.fruchterman_reingold_layout(g, dim=2, pos=pos, iterations = iterations)
    nodelist: List[np.array] = list(g.nodes)
    labels: Dict = None
    if get_label is not None:
        labels = {n: get_label(g.nodes[n]) for n in nodelist}
    colors: List = [get_color(g.nodes[n]) for n in nodelist]
    if labels is not None:
        nx_draw.draw(g, pos=pos, labels=labels, node_size=50, node_color=colors)
    else:
        nx_draw.draw(g, pos=pos, with_labels=False, node_size=50, node_color=colors)
