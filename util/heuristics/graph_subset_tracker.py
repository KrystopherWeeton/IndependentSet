import networkx as nx
import util.formulas as formulas
import random as random
import copy



"""
A class which tracks a subset and some relevant metadata, allowing limited access to
the subset to speed up metadata access / tracking. 

Currently tracks:
 * Degrees of every node in G into the subset
 * Density of the subset
"""
class GraphSubsetTracker:

    def __init__(self, G: nx.graph, initial_subset: set = set()):
        # Sets simple metadata to track
        self.G: nx.graph = G
        self.set_subset(initial_subset)


    def __str__(self) -> str:
        return f"<{self.subset}>"


    def replicate(self) -> "GraphSubsetTracker":
        return copy.deepcopy(self)


    """
        Just sets the subset, recalculating all appropriate metadata (slow)
    """
    def set_subset(self, subset: set):
        self.subset: set = subset
        self.vertices_not_in_subset = set(self.G.nodes).difference(self.subset)

        # Performs initial (expensive) calculation of internal degrees and density
        self.__internal_degrees: [int] = [
            sum((1 for i in nx.edge_boundary(self.G, set([v]), self.subset))) for v in self.G.nodes
        ]
        self.__subset_density: float = nx.density(nx.subgraph(self.G, self.subset))


    """
        Adds a node to the existing subset, doesn't need to recalculate that much
    """
    def add_node(self, node: int):
        if node in self.subset:
            raise RuntimeError("Attempt to add node in subset")
        self.subset.add(node)
        self.vertices_not_in_subset.remove(node)

        # Update calculated metadata
        for neighbor in self.G.neighbors(node):
            self.__internal_degrees[neighbor] += 1
        self.__subset_density = formulas.density_after_add(self.__subset_density, len(self.subset), self.__internal_degrees[node])


    """
        Adds a random node in G not currently in the subset
    """
    def add_random_node(self):
        if self.size() == len(self.G.nodes):
            raise Exception("Attempt to add random node to complete subset.")
        node = random.choice(list(self.vertices_not_in_subset))
        self.add_node(node)

    """
        Removes a random node in G that is currently in the subset
    """
    def remove_random_node(self):
        if self.size() == 0:
            raise Exception("Attempt to remove random node from empty subset.")
        node = random.choice(list(self.subset))
        self.remove_node(node)


    """
        Removes a node from the existing subset, doesn't need to recalculate that much
    """
    def remove_node(self, node: int):
        if node not in self.subset:
            raise RuntimeError("Attempt to remove node from subset which is not in subset.")
        self.subset.remove(node)
        self.vertices_not_in_subset.add(node)

        # Update calculated metadata
        for neighbor in self.G.neighbors(node):
            self.__internal_degrees[neighbor] -= 1
        self.__subset_density = formulas.density_after_rem(self.__subset_density, len(self.subset), self.__internal_degrees[node])


    """
        Returns the internal degree of node into the subset being tracked
    """    
    def internal_degree(self, node: int) -> int:
        return self.__internal_degrees[node]

    
    """
        Returns the current density
    """
    def density(self) -> float:
        return self.__subset_density

    
    """
        Returns the size of the current subset
    """
    def size(self) -> int:
        return len(self.subset)


    def __iter__(self):
        return iter(self.subset)

