from typing import Callable, List, Union

from util.models.graph_subset_tracker import GraphSubsetTracker
from util.models.heuristic import Heuristic


class IndependentSetHeuristic(Heuristic):

    def __init__(self, expected_metadata_keys: List[str] = [], verbose: bool = False, debug: bool = False):
        super().__init__(GraphSubsetTracker, expected_metadata_keys=expected_metadata_keys, verbose=verbose, debug=debug)
