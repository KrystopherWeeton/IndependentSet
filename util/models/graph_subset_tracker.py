import copy
import random as random
from typing import List, Tuple

import util.formulas as formulas
from util.graph import count_edge_boundary
from util.graph.graph import Graph
from util.models.solution import Solution

"""
    Tracks a subset of a provided graph along with some relevant meetadata, allowing limited
    access to the subset to speed up metadata access / tracking.
"""
class GraphSubsetTracker(Solution):

    def __init__(self, G: Graph = None, initial_subset: set = set()):
        #? If passed relevant context, proceed otherwise mark as
        #? not initialized and wait for initialize call.
        if G is None:
            # Whether or not the tracker has been initialized yet
            self.initialized = False    # Test
        else:
            self.initialize(G, initial_subset)
    

    def initialize(self, G: Graph, initial_subset: set):
        """ Initializes the graph subset tracker if not already initialized """
        #? Check arguments
        if not isinstance(initial_subset, set):
            raise Exception("Graph subset tracker passed non-set argument")
        #? Set metadata
        self.G: Graph = G
        self.__graph_size: int = len(G.nodes)
        self.set_subset(initial_subset)
        self.initialized = True


    def set_subset(self, subset: set):
        """ Manually sets all subset information for the provided subset """
        self.subset, self.subset_complement = self.G.partition_vertices(subset)
        self.__internal_degrees: List[int] = [
            self.G.edge_boundary(v, self.subset) for v in self.G.nodes
        ]
        self.__num_edges: int = self.G.edges(subset)


    def add_node(self, node: int):
        """ 
            Adds the provided node to the subset. Errors when node is already
            in the subset or not in the graph.
        """
        #? Validate arguments
        if not self.initialized:
            raise Exception("Cannot add a node without initialization.")
        if node in self.subset:
            raise Exception("Cannot add a node already in subset")
        if node >= self.__graph_size:
            raise Exception("Cannot add a node not in graph.")
        #? Add node. Update trackers.
        self.subset.add(node)
        self.subset_complement.remove(node)
        for neighbor in self.G.neighbors(node):
            self.__internal_degrees[neighbor] += 1
        self.__num_edges += self.internal_degree(node)

    
    def remove_node(self, node: int):
        """
            Removes the provided node from the subset being tracked. Errors
            on invalid arguments.
        """
        #? Validate arguments
        if not self.initialized:
            raise Exception("Cannot add a node without initialization.")
        if node >= self.__graph_size:
            raise Exception("Cannot add a node not in graph.")#? Validate arguments
        if node not in self.subset:
            raise Exception("Cannot add a node already in subset")
        #? Remove node. Update trackers.
        self.subset.remove(node)
        self.subset_complement.add(node)
        for neighbor in self.G.neighbors(node):
            self.__internal_degrees[neighbor] -= 1
        self.__num_edges -= self.internal_degree(node)

    
    def add_random_node(self) -> int:
        """
            Selects a uniformly random node not currently in the subset and
            adds it to the subset. Returns the node added.
        """
        #? Validate arguments
        if not self.initialized:
            raise Exception("Cannot add a random node without initialization.")
        if self.size() == self.__graph_size:
            raise Exception("Cannot add a random node with complete subset.")
        #? Add node
        node: int = random.choice(list(self.subset_complement))
        self.add_node(node)
        return node

    
    def remove_random_node(self) -> int:
        """
            Selects a uniformly random node in the subset and removes it from
            the subset. Errors on empty subset. Returns the node removed.
        """
        #? Validate arguments
        if not self.initialized:
            raise Exception("Cannot remove a random node without initialization")
        if self.size() == 0:
            raise Exception("Cannot remove a random node from empty subset.")
        #? Remove node
        node = random.choice(list(self.subset))
        self.remove_node(node)
        return node


    def swap_random_nodes(self):
        """
            Swaps a random node in the subset with one outside the subset. Errors on
            complete or empety subset.

            NOTE: Does not allow for the node swapped in to be swapped out. Random
            choices are made before any changes are made.
        """
        #? Validate arguments
        if not self.initialized:
            raise Exception("Cannot swap random node without initialization")
        if self.size() == 0:
            raise Exception("Cannot swap random nodes with empty subset.")
        if self.size() == self.__graph_size:
            raise Exception("Cannot swap random nodes with full subset.")
        to_add: int = random.choice(list(self.subset_complement))
        to_remove: int = random.choice(list(self.subset))
        self.add_node(to_add)
        self.remove_node(to_remove)


    def internal_degree(self, node: int) -> int:
        """
            Returns the degree of the provided node into the tracked subset
        """
        if not self.initialized:
            raise Exception("Cannot get internal degree without initialization.")
        if node >= self.__graph_size:
            raise Exception("Cannot get internal degree of invalid node.")
        return self.__internal_degrees[node]


    def max_internal_degree(self, S: set) -> Tuple[int, int]:
        """ Returns the node within S with the max internal degree, and it's degree"""
        n: int = max(S, key = lambda j : self.internal_degree(j))
        return (n, self.internal_degree(n))

    def min_internal_degree(self, S: set) -> Tuple[int, int]:
        """ Returns the node within S with the minimum internal degree, and it's degree"""
        n: int = min(S, key = lambda j : self.internal_degree(j))
        return(n, self.internal_degree(n))

    def size(self) -> int:
        """
            Returns the size of the subset being currently tracked.
        """
        if not self.initialized:
            raise Exception("Cannot get size without initialization.")
        return len(self.subset)


    def density(self) -> float:
        """
            Returns the density of the subset being tracked
        """
        if not self.initialized:
            raise Exception("Cannot get density without initialization")
        # Need to handle edge case to deal with division by 0
        if self.size() <= 1:
            return 0
        pos_edges: int = (self.size() * (self.size() - 1)) // 2
        return self.__num_edges / pos_edges
    

    def num_edges(self) -> int:
        """
            Returns the total number of edges in the currently tracked subset
        """
        if not self.initialized:
            raise Exception("Cannot get number of edges without initialization")
        return self.__num_edges
        

    def replicate(self) -> "GraphSubsetTracker":
        """
            Returns a copy of this tracker with a deep reference to the graph.
        """
        if not self.initialized:
            raise Exception("Cannot replicate an uninitialized subset tracker")
        other = GraphSubsetTracker()
        other.G = self.G
        other.__graph_size = self.__graph_size
        other.subset = copy.copy(self.subset)
        other.subset_complement = copy.copy(self.subset_complement)
        other.__internal_degrees = copy.copy(self.__internal_degrees)
        other.__num_edges = self.__num_edges
        other.initialized = True
        return other


    def __iter__(self):
        if not self.initialized:
            raise Exception("Cannot iterate through uninitialized graph subset tracker.")
        return iter(self.subset)


    def __str__(self) -> str:
        if not self.initialized:
            return f"<uninit>"
        return f"<{self.subset}>"


# TODO: Move this somewhere else
"""
    Returns min, avg, and max density for the provided graph subset trackers.
"""
def get_density(subsets: List[GraphSubsetTracker]) -> Tuple[float, float, float]:
    if len(subsets) == 0:
        return (None, None, None)
    densities = sorted([S.density() for S in subsets])
    return (densities[0], densities[len(densities) // 2], densities[len(densities) - 1])
