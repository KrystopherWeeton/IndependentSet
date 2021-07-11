import networkx as nx

import util.formulas as formulas
from util.heuristics.graph_subset_tracker import (GraphSubsetTracker,
                                                  create_graph_subset_tracker)


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
        self.solution = create_graph_subset_tracker(self.G, set())
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



class SeededHeuristic(Heuristic):

    def __init__(self, expected_metadata_keys: dict = None):
        super().__init__(expected_metadata_keys)
        self.seed: set = None


    def run_heuristic(self, G: nx.graph, seed: set, metadata: dict = None):
        if seed is None:
            raise RuntimeError("Cannot run seeded heuristic with no seeded subset.")

        self.seed = seed
        super().run_heuristic(G, metadata)