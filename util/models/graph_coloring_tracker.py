import copy
import random
from collections import defaultdict
from typing import Dict
from typing import Set

import networkx as nx
import numpy as np

from util.models.solution import Solution


# TODO: Add proper getter, setter and deleter methods with properties

class GraphColoringTracker(Solution):

    # FIXME: whenever I try to access the color of an uncolored node, I can't do that, nope
    def __init__(self, G: nx.Graph, coloring: defaultdict = None, labelling: dict = None):
        super(GraphColoringTracker, self).__init__()
        self.G: nx.Graph = G
        self.G_comp: nx.Graph = nx.complement(G)
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}
        self.uncolored_nodes: set = set(list(G.nodes))
        self.num_conflicting_edges: int = 0

        # Heuristic Data Tables

        # FIXME: Could be potentially dangerous to be using defaultdicts
        self.saturation: np.array = np.zeros(len(G))
        self.collisions_at: np.array = np.zeros(len(G))

        """
        Remember, num_neighbor_colors mandates that we keep our k-colors, (even if a color class is empty
        """
        self.num_neighbor_colors: np.array = np.array([defaultdict(int) for i in self.G])
        self.available_colors_at: Dict[int, Set[int]] = dict(zip(list(self.G.nodes), [set() for i in self.G]))

        if coloring != None:
            self.set_coloring_with_color_classes(coloring)
        elif labelling != None:
            self.set_coloring_with_node_labels(labelling)

    # TODO: Is complete coloring, and if so how many colors did we use?

    def get_found_chromatic_number(self):
        return len(self.color_to_nodes.keys())

    def get_uncolored_nodes(self):
        return self.uncolored_nodes

    def clear_coloring(self):
        self.color_to_nodes: dict = defaultdict(set)
        self.node_to_color: dict = {}

        # Reset tables and other coloring vars
        self.uncolored_nodes: set = set(list(self.G.nodes))
        self.saturation: np.array = np.zeros(len(self.G))
        self.collisions_at: np.array = np.zeros(len(self.G))
        self.available_colors_at: Dict[int, Set[int]] = dict(zip(list(self.G.nodes), [set() for i in self.G]))
        self.num_neighbor_colors: np.array = np.array([defaultdict(int) for i in self.G])
        self.num_conflicting_edges: int = 0

    def init_tables(self):
        """
        Takes care of initializing:
            saturation,
            collisions at v
            total # of collisions
            neighboring colors of v
        """
        self.init_saturation()
        self.init_collisions_available_colors_and_nn_colors()

    def get_num_conflicting_edges(self) -> int:
        return self.num_conflicting_edges

    def init_collisions_available_colors_and_nn_colors(self):
        for v in self.G:
            # We're going to start like v has all colors available to it, and then we will prune
            self.available_colors_at[v] = set(self.color_to_nodes.keys())
            for neighbor in self.G[v]:
                # Skip if neighbor has no color
                if neighbor not in self.node_to_color or v == neighbor:
                    continue

                neighbor_color: int = self.node_to_color[neighbor]

                self.num_neighbor_colors[v][neighbor_color] += 1
                if self.node_to_color[neighbor] in self.available_colors_at[v]:
                    self.available_colors_at[v].remove(neighbor_color)

                # Skip the rest if v doesn't have a color (because then collisions would be impossible.
                if v not in self.node_to_color:
                    continue
                self.collisions_at[v] += int(self.node_to_color[v] == neighbor_color)
                self.num_conflicting_edges += int(self.node_to_color[v] == neighbor_color)
        self.num_conflicting_edges /= 2  # Need to divide due to handshake lemma

    def init_saturation(self):
        # How to get saturation of v?
        for v in self.G:
            self.saturation[v] = np.count_nonzero(self.num_neighbor_colors[v])

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

        # The case in which we're using a NEW color to color this node
        # Optimizeme: So I think the problem is that if we add a new color, we need to update the non-edges to give it a new possibility
        if color not in self.color_to_nodes:
            for non_neighbor in self.G_comp[node]:
                self.available_colors_at[non_neighbor].add(color)

        # Update coloring labelling
        # First change in partitioning table
        self.color_to_nodes[color].add(node)
        if old_color != None:
            self.color_to_nodes[old_color].remove(node)

        # Then we do in color labelling
        self.node_to_color[node] = color
        if node in self.uncolored_nodes:
            self.uncolored_nodes.remove(node)

        # Update tables , complexity O(maxdeg(G))
        for neighbor in self.G[node]:
            # I guess we need to check if this node has a color Question: Can we skip it if it doesn't?
            self.num_neighbor_colors[neighbor][color] += 1

            # Update neighboring colors
            if old_color is not None:
                self.num_neighbor_colors[neighbor][old_color] -= 1

            if neighbor not in self.node_to_color:
                continue
            neighbor_color = self.node_to_color[neighbor]

            # In the case that we freed up a conflict by recoloring node
            if old_color != None and old_color == neighbor_color:
                self.collisions_at[neighbor] -= 1
                self.collisions_at[node] -= 1
                self.num_conflicting_edges -= 1

                # This is explicitely in the special case where we completely freed up the neighbor
                if self.num_neighbor_colors[neighbor][old_color] == 0:
                    # Sanity checks TODO: remove these
                    assert color != neighbor_color

                    self.available_colors_at[neighbor].add(old_color)
                    self.saturation[neighbor] -= 1

            if color == neighbor_color:
                self.collisions_at[neighbor] += 1
                self.collisions_at[node] += 1
                self.num_conflicting_edges += 1

                # NOTE: Ok, I'm almost positive that it's impossible for available colors to not have 'color' in it
                #   since we're doing this check, so that means we want it to fail
                # This is a special case in the case that neighbor had no other conflicts going into this recoloring
                if self.num_neighbor_colors[neighbor][color] == 1:

                    self.saturation += 1
                    try:
                        self.available_colors_at[neighbor].remove(color)
                    except KeyError:
                        raise KeyError(
                            "We tried to remove a color that wasn't there, but this also means that a color is not "
                            "getting added back for some reason"
                        )
                # Let's no see if we

            # TODO: Change to if statements to avoid repeated code
            #
            # # Update collisions table
            # self.collisions_at[neighbor] -= int(old_color is not None and self.node_to_color[neighbor] == old_color)
            # self.collisions_at[neighbor] += int(self.node_to_color[neighbor] == color)
            #
            # self.collisions_at[node] -= int(old_color is not None and self.node_to_color[neighbor] == old_color)
            # self.collisions_at[node] += int(self.node_to_color[neighbor] == color)
            #
            # # Update the number of conflicts
            # self.num_conflicting_edges -= int(self.node_to_color[neighbor] == old_color)
            # self.num_conflicting_edges += int(self.node_to_color[neighbor] == color)

    def is_proper(self):
        return self.num_conflicting_edges == 0

    def is_complete(self):
        return len(self.uncolored_nodes) == 0

    def recolor_random_node_a_random_color(self):
        # Pick a random node
        # Question, is G an iterable like this?
        node: int = random.choice(self.G.nodes)

        # Silently return if node has no available colors
        if len(self.available_colors_at[node]) == 0:
            return

        # Pick a random color that is available
        color = random.choice(list(self.available_colors_at[node]))

        # Color the node this color and finish
        self.color_node(node, color)

    # OptimizeMe: Implement as priority queue
    def most_collisions_node(self) -> int:
        """
        :return: Node that is most collisioned
        """
        return self.collisions_at.argmax()

    # OPTIMIZEMe: Add way to make recoloring loss function modular
    # Complexity: O()
    def most_distinctly_saturated_node(self) -> int:
        # Essentially we're counting the number of non-zero entries in a given row
        # return np.count_nonzero(self.num_neighbor_colors, axis=0).argmax()
        return self.saturation.argmax()

    def best_recoloring(self, node: int) -> int:
        """
        :param node:
        :return: color that is best for this node
        """
        # We want to pick the color that causes the least amount of conflicts for this node
        # That would be the argmin of this particular row? I think
        old_color: int = self.node_to_color[node]
        best_color: int = random.choice(list(self.color_to_nodes.keys()))
        best_conflicts: float = float('inf')
        for color, num_neighbors in self.num_neighbor_colors[node].items():
            if num_neighbors < best_conflicts:
                best_color = color
                best_conflicts = num_neighbors
        return best_color
