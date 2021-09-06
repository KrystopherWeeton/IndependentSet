from typing import Callable, List, Union

from util.graph.graph import Graph
from util.misc import pull_values

"""
NOTE: The exact same as the heuristic in util/heuristics, but made for new graph wrapper. As experiments are updated
to use the new model they should be updated to this import
"""

class Heuristic:
    """
    Abstract class for all heuristics to provide some baseline behavior and structure.
    Initialization takes in a class that is referenced as the type of solution this
    heuristic should return, along with a list of the keys which are expected to
    be passed in when this heuristic is run.

    NOTE: The order in which metadata is passed to the child's `run_heuristic` function
    is precisely the same as the keys are provided in `expected_metadata_keys` so take
    care with the order of the elements of this argument.

    NOTE: The verbose / debug flags can be passed into the construtor to provide more output.
    The specific level of output depends on the heuristic being run; however, in general verbose
    output should contain relevant heuristic information, while debug should be used as a flag
    for information useful for identifying problems with a heuristic.
    """

    def __init__(self, solution_class, expected_metadata_keys: List[str] = [], verbose=False, debug=False):
        self.__solution_class = solution_class

        # Trackers that are set on a per-run basis
        self.G: Graph = None
        self.solution = None
        self.metadata: dict = None
        self.verbose: bool = verbose
        self.debug: bool = debug

        # The keys which are expected in every metadata passed in, e.g. raise warning
        # if the keys are not found within the provided metadata.
        self.expected_metadata_keys = expected_metadata_keys

    def verbose_print(self, msg: Union[str, List[str]]) -> None:
        """Prints the output if verbose is turned on, with indicator in front of the message"""
        if isinstance(msg, List):
            msg = "\n".join(msg)
        if self.verbose:
            print(f"[V] {msg}")
    
    def debug_print(self, msg: str) -> None:
        """Prints the output if the debug flag is turned on, with indicator in front of the message"""
        if isinstance(msg, List):
            msg = "\n".join(msg)
        if self.debug:
            print(f"[DEBUG] {msg}")

    # TODO: Need to generalize to coloring/arbitrary experiments
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
        G: Graph, 
        metadata: dict = None, 
        seed = None, 
        post_step_hook: Callable = None
    ) -> None:
        # Clear self just to be completely sure that there is no bad info.
        self.clear()

        # Set metadata
        self.G = G
        # NOTE: Sets solution to NONE if no seed is passed in
        # TODO: Find a better way to do this, as the seed should be allowed to be other types and the heuristic itself
        # TODO: should handle the mapping to the expected solution type. Probbaly just functions in heuristic that
        # TODO: should be implement at some point.
        if not isinstance(seed, self.__solution_class) and seed is not None:
            raise Exception(f"Unable to set object of type {type(seed)} when expected type is {self.__solution_class}.")
        self.solution = seed
        self.metadata = metadata
        self.post_step_hook = post_step_hook

        # Validate the metadata using the expected keys.
        for key in self.expected_metadata_keys:
            if key not in self.metadata.keys():
                raise Warning(f"Call to heuristic that does not contain expected key of {key}")
        
        # Pull appropriate values out of metadata and pass to _run_heuristic
        # Note: Uses the order of expecteD_metadata_keys to pull values
        metadata_list: List = pull_values(metadata, *self.expected_metadata_keys)
        # Run the actual heuristic
        self._run_heuristic(*metadata_list)

    """
        Private function to actually run the heuristic which can be overwritten to 
        implement different independent_set_heuristics for improvement.
    """
    def _run_heuristic(self):
        raise RuntimeError("This is an abstract function. Implement in subclass.")


