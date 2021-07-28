import copy
import random

random.seed(1)
from collections import defaultdict
from typing import Dict
from typing import Set

import networkx as nx

from util.models.solution import Solution

### Requested Data strings ###
UNCOLORED_NODES = 'uncolored_nodes'


# TODO: Add proper getter, setter and deleter methods with properties

class GraphColoringTracker(Solution):

    # FIXME: whenever I try to access the color of an uncolored node, I can't do that, nope
    def __init__(self, G: nx.Graph, requested_data: set = set(), coloring: defaultdict = None,
                 labelling: dict = None):
        super(GraphColoringTracker, self).__init__()

        available_data: set = {'uncolored_nodes'}

        # Basic information that all coloring trackers must utilize
        self.G: nx.Graph = G
        self.G_comp: nx.Graph = nx.complement(G)
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}
        self.uncolored_nodes: set = set()

        self.requested_data = requested_data
        # Make sure we didn't get asked for more/wrong data then we wanted
        if (len(available_data.union(requested_data)) != len(available_data)):
            raise AttributeError("You requested some data that is not available!")

        self.init_requested_data_PRECOLORING()

        if coloring != None:
            self.set_coloring_with_color_classes(coloring)
        elif labelling != None:
            self.set_coloring_with_node_labels(labelling)

    def init_requested_data_PRECOLORING(self):
        if UNCOLORED_NODES in self.requested_data:
            self.uncolored_nodes: set = set(list(self.G.nodes))

    def get_found_chromatic_number(self):
        return len(self.color_to_nodes.keys())

    def get_uncolored_nodes(self):
        if UNCOLORED_NODES in self.requested_data:
            return self.uncolored_nodes
        else:
            raise AttributeError("You're trying to get information that you didn't request!")

    def clear_coloring(self):
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}

        # Reset tables and other coloring vars
        self.uncolored_nodes: set = set(list(self.G.nodes))

    def init_tables(self):
        pass

    def get_num_conflicting_edges(self) -> int:
        raise AttributeError("Not implemented")

    # TODO: Might be useful to add a way to color only a specific subgraph
    def set_coloring_with_color_classes(self, coloring: Dict[int, Set[int]]):
        """
        Sets the coloring given some partial (or complete coloring)
        :param coloring: Dict[int, List[int]], Must be a dictionary of color classes
        """
        self.clear_coloring()
        self.color_to_nodes = copy.copy(coloring)
        for color, nodes in coloring.items():
            for n in nodes:
                self.uncolored_nodes.remove(n)
                self.node_to_color[n] = color
        self.init_tables()

    def set_coloring_with_node_labels(self, labelling: dict):
        if len(labelling.keys()) > len(self.G):
            raise ValueError("Tried to color more nodes than are in the graph")
        self.clear_coloring()
        self.node_to_color = copy.copy(labelling)
        for node, color in labelling.items():
            self.uncolored_nodes.remove(node)
            self.color_to_nodes[color].add(node)
        self.init_tables()

    # Question: Should we make a dedicated method for RECOLORING a node
    def color_node(self, node: int, color: int):

        old_color: int = self.node_to_color.get(node, None)

        # Trivial recoloring case
        if old_color == color:
            return

        # # The case in which we're using a NEW color to color this node
        # # Optimizeme: So I think the problem is that if we add a new color, we need to update the non-edges to give it a new possibility
        # if color not in self.color_to_nodes:
        #     assert True == True
        #     for non_neighbor in self.G_comp[node]:
        #         self.available_colors_at[non_neighbor].add(color)

        # Update coloring
        # First change in partitioning table
        self.color_to_nodes[color].add(node)
        if old_color != None:
            self.color_to_nodes[old_color].remove(node)

        # Then we do in color labelling
        self.node_to_color[node] = color

        # Mark uncolored if we need to
        if 'uncolored_nodes' in self.requested_data and node in self.uncolored_nodes:
            self.uncolored_nodes.remove(node)

    def is_proper(self):
        raise AttributeError("Not implemented yet")

    def is_complete(self):
        return len(self.uncolored_nodes) == 0
