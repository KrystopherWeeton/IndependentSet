import copy
import random
import networkx as nx
from collections import defaultdict
from typing import overload
import numpy as np

from util.graph import count_edge_boundary
from util.models.solution import Solution


class GraphColoringTracker(Solution):
    def __init__(self, G: nx.Graph):
        self.G: nx.Graph = G
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}

    def clear_coloring(self):
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}

    def set_coloring_with_color_classes(self, coloring: dict):
        self.clear_coloring()
        self.color_to_nodes = copy.deepcopy(coloring)
        for color, nodes in coloring.items():
            for n in nodes:
                self.node_to_color[n] = color

    def set_coloring_with_node_labels(self, labelling: dict):
        self.clear_coloring()
        self.node_to_color = copy.deepcopy(labelling)
        for node, color in labelling:
            self.color_to_node[color].add(node)

    def color_node(self, node: int, color: int):
        self.color_to_nodes[color].add(node)
        self.node_to_color[node] = color


class PartialColoringTracker(GraphColoringTracker):
    def __init__(self, G: nx.Graph):
        super(PartialColoringTracker, self).__init__(G)
        self.uncolored_nodes: set = set(list(G.nodes))

    def color_node(self, node: int, color: int):
        super(PartialColoringTracker, self).color_node(node, color)
        self.uncolored_nodes.remove(node)


class CompleteColoringTracker(GraphColoringTracker):
    def __init__(self, G: nx.Graph, coloring: defaultdict = None, labelling: dict = None):
        super(CompleteColoringTracker, self).__init__(G)
        if coloring != None:
            self.set_coloring_with_color_classes(coloring)
        elif labelling != None:
            self.set_coloring_with_node_labels(labelling)
        else:
            raise Exception("No initial coloring was given")
        self.num_neighbor_colors: np.array = np.zeros((len(self.G), len(self.color_to_nodes)))
        self.init_conflict_matrix()

        self.saturation: np.array = np.zeros(len(self.G))
        self.init_saturation()

        self.collisions_at: np.array = np.zeros(len(self.G))
        self.init_collisions()

    def init_collisions(self):
        for v in self.G:
            for neighbor in self.G[v]:
                self.collisions[v] += int(self.node_to_color[v] == self.node_to_color[neighbor])

    def init_saturation(self):
        # How to get saturation of v?
        for v in self.G:
            self.saturation[v] = np.count_nonzero(self.num_neighbor_colors[v])

    def clear_coloring(self):
        super(CompleteColoringTracker, self).clear_coloring()
        self.num_neighbor_colors = defaultdict(int)

    def set_coloring_with_color_classes(self, coloring: dict):
        self.clear_coloring()
        super(CompleteColoringTracker, self).set_coloring_with_color_classes()

        # Set conflict matrix
        self.init_conflict_matrix()

    def set_coloring_with_node_labels(self, labelling: dict):
        self.clear_coloring()
        super(CompleteColoringTracker, self).set_coloring_with_node_labels()
        self.init_conflict_matrix()

    def init_conflict_matrix(self):
        self.num_neighbor_colors = np.zeros((len(self.G), len(self.color_to_nodes)))

        # Set up so that num_neighbor_colors[node, c] = Number of node's neighbors that have color c
        for node in self.G:
            for neighbor in self.G[node]:
                self.num_neighbor_colors[node, self.node_to_color[neighbor]] += 1

    def color_node(self, node: int, color: int):
        old_color: int = self.node_to_color[node]
        super(CompleteColoringTracker, self).color_node(node, int)

        # Update tables, complexity O(maxdeg(G))
        for neighbor in self.G[node]:
            # Update neighboring colors
            self.num_neighbor_colors[neighbor, old_color] -= 1
            self.num_neighbor_colors[neighbor, color] += 1

            # Update saturation
            self.saturation[neighbor] -= int(self.num_neighbor_colors[neighbor, old_color] == 0)
            self.saturation[neighbor] += int(self.num_neighbor_colors[neighbor, color] == 1)

            # Update collisions table
            self.collisions_at[neighbor] -= int(self.node_to_color[neighbor] == old_color)
            self.collisions_at[neighbor] += int(self.node_to_color[neighbor] == color)

    def most_collisions_node(self) -> int:
        return self.collisions_at.argmax()

    # Complexity O(k * n)
    def most_saturated_node(self) -> int:
        # Getting the max row-sum (how many neighboring colors we have)
        #return self.num_neighbor_colors.sum(axis=1).argmax()
        #return self.saturation.argmax()
        pass

    # Complexity: O(k * n)
    def most_distinctly_saturated_node(self) -> int:
        # Essentially we're counting the number of non-zero entries in a given row
        # return np.count_nonzero(self.num_neighbor_colors, axis=0).argmax()
        return self.saturation.argmax()

    def best_recoloring(self, node: int) -> int:
        # We want to pick the color that causes the least amount of conflicts for this node
        # That would be the argmin of this particular row? I think
        return self.num_neighbor_colors[node].argmin()


class ProperColoringTracker(CompleteColoringTracker):
    def __init__(self, G: nx.Graph, coloring: defaultdict = None, labelling: dict = None):
        super(ProperColoringTracker, self).__init__(G, coloring, labelling)


class ImproperColoringTracker(CompleteColoringTracker):
    def __init__(self, G: nx.Graph, coloring: defaultdict = None, labelling: dict = None):
        super(ImproperColoringTracker, self).__init__(G, coloring, labelling)


