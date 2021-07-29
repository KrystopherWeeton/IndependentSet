import copy
import random

random.seed(1)
from collections import defaultdict
from typing import Dict, List
from typing import Set

import networkx as nx

from util.models.solution import Solution

### Requested Data strings ###
UNCOLORED_NODES = 'uncolored_nodes'
NUM_CONFLICTING_EDGES = 'num_conflicting_edges'
COLORED_NODES = 'colored_nodes'
AVAILABLE_COLORS_AT = 'available_colors_at'
NUM_NEIGHBORING_COLORS = 'num_neighboring_colors'


# TODO: Add proper getter, setter and deleter methods with properties

class GraphColoringTracker(Solution):

    # FIXME: whenever I try to access the color of an uncolored node, I can't do that, nope
    def __init__(self, G: nx.Graph, requested_data: set = set(), coloring: defaultdict = None,
                 labelling: dict = None):
        super(GraphColoringTracker, self).__init__()

        available_data: set = {
            UNCOLORED_NODES,
            NUM_CONFLICTING_EDGES,
            COLORED_NODES,
            AVAILABLE_COLORS_AT,
            NUM_NEIGHBORING_COLORS
        }

        # Basic information that all coloring trackers must utilize
        self.G: nx.Graph = G
        self.G_comp: nx.Graph = nx.complement(G)
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}
        self.calls_to_color_node: int = 0

        self.requested_data = requested_data
        # Make sure we didn't get asked for more/wrong data then we wanted
        if (len(available_data.union(requested_data)) != len(available_data)):
            raise AttributeError("You requested some data that is not available!")

        self.init_requested_data_PRECOLORING()

        if coloring != None:
            self.set_coloring_with_color_classes(coloring)
        elif labelling != None:
            self.set_coloring_with_node_labels(labelling)

        self.init_requested_data_POSTCOLORING()

    def init_requested_data_PRECOLORING(self):
        if UNCOLORED_NODES in self.requested_data:
            self.uncolored_nodes: set = set(list(self.G.nodes))
        if COLORED_NODES in self.requested_data:
            self.colored_nodes: set = set()

    def init_requested_data_POSTCOLORING(self):
        self.num_conflicting_edges: int = 0
        if NUM_CONFLICTING_EDGES in self.requested_data:
            for v in self.colored_nodes:
                neighborhood_set: set = set(self.G[v])
                for neighbor in self.colored_nodes.intersection(set(self.G[v])):
                    if self.node_to_color[v] == self.node_to_color[neighbor]:
                        self.num_conflicting_edges += 1
        self.num_conflicting_edges /= 2

        if AVAILABLE_COLORS_AT in self.requested_data or NUM_NEIGHBORING_COLORS in self.requested_data:

            self.available_colors_at: dict = dict(zip(
                list(self.G.nodes),
                [set(self.color_to_nodes.keys()) for i in range(len(self.G))]
            ))

            # Initialize an array indexed by [node][color]
            self.num_neighboring_colors: List[List[int]] = []
            for i in range(len(self.G)):
                to_add = []
                for j in range(self.num_colors_used()):
                    to_add.append(0)
                self.num_neighboring_colors.append(to_add)
            # self.num_neighboring_colors: np.array = np.zeros((len(self.G), self.num_colors_used()))

            for v in self.G.nodes:
                for neighbor in self.G[v]:
                    neighbor_color: int = self.node_to_color.get(neighbor, -1)
                    if AVAILABLE_COLORS_AT in self.requested_data:
                        self.available_colors_at[v].discard(neighbor_color)

                    if NUM_NEIGHBORING_COLORS in self.requested_data and neighbor_color != -1:
                        self.num_neighboring_colors[v][neighbor_color] += 1

    def get_calls_to_color_node(self):
        return self.calls_to_color_node

    def num_colors_used(self):
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
        self.colored_nodes: set = set()

    def init_tables(self):
        pass

    def get_num_conflicting_edges(self) -> int:
        return self.num_conflicting_edges

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
                if UNCOLORED_NODES in self.requested_data:
                    self.uncolored_nodes.discard(n)
                if COLORED_NODES in self.requested_data:
                    self.colored_nodes.add(n)
                self.node_to_color[n] = color
        self.init_requested_data_POSTCOLORING()

    def set_coloring_with_node_labels(self, labelling: dict):
        if len(labelling.keys()) > len(self.G):
            raise ValueError("Tried to color more nodes than are in the graph")
        self.clear_coloring()
        self.node_to_color = copy.copy(labelling)
        for node, color in labelling.items():
            if UNCOLORED_NODES in self.requested_data:
                self.uncolored_nodes.discard(node)
            if COLORED_NODES in self.requested_data:
                self.colored_nodes.add(node)
            self.color_to_nodes[color].add(node)
        self.init_requested_data_POSTCOLORING()

    def get_random_node(self):
        return random.choice(list(self.G.nodes))

    def get_random_available_color(self, node: int):
        return random.choice(list(self.available_colors_at[node]))

    def add_new_color(self, node: int, new_color: int):
        if AVAILABLE_COLORS_AT in self.requested_data:
            for non_neighbor in self.G_comp[node]:
                self.available_colors_at[non_neighbor].add(new_color)

        if NUM_NEIGHBORING_COLORS in self.requested_data:
            for i, color_list in enumerate(self.num_neighboring_colors):
                color_list.append(0)

    # Question: Should we make a dedicated method for RECOLORING a node
    def color_node(self, node: int, color: int):
        self.calls_to_color_node += 1

        old_color: int = self.node_to_color.get(node, None)
        if color not in self.color_to_nodes:
            self.add_new_color(node, color)

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
            self.color_to_nodes[old_color].discard(node)

        # Then we do in color labelling
        self.node_to_color[node] = color

        # Now update our data tables
        self.update_requested_data_POSTRECOLOR(node, color, old_color)

    def update_requested_data_POSTRECOLOR(self, node_changed: int, new_color: int, old_color: int):

        # Mark uncolored if we need to
        if UNCOLORED_NODES in self.requested_data:
            self.uncolored_nodes.discard(node_changed)
        if COLORED_NODES in self.requested_data:
            self.colored_nodes.add(node_changed)

        if (
                NUM_CONFLICTING_EDGES in self.requested_data or
                AVAILABLE_COLORS_AT in self.requested_data or
                NUM_NEIGHBORING_COLORS in self.requested_data
        ):
            for neighbor in self.G[node_changed]:
                neighbor_color = self.node_to_color.get(neighbor, -1)

                if NUM_NEIGHBORING_COLORS in self.requested_data:
                    self.num_neighboring_colors[neighbor][new_color] += 1
                    if old_color != None and old_color != -1:
                        self.num_neighboring_colors[neighbor][old_color] -= 1

                if AVAILABLE_COLORS_AT in self.requested_data:
                    # Since we recolored the node, the neighbor has lost a possible color
                    self.available_colors_at[neighbor].discard(new_color)

                    # We only freed up the neighbor if we brought its neighboring colors down to zero
                    if (
                            old_color != None and
                            old_color != -1 and
                            self.num_neighboring_colors[neighbor][old_color] == 0
                    ):
                        self.available_colors_at[neighbor].add(old_color)

                if NUM_CONFLICTING_EDGES in self.requested_data:
                    if new_color == neighbor_color:
                        self.num_conflicting_edges += 1
                    if old_color != None and old_color != -1 and old_color == neighbor_color:
                        self.num_conflicting_edges -= 1

    def is_proper(self) -> bool:
        if NUM_CONFLICTING_EDGES in self.requested_data:
            return self.num_conflicting_edges == 0
        else:
            raise AttributeError(
                f'You tried requesting information ({NUM_CONFLICTING_EDGES}) that you never requested!')

    def is_complete(self) -> bool:
        return len(self.uncolored_nodes) == 0
