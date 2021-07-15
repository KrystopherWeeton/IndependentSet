from typing import Union, Callable

import networkx as nx

from util.models.graph_subset_tracker import GraphSubsetTracker
from util.models.solution import Solution

class Heuristic:

    def __init__(self, solution_class, expected_metadata_keys: [str] = []):
        self.__solution_class = solution_class

        # Trackers that are set on a per-run basis
        self.G: nx.Graph = None
        self.solution = None
        self.metadata: dict = None

        # The keys which are expected in every metadata passed in, e.g. raise warning
        # if the keys are not found within the provided metadata.
        self.expected_metadata_keys = expected_metadata_keys

    """
        Calls post_step_hook with appropriate values if the value is not None, otherwise no-ops
    """
    def call_post_step_hook(self, subset: set, step: int):
        if self.post_step_hook is not None:
            self.post_step_hook(subset, step)

    """
        Clears out the data stored in this heuristic, allowing it to be used again.
    """
    def clear(self):
        self.G = None
        self.solution = None
        self.metadata = None
        self.post_step_hook = None

    """
        Public function to run the optimization heuristic, which sets metadata before
        running the actual algorithm, which is overwritten by subclasses.

        NOTE: Metadata is the general metadata which subclasses may use on an algorithm
        per algorithm basis.
    """
    def run_heuristic(
        self, 
        G: nx.graph, 
        metadata: dict = None, 
        seed = None, 
        post_step_hook: Callable = None
    ):
        # Clear self just to be completely sure that there is no bad info.
        self.clear()

        # Set metadata
        self.G = G
        # Set seed based on appropriate type of argument
        self.solution = seed if seed is not None and isinstance(seed, self.__solution_class) else self.__solution_class()
        self.metadata = metadata
        self.post_step_hook = post_step_hook

        # Validate the metadata using the expected keys.
        for key in self.expected_metadata_keys:
            if key not in self.metadata.keys():
                raise Warning(f"Call to heuristic that does not contain expected key of {key}")
        
        # Run the actual heuristic
        self._run_heuristic()

    """
        Private function to actually run the heuristic which can be overwritten to 
        implement different independent_set_heuristics for improvement.
    """
    def _run_heuristic(self):
        raise RuntimeError("This is an abstract function. Implement in subclass.")


