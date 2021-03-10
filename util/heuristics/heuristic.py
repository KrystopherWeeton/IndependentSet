import networkx as nx
import util.formulas as formulas

class Heuristic:

    def __init__(self, expected_metadata_keys: [str] = []):

        # Trackers that are set on a per-run basis
        self.G: nx.Graph = None
        self.solution: GraphSubsetTracker = None
        self.metadata: dict = None

        # The keys which are expected in every metadata passed in, e.g. raise warning
        # if the keys are not found within the provided metadata.
        self.expected_metadata_keys = expected_metadata_keys

    """
        Clears out the data stored in this heuristic, allowing it to be used again.
    """
    def clear(self):
        self.G = None
        self.solution = None
        self.metadata = None

    """
        Public function to run the optimization heuristic, which sets metadata before
        running the actual algorithm, which is overwritten by subclasses.

        NOTE: Metadata is the general metadata which subclasses may use on an algorithm
        per algorithm basis.
    """
    def run_heuristic(self, G: nx.graph, metadata: dict = None):
        # Clear self just to be completely sure that there is no bad info.
        self.clear()

        # Set metadata
        self.G = G
        self.solution = GraphSubsetTracker(self.G)
        self.metadata = metadata

        # Validate the metadata using the expected keys.
        for key in self.expected_metadata_keys:
            if key not in self.metadata.keys():
                raise Warning(f"Call to heuristic that does not contain expected key of {key}")
        
        # Run the actual heuristic
        self._run_heuristic()

    """
        Private function to actually run the heuristic which can be overwritten to 
        implement different heuristics for improvement.
    """
    def _run_heuristic(self):
        raise RuntimeError("This is an abstract function. Implement in subclass.")




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


    """
        Just sets the subset, recalculating all appropriate metadata (slow)
    """
    def set_subset(self, subset: set):
        self.subset: set = subset

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

        # Update calculated metadata
        for neighbor in self.G.neighbors(node):
            self.__internal_degrees[neighbor] += 1
        self.__subset_density = formulas.density_after_add(self.__subset_density, len(self.subset), self.__internal_degrees[node])


    """
        Removes a node from the existing subset, doesn't need to recalculate that much
    """
    def remove_node(self, node: int):
        if node not in self.subset:
            raise RuntimeError("Attempt to remove node from subset which is not in subset.")
        self.subset.remove(node)

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