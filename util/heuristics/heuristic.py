from typing import Callable

import networkx as nx


class Heuristic:

    def __init__(self, solution_class, expected_metadata_keys: [str] = [], verbose: bool = False):
        self.__solution_class = solution_class

        # Trackers that are set on a per-run basis
        self.G: nx.Graph = None
        self.solution = None
        self.metadata: dict = None
        self.verbose: bool = verbose

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

        @Arguments
            G:              The graph to run the graph heuristic on
            metadata:       The metadata to pass to the heuristic. Used to set arguments on a run by run basis
            seed:           An initial solution for the heuristic. Pass in none to set initial solution to None.
            post_step_hook: A function to call after each 'step' of the heuristic (however the heuristic defines step). Leave None to do nothing.
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
        # Note: Sets solution to NONE if no seed is passed in
        self.solution = seed
        self.metadata = metadata
        self.post_step_hook = post_step_hook

        # Validate the metadata using the expected keys.
        for key in self.expected_metadata_keys:
            if key not in self.metadata.keys():
                raise Warning(f"Call to heuristic that does not contain expected key of {key}")
        
        # Run the actual heuristic
        self._run_heuristic()


    def print_if_verbose(self, msg: str) -> bool:
        """ Prints the provided message if the verbose flag is set to true """
        if self.verbose:
            print(msg)


    """
        Private function to actually run the heuristic which can be overwritten to 
        implement different independent_set_heuristics for improvement.
    """
    def _run_heuristic(self):
        raise RuntimeError("This is an abstract function. Implement in subclass.")


