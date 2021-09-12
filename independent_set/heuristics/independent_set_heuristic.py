from typing import List, Set

from util.models.heuristic import Heuristic


class IndependentSetHeuristic(Heuristic):

    def __init__(self, expected_metadata_keys: List[str] = [], verbose: bool = False, debug: bool = False):
        super().__init__(Set, expected_metadata_keys=expected_metadata_keys, verbose=verbose, debug=debug)
