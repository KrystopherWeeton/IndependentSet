import copy
from collections import defaultdict

import networkx as nx
import numpy as np

from util.models.solution import Solution


class GraphColoringTracker(Solution):
    def __init__(self, G: nx.Graph, coloring: defaultdict = None, labelling: dict = None):
        super(GraphColoringTracker, self).__init__()
        self.G: nx.Graph = G
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}
        self.uncolored_nodes: set = set(list(G.nodes))
        self.saturation: np.array = np.zeros(len(G))
        self.collisions_at: np.array = np.zeros(len(G))
        self.num_neighbor_colors: np.array = np.array([defaultdict(int)] * len(G))

        if coloring != None:
            self.set_coloring_with_color_classes(coloring)
        elif labelling != None:
            self.set_coloring_with_node_labels(labelling)

    def clear_coloring(self):
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}
        self.uncolored_nodes: set = set(list(self.G.nodes))

    def init_tables(self):
        self.init_saturation()
        self.init_collisions()

    def init_collisions(self):
        for v in self.G:
            for neighbor in self.G[v]:
                self.collisions_at[v] += int(self.node_to_color[v] == self.node_to_color[neighbor])

    def init_saturation(self):
        # How to get saturation of v?
        for v in self.G:
            self.saturation[v] = np.count_nonzero(self.num_neighbor_colors[v])

    def set_coloring_with_color_classes(self, coloring: dict):
        self.clear_coloring()
        self.color_to_nodes = copy.deepcopy(coloring)
        for color, nodes in coloring.items():
            for n in nodes:
                self.uncolored_nodes.remove((n))
                self.node_to_color[n] = color
        self.init_tables()

    def set_coloring_with_node_labels(self, labelling: dict):
        self.clear_coloring()
        self.node_to_color = copy.deepcopy(labelling)
        for node, color in labelling:
            self.uncolored_nodes.remove((node))
            self.color_to_nodes[color].add(node)
        self.init_tables()

    def color_node(self, node: int, color: int):
        old_color: int = self.node_to_color.get(node, default=None)
        # Update coloring labelling
        self.color_to_nodes[color].add(node)
        self.node_to_color[node] = color
        self.uncolored_nodes.remove(node)

        # Update tables, complexity O(maxdeg(G))
        for neighbor in self.G[node]:
            # Update neighboring colors
            if old_color != None:
                self.num_neighbor_colors[neighbor, old_color] -= 1
            self.num_neighbor_colors[neighbor, color] += 1

            # Update saturation
            self.saturation[neighbor] -= int(old_color != None and self.num_neighbor_colors[neighbor, old_color] == 0)
            self.saturation[neighbor] += int(self.num_neighbor_colors[neighbor, color] == 1)

            # Update collisions table
            self.collisions_at[neighbor] -= int(old_color != None and self.node_to_color[neighbor] == old_color)
            self.collisions_at[neighbor] += int(self.node_to_color[neighbor] == color)

    def most_collisions_node(self) -> int:
        return self.collisions_at.argmax()

    # Complexity: O()
    def most_distinctly_saturated_node(self) -> int:
        # Essentially we're counting the number of non-zero entries in a given row
        # return np.count_nonzero(self.num_neighbor_colors, axis=0).argmax()
        return self.saturation.argmax()

    def best_recoloring(self, node: int) -> int:
        # We want to pick the color that causes the least amount of conflicts for this node
        # That would be the argmin of this particular row? I think
        return min(self.num_neighbor_colors[node], key=self.num_neighbor_colors[node].get)
